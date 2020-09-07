from django.urls import path
from blog import views

app_name = 'blog'

urlpatterns = [
    path('', views.blog_index, name='blog_index'),
    path('<int:pk>/<slug:slug>/', views.blog_single, name='blog_single'),
    path('tag/<slug:tag_slug>/', views.blog_index, name='posts_by_tag'),
    path('search/', views.blog_search, name='blog_search'),

]
