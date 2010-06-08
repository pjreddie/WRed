
#Buffers.py
#!/usr/bin/env python
"""Instrument state description
    Also useful for the status client
"""
__author__  = "M.Doucet UMd/NIST <doucet@nist.gov>"
__date__    = "June, 2003"
__version__ = "$Id: Buffers.py 1738 2008-04-24 20:37:20Z mimartin $"

#import string, sys, copy, math, time
from LogFile import *
from PresetDeviceProperties import *

ScanNone     = 0
ScanEnergy   = 1 
ScanQ        = 2
ScanAngle    = 5
ScanFindPeak = 6
ScanSeries   = 7
FreeForm     = 8
Bragg        = 9

MAX_LIST_LEN = 5000

BUFFERDEBUG = 0

class ScanDescription:
    """Scan description class"""
                
    def __init__(self, desc='',geo=None):
         
        # Geometry description; default is Triple Axis geometry
        self.geometry = geo
        if self.geometry==None:
            LogAndRaise("Error","ScanDescription.init: no geometry given")

        # Description string
        #@todo: Add code to parse a passed in scan description.
        self.description = "None"

        # Scan status
        #self.currentPoint          = 0
        self.currentPoint          = -1
        self.estimatedTimePerPoint = 0
        self.inScan                = 0

        # Debug info
        self.debug = 1
        
        # Scan type:  0 = None
        #             1 = Energy
        #             2 = Q
        #             5 = Angle
        #             6 = FindPeak
        #             7 = Series of scans
        #             8 = Free-form scan
        #             9 = Bragg buffer
        self.type        = 0

        # Fixed energy type:  0=init 1=final
        self.fixedType   = -1

        # Fixed energy value
        self.fixedE      = 0

        # Count prefactor
        self.prefac      = 1

        # Count type: should be the name of a valid counter
        # Can count for time, neutrons, or detector counts
        self.countType   = ''

        # Number of counts
        self.counts      = [0]

        # Detector type (ex.: area, linear)
        self.detectorType= ''

        # Preset channel number
        self.presetChannel = 0

        # Description
        self.title       = "Empty"

        # List of angles
        self.angleList   = {}

        # List of constant devices
        self.constDevicesList   = {}

        # List of energy transfers
        self.eList       = []

        # Q list
        self.qList       = []

        # String describing the last decoded scan
        self.strOut      = ''

        # List of timers, counters and detectors to start before counting
        self.startList   = []

        # Comment
        self.comment     = ''

        # HoldScan: before the start of the scan [sec]
        self.holdScan    = 0

        # HoldPoint: before each point [sec]
        self.holdPoint   = 0

        # HoldEnv: hold after setting environment controller [sec]
        self.holdEnv     = 0

        # Timeout when counting
        self.timeout     = 0

        # Timeout device
        self.timeoutDevice = ''

        # Additional parameters
        self.additional  = []

        # Number of points
        self.numPoints=0

        # Device scan ranges  
        self.scanRange={}

        # Number of points for 2nd scan dimension
        self.numPoints2=0

        # Device scan ranges for 2nd scan dimension
        self.scanRange2={}

        # Device position list for 2nd scan dimension
        self.secondDev={}

        # Placeholder for file name
        self.filename=''
        
        #:Stores information about all device's whose properties must be preset before the scan is run
        self.presetDevicesProperties = PresetDevicesProperties("",None)
        
        
    def __str__(self):
        """Overloads the print operator"""
        out =  "Title            = %s\n" % self.title
        out += "Type             = %i" % self.type
        
        # If this is a scan series, we have enough info
        if self.type==ScanSeries: return out
        
        out += "Comment          = %s\n" % self.comment
        if not self.holdScan==0:
            out += "Hold-Scan        = %f sec\n" % self.holdScan
        if not self.holdPoint==0:
            out += "Hold-Point       = %f sec\n" % self.holdPoint
        if not self.holdEnv==0:
            out += "Hold-Env         = %f sec\n" % self.holdEnv
        if self.fixedType==0:
            out += "Fixed              E_init\n"
        elif self.fixedType==1:
            out += "Fixed              E_final\n"
        out += "Fixed energy     = %f meV\n" % self.fixedE
        if not self.prefac==1:
            out += "Prefac           = %g\n" % self.prefac
        if self.detectorType=='':
            out += "Detector         = Default\n"
        else:
            out += "Detector         = %s\n" % self.detectorType
        if self.countType=='':
            out += "Counter          = Default\n"
        else:
            out += "Counter          = %s\n" % self.countType
        out += "Number of counts = %s\n" % self.counts
        if self.presetChannel>0:
            out += "PresetChannel    = %i\n" % self.presetChannel
        if self.timeout>0:
            out += "Timeout          = %i sec\n" % self.timeout
            out += "Timeout device   = %s\n" % self.timeoutDevice
        out += "E                = %s\n" % self.eList
        out += "Q                = %s\n" % self.qList
        if len(self.angleList)>0:
            for i in self.angleList:
                out += "Angles           = %s = %s\n" % (i, string.join(self.angleList[i]))
        if len(self.startList)>0:
            out += "Counting devices = %s\n" % string.join(self.startList)
        out += "Filename         = %s\n" % self.filename
        return out
    
    def version(self):
        version=string.split(__version__)
        return version[2]
    
    def presetDeviceProperties(self):
        self.presetDevicesProperties.preset()
        
    def getToken(self, token):
        # Find the value of an additional token in the
        # scan description.
        if len(self.additional)>0:
            for i in range(len(self.additional)):
                if str(self.additional[i][0]).upper()==str(token).upper():
                    return self.additional[i][1]
        return None
    
    def getMoving(self):
        # List of all moving devices. Remove those that are constant
        # First dimension
        l1 = self.angleList.keys()
        toremove = []
        for k in l1:
            if len(self.angleList[k])==1: toremove.append(k)
        for k in toremove: l1.remove(k)
        
        # Second dimension
        l2 = self.secondDev.keys()        
        toremove = []
        for k in l2:
            if len(self.secondDev[k])==1: toremove.append(k)
            if k in l1: toremove.append(k)
        for k in toremove: l2.remove(k)
        if len(l2)>0: l1.extend(l2)
            
        # Q and E
        if len(self.eList)>1 or len(self.qList)>1:
            labels = self.geometry.getAllDevices()
            toremove = []
            for k in labels:
                if k in l1: toremove.append(k)
            for k in toremove: labels.remove(k)
            if len(labels)>0:l1.extend(labels)
                
        return l1
    
    def scanListInfo(self, desc):
        # Get information for scan list
        self.decode(desc,0)
        npts = self.getNumPoints()
        if self.numPoints2>0:  
            return "Npts=%dx%d %s=%s" % (int(npts/self.numPoints2), self.numPoints2, self.countType, str(self.counts))
        return "Npts=%d  %s=%s" % (npts, self.countType, str(self.counts))
    
    def getNumPoints(self):
        """Get the number of scan points"""
        npts = 0
        if self.numPoints>0: 
            npts=self.numPoints
            #~ if self.numPoints2>0: npts *= self.numPoints2
        else:
            #Energy scan or Q scan
            if self.type==1 or self.type==2:
                eLen = len(self.eList)
                qLen = len(self.qList)
                npts = 1
                if eLen>1 and (eLen<=qLen or qLen<=1): npts=eLen
                if qLen>1 and (qLen<=eLen or eLen<=1): npts=qLen
                
            #Increment Scan, Find Peak scan, Bragg Buffer
            elif self.type==5 or self.type==6 or self.type==9:
                keys   = self.angleList.keys()
                ntot   = len(keys)
                npts = MAX_LIST_LEN
                if ntot > 0:
                    for i in range(ntot):
                        length = len(self.angleList[keys[i]])
                        if length<npts and not length==1:
                            npts=len(self.angleList[keys[i]])
                else: npts=0
                if npts==MAX_LIST_LEN: npts=1
                    
        # Second dimension
        npts2 = 1
        if self.numPoints2>0: 
            npts2=self.numPoints2
        else:
            keys   = self.secondDev.keys()
            ntot   = len(keys)
            npts2 = MAX_LIST_LEN
            if ntot > 0:
                for i in range(ntot):
                    length = len(self.secondDev[keys[i]])
                    if length<npts2 and not length==1:
                        npts2=len(self.secondDev[keys[i]])
            else: npts2=1
            if npts2==MAX_LIST_LEN: npts2=1
            if npts2>1: self.numPoints2 = npts2
                
        return npts*npts2
        #~ return npts
    
    def getTypeString(self): return str(self.type)
        
    def decode(self,desc,tostates=1):
        """
        Decodes a description from a scan description string
        
        @param desc: A string with a scan description following the standard ICE scan description format.
        @type desc: string
        
        @param tostates: Integer flag indicating whether to translate the scan into instrument states.
        @type tostates: Integer
        
        @return: A string describing the results of the function.
        """
        # Keep track of errors
        nError  = 0
        
        # Flag to tell the function to replace or append new parameters
        AddFlag = 0

        self.setPropertyDevices = []
        
        if self.inScan==1:
            print "Cannot change scan while running"
            return "Cannot change scan while running"

        # Split the description
        list = string.split(desc,':')
        if len(list)<1:
            return "Input error"
        if not list[0]=="Scan":
            return "Bad scan description"
        self.description = desc

        # Loop through parameters
        # Should catch errors  (e.g. string to float)
        ntot = len(list)
        if ntot > 0:
            for i in range(1,ntot):
                sublist = string.split(list[i],'=')
                # 'Add' flag
                if sublist[0]=="Add":
                    AddFlag = 1
                    print "Appending lists of points"
                elif sublist[0]=="Replace":
                    AddFlag = 0
                    print "Replacing lists of points"
                # Scan type
                elif sublist[0]=="Type":
                    if   sublist[1]=="ScanEnergy":   self.type=ScanEnergy
                    elif sublist[1]=="ScanQ":        self.type=ScanQ
                    elif sublist[1]=="ScanAngle":    self.type=ScanAngle
                    elif sublist[1]=="ScanFindPeak": self.type=ScanFindPeak
                    elif sublist[1]=="ScanSeries":   self.type=ScanSeries
                    elif sublist[1]=="FreeForm":     self.type=FreeForm
                    elif sublist[1]=="Bragg":        self.type=Bragg
                    else:
                        try:
                            self.type=int(sublist[1])
                        except ValueError:
                            print "ScanDescription: 'Type' not an integer"
                            Logger("Error", "ScanDescription: 'Type' not an integer")
                            nError = nError + 1
                            continue
                # Fixed energy type: 0=initial 1=final
                elif sublist[0]=="Fixed":
                    try:
                        self.fixedType=int(sublist[1])
                    except ValueError:
                        print "ScanDescription: 'Fixed' not an integer"
                        Logger("Error", "ScanDescription: 'Fixed' not an integer")
                        nError = nError + 1
                        continue
                    if not self.fixedType==0 and not self.fixedType==1:
                        print "Bad fixed energy type %s: setting to E_init" % self.fixedType
                        self.fixedType=0
                # Fixed energy value
                elif sublist[0]=="FixedE":
                    try:
                        self.fixedE=float(sublist[1])
                    except ValueError:
                        print "ScanDescription: 'FixedE' not a float"
                        Logger("Error", "ScanDescription: 'FixedE' not a float")
                        nError = nError + 1
                        continue
                # Count prefactor
                elif sublist[0]=="Prefac":
                    try:
                        self.prefac=float(sublist[1])
                    except ValueError:
                        print "ScanDescription: 'Prefac' not a float"
                        Logger("Error", "ScanDescription: 'Prefac' not an integer")
                        nError = nError + 1
                        continue
                # Detector type    
                elif sublist[0]=="DetectorType":
                    self.detectorType=str(sublist[1])
                # Count type    [this should be determined from the Counter selection]
                elif sublist[0]=="CountType":
                    self.countType=str(sublist[1])
                # Number of counts
                elif sublist[0]=="Counts":
                    try:
                        self.counts=[float(sublist[1])]
                    except ValueError:
                        # Try to see if we have a list of counts
                        try: 
                            countItems = string.split(sublist[1])
                            self.counts=[]
                            for icountitem in range(len(countItems)):
                                self.counts.append(float(countItems[icountitem]))
                        except:
                            print "ScanDescription: 'Counts' not an integer"
                            Logger("Error", "ScanDescription: 'Counts' not an integer")
                            nError = nError + 1
                            continue
                # Preset channel
                elif sublist[0]=="PresetChannel":
                    try:
                        self.presetChannel=int(sublist[1])
                    except ValueError:
                        print "ScanDescription: 'PresetChannel' not an integer"
                        Logger("Error", "ScanDescription: 'PresetChannel' not an integer")
                        nError = nError + 1
                        continue
                # Timeout for counter
                elif sublist[0]=="Timeout":
                    try:
                        self.timeoutDevice=sublist[1]
                        self.timeout=int(sublist[2])
                    except ValueError:
                        print "ScanDescription: 'Timeout' not an integer"
                        Logger("Error", "ScanDescription: 'Timeout' not an integer")
                        nError = nError + 1
                        continue
                # Description
                elif sublist[0]=="Title":
                    self.title=string.join(sublist[1:])
                # Angle list
                elif sublist[0]=="Angle" or sublist[0]=="Dev":
                    if not AddFlag==1 or not self.angleList.has_key(sublist[1]):
                        self.angleList[sublist[1]] = []
                    l = string.split(sublist[2])
                    for i in l:
                        try:
                            self.angleList[sublist[1]].append(i)
                        except ValueError:
                            Logger("Error", "ScanDescription: value not a float: "+sublist[1]+"="+i)
                            nError = nError + 1
                # Angle list
                elif sublist[0]=="Angle2" or sublist[0]=="Dev2":
                    if not AddFlag==1 or not self.secondDev.has_key(sublist[1]):
                        self.secondDev[sublist[1]] = []
                    l = string.split(sublist[2])
                    for i in l:
                        try:
                            self.secondDev[sublist[1]].append(i)
                        except ValueError:
                            Logger("Error", "ScanDescription: value not a float: "+sublist[1]+"="+i)
                            nError = nError + 1
                # Energy transfer list
                elif sublist[0]=="E":
                    if not AddFlag==1:
                        self.eList = []
                    l = string.split(sublist[1])
                    for i in l:
                        try:
                            # We keep the list as strings, but we check that
                            # it can be turned into a float.
                            self.eList.append(str(float(i)))
                        except ValueError:
                            Logger("Error", "ScanDescription: E not a float: "+i)
                            nError = nError + 1
                # Q list (this will be replaced by h-k-l)
                elif sublist[0]=="Q":
                    if not AddFlag==1:
                        self.qList = []
                    l = string.split(sublist[1])
                    for i in l:
                        q = string.split(i,'~')
                        if not len(q)==3:
                            Logger("Error", "ScanDescription: bad Q "+str(q))
                            nError = nError + 1
                            continue
                        iError = 0
                        for j in range(3):
                            try:
                                qi = float(q[j])
                            except ValueError:
                                Logger("Error", "ScanDescription: Q(i) not a float: "+str(q))
                                nError = nError + 1
                                iError = 1
                                break
                        if iError==0:
                            self.qList.append(i)
                # Counting devices list
                elif sublist[0]=="StartList":
                    if not AddFlag==1:
                        self.startList = []
                    l = string.split(sublist[1])
                    for i in l:
                        self.startList.append(str(i))
                # This is a holder for comments
                elif sublist[0]=="Comment":
                    self.comment = sublist[1]
                # Holding time before scan
                elif sublist[0]=="HoldScan":
                    try:
                        self.holdScan=float(sublist[1])
                    except ValueError:
                        print "ScanDescription: 'HoldScan' not a float"
                        Logger("Error", "ScanDescription: 'HoldScan' not a float")
                        nError = nError + 1
                        continue
                # Holding time before point
                elif sublist[0]=="HoldPoint":
                    try:
                        self.holdPoint=float(sublist[1])
                    except ValueError:
                        print "ScanDescription: 'HoldPoint' not a float"
                        Logger("Error", "ScanDescription: 'HoldPoint' not a float")
                        nError = nError + 1
                        continue
                # Number of points
                elif sublist[0]=="Npts":
                    try: self.numPoints=int(sublist[1])
                    except:
                        LogAndPrint("Error", "ScanDescription: bad number of points")
                        nError = nError + 1
                        continue
                # Scan ranges
                elif sublist[0]=="Range":
                    try:
                        l = string.split(sublist[2])
                        self.scanRange[sublist[1]]=[l[0], l[1]]
                        print "Range %s: %s %s" % (sublist[1], l[0], l[1])
                        if len(l)>2 and l[2].upper()=="S":
                            self.scanRange[sublist[1]].append("S")
                        elif len(l)>2 and l[2].upper()=="I":
                            self.scanRange[sublist[1]].append("I")
                    except: 
                        LogAndPrint("Error", "ScanDescription: bad scan range")
                        nError = nError + 1
                        continue
                # Number of points for 2nd dimension
                elif sublist[0]=="Npts2":
                    try: self.numPoints2=int(sublist[1])
                    except:
                        LogAndPrint("Error", "ScanDescription: bad number of points for 2nd dimension")
                        nError = nError + 1
                        continue
                # Scan ranges for 2nd dimension
                elif sublist[0]=="Range2":
                    try:
                        l = string.split(sublist[2])
                        self.scanRange2[sublist[1]]=[l[0], l[1]]
                        if len(l)>2 and l[2].upper()=="S":
                            self.scanRange2[sublist[1]].append("S")
                        elif len(l)>2 and l[2].upper()=="I":
                            self.scanRange2[sublist[1]].append("I")
                    except: 
                        LogAndPrint("Error", "ScanDescription: bad scan range for 2nd dimension")
                        nError = nError + 1
                        continue
                # File name
                elif sublist[0]=="Filename":
                    self.filename = sublist[1]

                # Sets a device's properies before running the scan
                elif sublist[0].upper()=="PRESETDEVICESPROPERTIES":
                    self.presetDevicesProperties = PresetDevicesProperties(sublist[1],self.geometry.sequencer)
                # If we made it here, store the value for later use
                else: 
                    if len(sublist[0])>0:
                        if len(sublist)==1: self.additional.append([sublist[0],''])
                        else: self.additional.append([sublist[0],sublist[1]])

        # Skip this if we just want the information
        if tostates==0: return "Scan description parsed"
          
        # Translate the scan description into instrument states, except for scan series
        if not self.type==ScanSeries:
            try:
                self.toInstrStates()
            except:
                raise "Error", "Scan [%s]: State description incomplete\n  %s" % \
                    (self.title,sys.exc_value)
                
            if nError>0:
                return "%i scan description error(s): Check error log" % nError

        return "Scan description parsed"
        
    def getConstDevices(self):
        """ Returns the list of devices that do not vary for the duration of the scan, with their values."""
        eLen = len(self.eList)
        qLen = len(self.qList)
        
        self.constDevicesList = {}
        
        if not (self.type==5 or self.type==6) and eLen==1 and qLen==1:
            # Initial and final energies: Ef = Ei - E
            Einit  = 0
            Efinal = 0
            if self.fixedType==0:
                Einit  = self.fixedE
                Efinal = self.fixedE-float(self.eList[0])
            elif self.fixedType==1:
                Einit  = self.fixedE+float(self.eList[0])
                Efinal = self.fixedE
                
            # Initial Q
            q = string.split(self.qList[0],'~')

            labels = []
            values = []
            if hasattr(self.geometry,"getScanPointDevices"):
                labels, values = self.geometry.getScanPointDevices(Einit,Efinal,q,self)
            else:
                values = self.geometry.getDevices(Einit,Efinal,q,self)
                labels = self.geometry.getAllDevices()
            
            # We fill a dictionary because we want values to appear only once in the list
            for i in range(len(labels)):
                self.constDevicesList[labels[i].upper()]=values[i]
            
        keys = self.angleList.keys()
        ntot = len(keys)
        if ntot > 0:
            for i in range(ntot):
                length = len(self.angleList[keys[i]])
                # If there is a single entry, it's a constant
                # Otherwise, remove it if it's already in the list
                if length==1:
                    #~ self.constDevicesList[keys[i]]=float(self.angleList[keys[i]][0])
                    self.constDevicesList[keys[i].upper()]=self.angleList[keys[i]][0]
                else:
                    if keys[i].upper() in self.constDevicesList: 
                        del self.constDevicesList[keys[i].upper()]
                    
        # Sort them first
        motorNames = self.constDevicesList.keys()
        motorNames.sort()
        const=''
        for dev in motorNames:
            partValue = self.constDevicesList[dev]
            try: partValue = "%-8g" % partValue
            except: pass
            const += "%s=%s " % (dev, partValue)
            
        return const
        
    def getCount(self, point):
        nCounts = float(self.prefac*self.counts[0])
        ctlen = len(self.counts)
        if ctlen>1 and ctlen>point:
            nCounts = float(self.prefac*self.counts[point])
        return [self.countType, nCounts]
        
    def getPoint(self, pt):
        """ 
            Check if point is a good input
            @return: Command string for initiating device moves.  This will be move followed by \
                several devices ??and values??.  The devices will be in ??key??? order.
            @todo: Verify documentation guesses.
        """
        point = 0
        point2 = 0
        try:
            point = int(pt)
        except:
            LogAndRaise("Error","Buffers.getPoint: bad point parameter")
        
        # Check whether we have a second dimension
        if self.numPoints2>0:
            point2 = int(math.fmod(point, self.numPoints2))
            point = int(point/self.numPoints2)
        
        # Position list
        devList = {}
        
        if BUFFERDEBUG==1:
                print self.angleList
                print "E:", self.eList
                print "Q:",  self.qList
        
        # The following condition is to ensure that the old scan description
        # will be executed the same way they were. With the old descriptions
        # Q and E were defined even for increment scans that didn't change
        # their values.
        if not (self.type==5 or self.type==6):
            # Check whether we have a second dimension first
            eLen = len(self.eList)
            qLen = len(self.qList)
                
            # Initial and final energies: Ef = Ei - E
            if qLen>0 and eLen>0:
                
                # Check fixed energy selection
                if self.fixedType==-1: LogAndRaise("Error","Buffers.getPoint: no fixed energy selected")
                if self.fixedE==0: LogAndRaise("Error","Buffers.getPoint: no fixed energy value")
                    
                Einit  = 0
                Efinal = 0
                if self.fixedType==0:
                    Einit  = self.fixedE
                    Efinal = self.fixedE-float(self.eList[0])
                elif self.fixedType==1:
                    Einit  = self.fixedE+float(self.eList[0])
                    Efinal = self.fixedE
                    
                # Initial Q
                q = string.split(self.qList[0],'~')
                
                # Energies
                if eLen>point:
                    if self.fixedType==0:
                        Einit  = self.fixedE
                        Efinal = self.fixedE-float(self.eList[point])
                    else:
                        Einit  = self.fixedE+float(self.eList[point])
                        Efinal = self.fixedE
                        
                # Q
                if qLen>point:
                    q = string.split(self.qList[point],'~')
                    if not len(q)==3:
                        Logger("Error","Bad Q format: rejecting [%s]" % str(q))
                        
                # Get the angles
                if qLen>1 or eLen>1 or (point==0 and (qLen==1 or eLen==1)):
                    labels = []
                    values = []
                    if hasattr(self.geometry,"getScanPointDevices"):
                        labels, values = self.geometry.getScanPointDevices(Einit,Efinal,q,self)
                    else:
                        values = self.geometry.getDevices(Einit,Efinal,q,self)
                        labels = self.geometry.getAllDevices()
                    for i in range(len(values)):
                        devList[labels[i]] = values[i]
        
                    # Loop through constant devices to make sure they are not changed
                    if pt>0:
                        toRemove = []
                        for pdev in devList:
                            for cdev in self.constDevicesList:
                                if pdev.upper()==cdev.upper(): toRemove.append(pdev)
                        for ddev in toRemove: del devList[ddev]

        if len(self.angleList)>0: 
            for dev in self.angleList:
                npts = len(self.angleList[dev])
                if npts>point: devList[dev.upper()] = self.angleList[dev][point]
                    
        # Second scan dimension
        if self.numPoints2>0:
            for dev in self.secondDev:
                npts = len(self.secondDev[dev])
                if npts>point2: devList[dev] = self.secondDev[dev][point2]

        # Consistency check
        # If this is the first point, all the constant devices should be present
        if pt==0:
            for cdev in self.constDevicesList:
                ifound = 0
                for pdev in devList:
                        if pdev.upper()==cdev.upper(): ifound = 1
                if ifound==0: 
                    LogAndPrint("Error","Buffer.getPoint: pt 0 -> constant device [%s] notmoving" % cdev)

        cmdstr = ""
        if len(devList)>0:
            cmdstr = "Move"
            # Get the keynames and sort them
            keys = devList.keys()
            keys.sort()
            for dev in keys:
                cmdstr += " %s %s" % (dev, devList[dev])
            
        if BUFFERDEBUG==1: print cmdstr
        if len(cmdstr.lstrip().rstrip())>0: return [cmdstr]
        return []

    def toInstrStates(self):
        """Transforms the scan description into a list of instrument states"""
        
        # Check parameter list
        if hasattr(self.geometry,"checkParams") :
            check = self.geometry.checkParams()
            if len(check.rstrip().lstrip())>0: 
                LogAndRaise("Error",check)
        
        #~ if self.counts==[0]:
            #~ LogAndRaise("Error","Scan: No number of counts specified")
            
        # Generate device list if enough information is given 
        if self.numPoints>0 and len(self.scanRange)>0: 
            self.angleList={}
            # Compute list of points
            devlist=self.scanRange.keys()
            for dev in devlist:
                    if self.angleList.has_key(dev): del self.angleList[dev]
                    if dev=="Q": 
                        if self.angleList.has_key(dev): del self.angleList[dev]
                        self.qList=[]
                        if len(self.scanRange[dev])>=3 and self.scanRange[dev][2]=="S":
                            qtmp = string.split(self.scanRange[dev][0], '~')
                            qstart=[float(qtmp[0]),float(qtmp[1]),float(qtmp[2])]
                            qtmp = string.split(self.scanRange[dev][1], '~')
                            qstop=[float(qtmp[0]),float(qtmp[1]),float(qtmp[2])]
                            if self.numPoints>1:
                                qd = [ (float(qstop[0])-float(qstart[0]))/(self.numPoints-1),\
                                    (float(qstop[1])-float(qstart[1]))/(self.numPoints-1),\
                                    (float(qstop[2])-float(qstart[2]))/(self.numPoints-1)]
                            else:
                                qd = [ 0, 0, 0 ]
                        elif len(self.scanRange[dev])>=3 and self.scanRange[dev][2]=="I":
                            qtmp = string.split(self.scanRange[dev][0], '~')
                            qstart=[float(qtmp[0]),float(qtmp[1]),float(qtmp[2])]
                            qtmp = string.split(self.scanRange[dev][1], '~')
                            qd=[float(qtmp[0]),float(qtmp[1]),float(qtmp[2])]
                        else:
                            qcenter = string.split(self.scanRange[dev][0], '~')
                            qdelta = string.split(self.scanRange[dev][1], '~')
                            qc = [float(qcenter[0]), float(qcenter[1]), float(qcenter[2])]
                            qd = [float(qdelta[0]), float(qdelta[1]), float(qdelta[2])]
                            qstart = [qc[0]-qd[0]*(self.numPoints-1)/2,\
                                qc[1]-qd[1]*(self.numPoints-1)/2, qc[2]-qd[2]*(self.numPoints-1)/2]
                        if math.fabs(qd[0])>0 or math.fabs(qd[1])>0 or math.fabs(qd[2])>0:
                            for j in range(self.numPoints):
                                h = qstart[0]+qd[0]*j
                                k = qstart[1]+qd[1]*j
                                l = qstart[2]+qd[2]*j
                                q = "%g~%g~%g" % (h, k, l)
                                self.qList.append(q)
                        else:
                            self.qList.append(self.scanRange[dev][0])
                    else:
                        if len(self.scanRange[dev])>=3 and self.scanRange[dev][2]=="S":
                            start=float(self.scanRange[dev][0])
                            stop=float(self.scanRange[dev][1])
                            center=start
                            if self.numPoints>1:
                                delta=(stop-start)/(self.numPoints-1)
                            else:
                                delta=0
                        elif len(self.scanRange[dev])>=3 and self.scanRange[dev][2]=="I":
                            start=float(self.scanRange[dev][0])
                            delta=float(self.scanRange[dev][1])
                        else:
                            delta=float(self.scanRange[dev][1])
                            center=float(self.scanRange[dev][0])
                            start=center-delta*(self.numPoints-1)/2
                        if dev=="E": self.eList=[]
                        else:
                            if not self.angleList.has_key(dev):
                                self.angleList[dev] = []
                        if math.fabs(delta)>0:
                            for j in range(self.numPoints):
                                angle = start+delta*j
                                if dev=="E": 
                                    self.eList.append(str(angle))
                                else:
                                    self.angleList[dev].append(str(angle))
                        else:
                            if dev=="E": 
                                self.eList.append(str(start))
                            else:
                                self.angleList[dev].append(str(start))
                                    
        # Second scan dimension
        if self.numPoints2>0 and len(self.scanRange2)>0: 
            self.secondDev={}
            devlist=self.scanRange2.keys()
            for dev in devlist:
                if len(self.scanRange2[dev])>=3 and self.scanRange2[dev][2]=="S":
                    start=float(self.scanRange2[dev][0])
                    stop=float(self.scanRange2[dev][1])
                    center=start
                    delta=(stop-start)/(self.numPoints2-1)
                elif len(self.scanRange2[dev])>=3 and self.scanRange2[dev][2]=="I":
                    start=float(self.scanRange2[dev][0])
                    delta=float(self.scanRange2[dev][1])
                else:
                    delta=float(self.scanRange2[dev][1])
                    center=float(self.scanRange2[dev][0])
                    start=center-delta*self.numPoints2/2
                if not self.secondDev.has_key(dev):
                    self.secondDev[dev] = []
                for j in range(self.numPoints2):
                    angle = start+delta*j
                    self.secondDev[dev].append(str(angle))
            
    def nextPoint(self,run=0,nPts=0):
        raise "Error","Buffers.nextPoint is no longer supported"

    def initScan(self):
        """Initializes the scan"""
        self.inScan       = 0
        self.currentPoint = -1
        return "Scan initialized"

    def dryRun(self):
        raise "Error","Buffers.dryRun is no longer supported"
        
    def run(self):
        raise "Error","Buffers.run is no longer supported"
        
    def getDescription(self, xml=None):
        """Returns a string describing the scan.
            Can also write to an XML file.
        """
        if xml:
            f=LogFile(xml)
            f.write("ScanDescr", self.description)
            f.closeBlock("ScanDescr")
            f.terminate()
        return self.description
    
    def getProgress(self):
        """Gets the current scan progress"""
        npts = self.getNumPoints()
        if npts==0:
            return -1.0
        return float(self.currentPoint)/float(npts)

    def getInScan(self):
        """Returns 1 if we are in a scan, 0 otherwise"""
        return self.inScan

    def stopScan(self):
        """Stops the execution of the scan"""
        self.inScan = 0
        return "Scan stopped"

    def resumeScan(self):
        """Resumes the execution of the scan"""
        self.inScan = 1
        return "Scan resuming: use Scan NextPoint"

    def setPoint(self,value):
        """Set the current scan point to a particular value"""
        try:
            i = int(value)
        except ValueError:
            return "Scan: input point not an integer"
        #self.inScan = 1
        self.currentPoint = i-1
        return "Next scan point will be %i: scan paused" % int(self.currentPoint+1)
        
    def addPoint(self, Ei=0.0, Ef=0.0, q=[0.0,0.0,0.0]):
        raise "Error","Buffers.addPoint is no longer supported"

