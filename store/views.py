from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .models import Product, Collection
from .serializers import ProductSerializer, CollectionSerializer

# ======================
# Class Based API Views
# ======================
class ProductList(APIView):
    def get(self, request):
        products = Product.objects.select_related('collection').all() # select_related for joining tables
        serializer = ProductSerializer(products, many=True, context={'request': request}) # many=True for iterating on multiple objects
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ProductDetail(APIView):
    def get(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, id):
        product = get_object_or_404(Product, pk=id)
        if product.orderitems.count() > 0:
            return Response(
                {
                    'error': 'Product cannot be deleted because it is associated with an order item.'
                },
                status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ==================
# Product API Views
# ==================
# @api_view(['GET', 'POST'])
# def product_list(request):
#     if request.method == 'GET':
#         products = Product.objects.select_related('collection').all() # select_related for joining tables
#         serializer = ProductSerializer(products, many=True, context={'request': request}) # many=True for iterating on multiple objects
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = ProductSerializer(data=request.data)
#         # if serializer.is_valid():
#         #     print(serializer.validated_data)
#         #     return Response('OK')
#         # else:
#         #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

# @api_view(['GET', 'PUT', 'DELETE'])
# def product_detail(request, id):
#     product = get_object_or_404(Product, pk=id)

#     if request.method == 'GET':
#         serializer = ProductSerializer(product)
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer = ProductSerializer(product, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#     elif request.method == 'DELETE':
#         if product.orderitems.count() > 0:
#             return Response(
#                 {
#                     'error': 'Product cannot be deleted because it is associated with an order item.'
#                 },
#                 status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# =====================
# Collection API Views
# =====================
@api_view(['GET', 'POST'])
def collection_list(request):
    if request.method == 'GET':
        # collections = Collection.objects.all()
        collections = Collection.objects.annotate(products_count=Count('products')).all()
        serializer = CollectionSerializer(collections, many=True)
        return Response(serializer.data)
        # return Response(f'Collection List Page: {collections}')
    elif request.method == 'POST':
        serializer = CollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
def collection_detail(request, pk):
    # collection = get_object_or_404(Collection, pk=pk) # pk=pk is same as id=pk
    collection = get_object_or_404(
        Collection.objects.annotate(products_count=Count('products'), pk=pk)
    )

    if request.method == 'GET':
        serializer = CollectionSerializer(collection)
        return Response(serializer.data)
        # return Response(f'Collection Detail Page: {pk}')
    elif request.method == 'PUT':
        serializer = CollectionSerializer(collection, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        if collection.products.count() > 0:
            return Response({
                'error': 'Collection cannot be deleted because it contains products.'
            }, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Without get_obj_or_404
# def product_detail(request, id):
#     try:
#         product = Product.objects.get(pk=id)
#         serializer = ProductSerializer(product)
#         return Response(serializer.data)
#         # return Response(f'Product Detail Page: {id}')
#     except Product.DoesNotExist:
#         return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)