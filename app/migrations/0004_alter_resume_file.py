# Generated by Django 4.2.8 on 2024-01-22 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_resume_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resume',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]