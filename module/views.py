from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from module.models import Module
from module.paginators import ModulesPaginator
from module.permissions import IsOwner
from module.serializers import ModuleSerializer


class ModuleCreateAPIView(generics.CreateAPIView):
    """Создание Модуля"""
    serializer_class = ModuleSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        new_module = serializer.save()
        new_module.owner = self.request.user
        new_module.save()


class ModuleListAPIView(generics.ListAPIView):
    """Просмотр списка Модулей"""
    serializer_class = ModuleSerializer
    queryset = Module.objects.all()
    pagination_class = ModulesPaginator


class ModuleRetrieveAPIView(generics.RetrieveAPIView):
    """Просмотр отдельного Модуля по идентификатору (id)"""
    serializer_class = ModuleSerializer
    queryset = Module.objects.all()
    permission_classes = [IsAuthenticated]


class ModuleUpdateAPIView(generics.UpdateAPIView):
    """Изменение Модуля"""
    serializer_class = ModuleSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Module.objects.filter(owner=self.request.user)


class ModuleDestroyAPIView(generics.DestroyAPIView):
    """Удаление Модуля"""
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Module.objects.filter(owner=self.request.user)
