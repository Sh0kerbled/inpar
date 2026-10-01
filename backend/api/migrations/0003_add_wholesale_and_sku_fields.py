# Generated for Product wholesale and sku fields

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_product_price_field'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='sku',
            field=models.CharField(blank=True, db_index=True, help_text='Product code / SKU', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='wholesale_price_usd',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Wholesale price in USD', max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='min_wholesale_quantity',
            field=models.IntegerField(blank=True, default=1, help_text='Minimum quantity for wholesale', null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='source_url',
            field=models.URLField(blank=True, help_text='Source URL', max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='price_usd',
            field=models.DecimalField(decimal_places=2, help_text='Retail price in USD', max_digits=10),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='api.category'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['sku'], name='api_product_sku_b4e912_idx'),
        ),
    ]
