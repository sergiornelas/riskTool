# Generated by Django 3.0.6 on 2020-07-05 22:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exception', '0019_auto_20200705_2010'),
    ]

    operations = [
        migrations.RenameField(
            model_name='exception',
            old_name='server',
            new_name='server_id',
        ),
    ]