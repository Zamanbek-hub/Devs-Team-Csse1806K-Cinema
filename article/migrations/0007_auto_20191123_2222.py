# Generated by Django 2.2.6 on 2019-11-23 16:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0006_auto_20191120_2124'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cinema',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cinema_name', models.CharField(max_length=30, verbose_name='Name_of_cinema')),
                ('area', models.PositiveIntegerField()),
                ('cinema_address', models.CharField(default='71', max_length=30, verbose_name='cinema_address')),
            ],
        ),
        migrations.AlterField(
            model_name='block',
            name='movie_name',
            field=models.CharField(max_length=50, verbose_name='movie_name'),
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.PositiveIntegerField()),
                ('of_cinema', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='article.Cinema')),
            ],
        ),
    ]
