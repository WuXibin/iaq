#coding=utf-8
from django.db import models

# Create your models here.
from django.db.models import Model, IntegerField, FloatField, CharField, DateTimeField

class SensorNode(Model):
    '''节点模型'''
    node_id = CharField(max_length=10)
    description = CharField(max_length=30)
    # 以下字段存放节点最新数据
    temp = FloatField(null=True)
    humi = FloatField(null=True)
    iaqengine = IntegerField(null=True)
    tgs2600 = IntegerField(null=True)
    tgs2602 = IntegerField(null=True)
    formaldehyde = FloatField(null=True)
    time = DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.node_id

    class Meta:
        ordering = ['node_id']

class SensorData(Model):
    '''节点数据模型'''
    node_id = CharField(max_length=10)
    temp = FloatField()
    humi = FloatField()
    iaqengine = IntegerField()
    tgs2600 = IntegerField()
    tgs2602 = IntegerField()
    formaldehyde = FloatField()
    time = DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.node_id

    class Meta:
        ordering = ['-time']