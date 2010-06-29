#Author: Joe Redmon
#views.py

import os
from multiprocessing import Queue
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
import simplejson
from django.contrib import auth
from django.contrib.auth.decorators import login_required

from WRed.fileRead import *
from WRed.fitting import *
from fileToJson import displayfile
from WRed.display.models import *
from django import forms


class ViewFileForm(forms.Form):
    md5 = forms.CharField(max_length = 32)
class UploadFileForm(forms.Form):
    file = forms.FileField()
class UploadLiveFileForm(forms.Form):
    file = forms.FileField()
    proposalid = forms.CharField(max_length = 100)
    filename = forms.CharField(max_length = 100)
class DeleteFileForm(forms.Form):
    md5 = forms.CharField(max_length = 32)
class WaitForUpdateForm(forms.Form):
    pass
#Handles GET requests for individual files, returns a json object of the data file
@login_required
def json_file_display(request, idNum):
    print 'USERNAME: ',request.user.username
    print 'Authenticated: ', request.user.is_authenticated()
    rFile = DataFile.objects.get(id = idNum)
    if request.user.is_authenticated() and (request.user.username == str(rFile.proposal_id) or request.user.is_superuser):
        print 'Good To Go!'
        data = get_object_or_404(DataFile, id = idNum)
        md5 = data.md5
        all_objects = displayfile('db/' + md5 + '.file')
        data = simplejson.dumps(all_objects)
        return HttpResponse(data)
    else:
        print 'Not authenticated!'
    return HttpResponse('Go Login!')

#Handles GET requests for all file information, returns a json object of the files
@login_required
def json_all_files(request):
    files = DataFile.objects.filter(proposal_id = request.user.username)
    if request.user.is_superuser: files = DataFile.objects.all()
    variables = [['File Name','md5', 'id']]
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
            a[2] = f.id
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
#Handles POST requests to upload static files (cannot be update or changed later)
@login_required
def upload_file(request):
    json = {
        'errors': {},
        'text': {},
        'success': False,
    }
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            print '**********VALID********, User Name:', request.user.username

            handle_uploaded_file(request.FILES['file'], request.user.username)
            json['success'] = True
            json['text'] = {'file':request.FILES['file'].name}
        else:
            print '**********INVALID********'
    else:

        return HttpResponse('Get Outta Here!')
    return HttpResponse(simplejson.dumps(json))
#Handles POST requests to upload live files (files that may be updated or changed later)
def upload_file_live(request):
    print "Live Data Request"
    json = {
        'errors': {},
        'text': {},
        'success': False,
    }
    if request.method == 'POST':
        print "Live Data Post Request"
        form = UploadLiveFileForm(request.POST, request.FILES)
        if form.is_valid():
            print '**********Live Data:VALID********'
            handle_uploaded_live_file(request.FILES['file'], request.POST['filename'], request.POST['proposalid'])
            json['success'] = True
            json['text'] = {'file':request.FILES['file'].name}
        else:
            print '**********INVALID********'
    else:

        return HttpResponse('Get Outta Here!')
    return HttpResponse(simplejson.dumps(json))
#handles POST requests to delete files from the database
@login_required
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
@login_required
def all_files(request):
    return render_to_response('all_files.html')
@login_required
def view_file(request, idNum):
    return render_to_response('view_file.html', {'id': idNum})
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        print 'Proposal ID: ', username, 'Tag: ', password
        user = auth.authenticate(username = username, password = password)
        if user is not None and user.is_active:
            print '********LOGIN SUCCESSFUL*********'
            auth.login(request, user)
            return HttpResponseRedirect('/WRed/files/all/')
        else:
            return HttpResponse('Go Away!')
    elif request.method == 'GET':
        return render_to_response('registration/login.html')
def logout_view(request):
    auth.logout(request)
    return HttpResponseRedirect('/accounts/login')
