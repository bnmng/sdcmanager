from django.db import migrations

def populate_group_permissions(apps, schema_editor):
    
    Group=apps.get_model('auth', 'Group')
    Permission=apps.get_model('auth', 'Permission')

    sdcpeople_editors = Group.objects.create(name='sdcpeople_editors')
    all_permissions=Permission.objects.filter(content_type__app_label='sdcpeople');
    sdcpeople_editors.permissions.set(list(all_permissions))

class Migration(migrations.Migration):

    dependencies = [
        ('sdcpeople', 'data04_populate_group'),
    ]

    operations = [
        migrations.RunPython(populate_group_permissions)
    ]`
