from cmd3 import Cmd, make_option, options, Cmd2TestCase
import unittest, optparse, sys,math
import functools,inspect
import argparse
pi=math.pi
#import readline
#instrument='localhost'
#instrument='129.6.121.48'
import fnmatch, copy

from ice import * 
from ice import Controller
from ice import Global
from ice.ClientAPI import *
from ice import IceGuiManager
from ice.commands import *
from ice.data import *
from ice.communication import *
from ice.event import *
from ice.primitive import *
from ice.util import *
from ice.event.communication import BroadcastMessageListener


from java.awt import *
from javax.swing import *
from ice.gui.core import GenericIcePanel
from ice.gui.core import IceDialog
from ice.gui.core import IceEditPanel
from ice.gui.core import IceWindow
from ice.swing import *
import scanparser3 as scanparser

import readline
import sys

c=ClientAPI.getInstance('test','localhost')
#c=ClientAPI.getInstance('test','129.6.121.48')


###For now, I'm including stubs for testing purposes.  These need to be replaced with Java classes which have the actual 
###Actions that I require.  Things are probably safer this way, because there is more isolation between the python code and
###the Java Code.


##TODO Check Alias list for present device
##TODO Change print statements to stdout.write



"""
        #: A hash which maps queueable remote command names to the methods that actually run the command
        self.remote_commands                         = {}
        
        self.remote_commands['DIE']                  = self.command_Die
        self.remote_commands['WAIT']                 = self.command_Wait
        self.remote_commands['HOLD']                 = self.command_Wait
        self.remote_commands['SCAN']                 = self.command_Scan
        self.remote_commands['DATA']                 = self.command_Data
        self.remote_commands['DEVICE']               = self.command_Device
        self.remote_commands['MOVE']                 = self.command_Move
        self.remote_commands['COUNT']                = self.command_Count
        self.remote_commands['SCRIPT']               = self.command_Script
        if HAS_PYFIT==1 and self.sequencer.settings.usePyFit==1: 
            self.remote_commands['FINDPEAK']   = self.command_FPyfit
        else:            
            self.remote_commands['FINDPEAK']   = self.command_FP
        self.remote_commands['CORRECTLATTICE']   = self.command_CorrectLattice
        self.remote_commands['ACCEPTFINDPEAK']       = self.command_AcceptFindPeak
        self.remote_commands['ACCEPTLATTICE']        = self.command_AcceptLattice
        self.remote_commands['FINDPEAKSETPOS']       = self.command_FindPeakSetPos
        self.remote_commands['KILL']                 = self.command_Kill
        self.remote_commands['FILE']                 = self.command_File
        self.remote_commands['TRANSFER']             = self.command_Transfer
        self.remote_commands['PRINT']                = self.command_Print
        self.remote_commands['COUNTANDPRINT']        = self.command_CountAndPrint
        self.remote_commands['USER']                 = self.command_User
        self.remote_commands['REGTEST']              = self.command_RegTest
        self.remote_commands['ACCEPTCAL']            = self.command_AcceptCal
        self.remote_commands['RATE']                 = self.command_Rate 
        self.remote_commands['DVSCAN']               = self.command_DvScan
        self.remote_commands['QSCAN']                = self.command_QScan
        self.remote_commands['FLIPRAT']              = self.command_FlipRat
        self.remote_commands['Q']                    = self.command_Q
        self.remote_commands['QUEUESETPERSISTENCEMODE'] = self.command_Queuesetpersistencemode
        self.remote_commands['ICPSEQ']               = self.command_Icpseq
        self.remote_commands['INSTRUMENT']           = self.command_Instrument

        
        #: A hash which maps immediate remote command names to the methods that actually run the command
        self.remote_immediate_commands               = {}
        
        self.remote_immediate_commands['MOVE']       = self.command_Move
        self.remote_immediate_commands['STACK']      = self.command_Stack
        self.remote_immediate_commands['STOPALL']    = self.command_StopAll
        self.remote_immediate_commands['KILL']       = self.command_Kill
        self.remote_immediate_commands['KILLANDPAUSE'] = self.command_KillAndPause
        self.remote_immediate_commands['TRANSFER']   = self.command_Transfer
        self.remote_immediate_commands['FILE']       = self.command_File
        self.remote_immediate_commands['MESSAGE']    = self.command_Message
        self.remote_immediate_commands['CHECKFIT']   = self.command_CheckFit
        self.remote_immediate_commands['SCAN']       = self.command_Scan
        #self.remote_immediate_commands['VERSION']    = self.command_Version
        self.remote_immediate_commands['UPDATE']     = self.command_UpdateStatus
        self.remote_immediate_commands['RESUME']     = self.command_Pause
        self.remote_immediate_commands['PAUSE']      = self.command_Pause
        self.remote_immediate_commands['FLUSHSTACK'] = self.command_FlushStack
        self.remote_immediate_commands['XPEEK']      = self.command_XPeekStart
        self.remote_immediate_commands['COMMENT']    = self.command_DataComment
        self.remote_immediate_commands['PRINT']      = self.command_Print
        
        self.remote_immediate_commands['STATUS']     = self.command_Status
        self.remote_immediate_commands['DISPSTATUS'] = self.command_DispStatus
        self.remote_immediate_commands['STATE']      = self.command_State
        self.remote_immediate_commands['HELP']       = self.command_Help
        self.remote_immediate_commands['LISTSTACK']  = self.command_ListStack
        self.remote_immediate_commands['LOG']        = self.command_Log
        self.remote_immediate_commands['REGISTER']   = self.command_Register
        self.remote_immediate_commands['GETKEY']     = self.command_GetKey
        self.remote_immediate_commands['LOGIN']      = self.command_Passwd
        self.remote_immediate_commands['LOGOUT']     = self.command_Logout
        self.remote_immediate_commands['TEST']       = self.command_Test
        self.remote_immediate_commands['ASK']        = self.command_Ask
        self.remote_immediate_commands['INSTRUMENT'] = self.command_Instrument
        self.remote_immediate_commands['SAMPLE']     = self.command_Sample
        self.remote_immediate_commands['CALCLATTICE']= self.command_CalcLattice
        self.remote_immediate_commands['FILE']       = self.command_File
        self.remote_immediate_commands['SETTINGS']   = self.command_Settings
        self.remote_immediate_commands['DEVICE']     = self.command_Device
        self.remote_immediate_commands['EXPT']       = self.command_Experiment
        self.remote_immediate_commands['GIVEUP']     = self.command_GiveUp
        self.remote_immediate_commands['STACK']      = self.command_Stack
        self.remote_immediate_commands['GETNEWLATTICE'] = self.command_GetNewLattice
        self.remote_immediate_commands['ECHO']       = self.command_Echo

"""


class GetErrs(BroadcastMessageListener):
	def __init__(self):
		c=Controller.getReference()
		comm=c.getCommMgr()
		comm.addMessageListener(self)
	def actionPerformed(self,me):
		data=me.getData()
		print data
		if not  str(data).find('Stopped')==-1:
			print 'exiting'
			sys.exit()
		#if not str(data).find('Paused')==-1:
		#	print 'instrument paused'  #for now exit
		#	sys.exit()
		#if not str(data).find('Resuming')==-1:
		#	print 'instrument Resuming'  #for now exit
		#	sys.exit()
			
	def __del__(self):
		comm.removeMessageListener(self)
geterrs=GetErrs()


class Rate(QueuedCommand):
	def getCommandString(self):
		s="Rate"
		return s

	def parseSynchronousResponse(self):
		cid=self.getCommandId()
		imq=self.getResponseMessageQueue()
		cmq=imq.getMessagesForAbsCommandId(cid)
		f=cmq.remove()
		print "Rate ",f 
		self.rate=f
		#Note, the rate command doesn't seem to actually print the bloody rate!!!

class SimpleImmediateCommand(ImmediateCommand):
	def __init__(self,commandstr):
		self.commandstr=commandstr
	def getCommandString(self):
		s = "%s"%(self.commandstr,)
		return s
	def parseSynchronousResponse(self):
		f = self.getResponse()            
		self.result=f

class setLowerLimit(ImmediateCommand):
	def __init__(self,device,value):
		self.device=device
		self.value=value
	def getCommandString(self):
		s = "Device setlowerlimit %s %s"%(self.device,self.value)
		return s

	def parseSynchronousResponse(self):
		#cid = self.getCommandId()
		#imq = self.getResponseMessageQueue()
		#cmq = mq.getMessagesForAbsCommandId(cid)
		#f = cmq.remove()
		f = self.getResponse()
		print f 
                #f=str(f.split('\n')[1]).split(':')[1].strip().split()
                #self.soft=f[0]
                #self.hard=f[1]                
		self.f=f

class setUpperLimit(ImmediateCommand):
	def __init__(self,device,value):
		self.device=device
		self.value=value
	def getCommandString(self):
		s = "Device setupperlimit %s %s"%(self.device,self.value)
		return s

	def parseSynchronousResponse(self):
		#cid = self.getCommandId()
		#imq = self.getResponseMessageQueue()
		#cmq = mq.getMessagesForAbsCommandId(cid)
		#f = cmq.remove()
		f = self.getResponse()
		print f 
                #f=str(f.split('\n')[1]).split(':')[1].strip().split()
                #self.soft=f[0]
                #self.hard=f[1]                
		self.f=f


