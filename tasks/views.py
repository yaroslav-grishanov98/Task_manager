import django_filters.rest_framework
from rest_framework import viewsets, permissions, filters
from .models import Task, Project, Comment
from .serializers import TaskSerializer, ProjectSerializer, CommentSerializer
from .filters import TaskFilter
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from .auth_views import UserRegistrationView, CustomAuthToken


@extend_schema(
    description="API для управления пользовательскими проектами",
    tags = ["проекты"]
)

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


@extend_schema(
    description="API для управления задачами",
    parameters=[
        OpenApiParameter(name='status', type=OpenApiTypes.STR, description='Фильтр по статусу задачи (new, in_progress, completed, canceled)',
                         enum=['new', 'in_progress', 'completed', 'canceled'], required=False),
        OpenApiParameter(name='priority', type=OpenApiTypes.STR, description='Фильтр по приоритету задачи (low, medium, high)',
                         enum=['low', 'medium', 'high'], required=False),
        OpenApiParameter(name='due_date_before', type=OpenApiTypes.DATE, description='Фильтр по сроку выполнения (до даты: YYYY-MM-DD)', required=False),
        OpenApiParameter(name='due_date_after', type=OpenApiTypes.DATE, description='Фильтр по сроку выполнения (после даты: YYYY-MM-DD)', required=False),
        OpenApiParameter(name='search', type=OpenApiTypes.STR, description='Поиск по заголовку или описанию задачи', required=False),
        OpenApiParameter(name='project', type=OpenApiTypes.INT, description='Фильтр по ID проекта', required=False),
    ],
    tags=['Задачи']
)

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter]
    filterset_class = TaskFilter
    search_fields = ['title', 'description']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


@extend_schema(
    description="API для управления комментариями",
    tags=['Комментарии']
)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """Проверяем, что задача, к которой привязывается комментарий, существует и принадлежит текущему пользователю"""
        task_id = self.request.data.get('task')
        try:
            task = Task.objects.get(pk=task_id, user= self.request.user)
        except Task.DoesNotExist:
            raise serializer.ValidationError ("Задача с указанным айди не существует или не принадлежит вам")

        serializer.save(user=self.request.user, task=task)

    def get_queryset(self):
        return self.queryset.filter(task__user=self.request.user)

