from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .models import Task, Project


# BaseAPITestCase: Базовый класс для настройки тестовой среды Task и Project.
class BaseAPITestCase(APITestCase):
    """Базовый класс для настройки тестовой среды API"""
    def setUp(self):
        # 1. Создаем тестовых пользователей
        self.user1 = User.objects.create_user(username='testuser1', email='test1@example.com', password='testpassword1')
        self.user2 = User.objects.create_user(username='testuser2', email='test2@example.com', password='testpassword2')

        # 2. Создаем или получаем токены для этих пользователей
        self.token1 = Token.objects.create(user=self.user1).key
        self.token2 = Token.objects.create(user=self.user2).key

        # 3. Создаем тестовые проекты
        self.project1_alpha = Project.objects.create(
            title="Project Alpha", description="First project for user1", user=self.user1
        )
        self.project1_beta = Project.objects.create(
            title="Project Beta", description="Second project for user1", user=self.user1
        )
        self.project2_delta = Project.objects.create(
            title="Project Delta", description="Project for user2", user=self.user2
        )

        # 4. Создаем тестовые задачи
        # Задача для user1, без проекта
        self.task1_no_project = Task.objects.create(
            title="Task for User 1 (No Project)",
            description="This task belongs to user 1, no project.",
            user=self.user1,
            due_date="2026-04-01",
            priority="high",
            status="new",
            project=None
        )
        # Задача для user1, с проектом project1_alpha
        self.task1_with_project_alpha = Task.objects.create(
            title="Task for Project Alpha",
            description="Second task for Project Alpha.",
            user=self.user1,
            due_date="2026-05-01",
            priority="high",
            status="new",
            project=self.project1_alpha
        )
        # Задача для user2, без проекта
        self.task2_no_project = Task.objects.create(
            title="Task for User 2 (No Project)",
            description="This task belongs to user 2, no project.",
            user=self.user2,
            due_date="2026-04-03",
            priority="low",
            status="completed",
            project=None
        )
        # Задача для user2, с проектом project2_delta
        self.task2_with_project_delta = Task.objects.create(
            title="Task for Project Delta",
            description="This is task number two for Project Delta",
            user=self.user2,
            due_date="2026-05-04",
            priority="low",
            status="completed",
            project=self.project2_delta
        )

        # 5. Определяем URL для нашего API
        self.task_list_url = reverse('task-list')
        self.project_list_url = reverse('project-list')