class GetHowlong(ImmediateCommand):
	def __init__(self,scan,overhead=0.0,timeflag='-s'):
		self.scan=scan
		self.overhead=overhead
		self.timeflag=timeflag
	def getCommandString(self):
		s = "Scan Howlong "+self.scan+" "+self.timeflag+" -o "+str(self.overhead)#overhead is in seconds
		return s

	def parseSynchronousResponse(self):
		#cid = self.getCommandId()
		#imq = self.getResponseMessageQueue()
		#cmq = mq.getMessagesForAbsCommandId(cid)
		#f = cmq.remove()
		f = self.getResponse()
		print f 
		self.howlong=f


class GetScans(ImmediateCommand):
	def getCommandString(self):
		s = "Scan List"
		return s

	def parseSynchronousResponse(self):
		#cid = self.getCommandId()
		#imq = self.getResponseMessageQueue()
		#cmq = mq.getMessagesForAbsCommandId(cid)
		#f = cmq.remove()
		f = self.getResponse()
		#print f
                self.f=f
                self.scanlist=[]
                if f:
			scans=f.split('\n')[1:]
			for scan in scans:
				tmp=str(scan).split(':')
				if tmp[0] is not '' and len(tmp)>1:
					self.scanlist.append(tmp[1].strip())


class Count(QueuedCommand):
	def __init__(self,device,duration,printflag=True):
		self.device=device
		self.duration=duration
		self.printflag=printflag
	def getCommandString(self):
		s = "Count %s "%(self.device,)
		if self.printflag:
			s=s+'-p '    
		s=s+str(self.duration)
		return s
	def parseSynchronousResponse(self):
		cid = self.getCommandId()
		imq = self.getResponseMessageQueue()
		cmq = imq.getMessagesForAbsCommandId(cid)
		self.cmq=cmq
		self.imq=imq

		
class SimpleQueuedCommand(QueuedCommand):
	def __init__(self,commandstr):
		self.commandstr=commandstr
	def getCommandString(self):
		s=self.commandstr
		#s = "Count %s "%(self.device,)
		#if self.printflag:
		#	s=s+'-p '    
		#s=s+str(self.duration)
		return s
	def parseSynchronousResponse(self):
		cid = self.getCommandId()
		imq = self.getResponseMessageQueue()
		cmq = imq.getMessagesForAbsCommandId(cid)
		self.cmq=cmq
		self.imq=imq
		f=cmq.remove()
		self.result=f
		
		
		
		
		
		
class GetScanDescription(QueuedCommand):
	def __init__(self,scan):
		self.scan=scan
	def getCommandString(self):
		s = 'scan listdescr %s'%(self.scan,)
		return s
	def parseSynchronousResponse(self):
		cid=self.getCommandId()
		imq=self.getResponseMessageQueue()
		cmq=imq.getMessagesForAbsCommandId(cid)
		self.cmq=cmq
		self.imq=imq
		f=cmq.remove()
	    ##The following is a complete and utter hack and needs to be improved!!!!
	        self.scan_description=f.split(':Title')[0].split('iceuser:')[1]
        
class ScanDryRunCommand(QueuedCommand):
	def __init__(self,scan):
		self.scan=scan
	def getCommandString(self):
		s = 'scan dryrun %s'%(self.scan,)
		return s
	def parseSynchronousResponse(self):
		cid=self.getCommandId()
		imq=self.getResponseMessageQueue()
		cmq=imq.getMessagesForAbsCommandId(cid)
		self.cmq=cmq
		self.imq=imq
		f=cmq.remove()
		self.result=f

def Property(func):
	return property(**func())

