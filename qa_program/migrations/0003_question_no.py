# Generated by Django 2.2 on 2020-09-18 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qa_program', '0002_auto_20200918_1620'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='no',
            field=models.IntegerField(default=0),
        ),
    ]
