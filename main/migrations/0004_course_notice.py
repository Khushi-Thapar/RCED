# Generated by Django 4.0.5 on 2022-12-26 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_remove_course_document_course_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='notice',
            field=models.TextField(default='NULL'),
        ),
    ]