class Devices(object):
	@Property
	def present_devices():
		doc="list of devices currently present on the instrument"
		def fget(self):
			controller=self.controller
			self._present_devices=[str(device.name).lower() for device in controller.getDeviceList()]
			return self._present_devices
		
		return locals()
		#self._present_devices=['a3','a4']
		#controller=Controller.getReference()
		#self._present_devices=controller.deviceList  #controller.getAllDevices()
		#self._present_devices=[device.name for device in controller.deviceList]
		#device.name returns the name of the device
		#We should also note that controller.getAllDevices(Name) will return the device with name
		#We should also note that there are convenience methods such as device.getRealName() which will return the real name of the device
		#and device.getAlias() which will return aliases
		
		#print 'present_devices getter'
		
	    
	    #this will be read-only
	    #def fset(self):
	    #	self.name = name
    
	   
    
    
	@Property
	def present_scans():
		doc="list of devices currently present on the instrument"
		def fget(self):	
			controller=self.controller
			scanner=GetScans()
			scanner.run()
			self._present_scans=scanner.scanlist
			return self._present_scans
		return locals()
		#Java updtate
		#self._present_devices=['a3','a4']
		#controller=Controller.getReference()
		#self._present_devices=controller.deviceList  #controller.getAllDevices()
		#self._present_devices=[device.name for device in controller.deviceList]
		#self._present_devices=[str(device.name).lower() for device in controller.getDeviceList()]
		#device.name returns the name of the device
		#We should also note that controller.getAllDevices(Name) will return the device with name
		#We should also note that there are convenience methods such as device.getRealName() which will return the real name of the device
		#and device.getAlias() which will return aliases
		
		#print 'present_devices getter'
		
	    
	    #this will be read-only
	    #def fset(self):
	    #    self.name = name
    

	@Property
	def present_sequences():
		doc="list of devices currently present on the instrument"
		def fget(self):	
			controller=self.controller
			s3="File dir EXPT:"			
			sq=SimpleImmediateCommand(s3);sq.run()
			self._present_sequences=sq.result.split('\n')
			return self._present_sequences
		return locals()
	
		#EXPT: experiment directory
		#USER: user directory
		#COMM: common directory
		#DATA: data directory

		#Java updtate
		#self._present_devices=['a3','a4']
		#controller=Controller.getReference()
		#self._present_devices=controller.deviceList  #controller.getAllDevices()
		#self._present_devices=[device.name for device in controller.deviceList]
		#self._present_devices=[str(device.name).lower() for device in controller.getDeviceList()]
		#device.name returns the name of the device
		#We should also note that controller.getAllDevices(Name) will return the device with name
		#We should also note that there are convenience methods such as device.getRealName() which will return the real name of the device
		#and device.getAlias() which will return aliases
		
		#print 'present_devices getter'
		
	    
	    #this will be read-only
	    #def fset(self):
	    #    self.name = name

    
    
    
    
    
    
	@Property
	def environmental_devices():
		doc="list of environment devices currently present on the instrument"
		def fget(self):
			controller=self.controller
			#self._environmental_devices=['temp','magfield']
			#environmental_devices=c.getEnvDevices()
			self._environmental_devices=[str(device.name).lower() for device in controller.getEnvDevices()]
			return self._environmental_devices

		return locals()
		#Java updtate
		
		#print 'environmental_devices getter'
		#I could probably fake it--I could get all of the devices
		#then, use for example temp.getType() which will give me the type of the device
		#InstalledDevice.Type.environment==temp.getType()
		#if it were public, I could use controller.getEnvDevices() or 
		#controller.getNonEnvDevices()
		
	    #this will be read-only
	    #def fset(self):
	    #	self.name = name
    
	    
    
	@Property
	def counting_devices():
		doc="list of counting devices currently present on the instrument"
		def fget(self):
			controller=self.controller
			#self._counting_devices=['time','monitor']
			#counting_devices=c.getCounterDevices()
			self._counting_devices=[str(device.name).lower() for device in controller.getCounterDevices()]
			return self._counting_devices
		return locals()
		#Java updtate
		
		#print 'counting_devices getter'
		#I could probably fake it--I could get all of the devices
		#then, use for example temp.getType() which will give me the type of the device
		#InstalledDevice.Type.environment==temp.getType()
		#if it were public, I could use controller.getEnvDevices() or 
		#controller.getNonEnvDevices()
		
	    #this will be read-only
	    #def fset(self):
	    #    self.name = name
    
	    
    
	
	@Property
	def temperature_devices():
		doc="list of temperature devices currently present on the instrument"
		def fget(self):
			#self._temperature_devices=[]
			controller=self.controller
			#devices=self.present_devices
		
			#for device in devices:
			#	actual_device=controller.getAllDevices(device)
			#	if len(actual_device)>1:
			#		if type(actual_device[-1]) is InstalledTempDevice:
			#			self._temperature_devices.append(device)
			#self._temperature_devices=c.getTempDevices()
			self._temperature_devices=[str(device.name).lower() for device in controller.getTempDevices()]
			return self._temperature_devices
		return locals()
		#Here, the problem is that the type of temp is 'environment'
		#The work around is type(mytemp) is InstalledTempDevice
		#print 'temperature_devices getter'
		
	    #this will be read-only
	    #def fset(self):
	    #	self.name = name
    
	    
    
	@Property
	def magnetic_field_devices():
		doc="list of magnetic devices present on the instrument"	
		def fget(self):
			controller=self.controller
			#self._magnetic_field_devices=[]
			#controller=self.controller
			#devices=self.present_devices
			#for device in devices:
			#	actual_device=controller.getAllDevices(device)
			#	if len(actual_device)>1:
			#		if type(actual_device[-1]) is InstalledMagnetDevice:
			#			self._magnetic_field_devices.append(device)
			self._magnetic_field_devices=[str(device.name).lower() for device in controller.getMagnetDevices()]
			return self._magnetic_field_devices    
		return locals()
	
	@Property
	def fixed_devices():
		doc="list of fixed devices"
		def fget(self):
			self._fixed_devices=[]
			controller=self.controller		
			device_list=self.present_devices        #controller.getDeviceList()
			for device in device_list:
				actual_device=controller.getAllDevices(device)[0]
				if actual_device.isFixed():
					self._fixed_devices.append(device)
			return self._fixed_devices
	
	
		return locals()
    
	@Property
	def controller():
		doc="list of devices currently present on the instrument"
		def fget(self):
			self._controller=Controller.getReference()
			return self._controller

		#We should also note that there are conveniene methods such as device.getRealName() which will return the real name of the device
		#and device.getAlias() which will return aliases		
		return locals()

        def __init__(self):
		self._present_devices=None
		self._active_devices=None
		self._environmental_devices=None
		self._temperature_devices=None
		self._magnetic_field_devices=None
		self._counting_devices=None
		self._fixed_devices=None
		self._controller=None
		self._present_scans=None 
		self._present_sequences=None
		
	def isPresent(self,device):
		"""checks if device is on the instrument"""
		present_devices=self.present_devices
		return device in present_devices
	    
	def activate(self,devices):
		"""activate a device"""
		present_devices=self.present_devices
		for device in devices:
			print "activating", device
		return        
	def deactivate(self,devices):
		"""Deactivate a device"""
		present_devices=self.present_devices
		for device in devices:
			print "deactivating", device
		return
	    
	def rate(self):
		"""Determines the monitor rate"""
		print 'calculating monitor rate'
		mycommand=StackAddCommand("rate")
		mycommand.run()
		myid=mycommand.commandID
		return
	    
	def fix(self,devices):
		"""Fixes devices"""
		controller=self.controller
		for device in devices:
			DeviceFixCommand(device).run()
			print "Fixing", device
		    
		    
	def release(self,devices):
		"""Releases devices"""
		controller=self.controller
		for device in devices:
			DeviceFreeCommand(device).run()
			print "Releasing", device
		    
	def move(self,devices,positions,moveflag=False):
		"""Move devices to positions"""
		present_devices=self.present_devices
		print 'devices',devices
		for i in range(len(devices)):
			if not moveflag:
				print 'Moving',devices[i],'to',positions[i]
			else:
				print 'Moving',devices[i],'by',positions[i]
			m=MoveCommand(devices[i],positions[i],moveflag)
			m.run()  

		
	def move_relative(self,devices,increments):
		"""Move devices by a relative increment"""
		present_devices=self.present_devices
		for i in range(len(devices)):
			print 'Moving',device[i], 'by increment', increments[i]
	    
	def count(self,duration):
		if duration>0:
			counter='monitor'
		   #commandstr="CountAndPrint monitor %s"%(str(duration),)	   
		else:
			counter='time'
		#commandstr="CountAndPrint time %s"%(str(abs(duration),)
		#print 'commandstr',commandstr
		#ct=SimpleImmediateCommand(commandstr)
		####What we should be able to do is use countcommand
		#but someone neglected to add a print option!!!
		ct=Count(counter,abs(duration))
		ct.run()
		#print 'results',ct.result
		
		    
	    
		    
	def scan(self,device,scanrange):
		"""scans device scanrange"""
		present_devices=self.present_devices
		if device in self.present_devices:
			if device in self.counting_devices:
				print 'cannot scan a counting device',device
			elif device in self.environmental_devices:
				print 'scanning an environmental device',device
			else:
				print 'scanning device',device, scanrange
				print 'move to center of fit?'
	def run_scans(self,scanlist):
		"""run scans in scanlist"""
		present_scans=self.present_scans
		matched_scans=self.match(present_scans,scanlist)
		#print 'present_scans', present_scans
		#print 'matched_scans', matched_scans
		for scan in matched_scans:
			print 'running ',scan
			sc=ScanRunCommand(scan)
			sc.run()
			print scan,' finished'
		#for scan in scanlist:
		#    print 'running scan', scan
		
	def run_sequence(self,sequencelist):
		present_sequences=self.present_sequences #I need to figure out what these are!
		matched_sequences=self.match(present_sequences,sequencelist)
		#print 'sequencelist',sequencelist
	      
		#matched_sequences=sequencelist
		#print 'sequencelist',sequencelist
		for sequence in matched_sequences:
			print 'running',sequence
			s=r"stack appendfile EXPT:%s"%(sequence,)
			#print 's before',s
			sc=SimpleImmediateCommand(s)
			#print 'immediated'
			sc.run()
			#print 'ran'
		    
		    
		    
		
	def deleteScanFromScanList(self,scanName):
		controller = self.controller#Controller.getReference()
		sendManager = controller.getSendManager()
		#scanName = self.getName()
		deleteMessage = "scan delete %s" % (scanName)
	    
		sendManager.addMessage(deleteMessage)
		    
	def dry_run_scans(self,scanlist):
		""""dry run scans in scanlist"""
		present_scans=self.present_scans
		matched_scans=copy.deepcopy(self.match(present_scans,scanlist))
		#print 'present_scans', present_scans
		#print 'matched_scans', matched_scans
		for scan in matched_scans:
			print 'dry running ',scan
			getscandescription=GetScanDescription(scan)
			getscandescription.run()
			scan_description=getscandescription.scan_description
			scanName=scan+'_tmp'
			#print 'listing'
			scanDesrToListCommand = ScanDescrToListCommand(scanName,scan_description)
			print 'listed'
			scanDesrToListCommand.run()
			scandryrun = ScanDryRunCommand(scanName)
			scandryrun.run()
			self.deleteScanFromScanList(scanName)
			print scan,' dry ran'   
		    
		    #sc=ScanRunCommand(scan)
		    #sc.run()
		    
	    
		
	def merge(self,seq):
		""""merge a list of lists and return the unique elements
		"""
		merged=[]
		for s in seq:
			for x in s:
				merged.append(x)
		return list(set(merged))
	    
	def match(self,source,patterns):
		"""returns the list of results where the pattern list is found in the source list
		"""
		matched_list=[]
		#print 'pr devices',patterns
		for pattern in patterns:
			curr_matched=fnmatch.filter(source,pattern.lower())
			matched_list.append(curr_matched)
		    #print 'The current value of', device, 'is'
		#print 'devices',matched_devices
		return sorted(self.merge(matched_list))
	    
	def get_device_value(self,device):
		"""Gets the value of a device"""
		present_devices=self.present_devices
		if (device not in self.counting_devices):
			realdevice=self.controller.getAllDevices(device)[0]
			return realdevice.getCurrValue()
		else:
			return None
		    
			
		
	def pr(self,devices,flag='all'):
		"""Prints the values of devices"""
		present_devices=self.present_devices
		matched_devices=self.match(present_devices,devices)
		#print 'input devices', devices
		#print 'matched_devices',matched_devices
		if flag=='all':
			self.print_device_value(matched_devices)
		elif flag=='software':
			self.print_device_software_value(matched_devices)
		elif flag=='hardware':
			self.print_device_hardware_value(matched_devices)
		elif flag=='zeros':
			self.print_device_zero_value(matched_devices)
		elif flag=='upper':
			self.print_upper_limits(matched_devices)        
		elif flag=='lower':
			self.print_lower_limits(matched_devices)
	    
	    
		
	def print_device_value(self,devicelist):
		"""print the hardware and software values of devices in device list"""
		print 'device      software     hardware'
		for device in devicelist:
			realdevice=self.controller.getAllDevices(device)[0]
			if (device not in self.counting_devices) and (device not in self.environmental_devices):
				print '%s      %s     %s'%(device,realdevice.getCurrValue(),realdevice.getHardwareValue(),)
			else:
				print '%s      %s'%(device, realdevice.getCurrValue(),)
					    
	def print_device_software_value(self,devicelist):
		"""print the software values of devices in device list"""
		
		print 'device      software'
		for device in devicelist:
			realdevice=self.controller.getAllDevices(device)[0]
			if (device not in self.counting_devices):
				print '%s      %s'%(device,realdevice.getCurrValue())
			
	def print_device_hardware_value(self,devicelist):
		"""print the hardware values of devices in device list"""
		print 'device      hardware'
		for device in devicelist:
			realdevice=self.controller.getAllDevices(device)[0]
			if (device not in self.counting_devices) and (device not in self.environmental_devices):
				print '%s      %s'%(device,realdevice.getHardwareValue())
			#stderr.write('hardware value of',device,'is '+realdevice.getHardwareValue()+'\n')
			
	def print_device_zero_value(self,devicelist):
		"""print the zero values of devices in device list"""
		print 'device      zero'
		for device in devicelist:
			realdevice=self.controller.getAllDevices(device)[0]
			if (device not in self.counting_devices) and (device not in self.environmental_devices):
				zero=SimpleImmediateCommand('device getzero %s'%(device,))
				zero.run()
				print '%s      %s'%(device,zero.result)

	def print_lower_limits(self,devicelist):
		"""print the lower limit of devices"""
		print 'device      lower limit'
		for device in devicelist:
			realdevice=self.controller.getAllDevices(device)[0]
			if (device not in self.counting_devices):
				print '%s      %s'%(device,realdevice.getLowerLimit())
	    		    
	def print_upper_limits(self,devicelist):
		"""print the upper limit of devices"""
		print 'device      upper limit'
		for device in devicelist:
			realdevice=self.controller.getAllDevices(device)[0]
			if (device not in self.counting_devices):
				print '%s      %s'%(device,realdevice.getUpperLimit())
		    
	def set_lower_limit(self,device,value):
		"""set the lower limit for a device"""
		#can this be done for an environmental device?
		print 'setting lower limits'
		lower=setLowerLimit(device,value)
		lower.run()
		#real_device=self.controller.GetAllDevices(device)
		#real_device.setLowerLimit(float(value))
		#sys.stderr.write('setting lower limit of '+device+' to '+str(value)+'\n')
		
	def set_upper_limit(self,device,value):
		"""set the upper limit for a device"""
		print 'up', device,value
		upper=setUpperLimit(device,value)
		upper.run()
		#can this be done for an environmental device?
		#real_device=self.controller.GetAllDevices(device)
		#real_device.setUpperLimit(float(value))
		#sys.stderr.write('setting upper limit of '+device+' to '+str(value)+'\n')
		
	def set_device_software(self,device,value):
		"""set the software value of device to value"""
		print 'setting',device
		if (device not in self.counting_devices) and (device not in self.environmental_devices):
			real_device=self.controller.getAllDevices(device)[0]
			real_device.setCurrValue(value)
			sys.stderr.write('setting software value of '+device+' to '+value+'\n')
			
		
	def set_device_hardware(self,device,value):
		"""set the hardware value of device to value"""
		if (device not in self.counting_devices) and (device not in self.environmental_devices):
			real_device=self.controller.getAllDevices(device)[0]
			real_device.setHardwareValue(value)
			sys.stderr.write('setting hardware value of '+device+' to '+value+'\n')
			
	def scan_peak_th2th(self,device,scanrange,step,duration,dspacing,aptflag=False):
		"""perform a theta 2 theta scan, move to the center of the peak, calculate
		the lattice constant or do a th2th scan on the analyzer"""
		#print 'device',device
		if device.lower()=='a4':
			s="findpeak %s %s %s "%(device,scanrange,step)
			durationf=float(duration)
			if durationf > 0:
				s=s+"Monitor %s Detector -bragg A3 -func Gauss"%(str(abs(durationf)),) #should make detector a flag
			else:
				s=s+"Time %s Detector -bragg A3 -func Gauss"%(str(abs(durationf)),)
			#print 's',s
			fpt=SimpleQueuedCommand(s)
			#print 'about to run'
			fpt.run()
			#print 'ran', fpt.result
			if not aptflag:
				movetofit=raw_input('Move to Peak position [y/n]? ')
				if (movetofit==None) or (movetofit.lower() in ['n','no']):
					#print 'movetofit',movetofit
					return
				else:
					#print 'moving'
					s="ACCEPTFINDPEAK"  #moves to fit position
					fpt=SimpleQueuedCommand(s)
					fpt.run()
					return
			s="ACCEPTFINDPEAK"  #moves to fit position should probably error check to see if it managed to fit
			fpt=SimpleQueuedCommand(s)
			fpt.run()
			s="ask GETFITRESULTS getnewlattice" #gets dspacing assuming a is zero
			fpt=SimpleImmediateCommand(s)
			fpt.run()
			lattice_constant=float(dspacing)*float(fpt.result.split(':')[-1])
			print 'lattice constant',lattice_constant
			#s="Lattice parameter [      3.29132]"
			#s="AcceptFindPeak"
			#"CorrectLattice 1 -a"
			#"findpeak Temp 5.0 1.0 Monitor 1.0 Monitor -func Gauss"
			#print 'lattice th2th scan' #move to center of peak
			#print 'reset lattice constant?' 
		elif device.lower()=='a6':
			print 'scanning a6 and a5'
			s="findpeak %s %s %s "%(device,scanrange,step)
			durationf=float(duration)
			if duration > 0:
				s=s+"Monitor %s Detector  -bragg A5 -func Gauss"%(str(abs(durationf)),)
			else:
				s=s+"Time %s Detector -bragg A5 -func Gauss"%(str(abs(durationf)),)
			fpt=SimpleQueuedCommand(s)
			fpt.run()
			if not aptflag:
				movetofit=raw_input('Move to Peak position [y/n]? ')
				if (not movetofit==None) or (movetofit.lower() in ['n','no']):
					return
				else:
					pass
					#s="ACCEPTFINDPEAK"  #moves to fit position
					#fpt=SimpleQueuedCommand(s)
					#fpt.run()					
			
			
			s="ACCEPTFINDPEAK"  #moves to fit position
			fpt=SimpleQueuedCommand(s)
			fpt.run()
	
	def correct_lattice(self,dspacing,lattice_parameter):
		s="ask GETFITRESULTS getnewlattice" #gets dspacing assuming a is zero
		fpt=SimpleImmediateCommand(s)
		fpt.run()
		lattice_constant=float(dspacing)*float(fpt.result.split(':')[-1])
		print 'lattice constant',lattice_constant
		#assume lattice constant is 'a','b','c'
		s="CorrectLattice %s -%s"%(str(dspacing),lattice_parameter)
		fpt=SimpleQueuedCommand(s)
		fpt.run()
		
		
		
		
	def scan_peak(self,device,scanrange,step,duration,tol=1e-4,apflag=True):
		"""scan device for scan range.  Move to center of peak.  If center of peak is
		outside of tolerance of center position of scan, then set the software zero of 
		the device to the new position of the peak"""
		
		#print 'doing scan'
		if apflag==True and ((device in self.counting_devices) or (device in self.environmental_devices)):
			print 'cannot redefine the zero for counting and environmental devices'
			return
		print 'device', self.get_device_value(device)
		original_position=float(self.get_device_value(device))
		s="findpeak %s %s %s "%(device,scanrange,step)
		durationf=float(duration)
		if durationf > 0:
			s=s+"Monitor %s Detector -func Gauss"%(str(abs(durationf)),) #should make detector a flag
		else:
			s=s+"Time %s Detector -func Gauss"%(str(abs(durationf)),)
		fp=SimpleQueuedCommand(s)
		fp.run()
		if not apflag:
				movetofit=raw_input('Move to Peak position [y/n]? ')
				if (movetofit==None) or (movetofit.lower() in ['n','no']):
					return
				else:
					s="ACCEPTFINDPEAK"  #moves to fit position
					fpt=SimpleQueuedCommand(s)
					fpt.run()
					return
		
		
		s="ACCEPTFINDPEAK"  #moves to fit position
		fpt=SimpleQueuedCommand(s)
		fpt.run()
		new_position=float(self.get_device_value(device))
		#print 'old %3.5g new %3.5g tol %3.5g'%(original_position,new_position,tol)
		if abs(original_position-new_position)>float(tol):
			print 'redefining %s %3.5g to %3.4g '%(device,original_position,new_position)
			self.set_device_software(device,str(new_position))
		else:
			print 'new position is within tolerance of old position'
	    
	def scanIsPresent(self,scan):
		"""Checks if scan is present"""
		ispresent=False
		
		return ispresent
	    
	def sequenceIsPresent(self, sequence):
		"""Checks if sequence is present"""
		ispresent=False
		
		return ispresent
	
	def moveq(self,q,omega,etype,efixed):
		if efixed==None:
			device='ei'
			realdevice=self.controller.getAllDevices(device)[0]
			efixed=[realdevice.getCurrValue()]
		s="Q %s %s %s %s %s %s"%(omega,etype,efixed[0],q[0],q[1],q[2])
		#print 'moving',s
		fpt=SimpleQueuedCommand(s)
		fpt.run()
	def movebragg(self,device1,device2,position):
		s="MoveBragg %s %s %s"%(device1,position,device2)
		#print 'moving',s
		fpt=SimpleQueuedCommand(s)
		fpt.run()
		

	def qscan(self,qi,qf,qstep,monitor):
		s="qscan %s %s %s %s %s %s %s %s %s %s"%(qi[0],qi[1],qi[2],qf[0],qf[1],qf[2],monitor,qstep[0],qstep[1],qstep[2])
		fpt=SimpleQueuedCommand(s)
		fpt.run()
			
	def howlong_scan(self,scanlist,overhead=0.0,timeflag='-s'):
		"""Checks howlong a list of scans will take"""
		#If flag is set, we should calculate from current position in the running scan"""
		#Shall we sum the result?
		present_scans=self.present_scans
		matched_scans=self.match(present_scans,scanlist)
		#print 'present_scans', present_scans
		#print 'matched_scans', matched_scans
		for scan in matched_scans:
			hl=GetHowlong(scan,overhead=0.0,timeflag='-s')
			hl.run()
			duration=hl.howlong
			#units='hours'
			#print 'duration',duration
			#if timeflag=='-s':
			#	units='seconds'
			#s='duration of %s is %s %s'%(scan,str(duration),units)
			#print s
			

	def howlong_now(self,sequencelist,overhead=0.0,timeflag='-s'):
		"""Checks howlong a sequence will take"""
		#If flag is set, we should calculate based on current position in the running scan"""
		myrate=Rate()
		myrate.run()
		sq=SimpleImmediateCommand('stack howlong -o %s %s'%(str(overhead),timeflag))
		sq.run()			
			
	    
	def howlong_sequence(self,sequencelist,overhead=0.0,timeflag='-s'):
		"""Checks howlong a sequence will take"""
		#If flag is set, we should calculate based on current position in the running scan"""
		myrate=Rate()
		myrate.run()
		present_sequences=self.present_sequences
		matched_sequences=self.match(present_sequences,sequencelist)
		#Should add parsing for allowed sequences and perhaps even check extensions for people
		for sequence in matched_sequences:
			#print 'sequence',sequence,overhead,timeflag
			sq=SimpleImmediateCommand('sequence howlong -o %s %s %s'%(str(overhead),timeflag,sequence))
			sq.run()
			#print 'result',sq.result
			
		      
			
	def isScan(self, scan):
		"""Checks to see if scan is a valid scan"""
		print 'checking if ', scan, 'isvalid'
		isvalid=False
		return isvalid
	    
	def isSequence(self, sequence):
		"""Checks to see if sequence is a valid sequence"""
		print 'checking if ', sequence, 'isvalid'
		isvalid=False
		return isvalid
	    
	    
	def scanop(self, scanlist,myparseobj):
		"""For the scans in scanlist, sets the parameters to the given set of values"""
		present_scans=self.present_scans
		matched_scans=copy.deepcopy(self.match(present_scans,scanlist))
		#print 'present_scans', present_scans
		print 'matched_scans', matched_scans
		for scan in matched_scans:
			#print 'dry running ',scan
			getscandescription=GetScanDescription(scan)
			#print '1'
			getscandescription.run()
			#print '2'
			scan_description=getscandescription.scan_description
			#print 'scan_description', scan_description
			#print 'parseobj',myparseobj.__dict__['scanstr']
			new_scan_description=scanparser.driver(scan_description,copy.deepcopy(myparseobj))
			
			print 'new_scan\n',new_scan_description
			scanName=scan+'_tmp'
			#print 'listing'
			scanDesrToListCommand = ScanDescrToListCommand(scanName,new_scan_description)
			#print 'listed'
			scanDesrToListCommand.run()
			scandryrun = ScanDryRunCommand(scanName)
			scandryrun.run()
			print 'result',scandryrun.result
			if str(scandryrun.result).find('unknown scan') >=0:
				print 'epic fail.  Your scan operation was unsuccessful.  Sorry...'
				self.deleteScanFromScanList(scanName)
			else:
				self.deleteScanFromScanList(scanName)
				scanDesrToListCommand = ScanDescrToListCommand(scan,new_scan_description)
				scanDesrToListCommand.run()
				
			#print scan,' dry ran'   
			
			#scanDesrToListCommand = ScanDescrToListCommand(scan,new_scan_description)
			#scanDesrToListCommand.run()
			
		
		
		
		
		
		#self.send_command("Scan ListDescr "+self.Title)
		#for scan in scanlist:
		
		return
	    
	def run_asynchronous(commandstr):
		mycommand=StackAddCommand(commandstr)
		mycommand.runAsynchronous()
		return mycommand.commandID
	    
	def run_synchronous(commandstr):
		mycommand=StackAddCommand(commandstr)
		mycommand.run()
		return mycommand.commandID
		
	    
	def monitor_rate(self):
		"""Prints the monitor rate"""
		print 'calculating rate'
		myrate=Rate()
		myrate.run()
		#sys.stderr.write(myrate.rate)
		#commandstr='rate'
		#mycommand=StackAddCommand(commandstr)
		#print 'commanding'
		#mycommand.runAsynchronous()
		#print 'commanded'
		#myid=mycommand.commandID
		#print 'id'
		#sys.stderr.write('monitor rate is '+str(mrat)+'\n')
		
	    
	    
	    
	    
		    
    
    
