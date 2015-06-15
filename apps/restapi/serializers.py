from django.contrib.auth.models import User
from apps.main import models
from rest_framework import serializers

class TaskSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = models.Task
		fields = (
			'user_create',
			'task_type',
			'category',
			'member_type',
			'title',
			'text_content',
			'video_link',
			'members_min',
			'members_max',
			'cost_need',
			'cost_now',
			'min_level',
			'date_start',
			'date_finish',
			'date_add'
		)


class LevelSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = models.Level
		fields = (
			'number',
			'exp',
		)
	
class AchievementSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = models.Achievement
		fields = (
			'uid',
			'title',
			'image',
		)
	
class UserExtSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = models.UserExt
		fields = (
			'user',
			'current_level',
			'current_exp',
			'avatar',
			'achievement_list',
		)
	
class CategorySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = models.Category
		fields = (
			'title',
		)
	
class CategoryUserLevelSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = models.CategoryUserLevel
		fields = (
			'user',
			'category',
			'current_level',
			'current_exp',
		)
	
class TaskTypeSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = models.TaskType
		fields = (
			'title',
			'cost',
			'color',
		)
	
class CommentSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = models.Comment
		fields = (
			'user',
			'task',
			'title',
			'content',
			'image',
		)
	
class ProgressSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = models.Progress
		fields = (
			'task',
			'percent',
			'message',
		)
	
class ProgressImageSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = models.ProgressImage
		fields = (
			'progress',
			'image',
		)
	
class TaskImageSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = models.TaskImage
		fields = (
			'task',
			'image',
		)
	
class TaskUserSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = models.TaskUser
		fields = (
			'user',
			'task',
			'is_approve',
		)
	
class NewsSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = models.News
		fields = (
			'title',
			'content',
			'image',
			'date_add',
		)
	

class LogSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = models.Log
		fields = (
			'user',
			'message',
			'date_add',
		)

class UserSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = User
		fields = (
			'id',
			'username',
			'email',
		)