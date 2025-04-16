from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView
from .models import Issue, Comment, TipoIssue, EstadoIssue, PrioridadIssue, SeveridadIssue, Attachment
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from .forms import *
from django.contrib import messages
from django.db.models import Q
import operator
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import IssueFilterForm


class IssueListView(ListView):
    model = Issue
    template_name = 'issue_list.html'
    context_object_name = 'issues'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.form = IssueFilterForm(self.request.GET)

        if self.form.is_valid():
            data = self.form.cleaned_data
            if data.get('search'):
                query = data['search']
                queryset = queryset.filter(
                    Q(subject__icontains=query) |
                    Q(description__icontains=query) |
                    Q(severidad__nombre__icontains=query) |
                    Q(prioridad__nombre__icontains=query) |
                    Q(estado__nombre__icontains=query) |
                    Q(tipo__nombre__icontains=query)
                )
            if data.get('tipo'):
                queryset = queryset.filter(tipo=data['tipo'])
            if data.get('estado'):
                queryset = queryset.filter(estado=data['estado'])
            if data.get('prioridad'):
                queryset = queryset.filter(prioridad=data['prioridad'])
            if data.get('severidad'):
                queryset = queryset.filter(severidad=data['severidad'])

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = self.form
        return context

class CommentsListView(ListView):
    model = Comment
    template_name = 'comments_list.html'
    context_object_name = 'comments'

def issue_view(request, **kwargs):
    issue = Issue.objects.get(id=kwargs.get('issue_id'))
    return render(request, 'view_issue.html', context={'issue': issue}) 

@login_required
def new_issue_view(request):
    if request.method == 'POST':
        form = New_issue_Form(request.POST, request.FILES)
        attachment_form = AttachmentForm(request.POST, request.FILES)

        if form.is_valid():
            issue = form.save()

            if attachment_form.is_valid() and 'file' in request.FILES:
                attachment = attachment_form.save(commit=False)
                attachment.issue = issue
                attachment.save()

            return redirect('issues')
    else:
        form = New_issue_Form()
        attachment_form = AttachmentForm()

    return render(request, 'new_issue.html', {
        'form': form,
        'attachment_form': attachment_form,
    })

def edit_issue_view(request, **kwargs):
    issue = Issue.objects.get(id=kwargs.get('issue_id'))

    if request.method == 'POST':
        form = Edit_issue_Form(request.POST, request.FILES, instance=issue)
        attachment_form = AttachmentForm(request.POST, request.FILES)

        if form.is_valid():
            issue = form.save(commit=False)
            issue.save()
            if form.cleaned_data.get('user_assigned') is not None:
                issue.user_assigned.set(form.cleaned_data['user_assigned'])
            else:
                issue.user_assigned.clear()

            if form.cleaned_data.get('watchers') is not None:
                issue.watchers.set(form.cleaned_data['watchers'])
            else:
                issue.watchers.clear()

            if attachment_form.is_valid() and 'file' in request.FILES:
                attachment = attachment_form.save(commit=False)
                attachment.issue = issue
                attachment.save()

            return redirect('issue_view', issue_id=issue.id)
    else:
        form = Edit_issue_Form(instance=issue)
        attachment_form = AttachmentForm()

    return render(request, 'edit_issue.html', {
        'form': form,
        'attachment_form': attachment_form,
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


