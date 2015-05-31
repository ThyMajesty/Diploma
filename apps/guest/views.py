from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, logout as auth_logout, login as auth_login
from django.contrib.auth.models import User
from django.core.context_processors import csrf

from utils.decorators import render_to
from apps.main.models import *
# from apps.main.models import Organization, SystemUser, UserType
from django.http import HttpResponse
import json


def index(request):
    return HttpResponseRedirect('/user/profile/')

@render_to('login.html')
def login(request):
    c = {}
    c.update(csrf(request))
    return c

def auth(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            auth_login(request, user)
            return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('/login/')
    return HttpResponseRedirect('/login/')

def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/login/')

@render_to('register.html')
def register_user(request):
    if request.method == 'POST':
        if not request.POST['username']  or not request.POST['password'] or (0 < len(User.objects.filter(username=str(request.POST['username'])))):
            pass
        else:
            username = request.POST['username']
            password = request.POST['password']
            user = User.objects.create_user(username, username+'@'+username+'.ff', password)
            user.save()
            ue = UserExt()
            ue.user = user
            ue.save()

            user.ue_u.achievement_list.add(Achievement.objects.get(id=1))
            user.save()

            l = Log()
            l.user = user
            l.message = l.create_acc()
            l.save()

            l = Log()
            l.user = user
            l.message = l.achievement_get(1)
            l.save()


            user.ue_u.current_exp = user.ue_u.current_exp + 100
            user.ue_u.save()

            cs = Category.objects.all()
            for c in cs:
                cul = CategoryUserLevel()
                cul.user = user
                cul.category = c
                cul.save()

            return HttpResponseRedirect('/login/')
    args={}
    args.update(csrf(request))
    return args