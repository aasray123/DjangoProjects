from django.shortcuts import HttpResponse, render, redirect
from django.template import loader

def home(request):
    if ('tempExp' not in request.session) :
        request.session['tempExp'] = ''
    result = ''

    if request.method == 'POST':
        expression = request.POST.get('expression')
        if(expression == '='):
            try:
                result = eval(request.session['tempExp'])  # CAUTION: Use eval carefully
            except Exception as e:
                result = str(e)
        else:
            request.session['tempExp'] = request.session['tempExp'] + expression
            print(request.session['tempExp'])
        
    return render(request, 'index.html', {'result': result })