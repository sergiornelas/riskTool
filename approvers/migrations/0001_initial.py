# Generated by Django 3.0.5 on 2020-04-22 05:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('patches', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='patchApproverRelationship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('approver', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='approvers', to=settings.AUTH_USER_MODEL)),
                ('patch', models.ManyToManyField(to='patches.patch')),
            ],
        ),
    ]
