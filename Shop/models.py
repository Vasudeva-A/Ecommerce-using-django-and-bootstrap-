from django.db import models
from django.contrib.auth.models import User


import datetime

import os

def  getFileName(request,filename):

    now_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    newfile = "%s%s"%(now_time,filename)

    return os.path.join('uploads/',newfile)



class Category(models.Model):

    name = models.CharField( max_length=150,null=False,blank=False)

    image = models.ImageField(upload_to=getFileName, blank=True,null=True)

    description = models.TextField(null=False,blank=False)
    
    status = models.BooleanField(default=False,help_text="0-show,1-hidden")

    created_at  = models.DateTimeField( auto_now=True)


    def __str__(self):
        return self.name
    



class Products(models.Model):

    category = models.ForeignKey(Category,on_delete=models.CASCADE)

    name = models.CharField( max_length=150,null=False,blank=False)

    vendor = models.CharField( max_length=150,null=False,blank=False)

    product_image = models.ImageField(upload_to=getFileName, blank=True,null=True)

    quantity = models.IntegerField(null=False,blank=False)

    original_price = models.IntegerField(null=False,blank=False)
    
    selling_price = models.FloatField(null=False,blank=False)

    description = models.TextField(null=False,blank=False)

    trending = models.BooleanField(default=False,help_text="0-default,1-Trending")
    
    status = models.BooleanField(default=False,help_text="0-show,1-hidden")

    created_at  = models.DateTimeField( auto_now=True)


    def __str__(self):
        return self.name
    

class Carts(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    products = models.ForeignKey(Products,on_delete=models.CASCADE)
    product_quantity = models.PositiveIntegerField(default=1)  
    total = models.IntegerField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.username}"


class OrderProducts(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    order_products = models.ForeignKey(Products,on_delete=models.CASCADE)
    total_price = models.FloatField(null=True, blank=True)
    order_quantity = models.PositiveIntegerField(default=1)  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Orders of {self.user.username}"




