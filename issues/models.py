from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import datetime
from django.core.exceptions import ValidationError


class TipoIssue(models.Model):
    nombre = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.nombre

    def delete(self, *args, **kwargs):
        if TipoIssue.objects.count() <= 1:
            raise ValidationError("No se puede eliminar el único tipo existente")
        super().delete(*args, **kwargs)


class EstadoIssue(models.Model):
    nombre = models.CharField(max_length=40, unique=True)
    es_cerrado = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre

    def delete(self, *args, **kwargs):
        if EstadoIssue.objects.count() <= 1:
            raise ValidationError("No se puede eliminar el único estado existente")
        super().delete(*args, **kwargs)


class PrioridadIssue(models.Model):
    nombre = models.CharField(max_length=10, unique=True)
    nivel = models.IntegerField(default=0)

    def __str__(self):
        return self.nombre

    def delete(self, *args, **kwargs):
        if PrioridadIssue.objects.count() <= 1:
            raise ValidationError("No se puede eliminar la única prioridad existente")
        super().delete(*args, **kwargs)


class SeveridadIssue(models.Model):
    nombre = models.CharField(max_length=30, unique=True)
    impacto = models.IntegerField(default=0)

    def __str__(self):
        return self.nombre

    def delete(self, *args, **kwargs):
        if SeveridadIssue.objects.count() <= 1:
            raise ValidationError("No se puede eliminar la única severidad existente")
        super().delete(*args, **kwargs)


class Issue(models.Model):
    subject = models.CharField(max_length=100)
    description = models.CharField(max_length=400)
    creation_date = models.DateField(default=datetime.today)
    estado = models.ForeignKey(EstadoIssue, on_delete=models.PROTECT, null=True, blank=True)
    tipo = models.ForeignKey(TipoIssue, on_delete=models.PROTECT, null=True, blank=True)
    prioridad = models.ForeignKey(PrioridadIssue, on_delete=models.PROTECT, null=True, blank=True)
    severidad = models.ForeignKey(SeveridadIssue, on_delete=models.PROTECT, null=True, blank=True)
    deadline = models.DateField(default=datetime.today, null=True, blank=True)
    user_assigned = models.ManyToManyField(User, related_name='assigned_issues', blank=True)
    watchers = models.ManyToManyField(User, related_name='watching_issues', blank=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject


class Comment(models.Model):
    issue_id = models.ForeignKey(Issue, on_delete=models.CASCADE)
    author = models.CharField(max_length=100)
    text = models.CharField(max_length=400)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text


class File(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='attachments/%Y/%m/%d/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='attachments', null=True, blank=True)

    def __str__(self):
        return self.name

    def get_file_url(self):
        """Retorna l'URL del fitxer des de S3"""
        return self.file.url

    def get_file_size(self):
        """Retorna la mida del fitxer en bytes"""
        return self.file.size

    class Meta:
        ordering = ['-uploaded_at']
