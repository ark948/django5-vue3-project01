# Generated by Django 5.1.1 on 2024-09-11 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookmarker', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookmark',
            name='icon',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='Icon'),
        ),
    ]
