# Generated by Django 2.2.6 on 2019-11-20 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0005_auto_20191119_0107'),
    ]

    operations = [
        migrations.CreateModel(
            name='Jenre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jenre', models.CharField(max_length=30, verbose_name='Jenre of Movie')),
            ],
        ),
        migrations.RenameField(
            model_name='block',
            old_name='img',
            new_name='move_img',
        ),
        migrations.RenameField(
            model_name='block',
            old_name='article_date',
            new_name='movie_article_date',
        ),
        migrations.RenameField(
            model_name='block',
            old_name='available',
            new_name='movie_available',
        ),
        migrations.RenameField(
            model_name='block',
            old_name='block_explain',
            new_name='movie_explain',
        ),
        migrations.RenameField(
            model_name='block',
            old_name='name',
            new_name='movie_name',
        ),
        migrations.RenameField(
            model_name='block',
            old_name='numberOfClicks',
            new_name='movie_numberOfClicks',
        ),
        migrations.RenameField(
            model_name='block',
            old_name='rating',
            new_name='movie_rating',
        ),
        migrations.RemoveField(
            model_name='block',
            name='jenre',
        ),
        migrations.AddField(
            model_name='block',
            name='movie_genre',
            field=models.ManyToManyField(to='article.Jenre'),
        ),
    ]
