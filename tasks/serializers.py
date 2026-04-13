from django.template.context_processors import request
from rest_framework import serializers
from .models import Task, Project, Comment


class ProjectSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'created_at', 'updated_at', 'user']
        read_only_fields = ['id', 'created_at', 'updated_at', 'user']


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    task_title = serializers.ReadOnlyField(source='task.title')

    class Meta:
        model = Comment
        fields = [
            'id', 'text', 'created_at', 'updated_at',
            'user', 'task', 'task_title'
        ]
        read_only_field = [
            'id', 'created_at', 'updated_at',
            'user', 'task_title'
        ]

    def validated_task(self, value):
        """Проверяет что данная задача существует"""
        if not Task.objects.filter(pk=value.pk).exists():
            raise serializers.ValidationError(
                "Указанная задача не существует или не принадлежит вам"
            )
        return value


class TaskSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    project_detail = ProjectSerializer(source='project', read_only=True, allow_null=True)
    project_id_for_write = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all(),
        source='project',
        write_only=True,
        allow_null=True,
        required=False
    )
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'created_at', 'updated_at',
            'due_date', 'priority', 'status',
            'user',
            'project_detail',
            'project_id_for_write',
            'comments'
        ]
        read_only_fields = [
            'id', 'created_at', 'updated_at', 'user', 'project_detail',
            'comments'
        ]

    def validate_project_id_for_write(self, value):
        """Проверяем что проект принадлежит текущему пользователю"""
        request = self.context.get('request')
        if value is not None and request:
            if value.user != request.user:
                raise serializers.ValidationError(
                    "Проект с указанным ID не существует или не принадлежит вам"
                )
        return value

    def create(self, validated_data):
        instance = super().create(validated_data)
        return Task.objects.select_related('project__user', 'user').get(pk=instance.pk)

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        return Task.objects.select_related('project__user', 'user').get(pk=instance.pk)
