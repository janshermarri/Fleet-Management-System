# Generated by Django 3.0.4 on 2020-03-26 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fms', '0004_auto_20200326_1547'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='license_plate',
            field=models.CharField(default=123, max_length=50),
            preserve_default=False,
        ),
    ]