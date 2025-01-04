from django.shortcuts import HttpResponse, render, redirect
from django.template import loader

def home(request):
    #First time joining or var not made, then init blank
    if ('tempExp' not in request.session) or request.method == 'GET' :
        request.session['tempExp'] = '0'
    result = '0'

    if request.method == 'POST':
        expression = request.POST.get('expression')

        #Calculate final equation
        if(expression == '='):
            try:
                result = eval(request.session['tempExp'])  # CAUTION: Use eval carefully
                request.session['tempExp'] = str(result)
            except Exception as e:
                result = str(e)
        #Decimal point handling
        elif(expression == '.'):
            if(request.session['tempExp'][-1] not in "+-*/."):
                request.session['tempExp'] += expression 
            result = request.session['tempExp']   

        else:
            #Clear base 0
            if(len(request.session['tempExp']) == 1 and request.session['tempExp'][-1] == '0'):
                request.session['tempExp'] = ''

            #UPDATE the tempExp value 
            request.session['tempExp'] = request.session['tempExp'] + expression
            result = request.session['tempExp']
            #DEBUGGING 
            print(request.session['tempExp'])
        
    return render(request, 'index.html', {'result': result })