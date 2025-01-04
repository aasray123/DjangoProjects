from django.shortcuts import HttpResponse, render, redirect
from django.template import loader

def home(request):
    #First time joining or var not made, then init blank
    if ('tempExp' not in request.session) or request.method == 'GET' :
        request.session['tempExp'] = ''
    result = ''

    if request.method == 'POST':
        expression = request.POST.get('expression')

        #Calculate final equation
        if(expression == '='):
            try:
                result = eval(request.session['tempExp'])  # CAUTION: Use eval carefully
                request.session['tempExp'] = str(result)
            except Exception as e:
                result = str(e)
        else:
            #UPDATE the tempExp value 
            request.session['tempExp'] = request.session['tempExp'] + expression

            #DEBUGGING 
            print(request.session['tempExp'])
        
    return render(request, 'index.html', {'result': result })