# Parser Scan Descriptions
class ParseScan(ContentHandler):
    def __init__(self, tag="Scan"):
        ContentHandler.__init__(self)
        self.in_scan       = 0
        self.scanDescr     = "Scan"
        self.currentTag    = ''
        self.tag           = tag
        self.nScan         = 0
        self.scanList      = {}
        self.scanAttr      = None
    def startDocument(self):
        return 0
    def startElement(self, name, attrs):
        self.scanAttr    = attrs
        self.currentTag  = name
        if name == self.tag:
            self.in_scan = 1
    def endElement(self, name):
        if name == self.tag:
            self.in_scan = 0
    def characters(self, ch):
        if not str(ch).isspace():
            if self.in_scan==1:
                if self.tag=="Scan":
                    if not self.currentTag==self.tag:
                        self.scanDescr = self.scanDescr+":"+str(self.currentTag)+"="+str(ch)
                elif self.tag=="ScanDescr":
                    if self.scanAttr.has_key("name"):
                        self.scanList[self.scanAttr["name"]] = str(ch)
                    else:
                        self.scanList[str(self.nScan)] = str(ch)
                    self.nScan = self.nScan+1
    def getList(self):
        if self.tag=="Scan":
            return [self.scanDescr]
        elif self.tag=="ScanDescr":
            return self.scanList

