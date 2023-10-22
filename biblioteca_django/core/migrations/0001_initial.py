# Generated by Django 4.2.5 on 2023-10-21 23:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Autor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255, verbose_name='Autor/a o Autor@s del Libro')),
            ],
        ),
        migrations.CreateModel(
            name='Libro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=255, verbose_name='Título del Libro')),
                ('editorial', models.CharField(max_length=255, verbose_name='Editorial')),
                ('publicacion', models.DateField(verbose_name='fecha de publicación')),
                ('genero', models.CharField(max_length=255, verbose_name='Genero')),
                ('autores', models.ManyToManyField(to='core.autor', verbose_name='Autor/a o Autor@s del Libro')),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30, verbose_name='nombre')),
                ('apellido', models.CharField(max_length=30, verbose_name='apellido')),
                ('dni', models.IntegerField(unique=True, verbose_name='Dni')),
                ('email', models.EmailField(max_length=150, verbose_name='Email')),
            ],
        ),
        migrations.CreateModel(
            name='Prestamo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_prestamo', models.DateField(verbose_name='Fecha de Préstamo')),
                ('fecha_devolucion', models.DateField(verbose_name='Fecha de Devolución')),
                ('libro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.libro', verbose_name='Libro Prestado')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.usuario', verbose_name='Usuario')),
            ],
        ),
    ]
