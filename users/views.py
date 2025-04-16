from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.models import User
from issues.models import Issue, Comment
from .forms import ProfileAvatarForm
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from issues.forms import New_issue_Form
from allauth.account.views import LoginView

def user_list(request):
    users = User.objects.filter(is_superuser=False)
    return render(request, 'users/user_list.html', {'users': users})


def user_profile(request, user_id):
    user_obj = get_object_or_404(User, pk=user_id)
    profile = user_obj.profile
    editing_bio = False
    editing_avatar = False

    edit_param = request.GET.get('edit')
    if edit_param == 'bio':
        editing_bio = True
    elif edit_param == 'avatar':
        editing_avatar = True

    if request.method == 'POST':

        if editing_bio:
            profile.bio = request.POST.get('bio', '')
            profile.save()
            return redirect('user_profile', user_id=user_id)

        if editing_avatar:
            form = ProfileAvatarForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                form.save()
            return redirect('user_profile', user_id=user_id)

    if request.method == 'POST' and request.user.id == user_obj.id:
        new_bio = request.POST.get("bio", "").strip()
        if hasattr(user_obj, "profile"):
            user_obj.profile.bio = new_bio
            user_obj.profile.save()
        return redirect("user_profile", user_id=user_id)

    open_issues = Issue.objects.filter(user_assigned=user_obj).exclude(estado__es_cerrado=True)

    sort_field = request.GET.get("sort")
    valid_fields = ["tipo", "severidad", "id", "estado", "deadline", "last_modified"]
    if sort_field in valid_fields:
        open_issues = open_issues.order_by(sort_field)


    watched_issues = Issue.objects.filter(watchers=user_obj)

    user_comments = Comment.objects.filter(
        author=user_obj.username
    )

    editing_bio = request.GET.get("edit") == "bio"

    context = {
        'user': user_obj,
        'open_issues': open_issues,
        'watched_issues': watched_issues,
        'comments': user_comments,
        'editing_bio': editing_bio,
        'editing_avatar': editing_avatar,
    }

    return render(request, 'users/user_profile.html', context)



class CustomLoginView(LoginView):
    template_name = "account/login.html"

@login_required
def edit_profile_view(request):

    profile = request.user.profile

    if request.method == 'POST':
        form = ProfileAvatarForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('user_profile', user_id=request.user.id)
    else:
        form = ProfileAvatarForm(instance=profile)

    return render(request, 'users/edit_profile.html', {'form': form})