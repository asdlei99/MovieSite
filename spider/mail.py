# coding=utf-8
from django.core.mail import EmailMultiAlternatives
import datetime
"""
Not finish yet
"""


class Mail(object):
    def __init__(self):
        pass

    def send(self, operations, email):
        """

        :param operations: [{'type': op_type, 'state': state, 'l_url':l_url, 'l_name': l_name,
                'cate_eng': cate_eng, 'cate_chn': cate_chn}, ...]
                op_type: add/update
                state: 成功/失败
        :param email:
        :return:
        """
        subject = '%s Update Report' % datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        text_content = 'content here'

        # content
        movie_list = []
        tv_list = []
        anime_list = []
        show_list = []
        for op in operations:
            if op.get('cate_eng') == 'movie':
                movie_list.append(op)
            elif op.get('cate_eng') == 'tv':
                tv_list.append(op)
            elif op.get('cate_eng') == 'anime':
                anime_list.append(op)
            elif op.get('cate_eng') == 'show':
                show_list.append(op)
        content = ''
        for item in (movie_list, tv_list, anime_list, show_list):
            for op in item:
                op.get('')
        content = ''.encode(
            'utf8')
        html_content = open(
            BASE_DIR + '/templates/userinfo/mail/general_mail.html').read() \
            .replace('subject_default', subject).replace('content_default',
                                                         content).replace(
            'link_default', '')

        from_email = '比格电影 <no-reply@bigedianying.com>'
        # from_email = 'bigedianying@gmail.com'
        msg = EmailMultiAlternatives(subject, text_content, from_email, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()