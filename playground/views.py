from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from store.models import Product


def say_hello(request):
    # return HttpResponse('Hello, Django!')
    # return render(request, 'hello.html')

    # Simple Try/Except block
    # try:
    #     product = Product.objects.get(id=-2)
    # except ObjectDoesNotExist:
    #     pass

    # Get all products
    # query_set = Product.objects.all()
    # for product in query_set:
    #     print(product)

    # Filters
    query_set = Product.objects.filter(unit_price__range=(40, 60))
    # print(query_set)

    # Render the template with Products
    return render(request, 'hello.html', {'name': 'Arslan', 'products': list(query_set)})