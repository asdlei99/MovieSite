from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from ms_main import Main
import chardet
# Create your views here.


@csrf_exempt
def crawl(request):
    if request.method == 'POST':
        secret = '5826f119-c0bc-4ad7-9017-30369eb75b75'
        if request.POST.get('secret') == secret:
            l_content = request.POST.get('content', '')
            l_tag = request.POST.get('tag')
            l_url = request.POST.get('url')
            l_name = request.POST.get('name')
            cate_eng = request.POST.get('cate_eng')
            if all((l_content, l_tag, l_url, l_name, cate_eng)):
                m = Main()
                try:
                    # l_type1 = type(l_content.encode('utf-8'))
                    # l_type2 = chardet.detect(l_content.encode('utf-8'))
                    # return HttpResponse('%s ,%s' % (l_type1, l_type2))
                    m.update(l_tag.encode('utf-8'),
                             l_url,
                             l_name.encode('utf-8'),
                             l_content.encode('utf-8'),
                             cate_eng)
                except Exception as e:
                    return HttpResponse('Exception: %s' % str(e))
                else:
                    return HttpResponse('GOOD')
            else:
                return HttpResponse('BAD')


    
