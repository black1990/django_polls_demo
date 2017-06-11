#coding=utf-8
from django.contrib import admin
from .models import Question,Choice
# Register your models here.
'''
class QuestionAdmin(admin.ModelAdmin):
    fields=['pub_date','question_text']
admin.site.register(Question,QuestionAdmin)
admin.site.register(Choice)
'''

'''
#设置字段信息 折叠信息
class QuestionAdmin(admin.ModelAdmin):
    fieldsets=[
        (None,{'fields':['question_text']}),
        ('Date information',{'fields':['pub_date'],'classes':['collapse']}),#最后一个参数折叠
        ]
admin.site.register(Question,QuestionAdmin)    
admin.site.register(Choice)
'''
#在question里面添加内联 TabularInline（表格式） StackedInline(堆叠内联)
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra=3 #内联三个

class QuestionAdmin(admin.ModelAdmin):
    list_filter=['pub_date']#过滤
    search_fields=['question_text']
    list_display=('question_text','pub_date','was_published_recently')#最后一个为自定义的
    fieldsets=[
        (None,{'fields':['question_text']}),
        ('Date information',{'fields':['pub_date'],'classes':['collapse']}),
        ]
    inlines=[ChoiceInline]
admin.site.register(Question,QuestionAdmin)
admin.site.register(Choice)
