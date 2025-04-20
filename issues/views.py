from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Issue, Comment, TipoIssue, EstadoIssue, PrioridadIssue, SeveridadIssue, File
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from .forms import (
    IssueForm, CommentForm, TipoIssueForm, EstadoIssueForm,
    PrioridadIssueForm, SeveridadIssueForm
)
from django.contrib import messages
from django.db.models import Q
import operator
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import IssueFilterForm
from rest_framework import viewsets, permissions
from .serializers import (
    IssueSerializer, CommentSerializer, TipoIssueSerializer,
    EstadoIssueSerializer, PrioridadIssueSerializer, SeveridadIssueSerializer,
    FileSerializer
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


class IssueListView(LoginRequiredMixin, ListView):
    model = Issue
    template_name = 'issues/issue_list.html'
    context_object_name = 'issues'
    paginate_by = 10

    def get_queryset(self):
        queryset = Issue.objects.all()
        search = self.request.GET.get('search')
        tipo = self.request.GET.get('tipo')
        estado = self.request.GET.get('estado')
        prioridad = self.request.GET.get('prioridad')
        severidad = self.request.GET.get('severidad')

        if search:
            queryset = queryset.filter(subject__icontains=search) | queryset.filter(description__icontains=search)
        if tipo:
            queryset = queryset.filter(tipo_id=tipo)
        if estado:
            queryset = queryset.filter(estado_id=estado)
        if prioridad:
            queryset = queryset.filter(prioridad_id=prioridad)
        if severidad:
            queryset = queryset.filter(severidad_id=severidad)

        return queryset.order_by('-creation_date', '-last_modified')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tipos'] = TipoIssue.objects.all()
        context['estados'] = EstadoIssue.objects.all()
        context['prioridades'] = PrioridadIssue.objects.all()
        context['severidades'] = SeveridadIssue.objects.all()
        
        active_filters = {}
        if self.request.GET.get('tipo'):
            active_filters['Type'] = TipoIssue.objects.get(id=self.request.GET.get('tipo')).nombre
        if self.request.GET.get('estado'):
            active_filters['State'] = EstadoIssue.objects.get(id=self.request.GET.get('estado')).nombre
        if self.request.GET.get('prioridad'):
            active_filters['Priority'] = PrioridadIssue.objects.get(id=self.request.GET.get('prioridad')).nombre
        if self.request.GET.get('severidad'):
            active_filters['Severity'] = SeveridadIssue.objects.get(id=self.request.GET.get('severidad')).nombre
        
        context['active_filters'] = active_filters
        return context

class IssueDetailView(LoginRequiredMixin, DetailView):
    model = Issue
    template_name = 'issues/issue_detail.html'
    context_object_name = 'issue'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context

class IssueCreateView(LoginRequiredMixin, CreateView):
    model = Issue
    form_class = IssueForm
    template_name = 'issues/issue_form.html'
    success_url = reverse_lazy('issues')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class IssueUpdateView(LoginRequiredMixin, UpdateView):
    model = Issue
    form_class = IssueForm
    template_name = 'issues/issue_form.html'
    success_url = reverse_lazy('issues')

class IssueDeleteView(LoginRequiredMixin, DeleteView):
    model = Issue
    template_name = 'issues/issue_confirm_delete.html'
    success_url = reverse_lazy('issues')

def issue_view(request, **kwargs):
    issue = Issue.objects.get(id=kwargs.get('issue_id'))
    return render(request, 'view_issue.html', context={'issue': issue}) 

@login_required
def new_issue_view(request):
    if request.method == 'POST':
        form = IssueForm(request.POST)
        if form.is_valid():
            issue = form.save(commit=False)
            issue.created_by = request.user
            issue.save()
            return redirect('issues')
    else:
        form = IssueForm()

    return render(request, 'issues/new_issue.html', {
        'form': form,
    })

@login_required
def edit_issue_view(request, issue_id):
    issue = get_object_or_404(Issue, id=issue_id)

    if request.method == 'POST':
        form = IssueForm(request.POST, instance=issue)
        if form.is_valid():
            issue = form.save()
            return redirect('issue_view', issue_id=issue.id)
    else:
        form = IssueForm(instance=issue)

    return render(request, 'issues/edit_issue.html', {
        'form': form,
        'issue': issue,
    })

class ConfiguracionView(ListView):
    template_name = 'issues/settings.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'tipos': TipoIssue.objects.all(),
            'estados': EstadoIssue.objects.all(),
            'prioridades': PrioridadIssue.objects.all(),
            'severidades': SeveridadIssue.objects.all(),
            'tipo_form': TipoIssueForm(),
            'estado_form': EstadoIssueForm(),
            'prioridad_form': PrioridadIssueForm(),
            'severidad_form': SeveridadIssueForm(),
            'delete_tipo_form': DeleteTipoForm(),
            'delete_estado_form': DeleteEstadoForm(),
            'delete_prioridad_form': DeletePrioridadForm(),
            'delete_severidad_form': DeleteSeveridadForm(),
        })
        return context

    def get_queryset(self):
        return Issue.objects.none()

@require_POST
def add_tipo(request):
    form = TipoIssueForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, "Tipo añadido correctamente")
    return redirect('configuracion')

