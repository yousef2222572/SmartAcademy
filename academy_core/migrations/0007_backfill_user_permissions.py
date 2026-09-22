from django.db import migrations


def create_missing_permissions(apps, schema_editor):
    """Backfill a UserPermissions row for every user that is missing one."""
    User = apps.get_model('auth', 'User')
    UserPermissions = apps.get_model('academy_core', 'UserPermissions')

    existing_user_ids = set(
        UserPermissions.objects.values_list('user_id', flat=True)
    )

    UserPermissions.objects.bulk_create([
        UserPermissions(user_id=user.id)
        for user in User.objects.exclude(id__in=existing_user_ids)
    ])


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('academy_core', '0006_answer_file_question_file'),
    ]

    operations = [
        migrations.RunPython(create_missing_permissions, noop),
    ]
