from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from store.models import Product


def say_hello(request):
    # return HttpResponse('Hello, Django!')
    # return render(request, 'hello.html')

    # Simple Try/Except block
    try:
        product = Product.objects.get(id=-2)
    except ObjectDoesNotExist:
        pass

    # Get all products
    # query_set = Product.objects.all()
    # for product in query_set:
    #     print(product)

    # Return HTML page with name
    return render(request, 'hello.html', {'name': 'Arslan'})