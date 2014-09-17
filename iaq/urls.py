#coding=utf-8
from django.conf.urls import patterns, include, url
from views import Home, UploadData, NodesList, NodeMod, LatestData, NodeData, LatestPlot, NodePlot, History, Data, Nodes, Team

urlpatterns = patterns('iaq.views',
    # 首页
    url(r'^$', Home()),
    url(r'^histories.html$', History()),
    url(r'^data.html$', Data()),
    url(r'^nodes.html$', Nodes()),
    url(r'^team.html$', Team()),

    # 设备管理接口
    url(r'^nodes/$', NodesList()),
    url(r'^nodes/(?P<node_id>\d{1,4})/$', NodeMod()),

    # 数据查看接口
    url(r'data/$', LatestData()),
    url(r'^data/(?P<node_id>\d{1,4})/query/$', NodeData()),

    # 绘图接口
    url(r'^plot/$', LatestPlot()),
    url(r'^plot/(?P<node_id>\d{1,4})/query/$', NodePlot()),

    # 节点数据上传接口
    url(r'^upload/$', UploadData()),

    #more to add...
)
