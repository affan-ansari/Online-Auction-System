from django.urls import path
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name='auction-home'),
]

product_urls = [
    path('products/', views.ProductListView.as_view(), name='products-list'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(),
         name='product-detail'),
    path('products/<int:pk>/update/', views.ProductUpdateView.as_view(),
         name='product-update'),
    path('products/new/', views.ProductCreateView.as_view(), name='product-create'),
]

auction_urls = [
    path('auctions/', views.AuctionListView.as_view(), name='auctions-list'),
    path('auctions/<int:pk>/', views.AuctionDetailView.as_view(),
         name='auction-detail'),
    path('auctions/<int:pk>/update/', views.AuctionUpdateView.as_view(),
         name='auction-update'),
    path('auctions/new/', views.AuctionCreateView.as_view(), name='auction-create'),
]

urlpatterns += product_urls + auction_urls
