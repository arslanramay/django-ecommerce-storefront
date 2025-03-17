from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from .models import Product
from .serializers import ProductSerializer

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Define API Views
@api_view(['GET', 'POST'])
def product_list(request):
    if request.method == 'GET':
        products = Product.objects.select_related('collection').all() # select_related for joining tables
        serializer = ProductSerializer(products, many=True, context={'request': request}) # many=True for iterating on multiple objects
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        return Response('OK')
        # return Response(serializer.data, status=status.HTTP_201_CREATED)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data)


@api_view()
def product_detail(request, id):
    product = get_object_or_404(Product, pk=id)
    serializer = ProductSerializer(product)
    return Response(serializer.data)

@api_view()
def collection_detail(request, pk):
    return Response(f'Collection Detail Page: {pk}')



# Without get_obj_or_404
# def product_detail(request, id):
#     try:
#         product = Product.objects.get(pk=id)
#         serializer = ProductSerializer(product)
#         return Response(serializer.data)
#         # return Response(f'Product Detail Page: {id}')
#     except Product.DoesNotExist:
#         return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)