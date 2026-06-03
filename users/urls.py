from django.urls import path
from .views import ManageUsersView

urlpatterns = [
    path('', ManageUsersView.as_view(), name='users_manage'),
]
