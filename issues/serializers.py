from rest_framework import serializers
from .models import (
    Issue, Comment, TipoIssue, EstadoIssue,
    PrioridadIssue, SeveridadIssue, File
)

class TipoIssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoIssue
        fields = ['id', 'nombre']

class EstadoIssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoIssue
        fields = ['id', 'nombre']

class PrioridadIssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrioridadIssue
        fields = ['id', 'nombre']

class SeveridadIssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeveridadIssue
        fields = ['id', 'nombre']

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id', 'name', 'file', 'uploaded_at', 'user', 'issue']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_at', 'author', 'issue']

class IssueSerializer(serializers.ModelSerializer):
    tipo = TipoIssueSerializer(read_only=True)
    estado = EstadoIssueSerializer(read_only=True)
    prioridad = PrioridadIssueSerializer(read_only=True)
    severidad = SeveridadIssueSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    files = FileSerializer(many=True, read_only=True)

    class Meta:
        model = Issue
        fields = [
            'id', 'subject', 'description', 'tipo', 'estado',
            'prioridad', 'severidad', 'created_at', 'updated_at',
            'user_assigned', 'watchers', 'comments', 'files'
        ] 