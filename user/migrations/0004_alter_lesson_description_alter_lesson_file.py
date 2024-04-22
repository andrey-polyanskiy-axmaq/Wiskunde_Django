# Generated by Django 5.0.4 on 2024-04-16 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_schedule'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='Description',
            field=models.TextField(blank=True, null=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='', verbose_name='Прикрепленный файл'),
        ),
    ]
