from django.urls import path
from listings import views

app_name = 'listings'


urlpatterns = [
    path('', views.index, name='index'),
    path('listings/', views.listings, name='listings'),
    path('listing/-<int:id>/<slug:slug>/', views.single_listing, name='single_lisitng'),
]