# Generated by Django 4.2.2 on 2023-06-25 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('translation_manager', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chapter',
            name='contents',
            field=models.TextField(blank=True, verbose_name='Translated Content'),
        ),
    ]