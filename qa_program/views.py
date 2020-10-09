from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import loader

from .models import Question

# Create your views here.
def index(request):
    question_list = Question.objects.order_by('id')
    template_name = 'qa_program/index.html'
    template = loader.get_template(template_name)
    context = {
        'question_list': question_list,
    }

    return HttpResponse(template.render(context, request))


def detail(request, no, kind):
    q = get_object_or_404(Question, id=no)

    context = {
        'q': q,
    }

    template_name = 'qa_program/detail.html'
    template = loader.get_template(template_name)

    return HttpResponse(template.render(context, request))



def detail_direct(request, qid):
    q = get_object_or_404(Question, id=qid)
    context = {
        'q': q,
    }

    template_name = 'qa_program/detail.html'
    template = loader.get_template(template_name)

    return HttpResponse(template.render(context, request))