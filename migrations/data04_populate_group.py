from django.db import migrations

def populate_group(apps, schema_editor):
    
    GroupType=apps.get_model('sdcpeople', 'GroupType')
    executive=GroupType.objects.get(name='Executive Committee')
    standing=GroupType.objects.get(name='Standing Committee')

    Group=apps.get_model('sdcpeople', 'Group')

    Group.objects.bulk_create([
        Group(name='Executive Committee', grouptype=executive, protect=True),
        #From the 2016 Local Chairs Handbook
        Group(name='Finance Committee', grouptype=standing, protect=True),
        Group(name='Auditing Committee', grouptype=standing, protect=True),
        Group(name='Precinct Committee', grouptype=standing, protect=True),
        Group(name='Fundraising Committee', grouptype=standing, protect=True),
        Group(name='Legislative Committee', grouptype=standing, protect=True),
        Group(name='Bylaws Committee', grouptype=standing, protect=True),
    ])


class Migration(migrations.Migration):

    dependencies = [
        ('sdcpeople', 'data03_populate_grouptype'),
    ]

    operations = [
        migrations.RunPython(populate_group)
    ]
