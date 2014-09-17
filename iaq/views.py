#coding=utf-8
# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from datetime import datetime, timedelta
from django.utils import simplejson
from matplotlib.dates import DateFormatter
from RESTful.rest import RESTfulResource
from iaq.models import SensorData, SensorNode

import os.path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

zh_font = FontProperties(fname=os.path.abspath('wqy-microhei.ttf'))

class Home(RESTfulResource):
    '''首页'''
    def do_get(self, request, *args, **kwargs):
        return render_to_response('index.html')

class History(RESTfulResource):
    '''历史数据'''
    def do_get(self, request, *args, **kwargs):
        node_id = request.GET.get('node_id', '')
        return render_to_response('histories.html', {'node_id': node_id})
    
class Data(RESTfulResource):
    '''数据页'''
    def do_get(self, request, *args, **kwargs):
        return render_to_response('data.html')
    
class Nodes(RESTfulResource):
    '''设备页'''
    def do_get(self, request, *args, **kwargs):
        return render_to_response('nodes.html')
    
class Team(RESTfulResource):
    '''团队页'''
    def do_get(self, request, *args, **kwargs):
        return render_to_response('team.html')

class NodesList(RESTfulResource):
    '''设备列表'''
    def do_get(self, request, *args, **kwargs):
        rows = SensorNode.objects.all()
        array_list = []
        for row in rows:
            t = {'id': row.id, 'node_id': row.node_id, 'description': row.description}
            array_list.append(t)

        return HttpResponse(simplejson.dumps({'nodes':array_list}, ensure_ascii=False))

    def do_post(self, request, *args, **kwargs):
        nid = request.POST.get('node_id', '')
        if not nid.isalnum():
            return HttpResponse(simplejson.dumps({'errormsg': u'无效的设备'}, ensure_ascii=False), status=400)
        try:
            SensorNode.objects.get(node_id=nid)
        except SensorNode.DoesNotExist:
            node = SensorNode()
            node.node_id = nid
            node.description = request.POST.get('description', '')
            node.save()
            return HttpResponse()
        return HttpResponse(simplejson.dumps({'errormsg': u'设备已存在'}, ensure_ascii=False), status=400)


class NodeMod(RESTfulResource):
    '''设备操作'''
    def do_delete(self, request, *args, **kwargs):
        try:
            node = SensorNode.objects.get(node_id=kwargs['node_id'])
        except SensorNode.DoesNotExist:
            return HttpResponse(simplejson.dumps({'errormsg': u'无效的设备'}, ensure_ascii=False), status=404)

        node.delete()
        return HttpResponse()

    def do_put(self, request, *args, **kwargs):
        try:
            node = SensorNode.objects.get(node_id=kwargs['node_id'])
        except SensorNode.DoesNotExist:
            return HttpResponse(simplejson.dumps({'errormsg': u'无效的设备'}, ensure_ascii=False), status=404)

        try:
            data = simplejson.loads(request.raw_post_data)['node']
            node.description = data['description']
            node.save()
            return  HttpResponse()
        except KeyError:
            return HttpResponse(simplejson.dumps({'errormsg': u'无效的请求'}, ensure_ascii=False), status=400)


class LatestData(RESTfulResource):
    '''查询所有设备最新数据'''
    def do_get(self, request, *args, **kwargs):
        rows = SensorNode.objects.all()
        array_list = []
        for row in rows:
            time = row.time + timedelta(hours=8)
            ctime = datetime.strftime(time, '%F %H:%M:%S')
            t = {'node_id': row.node_id, 'temp': row.temp, 'humi': row.humi, 'iaqengine': row.iaqengine,
                 'tgs2600': row.tgs2600, 'tgs2602': row.tgs2602, 'formaldehyde': row.formaldehyde,'time': ctime}
            array_list.append(t)

        return HttpResponse(simplejson.dumps({'data': array_list}, ensure_ascii=False))


class NodeData(RESTfulResource):
    '''查询单个设备历史数据'''
    def do_get(self, request, *args, **kwargs):
        try:
            SensorNode.objects.get(node_id=kwargs['node_id'])
        except SensorNode.DoesNotExist:
            return HttpResponse(simplejson.dumps({'errormsg': u'无效的设备'}, ensure_ascii=False), status=404)

        n = int(request.GET.get('n', '100'))
        rows = SensorData.objects.filter(node_id=kwargs['node_id'])[0:n]
        array_list = []
        for row in rows:
            time = row.time + timedelta(hours=8)
            ctime = datetime.strftime(time, '%F %H:%M:%S')
            t = {'node_id': row.node_id, 'temp': row.temp, 'humi': row.humi, 'iaqengine': row.iaqengine,
                 'tgs2600': row.tgs2600, 'tgs2602': row.tgs2602, 'formaldehyde': row.formaldehyde, 'time': ctime}
            array_list.append(t)

        return HttpResponse(simplejson.dumps({'data': array_list}, ensure_ascii=False))


