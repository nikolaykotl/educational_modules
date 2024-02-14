from django.urls import path

from module.views import ModuleCreateAPIView, ModuleListAPIView, \
    ModuleRetrieveAPIView, ModuleUpdateAPIView, \
    ModuleDestroyAPIView

urlpatterns = [
    path('module/create/', ModuleCreateAPIView.as_view(),
         name='create_module'),
    path('', ModuleListAPIView.as_view(), name='list_modules'),
    path('module/<int:pk>/', ModuleRetrieveAPIView.as_view(),
         name='detail_module'),
    path('module/update/<int:pk>/', ModuleUpdateAPIView.as_view(),
         name='update_module'),
    path('module/delete/<int:pk>/', ModuleDestroyAPIView.as_view(),
         name='delete_module'),
]
