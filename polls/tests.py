import datetime
from urllib import response
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question

# Create your tests here.

class QuestionModelTests(TestCase):

  def test_was_published_recently_with_future_question(self):
    time = timezone.now() + datetime.timedelta(days=30)
    future_question = Question(pub_date=time)

    self.assertIs(future_question.was_published_recently(), False)

def create_question(question_test, days):
  time = timezone.now() + datetime.timedelta(days=days)
  return Question.objects.create(question_test=question_test, pub_date=time)

class QuestionIndexViewTests(TestCase):
  def test_no_questions(self):
    response = self.client.get(reverse('polls:index'))

    self.assertEqual(response.status_code, 200)
    self.assertContains(response, "No polls are available.")
    self.assertQuerysetEqual(response.context['latest_question_list'], [])

  def test_past_question(self):
    create_question(question_test="Past question.", days=-30)
    response = self.client.get(reverse('polls:index'))

    self.assertQuerysetEqual(
      response.context['latest_question_list'],
      ['<Question: Past question.>']
    )

  def test_future_question(self):
    create_question(question_test="Future question.", days=30)
    response = self.client.get(reverse('polls:index'))
    self.assertContains(response, "No polls are available.")
    self.assertQuerysetEqual(response.context['latest_question_list'])

  def test_future_question_and_past_question(self):
    create_question(question_test="Past question.", days=-30)
    create_question(question_test="Future question.", days=30)
    response = self.client.get(reverse('polls:index'))

    self.assertQuerysetEqual(
      response.context['latest_question_list'],
      ['<Question: Past question.>']
    )

  def test_two_past_question(self):
    create_question(question_test="Past question 1.", days=-30)
    create_question(question_test="Past question 2.", days=-5)
    response = self.client.get(reverse('polls:index'))

    self.assertQuerysetEqual(
    response.context['latest_question_list'],
      ['<Question: Past question 2.>', '<Question: Past question 1.>']
    )