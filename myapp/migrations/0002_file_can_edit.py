# Generated by Django 4.2.4 on 2023-08-09 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='can_edit',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
