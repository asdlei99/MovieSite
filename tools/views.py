# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from django.shortcuts import HttpResponse, render_to_response, render
from packages.general import loginInfo
import os
from django.template.context import RequestContext
from subprocess import check_output, CalledProcessError

# Create your views here.
SS_PATH = '/etc/shadowsocks.json'


def _get_ss_info():
    with open(SS_PATH) as f:
        content = f.read()
    return json.loads(content)


def _ss_is_running(port):
    return True
    assert isinstance(port, int)
    try:
        check_output('netstat -tnlp | grep "0.0.0.0:%d"' % port)
    except CalledProcessError:
        return False
    return True


def shadowsocks(request):
    ret = {'logined': False, 'ss_running': False}
    ret, user_obj = loginInfo(request, ret)
    ret['user_info'] = user_obj
    obj = _get_ss_info()
    ret['server'] = obj.get('server')
    ret['port'] = obj.get('server_port')
    if _ss_is_running(ret['port']):
        ret['ss_running'] = True
    return render(request, 'tools/shadowsocks.html', ret,)


def see_world(request):
    ret = {'success': False, 'data': {}}
    if request.method == 'POST':
        if request.POST.get('name') == '王懋':
            obj = _get_ss_info()

            ret['success'] = True
            ret['data']['server'] = obj.get('server')
            ret['data']['server_port'] = obj.get('server_port')
            ret['data']['password'] =obj.get('password')
        return HttpResponse(json.dumps(ret))
