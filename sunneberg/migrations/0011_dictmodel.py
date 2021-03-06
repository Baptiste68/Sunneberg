# Generated by Django 3.0.2 on 2020-03-10 10:47

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sunneberg', '0010_auto_20200221_1159'),
    ]

    operations = [
        migrations.CreateModel(
            name='DictModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dict_name', models.CharField(max_length=200)),
                ('dict_content', django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=200), size=None), size=None)),
            ],
        ),
    ]
