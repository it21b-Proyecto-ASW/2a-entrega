from django.db import migrations

def create_user_profiles(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    UserProfile = apps.get_model('users', 'UserProfile')
    
    for user in User.objects.all():
        UserProfile.objects.get_or_create(user=user)

class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_userprofile_delete_profile'),
    ]

    operations = [
        migrations.RunPython(create_user_profiles),
    ] 