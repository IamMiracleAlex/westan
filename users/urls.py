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
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/client/', views.client_dashboard, name='client_dashboard'),
    path('dashboard/marketer/', views.marketer_dashboard, name='marketer_dashboard'),
    path('dashboard/profile/', views.profile, name='profile'),
    path('dashboard/profile/<int:user_id>/', views.edit_profile, name='edit_profile'),

    path('test/', views.test, name='test'),
]
