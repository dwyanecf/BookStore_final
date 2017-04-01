# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import models


class Admin(models.Model):
    admin_id = models.IntegerField(db_column='ADMIN_ID', primary_key=True)  # Field name made lowercase.
    admin_name = models.CharField(db_column='ADMIN_NAME', max_length=30)  # Field name made lowercase.
    admin_pwd = models.CharField(db_column='ADMIN_PWD', max_length=30)  # Field name made lowercase.
    
    def __unicode__(self):
        return str(self.admin_id) + ' - ' + self.admin_name
        
    class Meta:
        managed = False
        db_table = 'admin'


class Authors(models.Model):
    author_id = models.BigIntegerField(db_column='AUTHOR_ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=100)  # Field name made lowercase.
        
    def __unicode__(self):
        return str(self.admin_id) + ' - ' + self.admin_name
        
    class Meta:
        managed = False
        db_table = 'authors'


class BlackList(models.Model):
    email = models.CharField(db_column='EMAIL', primary_key=True, max_length=50)  # Field name made lowercase.
    
    def __unicode__(self):
        return str(self.admin_id) + ' - ' + self.admin_name
    
    class Meta:
        managed = False
        db_table = 'black_list'


class Book(models.Model):
    isbn = models.CharField(db_column='ISBN', primary_key=True, max_length=13)  # Field name made lowercase.
    title = models.CharField(db_column='TITLE', max_length=500)  # Field name made lowercase.
    type = models.ForeignKey('BookTypes', db_column='TYPE_ID')  # Field name made lowercase.
    price = models.DecimalField(db_column='PRICE', max_digits=8, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    quantity = models.IntegerField(db_column='QUANTITY')  # Field name made lowercase.
    pages = models.IntegerField(db_column='PAGES')  # Field name made lowercase.
    publisher = models.CharField(db_column='PUBLISHER', max_length=200, blank=True)  # Field name made lowercase.
    cover = models.CharField(db_column='COVER', max_length=300, blank=True)  # Field name made lowercase.
    pubdate = models.DateField(db_column='PUBDATE', blank=True, null=True)  # Field name made lowercase.
    is_available = models.CharField(max_length=4, blank=True, null=True)
    def __unicode__(self):
        return self.isbn
        
    class Meta:
        managed = False
        db_table = 'book'


class BookAuthors(models.Model):
    author = models.ForeignKey(Authors, db_column='AUTHOR_ID', primary_key=True)  # Field name made lowercase.
    isbn = models.ForeignKey(Book, db_column='ISBN', primary_key=True)  # Field name made lowercase.
    
    class Meta:
        managed = False
        db_table = 'book_authors'


class BookTypes(models.Model):
    type_id = models.IntegerField(db_column='TYPE_ID', primary_key=True)  # Field name made lowercase.
    type_name = models.CharField(db_column='TYPE_NAME', max_length=50, blank=True)  # Field name made lowercase.
    
    def __unicode__(self):
        return str(self.type_id) + ' - ' + str(self.type_name)
        
    class Meta:
        managed = False
        db_table = 'book_types'


class Comments(models.Model):
    isbn = models.ForeignKey(Book, db_column='ISBN')  # Field name made lowercase.
    user = models.ForeignKey('UserInfo', db_column='USER_ID')  # Field name made lowercase.
    post_date = models.DateTimeField(db_column='POST_DATE', blank=True, null=True)  # Field name made lowercase.
    comment = models.CharField(db_column='COMMENT', max_length=500, blank=True)  # Field name made lowercase.
    rating = models.IntegerField(db_column='RATING')  # Field name made lowercase.
    
    def __unicode__(self):
        return str(self.isbn) + ' - ' + str(self.user) 
        
    class Meta:
        managed = False
        db_table = 'comments'


class OrderItems(models.Model):
    order = models.ForeignKey('Orders', db_column='ORDER_ID')  # Field name made lowercase.
    isbn = models.ForeignKey(Book, db_column='ISBN', primary_key=True)  # Field name made lowercase.
    quantity = models.IntegerField(db_column='QUANTITY')  # Field name made lowercase.
    
    def __unicode__(self):
        return str(self.order) + ' - ' + str(self.isbn) + ' - ' + str(self.quantity)
        
    class Meta:
        unique_together = ('order', 'isbn')
        managed = False
        db_table = 'order_items'


class Orders(models.Model):
    order_id = models.BigIntegerField(db_column='ORDER_ID', primary_key=True)  # Field name made lowercase.
    user = models.ForeignKey('UserInfo', db_column='USER_ID')  # Field name made lowercase.
    order_date = models.DateTimeField(db_column='ORDER_DATE', blank=True, null=True)  # Field name made lowercase.
    ship_address = models.CharField(db_column='SHIP_ADDRESS', max_length=200, blank=True)  # Field name made lowercase.
    ship_phone = models.CharField(db_column='SHIP_PHONE', max_length=10, blank=True)  # Field name made lowercase.
    total_price = models.DecimalField(db_column='TOTAL_PRICE', max_digits=8, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    message = models.CharField(db_column='MESSAGE', max_length=500, blank=True)  # Field name made lowercase.
    is_available = models.CharField(max_length=4, blank=True, null=False)
    def __unicode__(self):
         return str(self.order_id)
        
    class Meta:
        managed = False
        db_table = 'orders'


class UserInfo(models.Model):
    user_id = models.CharField(db_column='USER_ID', primary_key=True, max_length=30)  # Field name made lowercase.
    pwd = models.CharField(db_column='PWD', max_length=100)  # Field name made lowercase.
    address = models.CharField(db_column='ADDRESS', max_length=200, blank=True)  # Field name made lowercase.
    phone = models.CharField(db_column='PHONE', max_length=10, blank=True)  # Field name made lowercase.
    email = models.CharField(db_column='EMAIL', max_length=50, blank=True)  # Field name made lowercase.
    last_log = models.DateTimeField(db_column='LAST_LOG', blank=True, null=True)  # Field name made lowercase.
    
    def __unicode__(self):
        return str(self.user_id)
        
    class Meta:
        managed = False
        db_table = 'user_info'
class LineItem(models.Model):
    product = models.ForeignKey('Book', db_column='isbn')
    unit_price = models.DecimalField(max_digits=8,decimal_places=2)
    quantity = models.IntegerField()
class Cart(object):
    total_quantity=0
    def __init__(self, *args, **kwargs):
        self.items = []
        self.total_price = 0
        self.total_quantity=0
    def add_product(self,product):
        self.total_price += product.price
        self.total_quantity+=1
        for item in self.items:
            if item.product.isbn == product.isbn:
                item.quantity += 1
                return 
        self.items.append(LineItem(product=product,unit_price=product.price,quantity=1))
    def remove_product(self,product):
        for item in self.items:
            if item.product.isbn == product.isbn:
                self.total_price -= product.price*item.quantity
                self.total_quantity-=item.quantity
                self.items.remove(item)
                return
    def change_item_quantity(self,product,quantity):
        for item in self.items:
            if item.product.isbn == product.isbn:
                self.total_price += product.price*quantity
                self.total_quantity+=quantity
                item.quantity+=quantity
                if not item.quantity:
                    self.items.remove(item)
                return