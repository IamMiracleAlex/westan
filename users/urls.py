from django.urls import path

from users import views
from django.contrib.auth import views as auth_views



app_name = 'users'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('s/<str:refer_code>/', views.signup, name='signup'),
    path('activate-email/<str:uid>/<str:token>/', views.activate_email, name='activate_email'),
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', 
                    auth_views.PasswordResetDoneView.as_view(),
                    name='password_reset_done'),
    path('reset/<str:uidb64>/<str:token>/',
            auth_views.PasswordResetConfirmView.as_view(),
            name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('test/', views.test, name='test'),
]


# accounts/login/ [name='login']
# accounts/logout/ [name='logout']
# accounts/password_change/ [name='password_change']
# accounts/password_change/done/ [name='password_change_done']

# accounts/password_reset/ [name='password_reset']
# accounts/password_reset/done/ [name='password_reset_done']
# accounts/reset/<uidb64>/<token>/ [name='password_reset_confirm']
# accounts/reset/done/ [name='password_reset_complete']