# TaskAPITests: Класс для тестирования API-интерфейса TaskViewSet (ОБНОВЛЕННЫЙ).
class TaskAPITests(BaseAPITestCase):

    def test_unauthenticated_user_cannot_list_tasks(self):
        """ Неаутентифицированный пользователь не должен иметь доступ к списку задач"""
        response = self.client.get(self.task_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_can_list_only_their_tasks_with_project_detail(self):
        """ Аутентифицированный пользователь должен видеть только свои задачи"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token1)
        response = self.client.get(self.task_list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

        titles_in_response = {task['title'] for task in response.data['results']}
        self.assertIn(self.task1_no_project.title, titles_in_response)
        self.assertIn(self.task1_with_project_alpha.title, titles_in_response)
        self.assertNotIn(self.task2_no_project.title, titles_in_response)
        self.assertNotIn(self.task2_with_project_delta.title, titles_in_response)

        # Проверяем детали project_detail
        for task_data in response.data['results']:
            if task_data['id'] == self.task1_no_project.id:
                self.assertIsNone(task_data['project_detail'])
            elif task_data['id'] == self.task1_with_project_alpha.id:
                self.assertEqual(task_data['project_detail']['id'], self.project1_alpha.id)
                self.assertEqual(task_data['project_detail']['title'], self.project1_alpha.title)
                self.assertEqual(task_data['user'], self.user1.username)


    def test_authenticated_user_can_create_a_task_without_project(self):
        """ Аутентифицированный пользователь должен иметь возможность создать задачу без проекта"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token1)
        data = {
            "title": "New Task from Test without Project",
            "description": "Created via API test.",
            "due_date": "2026-04-04",
            "priority": "medium",
            "status": "new"
        }
        response = self.client.post(self.task_list_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(Task.objects.count(), 5)
        self.assertEqual(response.data['user'], self.user1.username)
        self.assertIsNone(response.data['project_detail'])


    def test_authenticated_user_can_create_a_task_with_project(self):
        """ Аутентифицированный пользователь должен иметь возможность создать задачу с привязкой к своему проекту"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token1)
        data = {
            "title": "New Task from Test with Project",
            "description": "Created via API test for Project Alpha.",
            "due_date": "2026-04-05",
            "priority": "high",
            "status": "in_progress",
            "project_id_for_write": self.project1_alpha.id
        }
        response = self.client.post(self.task_list_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(Task.objects.count(), 5)
        self.assertEqual(response.data['user'], self.user1.username)
        self.assertEqual(response.data['project_detail']['id'], self.project1_alpha.id)
        self.assertEqual(response.data['project_detail']['title'], self.project1_alpha.title)


    def test_authenticated_user_cannot_create_task_with_another_users_project(self):
        """ Аутентифицированный пользователь не должен иметь возможность создать задачу с привязкой к чужому проекту"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token1)
        data = {
            "title": "Task with other user's project",
            "description": "Should fail.",
            "due_date": "2026-04-06",
            "priority": "medium",
            "status": "new",
            "project_id_for_write": self.project2_delta.id
        }
        response = self.client.post(self.task_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertIn(
            "Проект с указанным ID не существует или не принадлежит вам",
            str(response.data['project_id_for_write'])
        )


    def test_unauthenticated_user_cannot_create_a_task(self):
        """Неаутентифицированный пользователь не должен иметь возможность создать задачу"""
        data = {
            "title": "Unauthorized Task",
            "description": "Should not be created.",
            "due_date": "2026-04-07",
        }
        response = self.client.post(self.task_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Task.objects.count(), 4) # Количество задач не должно измениться


    def test_authenticated_user_can_retrieve_their_task_with_project_detail(self):
        """Аутентифицированный пользователь должен иметь возможность получить детали своей задачи"""
        detail_url = reverse('task-detail', kwargs={'pk': self.task1_with_project_alpha.pk})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token1)
        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.task1_with_project_alpha.title)
        self.assertEqual(response.data['project_detail']['id'], self.project1_alpha.id)
        self.assertEqual(response.data['project_detail']['title'], self.project1_alpha.title)
        self.assertEqual(response.data['user'], self.user1.username)


    def test_authenticated_user_cannot_retrieve_another_users_task(self):
        """Аутентифицированный пользователь не должен иметь возможность получить детали чужой задачи"""
        detail_url = reverse('task-detail', kwargs={'pk': self.task2_with_project_delta.pk})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token1) # user1 пытается получить
        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_authenticated_user_can_update_their_task(self):
        """ Аутентифицированный пользователь должен иметь возможность обновить свою задачу"""
        detail_url = reverse('task-detail', kwargs={'pk': self.task1_with_project_alpha.pk})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token1)
        updated_data = {
            "title": "UPDATED Task for User 1",
            "description": "This task has been updated with new project.",
            "due_date": "2026-04-10",
            "priority": "low",
            "status": "completed",
            "project_id_for_write": self.project1_beta.id
        }
        response = self.client.put(detail_url, updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task1_with_project_alpha.refresh_from_db()
        self.assertEqual(self.task1_with_project_alpha.title, "UPDATED Task for User 1")
        self.assertEqual(self.task1_with_project_alpha.project.id, self.project1_beta.id)


    def test_authenticated_user_cannot_update_another_users_task(self):
        """ Аутентифицированный пользователь не должен иметь возможность обновить чужую задачу."""
        detail_url = reverse('task-detail', kwargs={'pk': self.task2_no_project.pk})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token1) # user1 пытается обновить task2
        updated_data = {"title": "Attempt to update", "status": "completed"}
        response = self.client.put(detail_url, updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        task_before_update = Task.objects.get(pk=self.task2_no_project.pk)
        self.assertNotEqual(task_before_update.title, "Attempt to update")


    def test_authenticated_user_can_delete_their_task(self):
        """ Аутентифицированный пользователь должен иметь возможность удалить свою задачу"""
        initial_task_count = Task.objects.count() # Получаем количество перед удалением
        detail_url = reverse('task-detail', kwargs={'pk': self.task1_no_project.pk})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token1)
        response = self.client.delete(detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), initial_task_count - 1)
        self.assertFalse(Task.objects.filter(pk=self.task1_no_project.pk).exists())


    def test_authenticated_user_cannot_delete_another_users_task(self):
        """ Аутентифицированный пользователь не должен иметь возможность удалить чужую задачу"""
        detail_url = reverse('task-detail', kwargs={'pk': self.task2_no_project.pk})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token1)
        response = self.client.delete(detail_url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Task.objects.filter(pk=self.task2_no_project.pk).exists())


