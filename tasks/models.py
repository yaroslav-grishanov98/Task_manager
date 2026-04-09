from django.db import models
from django.contrib.auth.models import User



class Project(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название проекта')
    description = models.TextField(blank=True, verbose_name='Описание проекта')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name='Последнее обновление')

    # Каждый пункт принадлежит одному пользователю
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='project',
        verbose_name='Владелец проекта'
    )

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'
        ordering = ['title']

    def __str__(self):
        return self.title


class Task(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    description = models.TextField(blank=True, verbose_name='Описание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения')
    due_date = models.DateField(null=True, blank=True, verbose_name='Срок выполнения')

    # Приоритетные задачи
    PRIORITY_CHOICES = [
        ('low', 'Низкий'),
        ('medium', 'Средний'),
        ('high', 'Высокий')
    ]
    priority = models.CharField(   # CharField - текстовое поле с ограниченной длиной.
        max_length= 10,
        choices= PRIORITY_CHOICES,
        default = 'medium',
        verbose_name= 'Приоритет'
    )

    # Статус задачи
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('in_progress', 'В работе'),
        ('completed', 'Завершена'),
        ('canceled', 'Отменена')
    ]
    status = models.CharField( # CharField - текстовое поле с ограниченной длиной.
        max_length=20,
        choices= STATUS_CHOICES,
        default= 'new',
        verbose_name= 'Статус'
    )

    project = models.ForeignKey(
        Project,
        on_delete=models.SET_NULL,
        related_name='tasks',
        blank=True, null=True,
        verbose_name='Проект'
    )

    # Связь с пользователем
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE, # models.CASCADE: Если пользователь удаляется, все его задачи также удаляются.
        related_name= 'reborn_tasks',
        verbose_name= 'Пользователь'
    )

    class Meta:  # Класс Meta используется для определения "метаданных" модели, то есть не-полевых вещей,
    # таких как порядок сортировки по умолчанию, удобочитаемые названия и т.д.
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
        ordering = ['-created_at']

    def __str__(self): # --- Метод __str__ ---
    # Определяет строковое представление объекта. Очень полезно для админ-панели Django (чтобы видеть название задачи,
    # а не просто "Task object (1)") и при отладке в консоли.
        return self.title








