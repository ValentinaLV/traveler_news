from django.urls import path

from .views import user_sign_up, activate_account

urlpatterns = [
    path('accounts/register/', user_sign_up, name='django_registration_register'),
    path('activate/<uuid>', activate_account, name='activate'),

]
