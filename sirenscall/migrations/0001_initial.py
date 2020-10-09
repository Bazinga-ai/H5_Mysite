# Generated by Django 3.1 on 2020-08-22 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Recorder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=63)),
                ('main_text', models.TextField()),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
                ('is_bold', models.BooleanField()),
            ],
        ),
    ]