# Generated by Django 3.0.6 on 2020-06-04 01:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('patches', '0006_patches_server'),
    ]

    operations = [
        migrations.DeleteModel(
            name='SERVER_PATCH_RELATION',
        ),
    ]