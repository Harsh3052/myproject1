# Generated by Django 2.2.5 on 2019-11-25 11:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_auto_20191125_1609'),
    ]

    operations = [
        migrations.DeleteModel(
            name='HR',
        ),
        migrations.DeleteModel(
            name='HR_emp',
        ),
    ]
