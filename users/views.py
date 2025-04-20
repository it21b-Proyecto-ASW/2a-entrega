from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.models import User
from issues.models import Issue, Comment
from .forms import ProfileAvatarForm, ProfileBioForm
from .models import UserProfile
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from issues.forms import New_issue_Form
from allauth.account.views import LoginView
from django.core.files.storage import FileSystemStorage

@login_required
def user_list(request):
    users = User.objects.all()
    return render(request, 'users/user_list.html', {'users': users})

@login_required
def user_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile = user.userprofile

    # Get editing status from query parameters
    editing_bio = request.GET.get('edit') == 'bio'
    editing_avatar = request.GET.get('edit') == 'avatar'

    if request.method == 'POST':
        if editing_avatar:
            form = ProfileAvatarForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                form.save()
                return redirect('user_profile', user_id=user_id)
        elif editing_bio:
            form = ProfileBioForm(request.POST, instance=profile)
            if form.is_valid():
                form.save()
                return redirect('user_profile', user_id=user_id)

    # Get user's issues and comments
    open_issues = Issue.objects.filter(user_assigned=user).exclude(estado__es_cerrado=True)
    watched_issues = Issue.objects.filter(watchers=user)
    comments = Comment.objects.filter(author=user.username)

    # Sort issues if requested
    sort_field = request.GET.get('sort')
    if sort_field in ['tipo', 'severidad', 'id', 'estado', 'deadline', 'last_modified']:
        open_issues = open_issues.order_by(sort_field)

    # Initialize forms based on editing mode
    if editing_avatar:
        form = ProfileAvatarForm(instance=profile)
    elif editing_bio:
        form = ProfileBioForm(instance=profile)
    else:
        form = None

    context = {
        'profile_user': user,
        'profile': profile,
        'open_issues': open_issues,
        'watched_issues': watched_issues,
        'comments': comments,
        'editing_bio': editing_bio,
        'editing_avatar': editing_avatar,
        'form': form,
    }
    return render(request, 'users/user_profile.html', context)

class CustomLoginView(LoginView):
    template_name = "account/login.html"

@login_required
def edit_profile_view(request):
    profile = request.user.userprofile

    if request.method == 'POST':
        form = ProfileAvatarForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('user_profile', user_id=request.user.id)
    else:
        form = ProfileAvatarForm(instance=profile)

    return render(request, 'users/edit_profile.html', {'form': form})