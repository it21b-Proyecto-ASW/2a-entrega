from django import forms
from .models import Issue, Comment, User, Attachment
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
        exclude = ('comment',)

class TipoIssueForm(forms.ModelForm):
    class Meta:
        model = TipoIssue
        fields = ['nombre']


class EstadoIssueForm(forms.ModelForm):
    class Meta:
        model = EstadoIssue
        fields = ['nombre', 'es_cerrado']


class PrioridadIssueForm(forms.ModelForm):
    class Meta:
        model = PrioridadIssue
        fields = ['nombre', 'nivel']


class SeveridadIssueForm(forms.ModelForm):
    class Meta:
        model = SeveridadIssue
        fields = ['nombre', 'impacto']


class DeleteTipoForm(forms.Form):
    tipo_a_eliminar = forms.ModelChoiceField(
        queryset=TipoIssue.objects.all(),
        label="Tipo a eliminar"
    )
    tipo_sustituto = forms.ModelChoiceField(
        queryset=TipoIssue.objects.all(),
        label="Reemplazar con"
    )

    def clean(self):
        cleaned_data = super().clean()
        tipo_a_eliminar = cleaned_data.get('tipo_a_eliminar')
        tipo_sustituto = cleaned_data.get('tipo_sustituto')

        if tipo_a_eliminar and tipo_sustituto and tipo_a_eliminar == tipo_sustituto:
            raise ValidationError("No puede reemplazar un tipo con él mismo")
        return cleaned_data

class DeleteEstadoForm(forms.Form):
    estado_a_eliminar = forms.ModelChoiceField(
        queryset=EstadoIssue.objects.all(),
        label="Estado a eliminar"
    )
    estado_sustituto = forms.ModelChoiceField(
        queryset=EstadoIssue.objects.all(),
        label="Reemplazar con"
    )

    def clean(self):
        cleaned_data = super().clean()
        estado_a_eliminar = cleaned_data.get('estado_a_eliminar')
        estado_sustituto = cleaned_data.get('estado_sustituto')

        if estado_a_eliminar and estado_sustituto and estado_a_eliminar == estado_sustituto:
            raise ValidationError("No puede reemplazar un estado con él mismo")
        return cleaned_data

class DeletePrioridadForm(forms.Form):
    prioridad_a_eliminar = forms.ModelChoiceField(
        queryset=PrioridadIssue.objects.all(),
        label="Prioridad a eliminar"
    )
    prioridad_sustituto = forms.ModelChoiceField(
        queryset=PrioridadIssue.objects.all(),
        label="Reemplazar con"
    )

    def clean(self):
        cleaned_data = super().clean()
        prioridad_a_eliminar = cleaned_data.get('prioridad_a_eliminar')
        prioridad_sustituto = cleaned_data.get('prioridad_sustituto')

        if prioridad_a_eliminar and prioridad_sustituto and prioridad_a_eliminar == prioridad_sustituto:
            raise ValidationError("No puede reemplazar una prioridad con ella misma")
        return cleaned_data

class DeleteSeveridadForm(forms.Form):
    severidad_a_eliminar = forms.ModelChoiceField(
        queryset=SeveridadIssue.objects.all(),
        label="Severidad a eliminar"
    )
    severidad_sustituto = forms.ModelChoiceField(
        queryset=SeveridadIssue.objects.all(),
        label="Reemplazar con"
    )

    def clean(self):
        cleaned_data = super().clean()
        severidad_a_eliminar = cleaned_data.get('severidad_a_eliminar')
        severidad_sustituto = cleaned_data.get('severidad_sustituto')

        if severidad_a_eliminar and severidad_sustituto and severidad_a_eliminar == severidad_sustituto:
            raise ValidationError("No puede reemplazar una severidad con ella misma")
        return cleaned_data

class Edit_issue_Form(forms.ModelForm):
    class Meta:
        model = Issue
        exclude = ('comment', 'creation_date')
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

    subject = forms.CharField(label="Subject")
    description = forms.CharField(label="Description", required=False)
    deadline = forms.DateField(
        label="Deadline",
        widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
        required=False,
    )

    estado = forms.ModelChoiceField(
        queryset=EstadoIssue.objects.all(),
        label="Estado",
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False,
        empty_label='None'
    )

    tipo = forms.ModelChoiceField(
        queryset=TipoIssue.objects.all(),
        label="Tipo",
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False,
        empty_label='None'
    )

    prioridad = forms.ModelChoiceField(
        queryset=PrioridadIssue.objects.all(),
        label="Prioridad",
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False,
        empty_label='None'
    )

    severidad = forms.ModelChoiceField(
        queryset=SeveridadIssue.objects.all(),
        label="Severidad",
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False,
        empty_label='None'
    )

    user_assigned = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        label="Usuarios asignados",
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    watchers = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        label="Watchers",
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['estado'].label_from_instance = lambda obj: obj.nombre
        self.fields['tipo'].label_from_instance = lambda obj: obj.nombre
        self.fields['prioridad'].label_from_instance = lambda obj: obj.nombre
        self.fields['severidad'].label_from_instance = lambda obj: obj.nombre
        self.fields['user_assigned'].label_from_instance = lambda obj: obj.get_full_name() or obj.username
        self.fields['watchers'].label_from_instance = lambda obj: obj.get_full_name() or obj.username



class New_comment_Form(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

    text = forms.CharField(label="Comentario", widget=forms.Textarea(attrs={'rows': 3}))


class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = ['file']

class IssueFilterForm(forms.Form):
    search = forms.CharField(
        required=False,
        label='Search',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Search...'})
    )
    tipo = forms.ModelChoiceField(
        queryset=TipoIssue.objects.all(),
        required=False,
        label='Tipo',
        empty_label='Tipo',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    estado = forms.ModelChoiceField(
        queryset=EstadoIssue.objects.all(),
        required=False,
        label='Estado',
        empty_label='Estado',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    prioridad = forms.ModelChoiceField(
        queryset=PrioridadIssue.objects.all(),
        required=False,
        label='Prioridad',
        empty_label='Prioridad',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    severidad = forms.ModelChoiceField(
        queryset=SeveridadIssue.objects.all(),
        required=False,
        label='Severidad',
        empty_label='Severidad',
        widget=forms.Select(attrs={'class': 'form-select'})
    )