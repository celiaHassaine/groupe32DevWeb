# Generated by Django 3.0.4 on 2020-03-18 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=100)),
                ('contenu', models.TextField()),
                ('chemin', models.ImageField(upload_to='pics')),
            ],
        ),
    ]