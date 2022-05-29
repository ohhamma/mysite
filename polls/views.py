#from django.shortcuts import render
from json import load
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic

from .models import Choice, Question

# Create your views here.

def index(request):
  # 1
  # return HttpResponse("Hello, World.")

  # 2
  # latest_question_list = Question.objects.order_by('-pub_date')[:5]
  # output = ', '.join([q.question_test for q in latest_question_list])
  # return HttpResponse(output)

  # 3
  # latest_question_list = Question.objects.order_by('-pub_date')[:5]
  # template = loader.get_template('polls/index.html')
  # context = {
  #   'latest_question_list': latest_question_list,
  # }
  # return HttpResponse(template.render(context, request))

  # 4. Use the shortcut - render
  latest_question_list = Question.objects.order_by('-pub_date')[:5]
  context = {'latest_question_list': latest_question_list}
  return render(request, 'polls/index.html', context)

# class IndexView(generic.ListView):
#   template_name = 'polls/index.html'
#   context_object_name = 'latest_question_list'

#   def get_queryset(self):
#     """Return the last five published questions."""
#     return Question.objects.order_by('-pub_date')[:5]

def detail(request, question_id):
  # 1
  # return HttpResponse("You're looking at question %s." % question_id)

  # 2
  # try:
  #   question = Question.objects.get(pk=question_id)
  # except Question.DoesNotExist:
  #   raise Http404("Question does not exist")
  # return render(request, 'polls/detail.html', {'question': question})

  # 3. Use the shortcut - get_object_or_404
  question = get_object_or_404(Question, pk=question_id)
  return render(request, 'polls/detail.html', {'question': question})

# class DetailView(generic.DeleteView):
#   model = Question
#   template_name = 'polls/detail.html'

def results(request, question_id):
  # 1
  # response = "You're looking at the results of question %s."
  # return HttpResponse(response % question_id)

  # 2
  question = get_object_or_404(Question, pk=question_id)
  return render(request, 'polls/results.html', {'question': question})

# class ResultsView(generic.DeleteView):
#   model = Question
#   template_name = 'polls/results.html'

def vote(request, question_id):
  # return HttpResponse("You're voting on question %s." % question_id)
  if request.method == 'GET':
    pass
  elif request.method == 'POST':
    question = get_object_or_404(Question, pk=question_id)
    try:
      selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
      return render(request, 'polls/detail.html', {
        'question': question,
        'error_message': "You didn't select a choice.",
      })
    else:
      selected_choice.votes += 1
      return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))