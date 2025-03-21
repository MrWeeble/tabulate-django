# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=2)

    def __str__(self):
        return self.name


class Account(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    country = models.ForeignKey(Country, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class Order(models.Model):
    account = models.ForeignKey(Account, on_delete=models.PROTECT)
    order_date = models.DateField()
    order_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.account.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.product
