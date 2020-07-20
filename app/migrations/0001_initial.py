# Generated by Django 2.2.14 on 2020-07-20 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Url',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shortened_url', models.CharField(max_length=50)),
                ('long_url', models.CharField(max_length=2000)),
                ('ip', models.CharField(max_length=45)),
                ('time', models.DateTimeField()),
                ('expiration_time', models.IntegerField(default=360)),
                ('hit_counter', models.IntegerField(default=0)),
            ],
        ),
    ]
