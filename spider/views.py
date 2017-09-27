from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from ms_main import Main
import chardet
# Create your views here.

SECRET = '5826f119-c0bc-4ad7-9017-30369eb75b75'


@csrf_exempt
def crawl(request):
    if request.method == 'POST':
        if request.POST.get('secret') == SECRET:
            MAIN = Main()
            l_content = request.POST.get('content', '') # acquire
            l_tag = request.POST.get('tag', '')
            l_url = request.POST.get('url', '')
            l_name = request.POST.get('name', '')
            cate_eng = request.POST.get('cate_eng', '')
            d_url = request.POST.get('d_url', None)
            if not d_url:
                if all((l_content, l_tag, l_name, cate_eng)):
                    try:
                        MAIN.update(l_tag.encode('utf-8'),
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
            else:
                if cate_eng:
                    # manually
                    # l_url may be ''
                    try:
                        MAIN.update(l_tag,
                                    l_url,
                                    l_name,
                                    l_content,
                                    cate_eng,
                                    d_url=d_url)
                    except Exception as e:
                        return HttpResponse('Exception: %s' % str(e))
                    else:
                        return HttpResponse('GOOD')
                else:
                    return HttpResponse('BAD')
