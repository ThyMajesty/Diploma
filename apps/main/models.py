from django.db import models

class Level(models.Model):
    number = models.IntegerField(default=1)
    exp = models.CharField(max_length=255, default='')
    def __unicode__(self):
        return str(self.number)

class Achievement(models.Model):
    uid = models.IntegerField(default=0)
    title = models.CharField(max_length=255,default='')
    image = models.ImageField(upload_to='achiv', default='')
    def __unicode__(self):
        return self.title

class UserExt(models.Model):
    user = models.OneToOneField('auth.User', related_name='ue_u')
    current_level = models.IntegerField(default=1)
    current_exp = models.IntegerField(default=0)
    avatar = models.ImageField(upload_to='avatar', default='avatar/default.jpg')
    achievement_list = models.ManyToManyField('main.Achievement', related_name='u_a', null=True)

    def reload_level(self):
        l = Level.objects.filter(number=self.current_level).all()[0]
        tmp = 100*float(self.current_exp)/float(l.exp)
        if int(tmp) >= 100:
            self.current_level+=1
            self.current_exp = int(self.current_exp) - int(l.exp)
        return 0

    def exp_procent(self):
        l = Level.objects.filter(number=self.current_level).all()[0]
        tmp = 100*float(self.current_exp)/float(l.exp)
        return tmp
    def exp_procent_last(self):
        l = Level.objects.filter(number=self.current_level).all()[0]
        return 100-100*float(self.current_exp)/float(l.exp)

    def __unicode__(self):
        return str(self.user.username)

class Category(models.Model):
    title = models.CharField(max_length=255, default='')
    def __unicode__(self):
        return self.title

class CategoryUserLevel(models.Model):
    user = models.ForeignKey('auth.User', related_name='cul_u')
    category = models.ForeignKey('main.Category', related_name='cul_c')
    current_level = models.IntegerField(default=1)
    current_exp = models.IntegerField(default=0)
    def reload_level(self):
        l = Level.objects.filter(number=self.current_level).all()[0]
        tmp = 100*float(self.current_exp)/float(l.exp)
        if int(tmp) >= 100:
            self.current_level+=1
            self.current_exp = int(self.current_exp) - int(l.exp)
        return 0
    def exp_procent(self):
        l = Level.objects.filter(number=self.current_level).all()[0]
        tmp = 100*float(self.current_exp)/float(l.exp)
        return tmp
    def exp_procent_last(self):
        l = Level.objects.filter(number=self.current_level).all()[0]
        return 100-100*float(self.current_exp)/float(l.exp)
    def __unicode__(self):
        return str(self.user.username)

class TaskType(models.Model):
    title = models.CharField(max_length=255, default='')
    cost = models.IntegerField(default=0)
    color = models.CharField(max_length=255, default='ff0000')
    def __unicode__(self):
        return str(self.title)

class Comment(models.Model):
    user = models.ForeignKey('auth.User', related_name='c_uc')
    task = models.ForeignKey('main.Task', related_name='c_t')
    title = models.CharField(max_length=255, default='')
    content = models.TextField()
    image = models.ImageField(upload_to='comment', default='')
    def __unicode__(self):
        return self.title

class Progress(models.Model):
    task = models.ForeignKey('main.Task', related_name='p_t')
    percent = models.IntegerField(default=1)
    message = models.CharField(max_length=255, default='')
    def perc_red(self):
        return 100-self.percent
    def __unicode__(self):
        return str(self.task.title)+str(self.percent)

class ProgressImage(models.Model):
    progress = models.ForeignKey('main.Progress', related_name='pi_p')
    image = models.ImageField(upload_to='progress', default='')
    def __unicode__(self):
        return str(self.image.url)

class TaskImage(models.Model):
    task = models.ForeignKey('main.Task', related_name='ti_t')
    image = models.ImageField(upload_to='task', default='')
    def __unicode__(self):
        return str(self.task.title)

class Task(models.Model):
    MEMBER_CHOICES = (
        (1, u'Not more'),
        (2, u'Range'),
        (3, u'Unlimit'),
    )
    user_create = models.ForeignKey('auth.User', related_name='t_uc')
    task_type = models.ForeignKey('main.TaskType', related_name='t_tt')
    category = models.ForeignKey('main.Category', related_name='t_c')
    member_type = models.IntegerField(null=True, blank=True, choices=MEMBER_CHOICES)
    title = models.CharField(max_length=255, default='')
    text_content = models.TextField()
    video_link = models.CharField(max_length=255, default='')
    members_min = models.IntegerField(default=1)
    members_max = models.IntegerField(default=0)
    cost_need = models.IntegerField(default=0)
    cost_now = models.IntegerField(default=0)
    min_level = models.IntegerField(default=0)
    date_start = models.DateTimeField(auto_now_add=True)
    date_finish = models.DateTimeField(auto_now_add=True)
    date_add = models.DateTimeField(auto_now_add=True)
    geojson = models.TextField()
    def an(self):
        a,n=0,0
        total = TaskUser.objects.filter(task=self)
        if total:
            n = len(total)
            a = len(total.filter(is_approve=True))
        return a,n
    def members_str(self):
        a,n=self.an()
        return str(a)+'/'+str(n)+'/'+str(self.members_min)
    def pers_a(self):
        a,n=self.an()
        return 100*a/(a+n+self.members_min)
    def pers_n(self):
        a,n=self.an()
        return 100*n/(a+n+self.members_min)
    def pers_m(self):
        a,n=self.an()
        return 100*self.members_min/(a+n+self.members_min)
    def pers_money_done(self):
        if self.cost_need == 0:
            return 100
        return 100*self.cost_now/self.cost_need
    def pers_money_need(self):
        if self.cost_need == 0:
            return 0
        return 100*(self.cost_need-self.cost_now)/self.cost_need
    def comments(self):
        return Comment.objects.filter(task=self)
    def images(self):
        return TaskImage.objects.filter(task=self).all()

    def __unicode__(self):
        return self.title

class TaskUser(models.Model):
    user = models.ForeignKey('auth.User', related_name='tu_u')
    task = models.ForeignKey('main.Task', related_name='tu_t')
    is_approve = models.BooleanField(default=False)
    def __unicode__(self):
        return str(self.task.title)

class News(models.Model):
    title = models.CharField(max_length=255, default='')
    content = models.TextField()
    image = models.ImageField(upload_to='news', default='')
    date_add = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-date_add']
    def __unicode__(self):
        return self.title


class Log(models.Model):
    user = models.ForeignKey('auth.User', related_name='l_u')
    message = models.TextField()
    date_add = models.DateTimeField(auto_now_add=True)
    def task_create(self, task):
        return "Create task: <a href='/task/"+str(task.id)+"/'>"+task.title+"</a>"
    def create_acc(self):
        return "Hello! I just create account =)"
    def comment(self, comment, exp_count):
        return "\""+comment.content+"\", think I about <a href='/task/"+str(comment.task.id)+"/'>"+comment.task.title+"</a>. You earned "+str(exp_count)+" experience!"
    def add_exp(self, exp_count):
        return "Congratulations! You earned "+str(exp_count)+" experience!"
    def progress_add(self, p):
        return "I create <a href='/task/"+str(p.task.id)+"/'>"+p.task.title+"</a> on "+p.percent+"%!"
    def achievement_get(self, a_id):
        a = Achievement.objects.get(id=a_id)
        return "You reached achievement \""+a.title+"\" and 100 experience!"
    class Meta:
        ordering = ['-date_add']
    def __unicode__(self):
        return self.message