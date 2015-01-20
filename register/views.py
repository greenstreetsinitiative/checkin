from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import RequestContext, loader

from register.forms import Form

# Create your views here.
def register_view(request):
    if request.method == 'POST':
        return form_submission(request)
    else:
        return form_view(request, {
            'open': True
        })

def form_view(request, context_dict):
    """ Returns the rendered form for registering """
    template = loader.get_template('register/form.html')
    context = RequestContext(request, context_dict)
    page = template.render(context)
    return HttpResponse(page)

def form_submission(request):
    #try:
    f = Form(request.POST)
    return HttpResponse(f.display())
    #except:
    #    return form_view(request, {
    #        'open': True,
    #        'from_post': True
    #    })
