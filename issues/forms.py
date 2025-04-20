from django import forms
from .models import Issue, Comment, User, File
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import Issue, Comment, TipoIssue, EstadoIssue, PrioridadIssue, SeveridadIssue
from django.utils.timezone import now

class New_issue_Form(forms.ModelForm):
    subject = forms.CharField(label="Subject")
    description = forms.CharField(label="Description", required=False)
    deadline = forms.DateField(
        label="Deadline",
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )
    creation_date = forms.DateField(
        label="Creation Date",
        widget=forms.DateInput(attrs={'type': 'date'}),
        initial=now 
    )

    estado = forms.ModelChoiceField(
        queryset=EstadoIssue.objects.all(),
        label="Estado",
        required=False,
        empty_label='None'
    )

    tipo = forms.ModelChoiceField(
        queryset=TipoIssue.objects.all(),
        label="Tipo",
        required=False,
        empty_label='None'
    )

    prioridad = forms.ModelChoiceField(
        queryset=PrioridadIssue.objects.all(),
        label="Prioridad",
        required=False,
        empty_label='None'
    )

    severidad = forms.ModelChoiceField(
        queryset=SeveridadIssue.objects.all(),
        label="Severidad",
        required=False,
        empty_label='None'
    )

    user_assigned = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=False,
        label="Assigned Users",
        widget=forms.CheckboxSelectMultiple
    )

    watchers = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=False,
        label="Watchers",
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Issue
        fields = ['subject', 'description', 'tipo', 'estado', 'prioridad', 'severidad', 'deadline', 'user_assigned', 'watchers']

class Edit_issue_Form(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ['subject', 'description', 'tipo', 'estado', 'prioridad', 'severidad', 'deadline', 'user_assigned', 'watchers']

class New_comment_Form(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

    text = forms.CharField(label="Comentario", widget=forms.Textarea(attrs={'rows': 3}))

class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['file']

class IssueFilterForm(forms.Form):
    search = forms.CharField(required=False)
    tipo = forms.ModelChoiceField(queryset=Issue.objects.none(), required=False)
    estado = forms.ModelChoiceField(queryset=Issue.objects.none(), required=False)
    prioridad = forms.ModelChoiceField(queryset=Issue.objects.none(), required=False)
    severidad = forms.ModelChoiceField(queryset=Issue.objects.none(), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tipo'].queryset = Issue.objects.values_list('tipo', flat=True).distinct()
        self.fields['estado'].queryset = Issue.objects.values_list('estado', flat=True).distinct()
        self.fields['prioridad'].queryset = Issue.objects.values_list('prioridad', flat=True).distinct()
        self.fields['severidad'].queryset = Issue.objects.values_list('severidad', flat=True).distinct()

class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ['subject', 'description', 'tipo', 'estado', 'prioridad', 'severidad']
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'prioridad': forms.Select(attrs={'class': 'form-control'}),
            'severidad': forms.Select(attrs={'class': 'form-control'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class TipoIssueForm(forms.ModelForm):
    class Meta:
        model = TipoIssue
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
        }

class EstadoIssueForm(forms.ModelForm):
    class Meta:
        model = EstadoIssue
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
        }

class PrioridadIssueForm(forms.ModelForm):
    class Meta:
        model = PrioridadIssue
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
        }

class SeveridadIssueForm(forms.ModelForm):
    class Meta:
        model = SeveridadIssue
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
        }

class DeleteTipoForm(forms.Form):
    tipo_a_eliminar = forms.ModelChoiceField(queryset=Issue.objects.values_list('tipo', flat=True).distinct())
    tipo_sustituto = forms.ModelChoiceField(queryset=Issue.objects.values_list('tipo', flat=True).distinct())

    def clean(self):
        cleaned_data = super().clean()
        tipo_a_eliminar = cleaned_data.get('tipo_a_eliminar')
        tipo_sustituto = cleaned_data.get('tipo_sustituto')

        if tipo_a_eliminar and tipo_sustituto and tipo_a_eliminar == tipo_sustituto:
            raise ValidationError("No puede reemplazar un tipo con él mismo")
        return cleaned_data

class DeleteEstadoForm(forms.Form):
    estado_a_eliminar = forms.ModelChoiceField(queryset=Issue.objects.values_list('estado', flat=True).distinct())
    estado_sustituto = forms.ModelChoiceField(queryset=Issue.objects.values_list('estado', flat=True).distinct())

    def clean(self):
        cleaned_data = super().clean()
        estado_a_eliminar = cleaned_data.get('estado_a_eliminar')
        estado_sustituto = cleaned_data.get('estado_sustituto')

        if estado_a_eliminar and estado_sustituto and estado_a_eliminar == estado_sustituto:
            raise ValidationError("No puede reemplazar un estado con él mismo")
        return cleaned_data

class DeletePrioridadForm(forms.Form):
    prioridad_a_eliminar = forms.ModelChoiceField(queryset=Issue.objects.values_list('prioridad', flat=True).distinct())
    prioridad_sustituto = forms.ModelChoiceField(queryset=Issue.objects.values_list('prioridad', flat=True).distinct())

    def clean(self):
        cleaned_data = super().clean()
        prioridad_a_eliminar = cleaned_data.get('prioridad_a_eliminar')
        prioridad_sustituto = cleaned_data.get('prioridad_sustituto')

        if prioridad_a_eliminar and prioridad_sustituto and prioridad_a_eliminar == prioridad_sustituto:
            raise ValidationError("No puede reemplazar una prioridad con ella misma")
        return cleaned_data

class DeleteSeveridadForm(forms.Form):
    severidad_a_eliminar = forms.ModelChoiceField(queryset=Issue.objects.values_list('severidad', flat=True).distinct())
    severidad_sustituto = forms.ModelChoiceField(queryset=Issue.objects.values_list('severidad', flat=True).distinct())

    def clean(self):
        cleaned_data = super().clean()
        severidad_a_eliminar = cleaned_data.get('severidad_a_eliminar')
        severidad_sustituto = cleaned_data.get('severidad_sustituto')

        if severidad_a_eliminar and severidad_sustituto and severidad_a_eliminar == severidad_sustituto:
            raise ValidationError("No puede reemplazar una severidad con ella misma")
        return cleaned_data