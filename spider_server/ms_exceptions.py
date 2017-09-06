# coding=utf-8
from selenium.common.exceptions import TimeoutException


class Warn(Exception):
    pass


class InvalidHTMLContent(Warn):
    pass


class WebDriverTimeOut(TimeoutException, Warn):
    pass


class Http404(Warn):
    pass

class Fatal(Exception):
    pass


class WebDriverNotSet(Fatal):
    pass


class GetLatestUrlsFailed(Fatal):
    pass