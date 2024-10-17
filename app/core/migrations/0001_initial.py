# Generated by Django 3.2.12 on 2024-06-20 21:58

import datetime
from decimal import Decimal
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc
import django.utils.timezone
import proy_sales.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=100, unique=True, verbose_name='Articulo')),
                ('image', models.ImageField(blank=True, null=True, upload_to='brands/', verbose_name='Imagen')),
                ('active', models.BooleanField(default=True, verbose_name='Activo')),
            ],
            options={
                'verbose_name': 'Marca',
                'verbose_name_plural': 'Marcas',
                'ordering': ['description'],
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=100, unique=True, verbose_name='Categoría')),
                ('image', models.ImageField(blank=True, null=True, upload_to='categories/', verbose_name='Imagen')),
                ('active', models.BooleanField(default=True, verbose_name='Activo')),
            ],
            options={
                'verbose_name': 'Categoria',
                'verbose_name_plural': 'Categorias',
                'ordering': ['description'],
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dni', models.CharField(blank=True, max_length=13, null=True, verbose_name='RUC')),
                ('name', models.CharField(max_length=50, verbose_name='Empresa')),
                ('address', models.CharField(blank=True, max_length=200, null=True, verbose_name='Dirección')),
                ('representative', models.CharField(blank=True, max_length=50, null=True, verbose_name='Responsable')),
                ('landline', models.CharField(blank=True, max_length=10, null=True, verbose_name='Teléfono Fijo')),
                ('website', models.URLField(blank=True, max_length=100, null=True, verbose_name='Sitio Web')),
                ('email', models.EmailField(blank=True, max_length=100, null=True, verbose_name='Correo Electrónico')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='company/', verbose_name='Logo')),
                ('establishment_code', models.CharField(blank=True, default='001', help_text='Código de tres dígitos asignado al establecimiento por el SRI. Para empresas sin sucursales, usar "001".', max_length=3, null=True, verbose_name='Código de Establecimiento')),
                ('emission_point_code', models.CharField(blank=True, default='001', help_text='Código de tres dígitos del punto de emisión. Para empresas con un solo punto de emisión, usar "001".', max_length=3, null=True, verbose_name='Código de Punto de Emisión')),
                ('authorization_number', models.CharField(blank=True, default='12345678901234567890123456789012345678901234567890', help_text='Número de autorización otorgado por el SRI.', max_length=49, null=True, verbose_name='Número de Autorización')),
                ('taxpayer_type', models.CharField(blank=True, choices=[('special', 'Contribuyente Especial'), ('ordinary', 'Contribuyente Ordinario')], default='ordinary', help_text='Tipo de contribuyente según clasificación del SRI.', max_length=50, null=True, verbose_name='Tipo de Contribuyente')),
                ('required_to_keep_accounting', models.BooleanField(default=True, help_text='Indica si la empresa está obligada a llevar contabilidad.', verbose_name='Obligado a Llevar Contabilidad')),
                ('economic_activity_code', models.CharField(blank=True, default='1234567890', help_text='Código de la actividad económica según el SRI.', max_length=10, null=True, verbose_name='Código de Actividad Económica')),
            ],
            options={
                'verbose_name': 'Empresa',
                'verbose_name_plural': 'Empresa',
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dni', models.CharField(blank=True, max_length=13, null=True, unique=True, verbose_name='Dni')),
                ('first_name', models.CharField(max_length=50, verbose_name='Nombres')),
                ('last_name', models.CharField(max_length=50, verbose_name='Apellidos')),
                ('address', models.TextField(blank=True, null=True, verbose_name='Dirección')),
                ('gender', models.CharField(choices=[('M', 'Masculino'), ('F', 'Femenino')], default='M', max_length=1, verbose_name='Sexo')),
                ('date_of_birth', models.DateField(blank=True, null=True, verbose_name='Fecha Nacimiento')),
                ('phone', models.CharField(blank=True, max_length=50, null=True, verbose_name='Telefono')),
                ('email', models.CharField(blank=True, max_length=100, null=True, verbose_name='Correo')),
                ('latitude', models.CharField(max_length=100, verbose_name='Latitud')),
                ('longitude', models.CharField(max_length=100, verbose_name='Longitud')),
                ('image', models.ImageField(blank=True, null=True, upload_to='customers/', verbose_name='Foto')),
                ('active', models.BooleanField(default=True, verbose_name='Activo')),
            ],
            options={
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'Clientes',
                'ordering': ['last_name'],
            },
        ),
        migrations.CreateModel(
            name='Iva',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=100, unique=True, verbose_name='Iva')),
                ('value', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Porcentaje(%)')),
                ('active', models.BooleanField(default=True, verbose_name='Activo')),
            ],
            options={
                'verbose_name': 'Iva',
                'verbose_name_plural': 'Ivas',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Line',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=100, unique=True, verbose_name='Linea')),
                ('image', models.ImageField(blank=True, null=True, upload_to='lines/', verbose_name='Imagen')),
                ('active', models.BooleanField(default=True, verbose_name='Activo')),
            ],
            options={
                'verbose_name': 'Linea',
                'verbose_name_plural': 'Lineas',
                'ordering': ['description'],
            },
        ),
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=100, verbose_name='Metodo de Pago')),
                ('image', models.ImageField(blank=True, null=True, upload_to='paymentmethods/', verbose_name='Foto')),
                ('active', models.BooleanField(default=True, verbose_name='Activo')),
            ],
            options={
                'verbose_name': 'Metodo de Pago',
                'verbose_name_plural': 'Metodo de Pagos',
                'ordering': ['description'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(db_index=True, max_length=100, unique=True, verbose_name='Nombre')),
                ('cost', models.DecimalField(decimal_places=2, default=Decimal('0.0'), max_digits=10, verbose_name='Costo Producto')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, validators=[proy_sales.utils.valida_numero_flotante_positivo], verbose_name='Precio')),
                ('stock', models.IntegerField(default=100, validators=[proy_sales.utils.valida_numero_entero_positivo], verbose_name='Costo')),
                ('expiration_date', models.DateTimeField(default=datetime.datetime(2024, 7, 20, 21, 58, 32, 863302, tzinfo=utc), verbose_name='Caducidad')),
                ('image', models.ImageField(blank=True, null=True, upload_to='products/', verbose_name='Imagen')),
                ('state', models.CharField(choices=[('A', 'Activo'), ('B', 'De Baja')], default='A', max_length=1, verbose_name='Activo')),
                ('active', models.BooleanField(default=True, verbose_name='Activo')),
            ],
            options={
                'verbose_name': 'Producto',
                'verbose_name_plural': 'Productos',
                'ordering': ['description'],
            },
        ),
        migrations.CreateModel(
            name='ProductPrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_increment', models.CharField(choices=[('P', 'Porcentaje'), ('V', 'Valor Fijo')], default='P', max_length=1, verbose_name='Tipo de Aumento')),
                ('value', models.DecimalField(decimal_places=2, default=0, max_digits=11, verbose_name='Incremento')),
                ('issue_date', models.DateTimeField(db_index=True, default=django.utils.timezone.now, verbose_name='Fecha Emision')),
                ('observaciones', models.TextField(blank=True, null=True, verbose_name='Obervacion')),
                ('active', models.BooleanField(default=True, verbose_name='Activo')),
            ],
            options={
                'verbose_name': 'Precios Producto',
                'verbose_name_plural': 'Precios Productos',
                'ordering': ('issue_date',),
            },
        ),
        migrations.CreateModel(
            name='ProductPriceDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('increment', models.DecimalField(decimal_places=2, default=0, max_digits=11, verbose_name='Incremento')),
                ('old_price', models.DecimalField(decimal_places=2, default=0, max_digits=11, verbose_name='Precio anterior')),
                ('issue_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Fecha Emision')),
                ('observation', models.TextField(blank=True, null=True)),
                ('active', models.BooleanField(default=True, verbose_name='Activo')),
            ],
            options={
                'verbose_name': 'Producto Precios Detalle',
                'verbose_name_plural': 'Productos Precios Detalles',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Nombres')),
                ('ruc', models.CharField(max_length=10, unique=True, validators=[proy_sales.utils.valida_cedula], verbose_name='Dni')),
                ('image', models.ImageField(blank=True, null=True, upload_to='suppliers/', verbose_name='Imagen')),
                ('phone', models.CharField(max_length=10, validators=[django.core.validators.RegexValidator(message='Caracteres inválidos para un número de teléfono.', regex='^\\d{9,15}$')], verbose_name='Telefono')),
                ('address', models.CharField(max_length=200, verbose_name='Direccion')),
                ('latitude', models.CharField(max_length=100, verbose_name='Latitud')),
                ('longitude', models.CharField(max_length=100, verbose_name='Longitud')),
                ('active', models.BooleanField(default=True, verbose_name='Activo')),
            ],
            options={
                'verbose_name': 'Proveedor',
                'verbose_name_plural': 'Proveedores',
                'ordering': ['name'],
            },
        ),
        migrations.AddIndex(
            model_name='supplier',
            index=models.Index(fields=['name'], name='core_suppli_name_c90f73_idx'),
        ),
        migrations.AddField(
            model_name='productpricedetail',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='price_detail', to='core.product', verbose_name='Producto Precio detalle'),
        ),
        migrations.AddField(
            model_name='productpricedetail',
            name='productpreci',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='productPrice_detail', to='core.productprice', verbose_name='Producto Precio detalle'),
        ),
        migrations.AddField(
            model_name='productprice',
            name='category',
            field=models.ManyToManyField(blank=True, related_name='productPrice_categories', to='core.Category', verbose_name='Categoria'),
        ),
        migrations.AddField(
            model_name='productprice',
            name='line',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='productPrice_lines', to='core.line', verbose_name='Linea'),
        ),
        migrations.AddField(
            model_name='productprice',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='productPrice', to='core.product', verbose_name='Producto Precio'),
        ),
        migrations.AddField(
            model_name='product',
            name='brand',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='product_brands', to='core.brand', verbose_name='Marca'),
        ),
        migrations.AddField(
            model_name='product',
            name='categories',
            field=models.ManyToManyField(related_name='products_categories', to='core.Category', verbose_name='Categoria'),
        ),
        migrations.AddField(
            model_name='product',
            name='iva',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='product_iva', to='core.iva', verbose_name='Iva'),
        ),
        migrations.AddField(
            model_name='product',
            name='line',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='product_lines', to='core.line', verbose_name='Linea'),
        ),
        migrations.AddIndex(
            model_name='customer',
            index=models.Index(fields=['last_name'], name='core_custom_last_na_c56f78_idx'),
        ),
        migrations.AddIndex(
            model_name='brand',
            index=models.Index(fields=['description'], name='core_brand_descrip_5b1a81_idx'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['description'], name='core_produc_descrip_f55423_idx'),
        ),
    ]
