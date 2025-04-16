"""
URL configuration for prueba project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from issues.views import *
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from users.views import CustomLoginView

def root_redirect_view(request):
    if request.user.is_authenticated:
        return redirect('issues')
    else:
        return redirect('account_login')

def custom_404_view(request, exception):
    if request.user.is_authenticated:
        return redirect('issues')
    else:
        return redirect('account_login')

urlpatterns = [
    path('', root_redirect_view, name='home'),
    path('admin/', admin.site.urls),
    path('logout/', LogoutView.as_view(next_page='account_login'), name='logout'),
    path('accounts/login/', CustomLoginView.as_view(), name='account_login'),
    path('accounts/', include('allauth.urls')),

    path('issues/', IssueListView.as_view(), name='issues'),
    path('issues/<int:issue_id>/', issue_view, name='issue_view'),
    path('issues/new/', new_issue_view, name='new_issue'),
    path('issues/<int:issue_id>/edit/', edit_issue_view, name='edit_issue'),
    path('issues/<int:issue_id>/delete/', delete_issue, name='delete_issue'),
    path('issues/<int:issue_id>/comments/new/', new_comment_view, name='new_comment'),

    path('comments/', CommentsListView.as_view(), name='comments'),
    path('comments/<int:comment_id>/delete/', delete_comment, name='delete_comment'),

    path('settings/', ConfiguracionView.as_view(), name='configuracion'),
    path('settings/tipo/add/', add_tipo, name='add_tipo'),
    path('settings/tipo/delete/', delete_tipo, name='delete_tipo'),
    path('settings/estado/add/', add_estado, name='add_estado'),
    path('settings/estado/delete/', delete_estado, name='delete_estado'),
    path('settings/prioridad/add/', add_prioridad, name='add_prioridad'),
    path('settings/prioridad/delete/', delete_prioridad, name='delete_prioridad'),
    path('settings/severidad/add/', add_severidad, name='add_severidad'),
    path('settings/severidad/delete/', delete_severidad, name='delete_severidad'),

    path('users/', include('users.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'prueba.urls.custom_404_view'