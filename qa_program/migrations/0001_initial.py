# Generated by Django 2.2 on 2020-09-18 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kind', models.CharField(default='0', max_length=1)),
                ('question', models.CharField(default='none', max_length=1023)),
                ('A', models.CharField(default='none', max_length=511)),
                ('B', models.CharField(default='none', max_length=511)),
                ('C', models.CharField(default='none', max_length=511)),
                ('D', models.CharField(default='none', max_length=511)),
                ('answer', models.CharField(default='0', max_length=2)),
                ('difficulty', models.IntegerField(default=-1, max_length=1)),
            ],
        ),
    ]
