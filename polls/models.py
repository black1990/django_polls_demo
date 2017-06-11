#coding=utf-8
from __future__ import unicode_literals
from django.utils import timezone
from django.db import models
import datetime
# Create your models here.
class Question(models.Model):
    question_text=models.CharField(max_length=200,verbose_name='问题')
    pub_date=models.DateTimeField(verbose_name='日期')
    
    def  was_published_recently(self):
        now=timezone.now()
        return now>=self.pub_date >=now - datetime.timedelta(days=1)
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

    def __str__(self):
        return self.question_text
class Choice(models.Model):
    question=models.ForeignKey(Question,verbose_name='问题')
    choice_txt=models.CharField(max_length=200,verbose_name="答案")
    votes=models.IntegerField(default=0,verbose_name='投票量')
    def __str__(self):
        return self.choice_txt
    
