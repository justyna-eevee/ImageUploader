# Generated by Django 3.2.3 on 2021-05-14 18:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ImageUploaderApp', '0002_accounttype_types'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='images',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='images_links', to='ImageUploaderApp.image'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='accounttype',
            name='types',
            field=models.IntegerField(choices=[(2, 'premium'), (1, 'basic'), (3, 'enterprise')], default=0),
        ),
    ]
