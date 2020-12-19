from django.urls import path
from listings import views

app_name = 'listings'


urlpatterns = [
    path('', views.index, name='index'),
    path('listings/', views.listings, name='listings'),
    path('listing/<int:id>/<slug:slug>/', views.single_listing, name='single_listing'),
    path('search/', views.search, name='search'),
    path('add-wishlist/', views.add_wishlist, name='add_wishlist'),
    path('sort/<str:by>', views.sort, name='sort'),
    path('dashboard/properties/', views.dashboard_properties, name='dashboard_properties'),
    path('dashboard/properties/marketer/', views.dashboard_marketer_properties, name='dashboard_marketer_properties'),
    path('dashboard/properties/client/', views.dashboard_client_properties, name='dashboard_client_properties'),
    path('dashboard/wishlist/', views.dashboard_wishlist, name='dashboard_wishlist'),
]
