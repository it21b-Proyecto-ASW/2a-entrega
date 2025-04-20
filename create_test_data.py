import os
import django
from datetime import datetime, timedelta

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'prueba.settings')
django.setup()

from django.contrib.auth.models import User
from issues.models import Issue, EstadoIssue, TipoIssue, SeveridadIssue, Comment
from users.models import UserProfile

def create_test_data():
    # Crear usuaris si no existeixen
    users = []
    for i in range(1, 4):
        username = f'user{i}'
        try:
            user = User.objects.get(username=username)
            users.append(user)
        except User.DoesNotExist:
            # Crear l'usuari
            user = User.objects.create_user(
                username=username,
                email=f'{username}@example.com',
                password='password123'
            )
            
            # Comprovar si ja té un perfil
            try:
                UserProfile.objects.get(user=user)
            except UserProfile.DoesNotExist:
                # Si no té perfil, crear-lo
                UserProfile.objects.create(user=user)
            
            users.append(user)

    # Crear estats si no existeixen
    estados = ['Open', 'In Progress', 'Resolved', 'Closed']
    for estado in estados:
        if not EstadoIssue.objects.filter(nombre=estado).exists():
            EstadoIssue.objects.create(nombre=estado, es_cerrado=(estado == 'Closed'))

    # Crear tipus si no existeixen
    tipos = ['Bug', 'Feature', 'Task', 'Improvement']
    for tipo in tipos:
        if not TipoIssue.objects.filter(nombre=tipo).exists():
            TipoIssue.objects.create(nombre=tipo)

    # Crear severitats si no existeixen
    severidades = ['Low', 'Medium', 'High', 'Critical']
    for severidad in severidades:
        if not SeveridadIssue.objects.filter(nombre=severidad).exists():
            SeveridadIssue.objects.create(nombre=severidad, impacto=severidades.index(severidad) + 1)

    # Crear issues de prova
    issues_data = [
        {
            'subject': 'Error en el login',
            'description': 'El botó de login no funciona correctamente',
            'tipo': 'Bug',
            'severidad': 'High',
            'estado': 'Open',
            'user_assigned': users[0],
            'watchers': [users[1], users[2]],
            'deadline': datetime.now() + timedelta(days=7)
        },
        {
            'subject': 'Implementar autenticació amb Google',
            'description': 'Añadir la opción de login con Google',
            'tipo': 'Feature',
            'severidad': 'Medium',
            'estado': 'In Progress',
            'user_assigned': users[1],
            'watchers': [users[0]],
            'deadline': datetime.now() + timedelta(days=14)
        },
        {
            'subject': 'Millorar rendiment de la base de dades',
            'description': 'Optimitzar les consultes SQL',
            'tipo': 'Improvement',
            'severidad': 'High',
            'estado': 'Open',
            'user_assigned': users[2],
            'watchers': [users[0], users[1]],
            'deadline': datetime.now() + timedelta(days=10)
        },
        {
            'subject': 'Actualitzar documentació',
            'description': 'Actualitzar la documentació de l\'API',
            'tipo': 'Task',
            'severidad': 'Low',
            'estado': 'Resolved',
            'user_assigned': users[0],
            'watchers': [users[1]],
            'deadline': datetime.now() + timedelta(days=5)
        }
    ]

    for issue_data in issues_data:
        issue = Issue.objects.create(
            subject=issue_data['subject'],
            description=issue_data['description'],
            tipo=TipoIssue.objects.get(nombre=issue_data['tipo']),
            severidad=SeveridadIssue.objects.get(nombre=issue_data['severidad']),
            estado=EstadoIssue.objects.get(nombre=issue_data['estado']),
            deadline=issue_data['deadline']
        )
        issue.user_assigned.set([issue_data['user_assigned']])
        issue.watchers.set(issue_data['watchers'])

        # Afegir alguns comentaris
        Comment.objects.create(
            issue_id=issue,
            author=issue_data['user_assigned'].username,
            text=f'He començat a treballar en {issue.subject}'
        )
        Comment.objects.create(
            issue_id=issue,
            author=users[1].username,
            text=f'Necessitem més informació sobre {issue.subject}'
        )

    print("Dades de prova creades correctament!")

if __name__ == '__main__':
    create_test_data() 