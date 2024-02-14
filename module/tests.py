from rest_framework.test import APITestCase
from django.urls import reverse

from module.serializers import ModuleSerializer
from users.models import User
from rest_framework import status

from django.test import TestCase

from module.models import Module


class ModuleTest(TestCase):
    """Тест для модели Module"""

    def setUp(self):

        Module.objects.create(
            name='Test',
            description='Test description'
        )

    def test_module_name(self):
        pk = Module.objects.all().latest('pk').pk
        module = Module.objects.get(pk=pk)
        self.assertEqual(module.name, 'Test')

    def test_module_description(self):
        pk = Module.objects.all().latest('pk').pk
        module = Module.objects.get(pk=pk)
        self.assertEqual(module.description, 'Test description')


class ModuleSerializerTest(TestCase):
    """Тест для ModuleSerializer"""
    def setUp(self):
        self.module = Module.objects.create(
            name='Test',
            description='Test description'
        )
        self.serializer = ModuleSerializer(instance=self.module)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set(['id',
                                                'name',
                                                'description',
                                                'owner']))


class ModuleTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='test@test.com',
                                        is_staff=True,
                                        is_superuser=True)
        self.user.set_password('test_password')
        self.user.save()
        self.client.force_authenticate(user=self.user)

    def test_create_module(self):
        """Тест создания Модуля"""
        data = {
            'name': 'Test',
            'description': 'Test description',
            }
        response = self.client.post(reverse('modules:create_module'),
                                    data=data, format='json')
        pk = Module.objects.all().latest('pk').pk
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.json(),
            {
                "id": pk,
                "name": "Test",
                "description": "Test description",
                "owner": self.user.pk
            }
        )

    def test_list_modules(self):
        """Тест просмотра списка Модулей"""
        self.test_create_module()
        response = self.client.get(reverse('modules:list_modules'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json()['results'],
            [
                {
                    "id": response.json()['results'][0]['id'],
                    "name": "Test",
                    "description": "Test description",
                    "owner": self.user.pk
                }
            ]
        )

    def test_retrieve_module(self):
        """Тест просмотра Модуля по id"""
        self.test_create_module()
        pk = Module.objects.all().latest('pk').pk
        response = self.client.get(
            reverse('modules:detail_module', args=[pk]),
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                "id": pk,
                "name": "Test",
                "description": "Test description",
                "owner": self.user.pk
            }
        )

    def test_update_module(self):
        """Тест обновления (изменения) Модуля"""
        self.test_create_module()
        pk = Module.objects.all().latest('pk').pk
        data = {'description': 'Description update'}
        response = self.client.patch(
            reverse('modules:update_module', args=[pk]),
            data=data,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                'id': pk,
                'name': 'Test',
                'description': 'Description update',
                'owner': self.user.pk
            }
        )

    def test_destroy_module(self):
        """Тест удаления Модуля"""
        self.test_create_module()
        pk = Module.objects.all().latest('pk').pk
        response = self.client.delete(reverse('modules:delete_module',
                                              args=[pk]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
