from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
import simplejson

def xhr(request):
    """
    handle an XMLHttpRequest
    """
    # see what message has been sent
    # print "POSTDATA: ", request.POST['message']
    message = unicode('hey')
    
    proxy = xmlrpclib.ServerProxy("http://localhost:8045")
    #proxy = xmlrpclib.ServerProxy("http://localhost:61613")
    print("transmitting")
    try:
      proxy.transmit('/topic/shouts', message)
    except:
      print "transmission failed"
    print "transmitted"
    return HttpResponse("OK")
