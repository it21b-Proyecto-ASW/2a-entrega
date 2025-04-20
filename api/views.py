from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth.models import User
from issues.models import Issue, Comment, Attachment, TipoIssue, EstadoIssue, PrioridadIssue, SeveridadIssue
from .serializers import (
    UserSerializer, IssueSerializer, CommentSerializer, AttachmentSerializer,
    TipoIssueSerializer, EstadoIssueSerializer, PrioridadIssueSerializer, SeveridadIssueSerializer
)
import firebase_admin
from firebase_admin import credentials, storage
from django.conf import settings
import os

# Initialize Firebase Admin SDK
if not firebase_admin._apps:
    cred = credentials.Certificate(settings.FIREBASE_CONFIG)
    firebase_admin.initialize_app(cred, {
        'storageBucket': settings.FIREBASE_CONFIG['storageBucket']
    })

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class TipoIssueViewSet(viewsets.ModelViewSet):
    queryset = TipoIssue.objects.all()
    serializer_class = TipoIssueSerializer
    permission_classes = [permissions.IsAuthenticated]

class EstadoIssueViewSet(viewsets.ModelViewSet):
    queryset = EstadoIssue.objects.all()
    serializer_class = EstadoIssueSerializer
    permission_classes = [permissions.IsAuthenticated]

class PrioridadIssueViewSet(viewsets.ModelViewSet):
    queryset = PrioridadIssue.objects.all()
    serializer_class = PrioridadIssueSerializer
    permission_classes = [permissions.IsAuthenticated]

class SeveridadIssueViewSet(viewsets.ModelViewSet):
    queryset = SeveridadIssue.objects.all()
    serializer_class = SeveridadIssueSerializer
    permission_classes = [permissions.IsAuthenticated]

class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    @action(detail=True, methods=['post'])
    def add_comment(self, request, pk=None):
        issue = self.get_object()
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(issue_id=issue, author=request.user.username)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def upload_attachment(self, request, pk=None):
        issue = self.get_object()
        file_obj = request.FILES.get('file')
        
        if not file_obj:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)

        # Upload to Firebase Storage
        bucket = storage.bucket()
        blob = bucket.blob(f'issue_{issue.id}/{file_obj.name}')
        blob.upload_from_file(file_obj)

        # Make the blob publicly accessible
        blob.make_public()

        # Create Attachment object
        attachment = Attachment.objects.create(
            issue=issue,
            file=blob.public_url
        )

        serializer = AttachmentSerializer(attachment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def add_watcher(self, request, pk=None):
        issue = self.get_object()
        user_id = request.data.get('user_id')
        
        try:
            user = User.objects.get(id=user_id)
            issue.watchers.add(user)
            return Response({'status': 'watcher added'})
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'])
    def remove_watcher(self, request, pk=None):
        issue = self.get_object()
        user_id = request.data.get('user_id')
        
        try:
            user = User.objects.get(id=user_id)
            issue.watchers.remove(user)
            return Response({'status': 'watcher removed'})
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user.username)

class AttachmentViewSet(viewsets.ModelViewSet):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def perform_destroy(self, instance):
        # Delete file from Firebase Storage
        if instance.file:
            try:
                bucket = storage.bucket()
                blob = bucket.blob(instance.file.name)
                blob.delete()
            except Exception as e:
                print(f"Error deleting file from Firebase Storage: {e}")
        
        instance.delete()
