from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader

from .models import Recorder
from django.utils import timezone
import string

# Create your views here.
def index(request):
    template_name = 'sirenscall/index.html'
    template = loader.get_template(template_name)

    return render(request, template_name, context=None)

    # return HttpResponse("Siren's Call")

def radar(request):
    template_name = 'sirenscall/radar.html'
    template = loader.get_template(template_name)

    return render(request, template_name, context=None)


def recorder_index(request):
    recorder_list = Recorder.objects.order_by('-pub_date')[:30]
    
    template_name = 'sirenscall/recorder_index.html'
    template = loader.get_template(template_name)
    context = {
        'recorder_list': recorder_list,
    }

    return HttpResponse(template.render(context, request))


def recorder_detail(request, recorder_id):
    try:
        recorder = Recorder.objects.get(pk=recorder_id)
    except Recorder.DoesNotExist:
        raise Http404("Record %s does not exist." % recorder_id)
    return render(request, 'sirenscall/recorder_detail.html', {'recorder': recorder})


def recorder_submit(request):
    title = request.POST['n_title']
    main_text = request.POST['n_main_text']
    author = request.POST['n_author']
    pub_date = timezone.now()
    is_bold = False

    # print(type(title))
    if len(main_text) == 0:
        pass
    else:
        if len(title) == 0:
            title = 'Untitled'
        if len(author) == 0:
            author = 'Unknown'
        print(title)
        print(main_text)
        print(author)
        print(pub_date)
        recorder = Recorder(title=title, main_text=main_text, pub_date=pub_date, is_bold=is_bold, author=author)
        recorder.save()

    print(request.get_full_path())
    # recorder_list = Recorder.objects.order_by('-pub_date')[:10]    
    # template_name = 'sirenscall/recorder_index.html'
    # template  =loader.get_template(template_name)
    # context = {
    #     'recorder_list': recorder_list,
    # }

    # return HttpResponse(template.render(context, request))
    return HttpResponse("OK")


    # return HttpResponseRedirect('http://sirenscall.top/recorder')
