#encoding:utf-8
from django.contrib.auth.decorators import login_required
#from django.http import HttpResponse
from utils.decorators import render_to
from models import *
from django.db.models import Q
#from django.core.context_processors import csrf
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
#
from datetime import datetime 
import json
#from dateutil import parser

@login_required
@render_to('profile.html')
def profile(request, user_id=0):
    if user_id == 0:
        user_id = request.user.id

    u = User.objects.get(id=user_id)
    u.ue_u.reload_level()
    u.ue_u.save()

    res = {'active_page': 'journal', 'user': User.objects.get(id=user_id), 'categories': Category.objects.all(),
           'log': Log.objects.filter(user=request.user).all() }
    return res


def addtask(request):
    task = Task()

    task.user_create = request.user
    task.task_type = TaskType.objects.get(id = request.POST.get('type'))
    task.category = Category.objects.get(id = request.POST.get('category'))
    task.member_type = request.POST.get('member_type')

    if request.POST.get('title'):
        task.title = request.POST.get('title')
    else:
        task.title = 'title'

    if request.POST.get('text_content'):
        task.text_content = request.POST.get('text_content')
    else:
        task.text_content = 'text_content'

    if request.POST.get('video_link'):
        task.video_link = request.POST.get('video_link')
    else:
        task.video_link = ''

    if request.POST.get('members_min'):
        task.members_min = request.POST.get('members_min')
        if task.members_min < 1:
            task.members_min = 1
    else:
        task.members_min = 1

    if request.POST.get('members_max'):
        task.members_max = request.POST.get('members_max')
    else:
        task.members_max = task.members_min

    if request.POST.get('cost_need'):
        task.cost_need = request.POST.get('cost_need')
    else:
        task.cost_need = 0
    task.cost_now = 0

    if request.POST.get('min_level'):
        task.min_level = request.POST.get('min_level')
    else:
        task.min_level = 1

    if request.POST.get('date_start'):
        task.date_start = request.POST.get('date_start')
    else:
        task.date_start = datetime.now

    if request.POST.get('date_finish'):
        task.date_finish = request.POST.get('date_finish')
    else:
        task.date_finish = datetime.now

    # import ipdb; ipdb.set_trace();

    if request.POST.get('geojson'):
        task.geojson = request.POST.get('geojson')
        print task.geojson
    else:
        task.geojson = ''

    task.save()

    if request.FILES.getlist('images'):
        images = request.FILES.getlist('images')
        for i in images:
            img = TaskImage()
            img.task = task
            img.image = i
            img.save()

    l = Log()
    l.user = request.user
    l.message = l.task_create(task)
    l.save()

    l = Log()
    l.user = request.user
    l.message = l.add_exp(30)
    l.save()

    u = User.objects.get(id=request.user.id)
    u.ue_u.current_exp = u.ue_u.current_exp + 30
    u.ue_u.save()
    try:
        cul = CategoryUserLevel.objects.filter(category_id=request.POST.get('category'), user=request.user).all()[0]
        cul.current_exp = cul.current_exp + 30
        cul.save()
    except:
        pass

    if len(u.t_uc.all())==1:
        u.ue_u.achievement_list.add(Achievement.objects.get(id=2))
        u.save()
        u.ue_u.current_exp = u.ue_u.current_exp + 100
        u.ue_u.save()
        l = Log()
        l.user = u
        l.message = l.achievement_get(2)
        l.save()
    if len(u.t_uc.all())==3:
        u.ue_u.achievement_list.add(Achievement.objects.get(id=3))
        u.save()
        u.ue_u.current_exp = u.ue_u.current_exp + 100
        u.ue_u.save()
        l = Log()
        l.user = u
        l.message = l.achievement_get(3)
        l.save()
    if len(u.t_uc.all())==5:
        u.ue_u.achievement_list.add(Achievement.objects.get(id=4))
        u.save()
        u.ue_u.current_exp = u.ue_u.current_exp + 100
        u.ue_u.save()
        l = Log()
        l.user = u
        l.message = l.achievement_get(4)
        l.save()
    if len(u.t_uc.all())==10:
        u.ue_u.achievement_list.add(Achievement.objects.get(id=5))
        u.save()
        u.ue_u.current_exp = u.ue_u.current_exp + 100
        u.ue_u.save()
        l = Log()
        l.user = u
        l.message = l.achievement_get(5)
        l.save()
    if len(u.t_uc.all())==100:
        u.ue_u.achievement_list.add(Achievement.objects.get(id=6))
        u.save()
        u.ue_u.current_exp = u.ue_u.current_exp + 100
        u.ue_u.save()
        l = Log()
        l.user = u
        l.message = l.achievement_get(6)
        l.save()

    return HttpResponseRedirect('/tasks/')


