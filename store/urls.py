from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from . import views
from pprint import pprint

# Nested Router URLs
router = routers.DefaultRouter()
router.register('products', views.ProductViewSet)
router.register('collections', views.CollectionViewSet)
router.register('carts', views.CartViewSet)
router.register('customers', views.CusdtomerViewSet)
router.register('orders', views.OrderViewSet, basename='orders')

products_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
products_router.register('reviews', views.ReviewViewSet, basename='product-reviews')

#lookup='cart_pk' provides the URL parameter which we retrieve in the CartItemViewSet with kwargs['cart_pk']
# carts_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart_pk')
carts_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
carts_router.register('items', views.CartItemViewSet, basename='cart-items')
# carts_router.register('items', views.CartItemViewSet, basename='cart-items-list')
# carts_router.register('items', views.CartItemViewSet, basename='cart-items-detail')

# Combine Router URLs i.e Default and Nested Router URLs
urlpatterns = router.urls + products_router.urls + carts_router.urls



# Default Router URLs
# router = DefaultRouter()
# router.register('products', views.ProductViewSet)
# router.register('collections', views.CollectionViewSet)

# pprint(router.urls)


# URLConf
# urlpatterns = router.urls

# urlpatterns = [
# #     # Function based views
# #     # path('products/', views.product_list),
# #     # path('products/<int:id>/', views.product_detail),
# #     # path('collections/', views.collection_list),
# #     # path('collections/<int:pk>/', views.collection_detail, name='collection-detail'),

# #     # Class based views
# #     # path('products/', views.ProductList.as_view()),
# #     # path('products/<int:pk>/', views.ProductDetail.as_view()),
# #     # path('collections/', views.CollectionList.as_view()),
# #     # path('collections/<int:pk>/', views.CollectionDetail.as_view()),
# ]