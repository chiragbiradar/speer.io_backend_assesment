# Generated by Django 5.0.1 on 2024-01-06 06:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('NotesApp', '0004_note_search_vector'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='note',
            name='search_vector',
        ),
    ]
