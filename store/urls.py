from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views
from pprint import pprint

# Router URLs
router = DefaultRouter()
router.register('products', views.ProductViewSet)
router.register('collections', views.CollectionViewSet)
# pprint(router.urls)

# URLConf
urlpatterns = router.urls

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