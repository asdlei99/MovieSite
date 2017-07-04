from django.shortcuts import render_to_response
from packages.general import loginInfo
from django.template.context import RequestContext
# Create your views here.

def topicIndex(request):
    ret = {}
    ret, user_obj = loginInfo(request, ret)
    ret['user_info'] = user_obj
    response = render_to_response('topic/topic_index.html', ret, context_instance=RequestContext(request))
    return response