def addcomment(request, task_id):
    comment = Comment()
    comment.user = request.user
    comment.task = Task.objects.get(id=task_id)
    if request.POST.get('title'):
        comment.title = request.POST.get('title')
    else:
        comment.title = ''

    if request.POST.get('content'):
        comment.content = request.POST.get('content')
    else:
        comment.content = ''

    if request.POST.get('image'):
        comment.image = request.POST.get('image')
    comment.save()

    l = Log()
    l.user = request.user
    l.message = l.comment(comment, 5)
    l.save()

    u = User.objects.get(id=request.user.id)
    u.ue_u.current_exp = u.ue_u.current_exp + 300
    u.ue_u.save()

    return HttpResponseRedirect('/task/' + task_id)


@login_required
@render_to('tasks.html')
def tasks(request, action=''):
    if action == '':
        return HttpResponseRedirect('/tasks/last/')
    else:
        tasks = None

        if action == 'my':
            tasks = Task.objects.filter(user_create=request.user)
        elif action == 'all':
            tasks = Task.objects.all()
        elif action == 'last':
            tasks = Task.objects.order_by('-date_add').all()[:20]
        elif action == 'available':
            tasks = Task.objects.filter(min_level__lte=request.user.ue_u.current_level)
        elif action == 'search':
            search = request.GET.get('s')
            tasks = Task.objects.filter(Q(text_content__icontains=search) | Q(title__icontains=search))
        else:
            tasks = Task.objects.filter(category=Category.objects.get(id=action))

        res = {'active_page': 'tasks', 'tasks': tasks, 'categories': Category.objects.all(), 'active_category': action,
               'search': request.GET.get('s')}
        return res


@login_required
@render_to('task_add.html')
def task_add(request):
    if request.method == "POST":
        return addtask(request)
    else:
        res = {'active_page': 'tasks', 'categories': Category.objects.all(), 'task_rarity': TaskType.objects.all()}
        return res


@login_required
@render_to('map.html')
def map(request, action='all'):
    res = { 'active_page': 'map', 'active_category':action, 'categories': Category.objects.all() }
    return res


@login_required
@render_to('task.html')
def task(request, task_id=0):#ADDED
    res = {'active_page': 'tasks', 'categories': Category.objects.all(), 'task': Task.objects.get(id=task_id),
           'progresses': Progress.objects.filter(task=Task.objects.get(id=task_id)).all() }
    return res


@login_required
@render_to('news.html')
def news(request, task_id=0):
    res = {'active_page': 'news', 'news': News.objects.all()}
    return res


@login_required
@render_to('statistic.html')
def statistic(request, task_id=0):
    top = UserExt.objects.order_by('current_level')[:10]
    res = { 'active_page': 'statistic', 'top':top}
    return res

#ADDED
@login_required
def add_percent(request, task_id=0):
    res = {'active_page': 'tasks', 'categories': Category.objects.all(), 'task_rarity': TaskType.objects.all()}
    p = Progress()
    p.task = Task.objects.get(id=task_id)
    p.percent = request.POST.get('percent')
    p.message = request.POST.get('message')
    p.save()

    l = Log()
    l.user = request.user
    l.message = l.progress_add(p)
    l.save()

    if request.FILES.getlist('images'):
        images = request.FILES.getlist('images')
        for i in images:
            print 'asdasds',i
            pi = ProgressImage()
            pi.image = i
            pi.progress = p
            pi.save()
    return HttpResponseRedirect('/task/' + task_id)