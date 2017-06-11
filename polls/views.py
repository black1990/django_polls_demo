#coding=utf-8
from django.shortcuts import render
from django.http import HttpResponse,Http404,HttpResponseRedirect                                    #1
from .models import Question ,Choice
from  django.template import RequestContext,loader #1
from  django.shortcuts import render,get_object_or_404
from django.core.urlresolvers import reverse
from  django.views import generic
from django.utils import timezone
# Create your views here.

def index(request):
    list_question_text=Question.objects.filter(pub_date__lte=timezone.now()).order_by('pub_date')[:6]
    context={'list_question_text':list_question_text}
    return render(request,'polls/index.html',context)

def details(request,question_id):
    question = get_object_or_404(Question.objects.filter(pub_date__lte=timezone.now()),pk=question_id)
    return render(request, 'polls/details.html',{'question':question})

def vote(request, question_id):
    q = get_object_or_404(Question, pk=question_id)
    try:
        select_choice = q.choice_set.get(pk=request.POST['choice'])
    except (KeyError,Choice.DoesNotExist):
        return  render(request,'polls/details.html',{'question':q,'error_message':'you did not choice'})
    else:
        select_choice.votes+=1;
        select_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(q.id,)))


def results(request,question_id):
     question=get_object_or_404(Question,pk=question_id)
     return render(request,'polls/results.html',{'question':question})