class CmdLineApp(Cmd):
	multilineCommands = ['orate']
	Cmd.shortcuts.update({'&': 'speak'})
	maxrepeats = 3
	Cmd.settable.append('maxrepeats')
	prompt='(icep) '
	use_rawinput=True
	completekey='tab'
	intro="Welcome to the icep interpereter.  For a list of commands, type 'help'"
	
	def precmd(self,line):
		if len(line)==0:
			line='help\n'
		return line
	def postcmd(self,stop,line):
		#print 'stop', stop
		#print 'line', line
		return stop
	
	def postloop(self):
		pass
		#print 'post'
		#java.lang.system.exit(0)
	
	
    #    @options([make_option('-p', '--piglatin', action="store_true", help="atinLay"),
    #              make_option('-s', '--shout', action="store_true", help="N00B EMULATION MODE"),
    #              make_option('-r', '--repeat', type="int", help="output [n] times")
    #              ])
    
    
    
	def do_ct(self, arg, opts=None):
		"""counts for [duration]  If duration is >0, counts by neutrons.
		If duration <=0, counts by time.  
		usage:  ct [duration]
		example:  ct -2 
		cts for 2 seconds
		"""
		try:
			duration=int(arg)
			devices=Devices()
			devices.count(duration)
		except:
			print 'the argument to count must be an integer!'
		   
	    
	    #args=arg.split()
	    #self.stdout.write(args)
	    #for i in range(min(repetitions, self.maxrepeats)):
	    #self.stdout.write('\n')
		# self.stdout.write is better than "print", because Cmd can be
		# initialized with a non-standard output destination
    
	do_count = do_ct     # now "count" is a synonym for "ct"
	
	def do_mrat(self,arg,opts=None):
		"""Returns the monitor rate
		usage: mrat
		example: mrat
		"""
		devices=Devices()
		devices.monitor_rate()
		
	rate=do_mrat #alias rate to mrat
	    
    
	def do_fix(self, arg,opts=None):
		"""This commmand freezes a list of devices.  Use rel to release the devices.  
		usage:  fix <devices>
		ex: fix a3 a4
		fixes motors a3 and a4
		ex: fix a?
		fixes devices a1,a2,a3,a4,a5,a6,an,etc.
		"""
		args=arg.split()
		#self.stdout.write(args)
		#self.stdout.write('\n')
		#print args
		devices=Devices() 
		devices.fix(args)  #fix the following devices  
	    
	def do_rel(self, arg,opts=None):
		"""This commmand releases a list of devices.  
		usage:  rel <devices>
		example: rel a3 a4
		releases devices a3 and a4
		"""
		args=arg.split()
		#self.stdout.write(args)
		#self.stdout.write('\n')
		devices=Devices() 
		devices.release(args)  #fix the following devices 
	    
    
	    
    
	
	def do_activate(self,arg,opts=None):
		"""This command activates a list of devices
		usage: activate <devices>
		ex: activate psd  
		"""
		#currently I think is only useful for flippers and psd
		pass
	
	def do_deactivate(self,arg,opts=None):
		"""This command deactivates a list of devices
		usage: deactivate <devices>
		ex: deactivate psd  
		"""
		#currently I think is only useful for fippers and psd
		pass
	    
     
	def parse_move(self,args,relative=False):
		"""Parse the move command"""
		#args=arg.split()
		if len(args) <2:
			self.stdout.write('Sorry, you need to specify both a device and a position you wish to drive to.')
			self.stdout.write('\n')
		else:
			device_list=[]
			position_list=[]
			myFlag=True
			for i in range(len(args)):
				if i%2!=0:
					try:
						position_list.append(float(args[i]))
					except ValueError:
						self.stdout.write('Sorry, your second argument must be a number.')
						self.stdout.write('\n')
						myFlag=False
						break
				else:
					device_list.append(args[i])
			if myFlag:
				devices=Devices()
				if relative:
					devices.move(device_list,position_list,moveflag=True)
				else:
					devices.move(device_list,position_list)
			
	
	def do_mv(self,arg,opts=None):
		""""This command moves a device to a given position.
		usage: mv <device> <position>
		ex:mv a3 4
		ex:mv temp 30
		ex:mv a3 4 a4 2.0
		"""
		args=arg.split()
		#devices=Devices()
		parser = argparse.ArgumentParser(description='Move devices')
		parser.add_argument('targets',nargs='*', help='devices and positions')
		parser.add_argument('-r', action='store_true', help='relative')
		myargs = parser.parse_args(args)
		#print 'relative',myargs.r
		self.parse_move(myargs.targets,relative=myargs.r)
	    
