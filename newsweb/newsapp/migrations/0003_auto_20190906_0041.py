# Generated by Django 2.2.5 on 2019-09-05 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsapp', '0002_auto_20190905_2306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
