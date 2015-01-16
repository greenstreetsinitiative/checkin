from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import RequestContext, loader

# Create your views here.
def register_view(request):
    if request.method == 'POST':
        return form_submission(request)
    else:
        template = loader.get_template('register/form.html')
        context = RequestContext(request, {
            'open' : True
        })
        page = template.render(context)
        return HttpResponse(page)

def form_submission(request):
    print request.POST


    return HttpResponse('post submitted yay')
