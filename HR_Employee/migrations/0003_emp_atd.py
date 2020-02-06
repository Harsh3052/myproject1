# Generated by Django 2.2.5 on 2020-02-06 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
        ('HR_Employee', '0002_auto_20200122_1614'),
    ]

    operations = [
        migrations.CreateModel(
            name='emp_atd',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('td_date', models.CharField(max_length=50)),
                ('pi_time', models.CharField(max_length=50)),
                ('po_time', models.CharField(max_length=50)),
                ('total_time', models.CharField(max_length=50)),
                ('over_time', models.CharField(max_length=50)),
                ('emp_id', models.ForeignKey(on_delete='', to='myapp.HR_emp')),
            ],
        ),
    ]
