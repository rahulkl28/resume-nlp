# Generated by Django 4.2.8 on 2024-01-19 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_resume_content_alter_resume_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resume',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='resumes/'),
        ),
    ]