@require_POST
def delete_tipo(request):
    form = DeleteTipoForm(request.POST)
    if form.is_valid():
        tipo_a_eliminar = form.cleaned_data['tipo_a_eliminar']
        tipo_sustituto = form.cleaned_data['tipo_sustituto']
        Issue.objects.filter(tipo=tipo_a_eliminar).update(tipo=tipo_sustituto)
        tipo_a_eliminar.delete()
        messages.success(request, "Tipo eliminado y reemplazado correctamente")
    return redirect('configuracion')

@require_POST
def add_estado(request):
    form = EstadoIssueForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, "Estado añadido correctamente")
    return redirect('configuracion')

@require_POST
def delete_estado(request):
    form = DeleteEstadoForm(request.POST)
    if form.is_valid():
        estado_a_eliminar = form.cleaned_data['estado_a_eliminar']
        estado_sustituto = form.cleaned_data['estado_sustituto']
        Issue.objects.filter(estado=estado_a_eliminar).update(estado=estado_sustituto)
        estado_a_eliminar.delete()
        messages.success(request, "Estado eliminado y reemplazado correctamente")
    return redirect('configuracion')

@require_POST
def add_prioridad(request):
    form = PrioridadIssueForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, "Prioridad añadida correctamente")
    return redirect('configuracion')

@require_POST
def delete_prioridad(request):
    form = DeletePrioridadForm(request.POST)
    if form.is_valid():
        prioridad_a_eliminar = form.cleaned_data['prioridad_a_eliminar']
        prioridad_sustituto = form.cleaned_data['prioridad_sustituto']
        Issue.objects.filter(prioridad=prioridad_a_eliminar).update(prioridad=prioridad_sustituto)
        prioridad_a_eliminar.delete()
        messages.success(request, "Prioridad eliminada y reemplazada correctamente")
    return redirect('configuracion')

@require_POST
def add_severidad(request):
    form = SeveridadIssueForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, "Severidad añadida correctamente")
    return redirect('configuracion')

@require_POST
def delete_severidad(request):
    form = DeleteSeveridadForm(request.POST)
    if form.is_valid():
        severidad_a_eliminar = form.cleaned_data['severidad_a_eliminar']
        severidad_sustituto = form.cleaned_data['severidad_sustituto']
        Issue.objects.filter(severidad=severidad_a_eliminar).update(severidad=severidad_sustituto)
        severidad_a_eliminar.delete()
        messages.success(request, "Severidad eliminada y reemplazada correctamente")
    return redirect('configuracion')

def delete_issue(request, **kwargs):
    issue = Issue.objects.get(id=kwargs.get('issue_id'))
    issue.delete()
    return redirect('/issues')

@login_required
def new_comment_view(request, **kwargs):
    issue = get_object_or_404(Issue, id=kwargs.get('issue_id'))
    
    if request.method == 'POST':
        form = New_comment_Form(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.issue_id = issue
            comment.author = request.user.username
            comment.save()
            return redirect('issue_view', issue_id=issue.id)
    else:
        form = New_comment_Form()
    
    return render(request, 'new_comment.html', {
        'form': form,
        'issue': issue,
    })

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/issues')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def delete_comment(request, **kwargs):
    comment = get_object_or_404(Comment, id=kwargs.get('comment_id'))
    comment.delete()
    return redirect('comments')

@login_required
@require_POST
def upload_file(request, issue_id=None):
    if 'file' not in request.FILES:
        return JsonResponse({'error': 'No file provided'}, status=400)

    uploaded_file = request.FILES['file']
    issue = None
    if issue_id:
        try:
            issue = Issue.objects.get(id=issue_id)
        except Issue.DoesNotExist:
            return JsonResponse({'error': 'Issue not found'}, status=404)

    file_instance = File.objects.create(
        name=uploaded_file.name,
        file=uploaded_file,
        user=request.user,
        issue=issue
    )

    return JsonResponse({
        'id': file_instance.id,
        'name': file_instance.name,
        'url': file_instance.get_file_url(),
        'size': file_instance.get_file_size()
    })

class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['tipo', 'estado', 'prioridad', 'severidad']
    search_fields = ['subject', 'description']

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class TipoIssueViewSet(viewsets.ModelViewSet):
    queryset = TipoIssue.objects.all()
    serializer_class = TipoIssueSerializer

class EstadoIssueViewSet(viewsets.ModelViewSet):
    queryset = EstadoIssue.objects.all()
    serializer_class = EstadoIssueSerializer

class PrioridadIssueViewSet(viewsets.ModelViewSet):
    queryset = PrioridadIssue.objects.all()
    serializer_class = PrioridadIssueSerializer

class SeveridadIssueViewSet(viewsets.ModelViewSet):
    queryset = SeveridadIssue.objects.all()
    serializer_class = SeveridadIssueSerializer

class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer

class CommentsListView(LoginRequiredMixin, ListView):
    model = Comment
    template_name = 'comments_list.html'
    context_object_name = 'comments'
    ordering = ['-created_at']

    def get_queryset(self):
        return Comment.objects.all().order_by('-created_at')


