# Generated by Django 3.0.2 on 2020-02-14 01:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
                ('email', models.CharField(max_length=45)),
            ],
        ),
        migrations.CreateModel(
            name='server',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hostname', models.CharField(max_length=45)),
                ('os', models.CharField(max_length=45)),
                ('reboot_required', models.CharField(max_length=45)),
            ],
        ),
    ]
