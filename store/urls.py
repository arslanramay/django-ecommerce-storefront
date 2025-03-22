from django.urls import path
from . import views

# URLConf
urlpatterns = [
    # Function based views
    # path('products/', views.product_list),
    # path('products/<int:id>/', views.product_detail),

    # Class based views
    path('products/', views.ProductList.as_view()),
    path('products/<int:id>/', views.ProductDetail.as_view()),

    # Function based views
    # path('collections/', views.collection_list),
    # path('collections/<int:pk>/', views.collection_detail, name='collection-detail'),

    # Class based views
    path('collections/', views.CollectionList.as_view()),
    path('collections/<int:pk>/', views.CollectionDetail.as_view()),
]