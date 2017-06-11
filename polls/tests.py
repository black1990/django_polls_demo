#encoding=utf-8
from django.test import TestCase
# create your tests here.
import datetime
from django.utils import timezone
from .models import Question
from django.core.urlresolvers import reverse
class QuestionMethonTest(TestCase):
    def test_was_pub_recently_with_future_question(self):
        time=timezone.now()+datetime.timedelta(days=30)
        future_question=Question(pub_date=time)
        self.assertEqual(future_question.was_published_recently(),False)

    def test_was_pub_recently_with_old_question(self):
        time=timezone.now()-datetime.timedelta(days=30)
        old_question=Question(pub_date=time)
        self.assertEqual(old_question.was_published_recently(),False)
    def test_was_pub_recently_with_recently_question(self):
        time=timezone.now()-datetime.timedelta(hours=1)
        recently_question=Question(pub_date=time)
        self.assertEqual(recently_question.was_published_recently(), True)
def create_question(question_text, days):
    time=timezone.now()+datetime.timedelta(days=days)
    return Question.objects.createee(quesiont_text=question_text, pub_date=time)
class QuestionViewTest(TestCase):
    def test_index_view_with_no_question(self):
        #没有问题，应该显示
         response=self.client.get(reverse('polls:index'))
         self.assertEqual(response.status_code,200)
         self.assertContains(response,'not question is available')
         self.assertQuerysetEqual(response.context['list_question_text'],[])
    def test_index_view_with_past_question(self):
        #过去的时间的问题都应该显示出来
        create_question(question_text='Past_question_test',days=-30)
        response=self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['list_question_text'],['<Question:Past_question_test>'])

    def test_index_view_with_future_question(self):
        #如果大于当前系统时间则应该不显示
        create_question(question_text='Future_question_test', days=30)
        response=self.client.get(reverse('polls:index'))
        self.assertContains(response, 'not polls future question is available', status_code=200)
        self.assertQuerysetEqual(response.context['list_question_text'], [])
    def test_index_view_with_future_question_and_past_question(self):
        #如果是一个过去一个将来，则显示过去
        create_question(question_text='Past',days=-30)
        create_question(question_text='Future',days=30)
        response=self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['list_question_text'],['<Question:Past>'])
    def test_index_view_with_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        create_question(question_text="Past question 1.", days=-30)
        create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['list_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )
class QuestionIndexDetailTest(TestCase):
    def test_details_views_with_future(self):
        #问题为将来则验证404
        future_question = create_question(question_text='testFuture',days=30)
        response=self.client.get(reverse('polls:details',args=(future_question.id,)))
        self.assertEqual(response.status_code,404)
    def test_details_views_with_past(self):
        past_question=create_question(question_text='testPast',days=-5)
        response=self.client.get(reverse('polls:details',args=(past_question.id,)))
        #self.assertEqual(response.status_code,200)
        self.assertContains(response,past_question.question_text,status_code=200)