#	def do_mvr(self,arg,opts=None):
#		""""This command moves a device by the given increment.
#		usage: mv <device> <position>
#		ex:mvr a3 4
#		ex:mvr temp 30
#		ex:mvr a3 4 a4 2.0
#		"""						
#		self.parse_move(arg,relative=True)
	    
	def do_mvt(self,arg,opts=None):
		""""This command moves two devices in a theta two theta fashion.
		usage: mvt <device1> <position> <device2>
		ex:mvt a4 32
		ex:mvt a6 41.177
		ex:mvt a2 41.177 a1
		"""
		devices=Devices()
		args=arg.split()
		if len(args)<2:
			print 'two few arguments'
			return
		elif len(args)==2:
			device1=args[0]
			if device1.lower()=='a4':
				device2='a3'
			elif device1.lower()=='a6':
				device2='a5'
			else:
				print "Sorry, I am not yet smart enough to guess the 2nd device"
				return
		else:
			device1=args[0]
			device2=args[2]
		position=args[1]
		devices.movebragg(device1,device2,position)
			
		
	    
    
	    
	    
	def do_fixed(self,arg,opts=None):
		"""This command prints a list of the fixed devices.
		usage: fixed
		ex:fixed
		
		"""
		devices=Devices()
		fixed_devices=devices.fixed_devices
		for device in fixed_devices:
			print str(device), 'is fixed'
		#TODO maybe find fixed devices by regex?
	
	def do_p(self,arg,opts=None):
		"""This command prints a list of software and hardware angles
		usage:pa <devices>
		ex:p a?
		ex:p tem*
		"""
		devices=Devices()
		args=arg.split()
		if len(args)>0:
			devices.pr(args,flag='all')
		else:
			args=['*']
			devices.pr(args,flag='all')
		
	do_pa=do_p #alias pa to p 
	def do_psa(self,arg,opts=None):
		"""This command prints a list of software angles
		usage:pa <devices>
		ex:psa a?
		ex:psa a*
		"""
		devices=Devices()
		args=arg.split()
		if len(args)>0:
			devices.pr(args,flag='software')
		else:
			args=['*']
			devices.pr(args,flag='software')
	    
	def do_pha(self,arg,opts=None):
		"""This command prints a list of hardware angles
		usage:pa <devices>
		ex:pha a?
		ex:pha a*
		"""
		devices=Devices()
		args=arg.split()
		if len(args)>0:
			devices.pr(args,flag='hardware')
		else:
			args=['*']
			devices.pr(args,flag='hardware')
	    
	def do_pz(self,arg,opts=None):
		"""This command prints a list of zero angles
		usage:pz <devices>
		ex:pz a?
		ex:pz a*
		"""
		devices=Devices()
		args=arg.split()
		if len(args)>0:
			devices.pr(args,flag='zeros')
		else:
			args=['*']
			devices.pr(args,flag='zeros')
	
	    
	def do_pu(self,arg,opts=None):
		"""This command prints a list of upper limits
		usage:pu <devices>
		ex:pu a?
		ex:pu a*
		"""
		devices=Devices()
		args=arg.split()
		if len(args)>0:
			devices.pr(args,flag='upper')
		else:
			args=['*']
			devices.pr(args,flag='upper')
	    
	def do_pl(self,arg,opts=None):
		"""This command prints a list of lower limits
		usage:pu <devices>
		ex:pl a?
		ex:pl a*
		"""
		devices=Devices()
		args=arg.split()
		if len(args)>0:
			devices.pr(args,flag='lower')
		else:
			args=['*']
			devices.pr(args,flag='lower')
	
	def do_lo(self,arg,opts=None):
		"""This command sets the lower limit for a device
		usage:lo <device> <value>
		ex:lo a3 5
		ex:lo a4 4
		"""
		devices=Devices()
		args=arg.split()  #need to error check
		value=args[1]
		device=args[0]
		devices.set_lower_limit(device,value)
	
	def do_up(self,arg,opts=None):
		"""This command sets the upper limit for a device
		usage:up <device> <value>
		ex:up a3 5
		ex:up a4 4
		"""
		devices=Devices()
		args=arg.split()
		value=args[1]
		device=args[0]
		devices.set_upper_limit(device,value)
	    
	def do_init(self,arg,opts=None):
		"""This command initializes the hardware value for a device
		usage: init <device> value
		ex: init a3 3
		"""
		devices=Devices()
		args=arg.split()
		value=args[1]
		device=args[0]
		devices.set_device_hardware(device,value)
	
	def do_def(self,arg,opts=None):
		"""This command sets the software value for a device
		usage: def <device> <value>
		ex:  def a3 3
		"""
		#Should have access levels!!!
		devices=Devices()
		args=arg.split()
		value=args[1]
		device=args[0]
		devices.set_device_software(device,value)
		    
	def do_rs(self,arg,opts=None):
		"""This command runs a set of scans
		usage:rs <scans>
		ex:rs tsca*
		ex:rs tsca[0-9]
		"""
		#should we also support rs scan1 scan2?
		devices=Devices()
		args=arg.split()
		if len(args)==0:
			print 'I need to know which scan to run!'
		else:
			devices.run_scans(args)
    
	do_run=do_rs #alias run to rs for ice users
	    
	def do_rsf(self,arg,opts=None):
		"""This command runs a list of sequence files
		usage:rsf <sequence files>
		ex:rsf myseq*
		"""
		
		devices=Devices()
		args=arg.split()
		if len(args)==0:
			print 'I need to know which sequence to run!'
		else:
			devices.run_sequence(args)
	    
	def do_drs(self,arg,opts=None):
		"""This command dry runs a set of scans
		usage: drs <scan list>
		ex:drs tsca*
		"""
		devices=Devices()
		args=arg.split()
		if len(args)==0:
			print 'I need to know which scan to dry run!'
		else:
			devices.dry_run_scans(args)
	    
	def do_drsf(self,arg,opts=None):
		"""This command dry runs a set of sequence files
		usage: drsf <sequence file list>
		ex:drsf myseq[0-4]
		"""
		devices=Devices()
		args=arg.split()
		if len(args)==0:
			print 'I need to know which sequence to dry run!'
		else:
			devices.dry_run_sequences(args)
	    
	def do_apt(self,arg,opts=None):
		"""
		This command scans a4 and a3 in a 2:1 fashion.  It moves to the center position of the scan and 
		uses the center position to calculate the lattice constant.
		usage:apt <device> <range> <step> <duration> <dspacing>
		ex:apt a4 3 .2 -1 1.4142
		"""
		args=arg.split()
		
		devices=Devices()
		if len(args)<4:
			print "you have too few arguments"
			
		device=args[0]
		scanrange=args[1]
		step=args[2]
		duration=args[3]
		if len(args)==4:
			dspacing=1.0
		else:
			dspacing=args[4]
			
		devices.scan_peak_th2th(device,scanrange,step,duration,dspacing,aptflag=True)
		
	def do_fpt(self,arg,opts=None):
		"""
		This command scans a4 and a3 in a 2:1 fashion.  
		usage:fpt <device> <range> <step> <duration>
		ex:fpt a4 3 .2 -1 
		"""
		args=arg.split()
		
		devices=Devices()
		if len(args)<4:
			print "you have too few arguments"
			
		device=args[0]
		scanrange=args[1]
		step=args[2]
		duration=args[3]
		dspacing=str(1.0)
		devices.scan_peak_th2th(device,scanrange,step,duration,dspacing,aptflag=False)
	    

	def do_latt(self,arg,opts=None):
		"""
		This command updates the lattice constant based on the last findpeak command run, 
		a user supplied dspacing, and the lattice parameter to update.  If no dspacing is provided, it
		will default to 1.0
		usage:latt <lattice_parameter> <dspacing>
		ex:latt a 2.0
		ex:latt a
		"""
		args=arg.split()
		
		devices=Devices()
		if len(args)<1:
			print "you have too few arguments"
			return
			
		lattice_parameter=args[0]
		if len(args)==1:
			dspacing=1.0
		else:
			dspacing=args[1]
			
		devices.correct_lattice(dspacing,lattice_parameter)
	    
	    
	    
	    
	def do_ap(self,arg,opts=None):
		"""
		This command scans a device, fits the scan, and then moves to the center of the fit of the scan.
		If this center is within tolerance of the center of the scan, it does nothing.  Otherwise,
		it redefines the software angle of the current position to be the center of the scan. If
		tolerance is not specified, it defaults to 0.01
		usage:ap <device> <range> <step> <duration> <tolerance>
		ex:ap a3 3 .1 -1 
		ex:ap a3 3 .1 -1 .02
		"""
		args=arg.split()
		devices=Devices()
		#parser = argparse.ArgumentParser(description='Frabble the foo and the bars')
		#parser.add_argument('-f', action='store_true', help='frabble the foos')
		#parser.add_argument('scans', nargs='+', help='a bar to be frabbled')
		#myargs = parser.parse_args(arg.split())
		#isFile=myargs.f
		#isSeconds=myargs.s
		#print args
		if len(args)<4:
			sys.stderr.write('too few arguments.  Type help ap for command description\n')
		else:
			device=args[0]
		for i in range(1,len(args)):
			try:
				val=float(args[i])
			except ValueError:
				sys.stderr.write('Values must be numbers.\n')
				return
		scanrange=args[1]
		step=args[2]
		duration=args[3]
		tolerance=0.01
		count_type='Time'
		if float(args[3])>0:
			count_type='Monitor'
		if len(args)==5:
			tolerance=float(args[4])
		    
		#print scanrange, step, duration, count_type, tolerance
		devices.scan_peak(device,scanrange,step,duration,tol=tolerance,apflag=True)
	
	def do_fp(self,arg,opts=None):
		"""
		This command scans a deviceand  fits the scan.
		usage:fp <device> <range> <step> <duration> 
		ex:fp a3 3 .1 -1 
		"""
		args=arg.split()
		devices=Devices()
		#parser = argparse.ArgumentParser(description='Frabble the foo and the bars')
		#parser.add_argument('-f', action='store_true', help='frabble the foos')
		#parser.add_argument('scans', nargs='+', help='a bar to be frabbled')
		#myargs = parser.parse_args(arg.split())
		#isFile=myargs.f
		#isSeconds=myargs.s
		#print args
		if len(args)<4:
			sys.stderr.write('too few arguments.  Type help fp for command description\n')
		else:
			device=args[0]
		for i in range(1,len(args)):
			try:
				val=float(args[i])
			except ValueError:
				sys.stderr.write('Values must be numbers.\n')
				return
		scanrange=args[1]
		step=args[2]
		duration=args[3]
		tolerance=0.01
		#count_type='Time'
		#if float(args[3])>0:
		#	count_type='Monitor'
		#if len(args)==5:
		#	tolerance=float(args[4])
		    
		#print scanrange, step, duration, count_type, tolerance
		devices.scan_peak(device,scanrange,step,duration,tol=1e-4,apflag=False)
		
		
	def do_ice(self,arg,opts=None):
		"""
		This command runs an ice command.  It will first try to run it as an immediate command.  If this fails,
		it will try it as a queued command.  For a queued command, you may see the result twice.
		usage:ice <command> 
		ex:ice move a3 4 a5 6 
		"""
		args=arg.split()
		
		#devices=Devices()
		try:
			#print 'immediate'
			command=SimpleImmediateCommand(arg)
			command.run()
			#print 'immediate result',command.result
			if not str(command.result).find('Command not allowed')==-1:
				#print 'queued'
				command=SimpleQueuedCommand(arg)
				command.run()
			print command.result
		except:
			pass
		
	def do_scanq(self,arg,opts=None):
		"""
		This command scans q at the current Ei and Ef
		usage:scanq <monitor> --h <hi> <hstep> <hf> --k <ki> <kstep> <kf> --l <li> <lstep> <lf> 
		ex:scanq 1 --h 1 .1 2 --k 1 .1 2 
		"""
		args=arg.split()
		devices=Devices()
		parser = argparse.ArgumentParser(description='Frabble the foo and the bars')
		parser.add_argument('mon', nargs=1, help='monitor')
		parser.add_argument('--h', nargs=3, help='hi hstep hf')
		parser.add_argument('--k', nargs=3, help='ki kstep kf')
		parser.add_argument('--l', nargs=3, help='li lstep lf')
		myargs = parser.parse_args(args)
		h=myargs.h
		k=myargs.k
		l=myargs.l
		monitor=myargs.mon[0]
		if h==None and k==None and l==None:
			print 'you must choose a scan direction!'
			return
		if h==None:
			h=[0,0,0]
		if k==None:
			k=[0,0,0]
		if l==None:
			l=[0,0,0]
		h=[str(i) for i in h]
		k=[str(i) for i in k]
		l=[str(i) for i in l]
		#print monitor,h,k,l
		qi=   [h[0],k[0],l[0]]
		qstep=[h[1],k[1],l[1]]
		qf=   [h[2],k[2],l[2]]
		devices.qscan(qi,qf,qstep,monitor)
		
	def do_dq(self,arg,opts=None):
		"""
		This command moves to the supplied q position.  Optionally, the user can set an energy transfer.
		usage:dq <h> <k> <l> -ei -ef -w <energy_transfer> -efixed <value of fixed energy> 
		ex:dq 1 0 0 
		ex:dq 1 0 0 -ei -w 3 -efixed 13.7
		ex:dq 1 0 0 -ei -w 3
		"""
		args=arg.split()
		devices=Devices()
		parser = argparse.ArgumentParser(description='Frabble the foo and the bars')
		parser.add_argument('q', nargs=3, help='h k l')
		parser.add_argument('-ef', action='store_true', help='fixed energy is ef')
		parser.add_argument('-ei', action='store_true', help='fixed energy is ei')
		parser.add_argument('-w', nargs=1, help='energy transfer')
		parser.add_argument('-efixed', nargs=1, help='fixed energy')
		myargs = parser.parse_args(args)
		q=myargs.q
		ef=myargs.ef
		ei=myargs.ei
		omega=myargs.w
		efixed=myargs.efixed
		
		if ei and ef:
			print 'you should only have one fixed energy'
			return
		if not(omega==None):
			if (not ei) and (not ef):
				print 'if you give an energy transfer, I need to know whether ei or ef is fixed'
				return
		if omega==None:
			omega=[str(0.0)]
			etype='i'
		if ei:
			etype='i'
		else:
			etype='f'
			
		
		devices.moveq(q,omega[0],etype,efixed)
	    
	    
	def do_scanop(self,arg,opts=None):
		"""
		This command takes a list of scans and changes a set of parameters in these scans.
		For a list of parameters type 'scanop -h'.  Generally, for any moving device you may use it as a scan parameter.
		There is relatively little error checking on the arguments, so it is possible this will corrupt your scan, so I
		suggest you save a backup and test it first.  Especially if you plan to use it in a sequence!!!!  The things that I
		do check for is if your parameter is consistent with the original form of the scan.  So, for example, if you add a new
		range, it should have all the parameters necessary to define a scan (for example, initial, final, npts.  If you are modifying
		and existing range, then you should check that your parameters are consistent.  For example, if the original scan defined
		h_center, h_step, and npts.  Then don't add a h_final parameter.  The resulting scan will be ambiguous.  Use the -delete <prange>
		delete the offending ranges.  I will first delete them, then attempt to add your new ranges.
		usage:scanop <scanlist> <-parameter name> <parameter value> <-parameter name> <parameter value>
		ex:scanop scan[1-5] tscan* -h_i 1.0 h_f 1.0 -prefac 2
		ex:scanop scanb* -temp_i 200 -a3_i 32.3
		ex:scanob scanb* -temp_i 200 -delete h_i h_f -npts 3 -h_c 4 to change from and initial step final scan to a center step npts scan
		"""
		args=arg.split()
		devices=Devices()
		parser = argparse.ArgumentParser(description='Frabble the foo and the bars')	
		parser.add_argument('scans', nargs='+', help='scans to be modified')
		parser.add_argument('-delete', nargs='+', help='scan ranges to be deleted')		
		parser.add_argument('-title', nargs=1, help='title of the scan')
		parser.add_argument('-type',choices='01256789',nargs=1, help='title')
		parser.add_argument('-ef', action='store_true', help='fixed energy is ef')
		parser.add_argument('-ei', action='store_true', help='fixed energy is ei')		
		parser.add_argument('-fixede', type=float, nargs=1, help='value of fixed energy')
		parser.add_argument('-counts', type=int, nargs=1, help='number of counts for the point')
		parser.add_argument('-counttype', nargs=1, help='device used to count')
		parser.add_argument('-detectortype', nargs=1, help='device used to accumulate data.  Used only for xpeek and metadata in file')
		parser.add_argument('-prefac',type=int, nargs=1, help='gives a multiplication factor for the number of counts')
		parser.add_argument('-npts',type=int, nargs=1, help='number of points in the scan')
		#parser.add_argument('-dev', nargs=*, help='as an alternative to range, the comple list of values to be visited can be suppplied:  Dev=[device name]=value1 value2 value3...')
		parser.add_argument('-timeout', type=int,nargs=1, help='time after which the preset counter will be stopped regardless of whether it has reached its preset value')
		parser.add_argument('-holdpoint', type=int,nargs=1, help='holding time before the preset counter is started at each point of a scan')
		parser.add_argument('-holdscan',type=int, nargs=1, help='holding time before a preset counter is started for the first point of a scan')
		parser.add_argument('-comment', nargs=1, help='the user can enter a comment here')
		parser.add_argument('-filename', nargs=1, help='specifies a string to be added at the beginning of the data filename')
		#parser.add_argument('-q', nargs=3, help='h k l')
		parser.add_argument('-w_i', nargs=1, help='energy transfer initial')
		parser.add_argument('-w_c', nargs=1, help='energy transfer center')
		parser.add_argument('-w_f', nargs=1, help='energy transfer final')
		parser.add_argument('-w_s', nargs=1, help='energy transfer step')
		parser.add_argument('-h_i', nargs=1, help='h initial')
		parser.add_argument('-h_c', nargs=1, help='h center')
		parser.add_argument('-h_f', nargs=1, help='h final')
		parser.add_argument('-h_s', nargs=1, help='h step')
		parser.add_argument('-k_i', nargs=1, help='k initial')
		parser.add_argument('-k_c', nargs=1, help='k center')
		parser.add_argument('-k_f', nargs=1, help='k final')
		parser.add_argument('-k_s', nargs=1, help='k step')
		parser.add_argument('-l_i', nargs=1, help='l initial')
		parser.add_argument('-l_c', nargs=1, help='l center')
		parser.add_argument('-l_f', nargs=1, help='l final')
		parser.add_argument('-l_s', nargs=1, help='l step')
		present_devices=devices.present_devices
		omitted=['h','k','l','hkl','e','qx','q(x)','q(y)','qz','q(z)']
		for dev in present_devices:
			if not (dev in omitted):
				parser.add_argument('-%s_i'%(dev,), nargs=1, help=argparse.SUPPRESS)#, help='%s initial'%(dev,))
				parser.add_argument('-%s_c'%(dev,), nargs=1, help=argparse.SUPPRESS)#, help='%s center'%(dev,))
				parser.add_argument('-%s_f'%(dev,), nargs=1, help=argparse.SUPPRESS)#, help='%s final'%(dev,))
				parser.add_argument('-%s_s'%(dev,), nargs=1, help=argparse.SUPPRESS)#, help='%s step'%(dev,))
		#print 'parsing'
		myargs = parser.parse_args(args)
		#print 'parsed'
		
		
		#print 'myargs',myargs.__dict__.keys()
		#print 'myargs',myargs.__dict__['psdc14_s']
		#print 'myargs',myargs.psdc14_s
		devices.scanop(myargs.scans,myargs)
		
		#q=myargs.q
		#ef=myargs.ef
		#ei=myargs.ei
		#omega=myargs.w
		#efixed=myargs.efixed
		if 0:
			paramlist=args[1].split()
			if len(paramlist)%2!=0:
				sys.stderr.write('there must be an equal number of parameters and values.\n')
				return
		    #Actually, let the server process this, because if someone wants to change a comment, the parameter need not be numeric
		    #for i in range(0,len(paramlist),2):
		    #    try:
		    #        float(paramlist[i])
		    #    except ValueError:
		    #        sys.stderr.write('parameter values must be numbers.\n')
		    
		
	    
	    
	def do_howlong(self,arg,opts=None):
		"""
		This command tells howlong a scan or file will take to execute.  Use the -f flag to
		denote a sequence file.  Use the -s flag to get the result in seconds.  Use -now
		to get the time from the current position
		usage: howlong -f <scan> -s  -now
		ex:howlong -f -s -now sequence1
		"""
		args=arg.split()
		#flags=opts.split()
		parser = argparse.ArgumentParser(description='Frabble the foo and the bars')
		parser.add_argument('-f', action='store_true', help='frabble the foos')
		parser.add_argument('-s', action='store_true', help='frabble the foos')
		parser.add_argument('-now', action='store_true', help='frabble the foos')
		parser.add_argument('scans', nargs='*', help='a bar to be frabbled')
		parser.add_argument('-o', nargs=1, help='frabble the foos')
		myargs = parser.parse_args(arg.split())
		isFile=myargs.f
		isSeconds=myargs.s
		isNow=myargs.now
		scans=myargs.scans
		overhead=myargs.o
		#print 'isFile',isFile
		#print 'isSeconds',isSeconds
		#print 'isNow',isNow
		#print 'scans',scans
		#print 'overhead',overhead
		if overhead==None:
			overhead=[0.0]
		devices=Devices()
		#args=arg.split()
		if (not isFile) and (not isNow):
			if isSeconds:
				devices.howlong_scan(args,overhead=overhead[0],timeflag='-s')
			else:
				devices.howlong_scan(args,overhead=overhead[0],timeflag='')
		elif (isFile) and (not isNow):
			if isSeconds:
				devices.howlong_sequence(args,overhead=overhead[0],timeflag='-s')
			else:
				devices.howlong_sequence(args,overhead=overhead[0],timeflag='')		
		elif (not isFile) and (isNow):
			if isSeconds:
				devices.howlong_now(args,overhead=overhead[0],timeflag='-s')
			else:
				devices.howlong_now(args,overhead=overhead[0],timeflag='')
			
			
			
			
			
				
	    
	    
	    
	def do_dqt(self, arg,opts=None):
		""""Converts q to two theta given q in Angstrom^-1 and the wavelength in Angstroms.
		    usage:dqt <q> <wavelength>
		    example:dqt 1.5 2.35916
		"""
		args=arg.split()
		if len(args)<3:
			print __doc__
		else:
			try:
				q=float(args[0])
				wavelength=float(args[1])
				tth=math.degrees(math.asin(q*wavelength/4/pi))
				sys.stdout.write('%f\n'%(tth,))
			except ValueError:
				sys.stdout.write("wavelength and q must be numbers.\n")
		    
     
	def do_dtq(self, arg,opts=None):
		""""Converts two theta to q in Angstrom^-1 given two theta in degrees and the wavelength in Angstroms.
		    usage:dtq <two theta> <wavelength>
		    example:dtq 40.0 2.35916
		"""
		args=arg.split()
		if len(args)<3:
			print __doc__
		else:
			try:
				tth=float(args[0])
				wavelength=float(args[1])
				q=4*pi*sin(tth)/wavelength
				sys.stdout.write('%f\n'%(q,))
				
			except ValueError:
				sys.stdout.write("wavelength and tth must be numbers.\n")
			    
			except ZeroDivisionError:
				sys.stdout.write('wavelength cannot be zero!\n')
		    
	def do_we(self, arg,opts=None):
		""""Converts wavelength in Angstroms to energy in meV.
		    usage:we <wavelength>
		    example:we 2.35916
		"""     
		args=arg.split()
		if len(args)<1:
			print __doc__
		else:
			try:
				wavelength=float(args[0])
				sys.stdout.write('wavelenth %5.3f\n'%(wavelength,))
				#sys.stdout.write(args[0]+'\n')
				#sys.stdout.write(args[1]+'\n')
				#sys.stdout.write(args[2]+'\n')
				#sys.stdout.write(args[3]+'\n')
				#sys.stdout.write(str(len(args))+'\n')
				
				energy=81.81/wavelength**2
				sys.stdout.write('%5.3f\n'%(energy,))
			except ValueError:
				sys.stdout.write("wavelength must be a number.\n")
			except ZeroDivisionError:
				sys.stdout.write('wavelength cannot be zero!\n')
    
    
	def do_ew(self, arg,opts=None):
		""""Converts energy in meV to wavelength in Angstroms
		    usage:ew <energy>
		    example:ew 2.35916
		"""     
		args=arg.split()
		if len(args)<1:
			print __doc__
		else:
			try:
				energy=abs(float(args[0]))
				wavelength=9.045/math.sqrt(energy)
				sys.stdout.write('%f\n'%(wavelength,))
			except ValueError:
				sys.stdout.write("energy must be a number.\n")
			except ZeroDivisionError:
				sys.stdout.write('energy cannot be zero!\n')
    
	def do_ds(self, arg,opts=None):
		""""Given two theta in degrees and wavelength in Angstroms, calculates dspacing.
		    usage:ds <two theta> <wavelength>
		    example:ds 30 2.35916
		""" 
		args=arg.split()
		if len(args)<2:
			print __doc__
		else:
			try:
				wavelength=float(args[1])
				tth=math.radians(float(args[0]))
				dspacing=wavelength/2/math.sin(tth)
				sys.stdout.write('%f\n'%(dspacing,))
			except ValueError:
				sys.stdout.write("wavelength and dspacings must be numbers.\n")
			except ZeroDivisionError:
				sys.stdout.write('two theta cannot be zero!\n')
				
	
	    
    
    
#class TestMyAppCase(Cmd2TestCase):
#	CmdApp = CmdLineApp
#	transcriptFileName = 'exampleSession.txt'
#    
#	parser = optparse.OptionParser()
#	parser.add_option('-t', '--test', dest='unittests', action='store_true', default=False, help='Run unit test suite')
#	(callopts, callargs) = parser.parse_args()
#	if callopts.unittests:
#		sys.argv = [sys.argv[0]]  # the --test argument upsets unittest.main()
#		unittest.main()
#	else:
#		print 'calling'
#		app = CmdLineApp(stdin=sys.stdin, stdout=sys.stdout)
#		app.cmdloop()

if __name__=="__main__":
	app = CmdLineApp()
	res=app.cmdloop()
	#print 'res', res
	sys.exit()
	
