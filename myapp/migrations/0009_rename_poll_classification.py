# Generated by Django 4.2.4 on 2023-08-12 15:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_alter_file_mime_type'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Poll',
            new_name='Classification',
        ),
    ]