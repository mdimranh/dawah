# Generated by Django 3.2.3 on 2021-07-17 12:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('channel', '0048_video_duration'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='video',
        ),
        migrations.AlterField(
            model_name='video',
            name='title',
            field=models.CharField(max_length=255),
        ),
        migrations.CreateModel(
            name='videofile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video', models.URLField()),
                ('title', models.CharField(max_length=255)),
                ('video_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='channel.video')),
            ],
        ),
    ]
