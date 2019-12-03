from django.urls import path
from users import views as user_view


app_name = 'users'
urlpatterns = [

    path('register/', user_view.register, name='user-register'),
    path('profile/', user_view.profile, name='user-profile'),
    path('register/complete/', user_view.register_complete, name='register-complete'),
    path('register/account/activation/', user_view.user_account_activation_sent, name='user_account_activation_sent'),
    path('activate/<uidb64>/<token>/', user_view.activate, name='activate'),
]