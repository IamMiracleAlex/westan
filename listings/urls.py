from django.urls import path
from listings import views

app_name = 'listings'


urlpatterns = [
    path('', views.index, name='index'),
    path('listings/', views.listings, name='listings'),
    path('listing/<int:id>/<slug:slug>/', views.single_listing, name='single_lisitng'),
    path('search/', views.search, name='search'),
    path('add-wishlist/', views.add_wishlist, name='add_wishlist'),
    path('sort/<str:by>', views.sort, name='sort'),
    path('dashboard/properties/', views.dashboard_properties, name='dashboard_properties'),
    path('dashboard/marketer/properties/', views.dashboard_marketer_properties, name='dashboard_marketer_properties'),
    path('dashboard/client/properties/', views.dashboard_client_properties, name='dashboard_client_properties'),
    path('dashboard/client/property/<int:id>/<slug:slug>/', views.dashboard_client_single_properties, name='dashboard_client_single_properties'),
]