class LatestPlot(RESTfulResource):
    '''绘制所有设备最新数据'''
    def do_get(self, request, *args, **kwargs):
        rows = SensorNode.objects.all()
        node_id = []
        temps = []
        humis = []
        VOCs = []
        for row in rows:
            if not row.temp:
                continue
            node_id.append(row.node_id)
            temps.append(row.temp)
            humis.append(row.humi)
            VOCs.append(row.formaldehyde)

        N = len(temps)
        ind = np.arange(N)+0.1  # the x locations for the groups
        width = 0.2             # the width of the bars
        fig = plt.figure()
        ax = fig.add_subplot(111)

        rects1 = ax.bar(ind, temps, width, color='g', alpha=0.5)
        rects2 = ax.bar(ind+width, humis, width, color='b', alpha=0.5)
        rects3 = ax.bar(ind+width+width, VOCs, width, color='r', alpha=0.5)
        #ax.set_ylabel(u'值', fontproperties=zh_font)
        ax.set_title(u'各节点最新数据', fontproperties=zh_font)
        ax.set_xticks(ind+width)
        ax.set_xticklabels(node_id)
        #ax.set_ylim(0, 50)
        ax.legend((rects1[0], rects2[0], rects3[0]), (u'温度', u'湿度', u'CH2O'), prop=zh_font)

        def autolabel(rects):
            for rect in rects:
                height = rect.get_height()
                ax.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%1.2f'%float(height), ha='center', va='bottom')
        autolabel(rects1)
        autolabel(rects2)
        autolabel(rects3)

        response = HttpResponse(mimetype = 'image/png')
        plt.savefig(response, format='png')

        return response


class NodePlot(RESTfulResource):
    '''绘制单个设备历史数据'''
    def do_get(self, request, *args, **kwargs):
        try:
            SensorNode.objects.get(node_id=kwargs['node_id'])
        except SensorNode.DoesNotExist:
            return HttpResponse(simplejson.dumps({'errormsg': u'无效的设备'}, ensure_ascii=False), status=404)

        n = int(request.GET.get('n', '100'))
        rows = SensorData.objects.filter(node_id=kwargs['node_id'])[0:n]
        temp = [t.temp for t in rows]
        humi = [t.humi for t in rows]
        iaq = [t.iaqengine for t in rows]
        tgs00 = [t.tgs2600 for t in rows]
        tgs02 = [t.tgs2602 for t in rows]
        formaldehyde = [t.formaldehyde for t in rows]
        time = [t.time+timedelta(hours=8) for t in rows]  #时区转换

        #温湿度曲线
        fig = plt.figure()
        ax = fig.add_subplot(311)
        t, = ax.plot(time, temp, 'r.-')
        h, = ax.plot(time, humi, 'b.-')
        ax.set_ylabel(u'温湿度', fontproperties=zh_font)
        ax.legend((t, h), (u'温度', u'湿度'), 'upper right', prop=zh_font)

        #甲醛曲线
        ax = fig.add_subplot(312)
        i, = ax.plot(time, formaldehyde, 'r.-')
        ax.set_ylabel(u'CH2O/ppm', fontproperties=zh_font)
        ax.legend((i, ), (u'CH2O', ), 'upper right', prop=zh_font)

        #传感器读数曲线
        ax = fig.add_subplot(313)
        s1, = ax.plot(time, iaq, 'r.-')
        s2, = ax.plot(time, tgs00, 'b.-')
        s3, = ax.plot(time, tgs02, 'y.-')
        ax.set_ylabel(u'空气传感器/mV', fontproperties=zh_font)
        ax.legend((s1, s2, s3), ('QS-01', 'tgs2600', 'tgs2602'), 'upper right', prop=zh_font)

        ax.xaxis.set_major_formatter(DateFormatter('%H:%M'))
        fig.autofmt_xdate()

        response = HttpResponse(mimetype = 'image/png')
        plt.savefig(response, format='png')

        return response


class UploadData(RESTfulResource):
    '''节点上传数据'''
    def do_post(self, request, *args, **kwargs):
        data = request.POST.get('data', '')
        array = data.split()
        if len(array) != 6:
            return HttpResponse(status=400)

        try:
            node = SensorNode.objects.get(node_id=array[0])
        except SensorNode.DoesNotExist:
            return HttpResponse(status=404)

        sensor = SensorData()
        sensor.node_id = array[0]
        sensor.temp = node.temp = array[1]
        sensor.humi = node.humi = array[2]
        sensor.iaqengine = node.iaqengine = array[3]
        sensor.tgs2600 = node.tgs2600 = array[4]
        sensor.tgs2602 = node.tgs2602 = array[5]
        sensor.time = node.time = datetime.now()
        sensor.save()               # 插入节点最新数据
        node.save()                 # 更新节点最新数据

        return HttpResponse()