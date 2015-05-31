__author__ = 'Detonavomek'
#-*- coding: utf-8 -*-

import json
from django.template import RequestContext
from django.http import HttpResponse
from django.shortcuts import render_to_response


def render_to(template_path, allow_ajax=False):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            output = func(request, *args, **kwargs)
            if not isinstance(output, dict):
                return output
            kwargs = {'context_instance': RequestContext(request)}

            if allow_ajax and request.is_ajax():
                return HttpResponse(json.dumps(output), 'application/json')

            if 'MIME_TYPE' in output:
                kwargs['mimetype'] = output.pop('MIME_TYPE')
            template = template_path
            if 'TEMPLATE' in output:
                template = output.pop('TEMPLATE')
            return render_to_response(template, output, **kwargs)
        return wrapper
    return decorator