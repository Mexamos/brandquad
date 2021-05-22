# Generated by Django 3.2.3 on 2021-05-22 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DataLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=16)),
                ('date', models.DateTimeField(db_index=True)),
                ('method', models.CharField(max_length=50)),
                ('uri', models.CharField(db_index=True, max_length=200)),
                ('response_status', models.IntegerField(db_index=True)),
                ('response_size', models.IntegerField()),
            ],
        ),
    ]
