from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'issues', views.IssueViewSet)
router.register(r'comments', views.CommentViewSet)
router.register(r'attachments', views.AttachmentViewSet)
router.register(r'tipos', views.TipoIssueViewSet)
router.register(r'estados', views.EstadoIssueViewSet)
router.register(r'prioridades', views.PrioridadIssueViewSet)
router.register(r'severidades', views.SeveridadIssueViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
] 