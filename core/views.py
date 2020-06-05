from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import (get_object_or_404, redirect, render)
from django.utils import timezone
from django.views.generic import (ListView, DetailView)

from .models import (Item, OrderItem, Order)


# home
class HomeView(ListView):
    model = Item
    template_name = 'home/index.html'


# product
class ProductDetailView(DetailView):
    model = Item
    template_name = 'product/product-page.html'


# add to cart
@login_required
def add_to_cart(request, slug):
    # get the specified item
    item = get_object_or_404(Item, slug=slug)
    # get or create an Order Item and add the item to list
    order_item, created = OrderItem.objects.get_or_create(
        item=item, user=request.user, ordered=False)
    # query existing unfulfilled orders of the current user
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    # (if any) -> increase its quantity
    if order_qs.exists():
        # grab the Order queryset
        order = order_qs[0]
        # check if the order_item is in this existing order
        if order.items.filter(item__slug=item.slug).exists():
            # increment the order_item's quantity in the Order(cart)
            order_item.quantity += 1
            # save the order_item to (cart)
            order_item.save()
            # inform the user of the action done
            messages.info(request, "This item's quantity has been updated!",
                          fail_silently=False)
        # if the order_item is not in this existing order, add it
        else:
            # inform the user of the action done
            messages.success(
                request, "This item has been added to your cart!", fail_silently=False)
            order.items.add(order_item)
    # (if none) -> create it
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        # add the order_item to the new Order
        order.items.add(order_item)
    # now back to the item's page
    return redirect('core:product', slug=slug)


# remove from cart
@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    # query existing unfulfilled orders from the current user
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    # (if any) -> remove it from cart
    if order_qs.exists():
        # grab the Order queryset
        order = order_qs[0]
        # check if the item is among the grabbed order's items
        if order.items.filter(item__slug=item.slug).exists():
            # query the current item inside the current OrderItem(cart)
            order_item = OrderItem.objects.filter(
                item=item, user=request.user, ordered=False)[0]
            # remove that item from the OrderItem(s)
            order.items.remove(order_item)
            # inform the user of the action done
            messages.warning(request, "This item was removed from your cart!",
                             fail_silently=False)
        else:
            # inform the user of the action done
            messages.error(
                request, "This item was not in your cart!", fail_silently=False)
            return redirect('core:product', slug=slug)
    # (if none) -> stay on the item's page
    else:
        # inform the user of the action done
        messages.error(request, "Sorry! You don't have an active order!",
                       fail_silently=False)
        return redirect('core:product', slug=slug)
    # now back to the item's page
    return redirect('core:product', slug=slug)


# checkout
@login_required
def checkout(request):
    return render(request, 'checkout/checkout-page.html')
