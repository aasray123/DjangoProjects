from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import ChatmessageCreateForm
from .forms import *

# Create your views here.
@login_required
def chat_view(request):
    chat_group = get_object_or_404(ChatGroup, group_name="public-chat")
    chat_messages = chat_group.chat_messages.all()[:30]
    form = ChatmessageCreateForm()

    if request.htmx:
        form = ChatmessageCreateForm(request.POST)
        if form.is_valid: 
            
            #Need to add user info so dont commit auto
            message = form.save(commit=False)
            
            if (message.body == "Clear"):
                GroupMessage.objects.filter(author = request.user).delete()
                
                # records.save()
            
            #Adding user info
            message.author = request.user
            message.group = chat_group
            
            #Commiting
            message.save()
            context = {
                'message' : message,
                'user' : request.user,
                

            }
            return render(request, 'a_rtchat/partials/chat_message_p.html', context)

    return render(request, 'a_rtchat/chat.html', {'chat_messages' : chat_messages, 'form' : form})
