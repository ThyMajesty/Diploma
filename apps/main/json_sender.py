import json

from django.http import HttpResponse
from models import *
#from models import Task

def send_all_geo_points(request, action='all'):
    tasks = None

    if action == 'my':
        tasks = Task.objects.filter(user_create=request.user)
    elif action == 'all':
        tasks = Task.objects.all()
    elif action == 'last':
        tasks = Task.objects.order_by('date_add').all()[:20]
    elif action == 'available':
        tasks = Task.objects.filter(min_level__lte=request.user.ue_u.current_level)
    else:
        tasks = Task.objects.filter(category=Category.objects.get(id=action))

    response_data = {}
    response_data['type'] = 'FeatureCollection'
    response_data['features'] = []
    for task in tasks:
        try:
            if task.geojson and not task.geojson == '':
                properties = {}
                properties['title'] = task.title
                properties['description'] = task.text_content
                properties['category'] = task.category.title
                geometry = json.loads(task.geojson.replace("u'", "\"").replace("': ", "\":").replace("'", "\""))
                geometry['type'] = 'Point'
                obj = {'properties': properties, 'geometry': geometry, 'type': 'Feature'}
                response_data['features'].append(obj)
        except:
            print "geo: " + task.geojson.replace("u'", "'")

    return HttpResponse(json.dumps(response_data), content_type="application/json")