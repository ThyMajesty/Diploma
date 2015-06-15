from django.contrib.auth.models import User
from apps.main import models
from rest_framework import viewsets
from rest_framework import routers
import serializers

class TaskViewSet(viewsets.ModelViewSet):
    queryset = models.Task.objects.all()
    serializer_class = serializers.TaskSerializer

class LevelViewSet(viewsets.ModelViewSet):
	queryset = models.Level.objects.all()
	serializer_class = serializers.LevelSerializer

class AchievementViewSet(viewsets.ModelViewSet):
	queryset = models.Achievement.objects.all()
	serializer_class = serializers.AchievementSerializer

class UserExtViewSet(viewsets.ModelViewSet):
	queryset = models.UserExt.objects.all()
	serializer_class = serializers.UserExtSerializer

class CategoryViewSet(viewsets.ModelViewSet):
	queryset = models.Category.objects.all()
	serializer_class = serializers.CategorySerializer

class CategoryUserLevelViewSet(viewsets.ModelViewSet):
	queryset = models.CategoryUserLevel.objects.all()
	serializer_class = serializers.CategoryUserLevelSerializer

class TaskTypeViewSet(viewsets.ModelViewSet):
	queryset = models.TaskType.objects.all()
	serializer_class = serializers.TaskTypeSerializer

class CommentViewSet(viewsets.ModelViewSet):
	queryset = models.Comment.objects.all()
	serializer_class = serializers.CommentSerializer

class ProgressViewSet(viewsets.ModelViewSet):
	queryset = models.Progress.objects.all()
	serializer_class = serializers.ProgressSerializer

class ProgressImageViewSet(viewsets.ModelViewSet):
	queryset = models.ProgressImage.objects.all()
	serializer_class = serializers.ProgressImageSerializer

class TaskImageViewSet(viewsets.ModelViewSet):
	queryset = models.TaskImage.objects.all()
	serializer_class = serializers.TaskImageSerializer

class TaskUserViewSet(viewsets.ModelViewSet):
	queryset = models.TaskUser.objects.all()
	serializer_class = serializers.TaskUserSerializer

class NewsViewSet(viewsets.ModelViewSet):
	queryset = models.News.objects.all()
	serializer_class = serializers.NewsSerializer

class LogViewSet(viewsets.ModelViewSet):
	queryset = models.Log.objects.all()
	serializer_class = serializers.LogSerializer

class UserViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all()
	serializer_class = serializers.UserSerializer


router = routers.DefaultRouter()
router.register(r'task', TaskViewSet)
router.register(r'level', LevelViewSet)
router.register(r'achievement', AchievementViewSet)
router.register(r'userext', UserExtViewSet)
router.register(r'category', CategoryViewSet)
router.register(r'categoryuserlevel', CategoryUserLevelViewSet)
router.register(r'tasktype', TaskTypeViewSet)
router.register(r'comment', CommentViewSet)
router.register(r'progress', ProgressViewSet)
router.register(r'progressimage', ProgressImageViewSet)
router.register(r'taskimage', TaskImageViewSet)
router.register(r'taskuser', TaskUserViewSet)
router.register(r'news', NewsViewSet)
router.register(r'log', LogViewSet)
router.register(r'user', UserViewSet)