if __name__ == "__main__":
    import InstrumentDescription
    instrument       = InstrumentDescription.InstrumentDescription()
    if instrument.decode("input.xml")<0:
        print "No instrument description loaded"
    list=sys.argv[1:]
    b=ScanDescription(geo=instrument.geometry)
    if len(list)>0:
        desc=string.join(list)
        b.decode(desc)
    else:
        print "---"
        print b.decode("Scan:Title=Goo goo 2:Type=2:Field=12.3:Temp=55.5 56.5:Fixed=0:FixedE=14.7:E=2:Q=0.275~0~0 0.325~0~0 0.375~0~0 0.425~0~0:Counts=100:CountType=Timer:Angle=A1=34 35 36:Angle=A2=44 45 46")
    if b:
        print b
        print b.getDescription()
        
#
# $Log$
# Revision 1.43  2007/11/23 21:13:53  mimartin
# Add commenting, some spacing to improve readability.
#
# Revision 1.42  2007/09/10 20:15:04  pheiffer
# *** empty log message ***
#
# Revision 1.41  2007/09/10 19:58:00  pheiffer
# *** empty log message ***
#
# Revision 1.40  2007/09/10 14:46:59  pheiffer
# *** empty log message ***
#
# Revision 1.39  2007/08/21 14:27:00  pheiffer
# *** empty log message ***
#
# Revision 1.38  2007/01/10 14:28:26  doucet
# Fixed problem with single-point vector scans (division by zero).
#
# Revision 1.37  2006/11/08 20:40:45  doucet
# Added a getToken method
#
# Revision 1.36  2006/09/13 17:52:48  doucet
# No longer import InstrumentGeo
#
# Revision 1.35  2006/09/07 19:26:30  doucet
# Fixed bug with init-final mode
#
# Revision 1.34  2006/08/09 18:41:23  doucet
# Added Initial/Step mode for device Range
#
# Revision 1.33  2006/07/17 18:26:35  doucet
# Modified 'decode' so that it does not log an error each time
# a scan is parsed.
#
# Revision 1.32  2006/06/29 14:00:40  doucet
# - Modified getConstantDevices to be consistent with getPoint
#   Old scan types 5 and 6 will not consider Q and E.
# - Make getPoint case insensitive
# - TO DO: re-write the whole thing to be case insensitive from the start
#   The devices should be stored in lowercase
#
# Revision 1.31  2006/06/07 14:26:42  doucet
# Got rid of "wrong scan description" message
#
# Revision 1.30  2006/05/12 20:44:31  doucet
# Allowed constant device values to be string and not only float
#
# Revision 1.29  2006/05/09 14:45:29  doucet
# - Improved getNumPoints to allow second dimension as a list of positions
# - Added the possibility to specify list of positions for 2nd dimension
#
# Revision 1.28  2006/04/25 14:35:00  doucet
# Got rid of scan_backup.xml
#
# Revision 1.27  2006/04/17 13:38:31  doucet
# Got rid of exception for empty scan defs
#
# Revision 1.26  2006/04/03 20:13:43  doucet
# Added GetScanPointDevices to get devices values for a scan point
#
# Revision 1.25  2006/03/15 21:06:19  doucet
# Added version information at startup
#
# Revision 1.24  2006/03/03 15:09:19  doucet
# Fill default description with None
#
# Revision 1.23  2006/02/27 20:18:33  doucet
# Fixed problem with negative Q steps
#
# Revision 1.22  2006/02/14 19:11:16  doucet
# Huge re-engineering of scan description
#
# Revision 1.21  2005/11/08 20:24:37  doucet
# Fixed start/stop Q scans
#
# Revision 1.20  2005/11/02 21:18:24  doucet
# Simplified getDescription
#
# Revision 1.19  2005/10/25 15:29:40  doucet
# minor change in the list of points using Range for E and other devices
#
# Revision 1.18  2005/10/21 17:57:28  doucet
# Allow for 2D scans
#
# Revision 1.17  2005/10/18 15:55:09  doucet
# -Added filename field in scan description
# -fixed bug in point calculation
#
# Revision 1.16  2005/10/17 15:08:51  doucet
# -Removed TEmp and Field scans
# -Added possibility to given start/stop points instead of center/incr
#
# Revision 1.15  2005/10/14 19:30:39  doucet
# Allow prefactors as floats
#
# Revision 1.14  2005/10/12 20:34:51  doucet
# Improved scan descriptions with server-side calculations
#
# Revision 1.13  2005/10/05 20:24:17  doucet
# -Added getNumPoint
# -Fixed bug with new scan descriptions
#
# Revision 1.12  2005/10/05 18:50:03  doucet
# Allow Q scan, E scan, and Q+E scans using the new scan range description
#
# Revision 1.11  2005/10/04 19:32:58  doucet
# Repaired Range field for Q in scan description
#
# Revision 1.10  2005/09/30 18:21:42  doucet
# Small changes to accomodate MACS (passing scan description when calling getDevices)
#
# Revision 1.9  2005/09/14 15:35:31  doucet
# Added scan descriptions for which the series of points are computed on the server side
#
# Revision 1.8  2005/09/09 21:03:07  doucet
# Added scanListInfo
#
# Revision 1.7  2005/09/09 15:01:07  doucet
# Added condition statements for calls to InstrGeo functions that might not exist
#
# Revision 1.6  2005/07/26 15:47:31  doucet
# Modified Bragg buffers to include initialization in first point
#
# Revision 1.5  2005/02/17 14:47:24  doucet
# -Changed instrState so that moves are done in a single command
# -Added Bragg buffer
#
# Revision 1.4  2005/02/03 16:25:05  doucet
# Change of GUI printout format
#
# Revision 1.3  2005/02/01 20:53:56  doucet
# Allow Triax scans that do not have d-spacing specified
#
# Revision 1.2  2005/01/05 21:20:29  doucet
# Modified precision on state.info string
#
# Revision 1.1  2004/10/20 16:59:24  doucet
# Reorganized the directory structure
#
# Revision 1.17  2004/10/08 15:57:54  doucet
# Added possibility to have a different count number for each point in a scan
#
# Revision 1.16  2004/10/06 19:25:46  doucet
# Bug with XML scan descr...
#
# Revision 1.15  2004/10/06 19:19:01  doucet
# Modified the way I keep track of additional parameters in the scan description.
#
# Revision 1.14  2004/10/04 18:58:36  doucet
# Added the possibility to have user tags in a scan description (this will be used to store meta-data).
#
#
