# Generated by Django 3.0.2 on 2020-02-21 10:59

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sunneberg', '0009_pdfmodel_pdf_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='UnsubModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unsub_email', models.CharField(max_length=200)),
                ('unsub_code', models.IntegerField()),
                ('unsub_duration', models.DurationField()),
            ],
        ),
        migrations.AlterField(
            model_name='listmodel',
            name='list_content',
            field=django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=200), size=None), size=None),
        ),
    ]