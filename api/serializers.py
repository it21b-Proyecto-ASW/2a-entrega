from rest_framework import serializers
from django.contrib.auth.models import User
from issues.models import Issue, Comment, Attachment, TipoIssue, EstadoIssue, PrioridadIssue, SeveridadIssue

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class TipoIssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoIssue
        fields = ['id', 'nombre']

class EstadoIssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoIssue
        fields = ['id', 'nombre', 'es_cerrado']

class PrioridadIssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrioridadIssue
        fields = ['id', 'nombre', 'nivel']

class SeveridadIssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeveridadIssue
        fields = ['id', 'nombre', 'impacto']

class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = ['id', 'file', 'uploaded_at']

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'issue_id', 'author', 'text', 'created_at']

class IssueSerializer(serializers.ModelSerializer):
    estado = EstadoIssueSerializer(read_only=True)
    tipo = TipoIssueSerializer(read_only=True)
    prioridad = PrioridadIssueSerializer(read_only=True)
    severidad = SeveridadIssueSerializer(read_only=True)
    user_assigned = UserSerializer(many=True, read_only=True)
    watchers = UserSerializer(many=True, read_only=True)
    attachments = AttachmentSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True, source='comment_set')

    class Meta:
        model = Issue
        fields = [
            'id', 'subject', 'description', 'creation_date', 'estado',
            'tipo', 'prioridad', 'severidad', 'deadline', 'user_assigned',
            'watchers', 'last_modified', 'attachments', 'comments'
        ]

    def create(self, validated_data):
        estado_id = self.context['request'].data.get('estado')
        tipo_id = self.context['request'].data.get('tipo')
        prioridad_id = self.context['request'].data.get('prioridad')
        severidad_id = self.context['request'].data.get('severidad')
        user_assigned_ids = self.context['request'].data.getlist('user_assigned')
        watchers_ids = self.context['request'].data.getlist('watchers')

        issue = Issue.objects.create(**validated_data)

        if estado_id:
            issue.estado_id = estado_id
        if tipo_id:
            issue.tipo_id = tipo_id
        if prioridad_id:
            issue.prioridad_id = prioridad_id
        if severidad_id:
            issue.severidad_id = severidad_id

        issue.save()

        if user_assigned_ids:
            issue.user_assigned.set(User.objects.filter(id__in=user_assigned_ids))
        if watchers_ids:
            issue.watchers.set(User.objects.filter(id__in=watchers_ids))

        return issue

    def update(self, instance, validated_data):
        estado_id = self.context['request'].data.get('estado')
        tipo_id = self.context['request'].data.get('tipo')
        prioridad_id = self.context['request'].data.get('prioridad')
        severidad_id = self.context['request'].data.get('severidad')
        user_assigned_ids = self.context['request'].data.getlist('user_assigned')
        watchers_ids = self.context['request'].data.getlist('watchers')

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if estado_id:
            instance.estado_id = estado_id
        if tipo_id:
            instance.tipo_id = tipo_id
        if prioridad_id:
            instance.prioridad_id = prioridad_id
        if severidad_id:
            instance.severidad_id = severidad_id

        instance.save()

        if user_assigned_ids:
            instance.user_assigned.set(User.objects.filter(id__in=user_assigned_ids))
        if watchers_ids:
            instance.watchers.set(User.objects.filter(id__in=watchers_ids))

        return instance 