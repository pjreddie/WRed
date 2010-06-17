#Script written by Paul Kienzle with some additions by me for retrieving data from the ipeek stream
#Fairly sure you have to be local to use it, but you can see how it is used to send the POST request
#to the server to update live data.

import sys
import os
import logging
import urllib
from xpeek import XPeek
import subprocess as sub
import urllib2, urllib2_file
# KEYFILE is the file containing the private key needed to copy data from
# the instrument computer; you need to copy the corresponding public key to
# the instrument computer and append it to the ssh authorized_keys file,
# making sure that it is not publicly readable.  E.g.,
#     cat webred_access.pub >> ~/.ssh/authorized_keys
#     chmod go-a ~/.ssh/authorized_keys
#KEYFILE="~/.ssh/webred_access"
INSTRUMENT_KEY="~/.ssh/livedatakey"
INSTRUMENT_COMPUTER="bt7@bach.ncnr.nist.gov"
INSTRUMENT = "BT7"
UPDATEURL="http://localhost:8000/fileviewer/files/forms/upload/live/"
PROPOSAL="http://www-i.ncnr.nist.gov/schedule"

def instrument_command(cmd):
    cmd = 'ssh -i %s %s %s'%(INSTRUMENT_KEY, INSTRUMENT_COMPUTER, cmd)
    p = sub.Popen(cmd, stdout=sub.PIPE, stderr=sub.PIPE, shell=True)
    output, errors = p.communicate()
    print cmd, "->", output
    return output.strip()

def instrument_time():
    return instrument_command('date +%s')

def current_proposal():
    """
    Assume current proposal id is the most recent ice data directory.
    """
    #TODO: use proper command to ice server to query state
    return instrument_command('ls /usr/local/ice/usr -t | head -1')

def copy_data(proposalid, filename):
    path = "/usr/local/ice/usr/%s/data/%s"%(proposalid,filename)
    print "grabbing", path
    #return instrument_command('cat '+path)
    # Fetch a new copy of the file from the server 
    os.system("scp -i %s %s:%s %s"%(INSTRUMENT_KEY, INSTRUMENT_COMPUTER,
                                    path, "/tmp/newdata"))
    print "copied"

def notify(**kwargs):
    """
    RESTful notification to webred using url "notify?par=val&..."
    One parameter must be event name.
    """
    #params = urllib.urlencode(kwargs)
    #fid = urllib.urlopen(UPDATEURL+"?"+params)
    #msg = fid.read()
    #fid.close()
    data = {'filename': kwargs['filename'],
            'file' : open('/tmp/newdata/'+kwargs['filename']),
            'proposalid': kwargs['proposalid'],
           }
    urllib2.urlopen(UPDATEURL, data)

def monitor(instrument):
    START_TIME = float(instrument_time())
    class XPeekFilename(XPeek):
        def newdata(self, lineid):
            #print lineid,"starting",self.data[lineid].filename
            self.proposalid = current_proposal()
            #notify(event='newdata', 
            #       proposalid=self.proposalid, 
            #       filename=self.data[lineid].filename)
        def enddata(self, lineid):
            pass
            #notify(event='enddata',
            #       proposalid=self.proposalid, 
            #       filename=self.data[lineid].filename)
        def newpoint(self, lineid):
            if self.data[lineid].columns['TIMESTAMP'][-1] < START_TIME:
                #print "skipping",self.data[lineid].columns['TIMESTAMP'][-1]
                return
            data = copy_data(self.proposalid,self.data[lineid].filename)
            notify(
                   proposalid=self.proposalid, 
                   filename=self.data[lineid].filename,
                   file=data)
    xpeek = XPeekFilename(instrument)
    xpeek.process_stream()

if __name__ == "__main__":
    logging.basicConfig(level=logging.ERROR)
    #debug_eta(sys.argv[1] if len(sys.argv)>1 else 'NG1')
    monitor(INSTRUMENT)

