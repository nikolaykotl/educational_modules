from django.urls import reverse
from rest_framework.test import APITestCase
from django.test import TestCase
from rest_framework import status

from users.models import User
from users.serializers import UserSerializer


class ModuleTest(TestCase):
    """Test for Module model"""

    def setUp(self):
        User.objects.create(
            email='test@test.ru',
            first_name='Test',
            password='test'
        )

    def test_user_first_name(self):
        module = User.objects.get(email='test@test.ru')
        self.assertEqual(module.first_name, 'Test')


class UserSerializerTest(TestCase):
    """Тест для UserSerializer"""

    def setUp(self):
        self.user = User.objects.create(
            email='test@test.ru',
            password='test',
            first_name='Test',
            last_name='Testov'
        )

        self.serializer = UserSerializer(instance=self.user)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertEqual(set(data.keys()),
                         set(['email', 'first_name', 'last_name', 'phone']))


class UserTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='test@test.com', is_staff=True, is_superuser=True)
        self.user.set_password('1234')
        self.user.save()

        response = self.client.post(
            '/users/token/',
            {'email': 'test@test.com', 'password': "1234"}
        )
        self.access_token = response.json().get('access')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

    def test_create_user(self):
        """Тест создание пользователя"""
        data = {
            'email': 'Test@testov.com',
            'password': 'test_2',
        }
        response = self.client.post(reverse('users:user_create'),
                                    data=data, format='json')

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertTrue(
            User.objects.all().exists()
        )

    def test_list_users(self):
        """Тест просмотр списка пользователей"""
        response = self.client.get(
            reverse('users:users_list'),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_retrieve_user(self):
        """Тест просмотр деталей профиля пользователя"""
        self.test_create_user()
        pk = User.objects.all().latest('pk').pk
        response = self.client.get(
            reverse('users:user_detail', args=[pk]),
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                'email': 'Test@testov.com',
                'first_name': None,
                'last_name': None,
                'phone': None,
            }
        )

    def test_update_user(self):
        """Тест обновление (изменение) пользователя"""
        self.test_create_user()
        pk = User.objects.all().latest('pk').pk
        data = {'first_name': 'Test_update'}
        response = self.client.patch(
            reverse('users:user_update', args=[pk]),
            data=data,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                'email': 'Test@testov.com',
                'first_name': 'Test_update',
                'last_name': None,
                'phone': None,

            }
        )

    def test_destroy_user(self):
        """Тест удаления пользователя"""
        self.test_create_user()
        pk = User.objects.all().latest('pk').pk
        response = self.client.delete(reverse('users:user_delete', args=[pk]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
