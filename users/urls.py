from django.urls import path

from users import views


app_name = 'users'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('s/<str:refer_code>/', views.signup, name='signup'),
    path('activate-email/<str:uid>/<str:token>/', views.activate_email, name='activate_email'),
    path('resend-activation-email/', views.resend_activation_email, name='resend_activation_email'),
    path('subscribe/', views.subscribe, name='subscribe'),

    path('test/', views.test, name='test'),
]
