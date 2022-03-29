# Generated by Django 3.2.6 on 2022-03-22 03:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('rmid', models.AutoField(primary_key=True, serialize=False)),
                ('rmtype', models.CharField(max_length=8)),
                ('rmnum', models.CharField(max_length=3)),
                ('rmname', models.CharField(max_length=40)),
                ('rmdesc', models.CharField(max_length=300)),
                ('prc', models.DecimalField(decimal_places=2, max_digits=7)),
                ('cap', models.IntegerField()),
                ('rmimg', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'tblRoom',
            },
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('uid', models.AutoField(primary_key=True, serialize=False)),
                ('fname', models.CharField(max_length=25)),
                ('lname', models.CharField(max_length=25)),
                ('pword', models.CharField(max_length=30)),
                ('email', models.CharField(max_length=50, unique=True)),
                ('add', models.CharField(max_length=100)),
                ('mobile', models.CharField(max_length=13)),
            ],
            options={
                'db_table': 'tblUsers',
            },
        ),
        migrations.CreateModel(
            name='RoomPics',
            fields=[
                ('rmpixid', models.AutoField(primary_key=True, serialize=False)),
                ('rmpixurl', models.CharField(max_length=200)),
                ('rmid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='upserve.room')),
            ],
        ),
        migrations.CreateModel(
            name='Reserve',
            fields=[
                ('resid', models.AutoField(primary_key=True, serialize=False)),
                ('resdate', models.DateField(blank=True, null=True)),
                ('tmslt', models.CharField(max_length=40)),
                ('rmid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='upserve.room')),
                ('uid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='upserve.users')),
            ],
            options={
                'db_table': 'tblReserve',
            },
        ),
    ]
