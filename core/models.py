from django.conf import settings
from django.db import models
from django.shortcuts import reverse


# product category choices
CATEGORY_CHOICES = (
    ('S', 'Shirt'),
    ('SW', 'Sport wear'),
    ('OW', 'Outwear'),
)
# product label choices
LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'dark'),
)


# Item -> (product)
class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(null=True, blank=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    label = models.CharField(choices=LABEL_CHOICES, max_length=1)
    slug = models.SlugField()
    description = models.TextField(max_length=255)

    def __str__(self):
        return self.title

    # product url
    def get_absolute_url(self):
        return reverse("core:product", kwargs={"slug": self.slug})

    # add to cart url
    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={"slug": self.slug})

    # remove from cart url
    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={"slug": self.slug})

    # product discount(%)
    def get_discounted(self):
        # change those float variables to integers
        discounted_price = int(self.discount_price)
        original_price = int(self.price)
        # get the discount
        if original_price > discounted_price and discounted_price >= 1:
            discount = ((discounted_price / original_price) * 100)
            msg = round(discount)
            result = f"{msg}% OFF"
        else:
            result = None
        # return percentage
        return result

    # price validation
    def prices_are_ok(self):
        discounted_price = int(self.discount_price)
        original_price = int(self.price)
        if discounted_price >= 1 and original_price > discounted_price:
            return True
        else:
            return False


# Order Item -> (cart)
class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f"{ self.item.title } - X{ self.quantity }"


# Order -> (order)
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
