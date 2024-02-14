from users import views
from users.apps import UsersConfig

from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = UsersConfig.name


urlpatterns = [
    path('user/register/', views.UserCreate.as_view(), name='user_create'),
    path('users/list/', views.UsersList.as_view(), name='users_list'),
    path('user/<int:pk>/', views.UserRetrieve.as_view(), name='user_detail'),
    path('user/update/<int:pk>/', views.UserUpdate.as_view(),
         name='user_update'),
    path('user/delete/<int:pk>/', views.UserDestroy.as_view(),
         name='user_delete'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
