# Generated by Django 4.0.2 on 2022-02-15 16:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('income', '0003_source_source'),
    ]

    operations = [
        migrations.RenameField(
            model_name='income',
            old_name='source',
            new_name='category',
        ),
        migrations.RenameField(
            model_name='source',
            old_name='source',
            new_name='category',
        ),
    ]
