# Generated by Django 4.2.1 on 2023-05-25 02:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_nftuser'),
        ('gallery', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nft_object',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.nftuser'),
        ),
    ]
