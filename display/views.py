import os
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
import simplejson
from fileviewer.fileRead import handle_uploaded_file
from fileToJson import displayfile
from models import DataFile, MetaData
from django import forms
class ViewFileForm(forms.Form):
    md5 = forms.CharField(max_length = 32)
class UploadFileForm(forms.Form):
    file = forms.FileField()
class DeleteFileForm(forms.Form):
    md5 = forms.CharField(max_length = 32)
def json_file_display(request, md5):
    all_objects = displayfile('db/' + md5 + '.file')
    data = simplejson.dumps(all_objects)
    return HttpResponse(data)
def json_all_files(request):
    files = DataFile.objects.all()
    variables = [['File Name','md5']]
    maxv = []
    minv = []
    for f in files:
        metadata = f.metadata_set.all()
        a = ['N/A'] * len(variables[0])
        for m in metadata:
            if m.field in variables[0]:
                pass
            else:
                variables[0].append(m.field)
                a.append('N/A')
            a[variables[0].index(m.field)] = str(m.low) + ',' + str(m.high)
            maxv.extend(['N/A']*(len(variables[0]) - len(maxv)))
            minv.extend(['N/A']*(len(variables[0]) - len(minv)))
            if maxv[variables[0].index(m.field)] == 'N/A': maxv[variables[0].index(m.field)] = m.high
            if minv[variables[0].index(m.field)] == 'N/A': minv[variables[0].index(m.field)] = m.low
            maxv[variables[0].index(m.field)] = max(m.high, maxv[variables[0].index(m.field)])
            minv[variables[0].index(m.field)] = min(m.low, minv[variables[0].index(m.field)])
            a[0] = f.name
            a[1] = f.md5
        variables.append(a)
    if(len(maxv) >0):
        maxv[0] = 'Max Values'
        minv[0] = 'Min Values'
    else:
        maxv.append('Max Values')
        minv.append('Min Values')
    variables.insert(1,maxv)
    variables.insert(2,minv)
    for row in variables[1:]:
        row.extend(['N/A']*(len(variables[0]) - len(row)))
    return HttpResponse(simplejson.dumps(variables))
def upload_file(request):
    json = {
        'file': {},
        'errors': {},
        'text': {},
        'success': False,
    }
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            print '**********VALID********'
            handle_uploaded_file(request.FILES['file'])
            json['success'] = True
            json['file'] = request.FILES['file'].name
        else:
            print '**********INVALID********'
    else:

        return HttpResponse('Get Outta Here!')
    return HttpResponse(simplejson.dumps(json))
def delete_file(request):
    json = {
        'file': {},
        'errors': {},
        'text': {},
        'success': False,
    }
    if request.method == 'POST':
        form = DeleteFileForm(request.POST, request.FILES)
        if form.is_valid():
            DataFile.objects.get(md5=request.POST['md5']).delete()
            print os.path.join('db', request.POST['md5'])+ '.file'
            os.remove(os.path.join('db', request.POST['md5'])+ '.file')
            json['success'] = True
        else:
            print 'invalid'
    else:
        return HttpResponse('Go Away!')
    return HttpResponse(simplejson.dumps(json))
def view_file(request):
    json = {
        'success': False,
        'text':{},
    }
    if request.method == 'GET':
        form = ViewFileForm(request.GET)
        if form.is_valid():
            return render_to_response('view_file.html',{'params.md5':request.GET['md5']})
            json['success'] = True

    return HttpResponse(simplejson.dumps(json))