# ProjectAPITests: Класс для тестирования API-интерфейса ProjectViewSet.
class ProjectAPITests(BaseAPITestCase): # <--- Наследуем от BaseAPITestCase

    def test_unauthenticated_user_cannot_list_projects(self):
        """ Неаутентифицированный пользователь не должен иметь доступ к списку проектов"""
        response = self.client.get(self.project_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_authenticated_user_can_list_only_their_projects(self):
        """ Аутентифицированный пользователь должен видеть только свои проекты"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token1)
        response = self.client.get(self.project_list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2) # user1 имеет 2 проекта

        # Проверяем наличие по заголовкам
        titles_in_response = {proj['title'] for proj in response.data['results']}
        self.assertIn(self.project1_alpha.title, titles_in_response)
        self.assertIn(self.project1_beta.title, titles_in_response)
        self.assertNotIn(self.project2_delta.title, titles_in_response)


    def test_authenticated_user_can_create_a_project(self):
        """ Аутентифицированный пользователь должен иметь возможность создать проект"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token1)
        data = {
            "title": "New Project from Test",
            "description": "Created via API test for user1."
        }
        response = self.client.post(self.project_list_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(Project.objects.count(), 4) # Было 3, стало 4
        self.assertEqual(response.data['user'], self.user1.username) # user ожидаем username


    def test_unauthenticated_user_cannot_create_a_project(self):
        """ Неаутентифицированный пользователь не должен иметь возможность создать проект"""
        data = {"title": "Unauthorized Project", "description": "Should not be created."}
        response = self.client.post(self.project_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Project.objects.count(), 3) # Количество проектов не должно измениться


    def test_authenticated_user_can_retrieve_their_project(self):
        """ Аутентифицированный пользователь должен иметь возможность получить детали своего проекта"""
        detail_url = reverse('project-detail', kwargs={'pk': self.project1_alpha.pk})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token1)
        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.project1_alpha.title)
        self.assertEqual(response.data['user'], self.user1.username)


    def test_authenticated_user_cannot_retrieve_another_users_project(self):
        """ Аутентифицированный пользователь не должен иметь возможность получить детали чужого проекта"""
        detail_url = reverse('project-detail', kwargs={'pk': self.project2_delta.pk})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token1)
        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_authenticated_user_can_update_their_project(self):
        """ Аутентифицированный пользователь должен иметь возможность обновить свой проект"""
        detail_url = reverse('project-detail', kwargs={'pk': self.project1_alpha.pk})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token1)
        updated_data = {"title": "Updated Project Name", "description": "Updated Description"}
        response = self.client.put(detail_url, updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.project1_alpha.refresh_from_db()
        self.assertEqual(self.project1_alpha.title, "Updated Project Name")


    def test_authenticated_user_cannot_update_another_users_project(self):
        """ Аутентифицированный пользователь не должен иметь возможность обновить чужой проект"""
        detail_url = reverse('project-detail', kwargs={'pk': self.project2_delta.pk})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token1)
        updated_data = {"title": "Attempt to Update", "description": "Should not change"}
        response = self.client.put(detail_url, updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        project_before_update = Project.objects.get(pk=self.project2_delta.pk)
        self.assertNotEqual(project_before_update.title, "Attempt to Update")


    def test_authenticated_user_can_delete_their_project(self):
        """ Аутентифицированный пользователь должен иметь возможность удалить свой проект"""
        initial_project_count = Project.objects.count()
        detail_url = reverse('project-detail', kwargs={'pk': self.project1_alpha.pk})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token1)
        response = self.client.delete(detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Project.objects.count(), initial_project_count - 1)
        self.assertFalse(Project.objects.filter(pk=self.project1_alpha.pk).exists())


    def test_authenticated_user_cannot_delete_another_users_project(self):
        """ Аутентифицированный пользователь не должен иметь возможность удалить чужой проект"""
        detail_url = reverse('project-detail', kwargs={'pk': self.project2_delta.pk})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token1)
        response = self.client.delete(detail_url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Project.objects.filter(pk=self.project2_delta.pk).exists())
