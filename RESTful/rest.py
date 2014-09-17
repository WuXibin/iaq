# coding=utf-8
"""定义RESTful相关的类、接口"""
from django.http import HttpResponseNotAllowed

class RESTfulResource(object):
    """定义RESTful资源基类"""
    def __call__(self, request, *args, **kwargs):
        # 试图找一个处理方法
        print self.__class__
        try:
            callback = getattr(self, 'do_%s' % request.method.lower())
        except AttributeError:
            # 本类不支持该HTTP方法
            #  返回405响应
            #  列出本类支持的HTTP方法
            allowed_methods = [m.lstrip('do_') for m in dir(self) if m.startswith('do_')]
            return HttpResponseNotAllowed(allowed_methods)

        # 找到调用的方法
        return callback(request, *args, **kwargs)