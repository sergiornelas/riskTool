# Generated by Django 3.0.6 on 2020-06-02 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advisory', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advisory',
            name='criticality',
            field=models.CharField(choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')], max_length=8),
        ),
    ]
