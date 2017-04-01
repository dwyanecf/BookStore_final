# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('admin_id', models.IntegerField(serialize=False, primary_key=True, db_column='ADMIN_ID')),
                ('admin_name', models.CharField(max_length=30, db_column='ADMIN_NAME')),
                ('admin_pwd', models.CharField(max_length=30, db_column='ADMIN_PWD')),
            ],
            options={
                'db_table': 'admin',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Authors',
            fields=[
                ('author_id', models.BigIntegerField(serialize=False, primary_key=True, db_column='AUTHOR_ID')),
                ('name', models.CharField(max_length=100, db_column='NAME')),
            ],
            options={
                'db_table': 'authors',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BlackList',
            fields=[
                ('email', models.CharField(max_length=50, serialize=False, primary_key=True, db_column='EMAIL')),
            ],
            options={
                'db_table': 'black_list',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('isbn', models.CharField(max_length=13, serialize=False, primary_key=True, db_column='ISBN')),
                ('title', models.CharField(max_length=500, db_column='TITLE')),
                ('price', models.DecimalField(null=True, decimal_places=2, max_digits=8, db_column='PRICE', blank=True)),
                ('quantity', models.IntegerField(db_column='QUANTITY')),
                ('pages', models.IntegerField(db_column='PAGES')),
                ('publisher', models.CharField(max_length=200, db_column='PUBLISHER', blank=True)),
                ('cover', models.CharField(max_length=300, db_column='COVER', blank=True)),
                ('pubdate', models.DateField(null=True, db_column='PUBDATE', blank=True)),
            ],
            options={
                'db_table': 'book',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BookAuthors',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'db_table': 'book_authors',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BookTypes',
            fields=[
                ('type_id', models.IntegerField(serialize=False, primary_key=True, db_column='TYPE_ID')),
                ('type_name', models.CharField(max_length=50, db_column='TYPE_NAME', blank=True)),
            ],
            options={
                'db_table': 'book_types',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('post_date', models.DateTimeField(null=True, db_column='POST_DATE', blank=True)),
                ('comment', models.CharField(max_length=500, db_column='COMMENT', blank=True)),
                ('rating', models.IntegerField(db_column='RATING')),
            ],
            options={
                'db_table': 'comments',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OrderItems',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantity', models.IntegerField(db_column='QUANTITY')),
            ],
            options={
                'db_table': 'order_items',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('order_id', models.BigIntegerField(serialize=False, primary_key=True, db_column='ORDER_ID')),
                ('order_date', models.DateTimeField(null=True, db_column='ORDER_DATE', blank=True)),
                ('ship_address', models.CharField(max_length=200, db_column='SHIP_ADDRESS', blank=True)),
                ('ship_phone', models.CharField(max_length=10, db_column='SHIP_PHONE', blank=True)),
                ('total_price', models.DecimalField(null=True, decimal_places=2, max_digits=8, db_column='TOTAL_PRICE', blank=True)),
                ('message', models.CharField(max_length=500, db_column='MESSAGE', blank=True)),
            ],
            options={
                'db_table': 'orders',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('user_id', models.CharField(max_length=30, serialize=False, primary_key=True, db_column='USER_ID')),
                ('pwd', models.CharField(max_length=30, db_column='PWD')),
                ('address', models.CharField(max_length=200, db_column='ADDRESS', blank=True)),
                ('phone', models.CharField(max_length=10, db_column='PHONE', blank=True)),
                ('email', models.CharField(max_length=50, db_column='EMAIL', blank=True)),
                ('last_log', models.DateTimeField(null=True, db_column='LAST_LOG', blank=True)),
            ],
            options={
                'db_table': 'user_info',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LineItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('unit_price', models.DecimalField(max_digits=8, decimal_places=2)),
                ('quantity', models.IntegerField()),
                ('product', models.ForeignKey(to='search.Book', db_column='isbn')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
