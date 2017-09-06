# coding=utf-8


class Warn(Exception):
    pass


class Fatal(Exception):
    pass


class GetHtmlFailed(Warn):
    pass


class Http404(Warn):
    pass


class InvalidHTMLContent(Warn):
    pass


class GetLatestUrlsFailed(Warn):
    pass