# Generated by Django 3.0.5 on 2020-04-26 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exception', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exclude_patch',
            name='patch_from',
        ),
        migrations.AddField(
            model_name='exclude_patch',
            name='patch_id',
            field=models.IntegerField(null=True),
        ),
    ]