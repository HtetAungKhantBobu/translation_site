# Generated by Django 4.2.2 on 2023-06-25 17:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Translation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Title or Name of the translation.')),
                ('author', models.CharField(blank=True, max_length=255, verbose_name='Author(s) of the source material')),
                ('source_language', models.CharField(choices=[('EN', 'English'), ('JP', 'Japanese'), ('CN', 'Chinese'), ('KR', 'Korean')], default='JP', max_length=2, verbose_name='Language of the main source.')),
                ('type', models.CharField(choices=[('WN', 'Web Novel'), ('LN', 'Light Novel')], default='WN', max_length=2, verbose_name='Type of the source material.')),
                ('status', models.CharField(choices=[('ON', 'On Going'), ('HI', 'Hiatus'), ('ED', 'Ended'), ('UK', 'Unknown')], default='UK', max_length=2, verbose_name='Current Status of the translation.')),
            ],
            options={
                'indexes': [models.Index(fields=['title'], name='translation_title_idx')],
            },
        ),
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Chapter Title')),
                ('serial', models.IntegerField(default=0, verbose_name='Chapter No.')),
                ('status', models.CharField(choices=[('PB', 'Published'), ('IP', 'In Progress'), ('UK', 'Unknown')], default='UK', max_length=2, verbose_name='Current translation status of the chapter')),
                ('published_date', models.DateTimeField(verbose_name='Published Date and Time')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('parent_translation', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='translation_manager.translation')),
            ],
            options={
                'indexes': [models.Index(fields=['serial'], name='chapter_no_idx'), models.Index(fields=['parent_translation'], name='chapter_parent_translation_idx')],
            },
        ),
    ]
