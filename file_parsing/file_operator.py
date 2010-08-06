#Author: Joe Redmon
#file_operator.py

from json_parser import read_standards
import scanparser3
import readncnr3
import numpy as np
import copy
from scipy import interpolate
def split_det(s):
    try:
        if s[0] == 'A' and int(s[1]) in range(1,7):
            return s
    except ValueError:
        pass
    
    for i in range(len(s)):
        if ord(s[i]) in range(48,58):
            return [s[:i], int(s[i:])-1]
    return s
class Standard:
    def __init__(self,units = 'unknown', epsilon = .0001, distinct = False, interpolatable = False, spectator = False, friends = None, plottable = None, metadata = False, _comment = None):
        self.units = units
        self.distinct = distinct
        self.interpolatable = interpolatable
        self.spectator = spectator
        self.friends = friends
        self.plottable = plottable
        self.metadata = metadata
        self._comment = _comment

class Data:
    def __init__(self,filename):
        self.data = []
        self.standards = read_standards()
        f = file(filename, 'r')
        t = []
        template = {}
        for s in self.standards:
            template[s] = [None]
            
        s = f.read()
        f.close()
        f = file(filename, 'r')

        if s[0] == '#':
            print 'hey'
            for lines in f:
                lines = lines.split()
                if len(lines) == 0:
                    continue
                if lines[0] == '#Columns':
                    t.append(lines[1:])
                    break
                else:
                    if lines[0][1:] in self.standards:
                        pass
                    else:
                        self.standards[lines[0][1:]] = Standard(metadata = True).__dict__
                    template[lines[0][1:]] = lines[1:] or [None]
            for lines in f:
                if lines[0] == '#': break
                t.append(lines.split())
            f.close()

            for s in t[0]:
                if s in self.standards:
                    self.standards[s]['metadata'] = False
                else:
                    self.standards[s] = Standard().__dict__
                    template[s] = [None]
            for i in range(1,len(t)):
                self.data.append(copy.copy(template))
                for j in range(len(t[0])):
                    try:
                        self.data[i-1][t[0][j]] = [float(t[i][j])]
                    except ValueError:
                        self.data[i-1][t[0][j]] = [t[i][j]]
            self.detectors = set(['Detector','_Detector'])
            for s in self.standards:
                if s[:8] == 'Analyzer' and s[-5:] == 'Group':
                    self.detectors = self.detectors | set(self.data[0][s])
                    for d in self.data[0][s]:
                        self.detectors.add('_' + d)
            for d in self.detectors:
                if d in self.standards and d[0] is not '_':
                    if '_' + d not in self.standards:
                        self.standards['_' + d] = Standard().__dict__
                        for p in self.data:
                            p['_' + d] = p[d]
                            
                            
        elif 'fpx' in filename or 'fpt' in filename and s[0] != '#':
            fields = []
            date = []
            first = True
            for lines in f:
                if first:
                    first = False
                    spl = lines.split()
                    for i in range(len(spl)):
                        try:
                            if int(spl[i]) in range(1,7):
                                fields.append('A'+spl[i])
                        except:
                            if spl[i] == 'Intensity':
                                fields.append('Detector')
                                date = spl[i+1:]
                                break
                    self.standards = {'Date': Standard(metadata = True).__dict__}
                    for s in fields:
                        self.standards[s] = Standard(metadata = False).__dict__
                else:
                    newdata = {}
                    spl = lines.split()
                    for i in range(len(spl)):
                        
                        try:    
                            newdata[fields[i]] = [float(spl[i])]
                        except:
                            pass
                    newdata['Date'] = date
                    self.data.append(newdata)
        else:
            reader = readncnr3.datareader()
            mydata = reader.readbuffer(filename)
            try:
                template['Collimations'] = [mydata.metadata['collimations']['coll1'],mydata.metadata['collimations']['coll2'],mydata.metadata['collimations']['coll3'],mydata.metadata['collimations']['coll4']]
                self.standards['Collimations'] = Standard(metadata = True).__dict__
            except:
                pass
            try:
                template['Lattice'] = [mydata.metadata['lattice']['a'],mydata.metadata['lattice']['b'],mydata.metadata['lattice']['c'],mydata.metadata['lattice']['alpha'],mydata.metadata['lattice']['beta'],mydata.metadata['lattice']['gamma']]
            except:
                pass
            
            try:
                for sl in mydata.metadata['count_info']:
                    inStandards = False
                    for s in self.standards:
                        if s.lower().split() == ''.join(sl.split('_')):
                            inStandards = True
                            template[s] = [mydata.metadata['count_info'][s]]
                    if not inStandards:
                        s = sl.split('_')
                        for i in range(len(s)):
                            s[i] = s[i].capitalize()
                        s = ''.join(s)
                        template[s] = [mydata.metadata['count_info'][s]]
                        self.standards[s] = Standard(metadata = True).__dict__
            except:
                pass
            try:
                template['MonoSpacing'] = [mydata.metadata['dspacing']['monochromator_dspacing']]
                template['AnaSpacing'] = [mydata.metadata['dspacing']['analyzer_dspacing']]
            except:
                pass
            try:
                template['FixedE'] = [mydata.metadata['energy_info']['efixed'], mydata.metadata['energy_info']['ef']]
            except:
                pass 
                        
            try:

                for sl in mydata.metadata['file_info']:
                    inStandards = False
                    for s in self.standards:
                        if s.lower().split().join('_') == sl:
                            inStandards = True
                            template[s] = [mydata.metadata['file_info'][s]]
                    if not inStandards:
                        s = sl.split('_')
                        for i in range(len(s)):
                            s[i] = s[i].capitalize()
                        s = ' '.join(s)
                        template[s] = [mydata.metadata['file_info'][s]]
                        self.standards[s] = Standard(metadata = True).__dict__
            except:
                pass
            try:
                template['HField'] = [mydata.metadata['magnetic_field']['hfield']]
                self.standards['HField'] = Standard(metadata = True).__dict__
            except:
                pass
            try:
                template['AnalyzerMosaic'] = [mydata.metadata['mosaic']['mosaic_analyzer']]
                self.standards['AnalyzerMosaic'] = Standard(metadata = True).__dict__
                template['MonochromatorMosaic'] = [mydata.metadata['mosaic']['mosaic_monochromator']]
                self.standards['MonochromatorMosaic'] = Standard(metadata = True).__dict__
                template['SampleMosaic'] = [mydata.metadata['mosaic']['mosaic_sample']]
                self.standards['SampleMosaic'] = Standard(metadata = True).__dict__
            except:
                pass
            try:
                template['Orient'] = [mydata.metadata['orient1']['h'], mydata.metadata['orient1']['k'],mydata.metadata['orient1']['l'],mydata.metadata['orient2']['h'],mydata.metadata['orient2']['k'], mydata.metadata['orient2']['l']]
            except:
                pass
            areMotors = True
            motors = []
            try:
                for i in range(6):
                    motors.append([mydata.metadata['motor'+str(1+i)]['start'], mydata.metadata['motor' + str(1+i)]['step']])
            except:
                #print mydata.metadata
                areMotors = False
            try:
                for p in mydata.data:
                    pcorr = p.split('_')
                    for i in range(len(pcorr)):
                        pcorr[i] = pcorr[i].capitalize()
                    pcorr = ''.join(pcorr)

                    if pcorr not in self.standards and pcorr not in ['Qx','Qy','Qz','Counts']:
                        self.standards[pcorr] = Standard(metadata = False).__dict__
                count = 0
                while(True):
                    print 'hey'
                    try:
                        newdata = copy.copy(template)
                        for p in mydata.data:
                            pcorr = p.split('_')
                            for i in range(len(pcorr)):
                                pcorr[i] = pcorr[i].capitalize()
                            pcorr = ''.join(pcorr)
                            if pcorr[0] == 'Q':
                                if pcorr[1] == 'x':
                                    pcorr = 'QX'
                                elif pcorr[1] == 'y':
                                    pcorr = 'QY'
                                elif pcorr[1] == 'z':
                                    pcorr = 'QZ'
                            if pcorr == 'Counts':
                                pcorr = 'Detector'
                            newdata[pcorr] = [mydata.data[p][count]]

                        if(areMotors):
                            for i in range(len(motors)):
                                newdata['A' + str(i+1)] = [motors[i][0] +  motors[i][1] * count]
                        self.data.append(newdata)
                        count+=1
                    except:
                        break
                        
                            
            except:
                pass
    def correct_scan(self):
        try:        
            if 'ScanDescr' in self.standards and self.standards['ScanDescr']['metadata']:
                scanstr = '' + self.data[0]['ScanDescr'][0]
                for s in self.data[0]['ScanDescr'][1:]:
                    scanstr += ' ' + s
                myparser = scanparser3.scanparser(scanstr)
                scanlc = myparser.get_varying()
                scan = []
                for s in self.standards:
                    if s.lower() in scanlc:
                        scan.append(s)
                self.standards['Scan'] = Standard(metadata = True).__dict__
                self.standards['ScanRanges'] = Standard(metadata = True).__dict__
                for p in self.data:
                    p['ScanRanges'] = scan
                    p['Scan'] = scan
        except:
            for p in self.data:
                    p['ScanRanges'] = ['QY']
                    p['Scan'] = ['QY']
            
    def write(self, filename):
        f = file(filename, 'w')
        f.write(self.__str__())
        f.close()
    def __str__(self):
        out = ''
        if len(self.data):
            for s in self.standards:
                if self.standards[s]['metadata']:
                    out += ('#' + s.ljust(11))
                    for val in self.data[0][s]:
                        out += (' ' + str(val))
                    out += ('\n')
            out += ('#Columns')
            field_order = self.standards.keys()
            field_order.sort()
            for i in field_order:
                if not self.standards[i]['metadata']:
                    out += (' ' + i.rjust(13))
            for p in self.data:
                out += ('\n        ')
                for i in field_order:
                    if not self.standards[i]['metadata']:
                        valstr = p[i][0]
                        for val in p[i][1:]:
                            valstr+='_' + val
                        out += (' ' + str(valstr).rjust(13))

        return out
    def interpolate_data(self, iv):
        self.data.sort(cmp = lambda x,y: cmp(x[iv][0],y[iv][0]))
        interpolaters = {}
        iv_vals = []
        for p in self.data:
            iv_vals.append(p[iv][0])
        for s in self.standards:
            if s in self.detectors:
                pts = []
                for p in self.data:
                    pts.append(p[s][0])
                try:
                    interpolaters[s] = interpolate.interp1d(iv_vals, pts)
                except ValueError:
                    interpolaters[s] = None
        return interpolaters
    def sub(self, bkg, iv):
        out = copy.deepcopy(self)
        minv = float('+infinity')
        maxv = float('-infinity')
        for p in bkg.data:
            minv = min(minv, p[iv][0])
            maxv = max(maxv, p[iv][0])
        data_in_range = []
        for p in out.data:
            if p[iv][0] <= maxv and p[iv][0] >= minv:
                data_in_range.append(p)
        out.data = data_in_range
        bkg.monitor_normalization(out.data[0]['Monitor'][0])
        interps = bkg.interpolate_data(iv)
        for p in out.data:
            for s in self.detectors:
                try:
                    if s in interps:
                        try:
                            if s[0] == '_':
                                p[s] = [p[s][0] + interps[s](p[iv][0])]
                            else:
                                p[s] = [p[s][0] - interps[s](p[iv][0])]
                        except ValueError:
                            break
                        except TypeError:
                            p[s][0] = None
                    else:
                        p[s][0] = None
                except KeyError:
                    pass
        return out
    def monitor_normalization(self, m0):
        for p in self.detectors:
            for s in self.detectors:
                try:
                    p[s][0] = p[s][0] * m0 / p['Monitor'][0]
                except:
                    pass
    def scalar_add(self, scalar):
        out = copy.deepcopy(self)
        for p in out.data:
            for s in out.detectors:
                try:
                    if s[0] == '_':
                        pass
                    else:
                        p[s][0] = p[s][0] + scalar
                except KeyError:
                    pass
        return out
    def scalar_mult(self, scalar):
        out = copy.deepcopy(self)
        for p in out.data:
            for s in out.detectors:
                try:
                    if s[0] == '_':
                        p[s][0] = p[s][0] * scalar * scalar
                    else:
                        p[s][0] = p[s][0] * scalar
                except KeyError:
                    pass
        return out
    def detailed_balance(self):
        out = copy.deepcopy(self)
        beta_times_temp = 11.6
        for p in out.data:
            temp = p['Temp'][0]
            beta = beta_times_temp / temp
            E = p['E'][0]
            for s in out.detectors:
                try:
                    p[s][0] = p[s][0] * np.exp(-beta*E/2)
                except KeyError:
                    pass
        return out
    def __add__(self, d):
        def combine(p1, p2):
            pass
        def same_point(p1, p2):
            return False
        out = copy.deepcopy(d)
        out.standards = copy.deepcopy(d.standards)
        for s in self.standards:
            if not s in out.standards:
                out.standards[s] = (self.standards[s])
        for s in out.standards:
            if s in self.standards and s in d.standards:
                if (not d.standards[s]['metadata']) or (not self.standards[s]['metadata']) or (self.data[0][s] != d.data[0][s]):
                    out.standards[s]['metadata'] = False
                else:
                    out.standards[s]['metadata'] = True
            else:
                out.standards[s]['metadata'] = False
        out.data = self.data + d.data
        for p in out.data:
            for s in out.standards:
                if s not in p:
                    p[s] = [None]
        out.data.sort(cmp = lambda x,y: cmp(x['A1'],y['A1']))
        for i in range(len(out.data)-1):
            if same_point(out.data[i], out.data[i+1]):
                combine(out.data[i], out.data[i+1])
                out.data.remove(out.data[i+1])
                i -= 1
        return out
    def add(self, *args):
        def combine(p1, p2):
            pass
        def same_point(p1, p2):
            return False
        out = copy.deepcopy(self)
        out.standards = copy.deepcopy(self.standards)
        for d in args:
            for s in d.standards:
                if not s in out.standards:
                    out.standards[s] = (d.standards[s])
                    out.standards[s]['metadata'] = False
        for s in out.standards:
            if out.standards[s]['metadata']:
                for d in args:
                    try:
                        if not d.standards[s]['metadata']:
                            out.standards[s]['metadata'] = False
                        elif out.data[0][s][0] != d.data[0][s][0]:
                            out.standards[s]['metadata'] = False
                    except:
                        out.standards[s]['metadata'] = False
        for d in args:
            out.data += d.data
        for p in out.data:
            for s in out.standards:
                if s not in p:
                    p[s] = [None]
        out.monitor_normalization(out.data[0]['Monitor'][0])
        try:
            out.data.sort(cmp = lambda x,y: cmp(x[out.data[0]['Scan'][0]],y[out.data[0]['Scan'][0]]))
        except:
            pass
        for i in range(len(out.data)-1):
            if same_point(out.data[i], out.data[i+1]):
                combine(out.data[i], out.data[i+1])
                out.data.remove(out.data[i+1])
                i -= 1
        return out
    
if __name__=="__main__":
    a = Data('../db/117eb3afc127e22e0d3fc74eb8efa3ea.file')
    a.sub(a, 'A3')
    
