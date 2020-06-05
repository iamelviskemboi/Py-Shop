from django.shortcuts import render
from .models import (Product)


# /products -> index
def index(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'products.html', context)
