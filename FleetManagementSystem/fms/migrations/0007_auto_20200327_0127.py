# Generated by Django 3.0.4 on 2020-03-26 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fms', '0006_auto_20200326_1605'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='items',
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
