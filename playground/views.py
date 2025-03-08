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
    # query_set = Product.objects.filter(unit_price__range=(40, 60))
    # query_set = Product.objects.filter(collection__id=6)
    # query_set = Product.objects.filter(title__icontains='coffee')
    # query_set = Product.objects.filter(title__startswith='Coffee')
    # query_set = Product.objects.filter(last_update__year='2021')
    query_set = Product.objects.filter(last_update__month='6')
    # print(query_set)

    # Filters
    # Products: inventory < 10 AND price < 20

    # Render the template with Products
    return render(request, 'hello.html', {'name': 'Arslan', 'products': list(query_set)})