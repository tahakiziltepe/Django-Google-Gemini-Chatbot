from django.shortcuts import render, redirect
from online_users.models import OnlineUserActivity
import markdown
from .models import *
from .forms import *
from .utils import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User


def register_page(request):
    form = register_form()
    if request.method == 'POST':
        form = register_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('bot:login')
    context = {'form': form}
    return render(request, 'bot/register.html', context)


def login_page(request):
    form = login_form()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('bot:chat_page')
        else:
            messages.info(request, 'Username or password is incorrect.')

    context = {'form': form}
    return render(request, 'bot/login.html', context)


def logout_page(request):
    logout(request)
    return redirect('bot:login')


@staff_member_required
def online_people(request):
    users = User.objects.all()
    online_people = OnlineUserActivity.get_user_activities()
    return render(request, 'bot/online_people.html', {'online_people': online_people, 'users': users})


@login_required(login_url='bot:login')
def chat_page(request):
    chat_history = ChatHistory.objects.filter(username=request.user.username).order_by('-datetime')
    for row in chat_history:
        md = markdown.Markdown(extensions=["fenced_code", "codehilite"])
        row.message = md.convert(row.message)

    form = send_message()
    data = {'chat_history': chat_history,
            'form': form}
    return render(request, 'bot/chat_page.html', data)


@login_required(login_url='bot:login')
def submit_form(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        messages = []
        if request.user.username != 'admin':
            for chat in Prompt.objects.all().order_by('datetime'):
                if chat.user == '🤖🤖 Bot':
                    messages.append({'role': 'model', 'parts': [chat.message]})
                else:
                    messages.append({'role': 'user', 'parts': [chat.message]})
        for chat in ChatHistory.objects.filter(username=request.user.username).order_by('datetime'):
            if chat.user == '🤖🤖 Bot':
                messages.append({'role': 'model', 'parts': [chat.message]})
            else:
                messages.append({'role': 'user', 'parts': [chat.message]})
        messages.append({'role': 'user', 'parts': [message]})
        obj = ChatHistory(username=request.user.username,
                          user='👩🏻‍💻👨🏻‍💻 '+request.user.username,
                          message=message
                          )
        obj.save()
        bot_yanit = generate_content_bot(messages)
        obj = ChatHistory(username=request.user.username,
                          user='🤖🤖 Bot',
                          message=bot_yanit
                          )
        obj.save()
        return redirect('bot:chat_page')
    return redirect('bot:chat_page')


@login_required(login_url='bot:login')
def clear_chat_history(request):
    ChatHistory.objects.filter(username=request.user.username).delete()
    return redirect('bot:chat_page')


@login_required(login_url='bot:login')
def delete_message_from_db(request, v_id):
    message = ChatHistory.objects.filter(id=v_id)
    message.delete()
    return redirect('bot:chat_page')