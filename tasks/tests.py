from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from .models import Task

class TaskModelTests(TestCase):
    def setUp(self):
        self.task = Task.objects.create(
            title='Deploy to Cloud',
            description='Configure GitHub Actions and deploy on Render',
            priority=Task.Priority.HIGH,
            status=Task.Status.IN_PROGRESS,
            category=Task.Category.DEVELOPMENT,
            due_date=timezone.now().date() + timedelta(days=2)
        )

    def test_task_str(self):
        self.assertEqual(str(self.task), 'Deploy to Cloud')

    def test_is_completed(self):
        self.assertFalse(self.task.is_completed)
        self.task.status = Task.Status.COMPLETED
        self.task.save()
        self.assertTrue(self.task.is_completed)

    def test_is_overdue(self):
        self.assertFalse(self.task.is_overdue)
        self.task.due_date = timezone.now().date() - timedelta(days=1)
        self.task.status = Task.Status.PENDING
        self.task.save()
        self.assertTrue(self.task.is_overdue)

class TaskViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.task = Task.objects.create(
            title='Initial Sample Task',
            description='Test description',
            priority=Task.Priority.MEDIUM,
            status=Task.Status.PENDING,
            category=Task.Category.WORK
        )

    def test_task_list_view(self):
        response = self.client.get(reverse('tasks:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Initial Sample Task')
        self.assertEqual(response.context['total_count'], 1)

    def test_task_search(self):
        response = self.client.get(reverse('tasks:list') + '?q=Sample')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Initial Sample Task')

        response = self.client.get(reverse('tasks:list') + '?q=NonExistentTaskXYZ')
        self.assertNotContains(response, 'Initial Sample Task')

    def test_task_create_view(self):
        response = self.client.post(reverse('tasks:create'), {
            'title': 'New Functional Task',
            'description': 'Created via test',
            'category': Task.Category.WORK,
            'priority': Task.Priority.HIGH,
            'status': Task.Status.PENDING,
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(title='New Functional Task').exists())

    def test_task_update_view(self):
        response = self.client.post(reverse('tasks:update', args=[self.task.pk]), {
            'title': 'Updated Title',
            'description': 'Updated description',
            'category': Task.Category.DESIGN,
            'priority': Task.Priority.LOW,
            'status': Task.Status.IN_PROGRESS,
        })
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Updated Title')
        self.assertEqual(self.task.priority, Task.Priority.LOW)

    def test_task_toggle_view(self):
        self.assertEqual(self.task.status, Task.Status.PENDING)
        response = self.client.post(reverse('tasks:toggle', args=[self.task.pk]))
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertEqual(self.task.status, Task.Status.COMPLETED)

    def test_task_delete_view(self):
        response = self.client.post(reverse('tasks:delete', args=[self.task.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())

    def test_health_check_view(self):
        response = self.client.get(reverse('tasks:health'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'healthy')
        self.assertEqual(data['app'], 'TaskPulse Django')
