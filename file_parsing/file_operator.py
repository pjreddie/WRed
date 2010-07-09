from json_parser import read_standards
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
        self.standards = read_standards()
        f = file(filename, 'r')
        t = []
        template = {}
        for s in self.standards:
            template[s] = [None]
        for lines in f:
            lines = lines.split()
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
        self.data = []
        for s in t[0]:
            if s in self.standards:
                pass
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
        self.detectors = ['Detector',]
        for s in self.standards:
            if s[:8] == 'Analyzer' and s[-5:] == 'Group':
                self.detectors.extend(self.data[0][s])
        for d in self.detectors:
            if '_' + d in self.standards:
                self.standards['_' + d] = Standards().__dict__
                for p in self.data:
                    p['_' + d] = p[d]
    def write(self, filename):
        f = file(filename, 'w')
        f.write(self.to_string())
    def to_string(self):
        out = ''
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
        self.data.sort(cmp = lambda x,y: cmp(x[iv],y[iv]))
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
        for p in out.data:
            if p[iv][0] > maxv or p[iv][0] < minv:
                out.data.remove(p)
        interps = bkg.interpolate_data(iv)
        for p in out.data:
            for s in out.standards:
                if s in self.detectors:
                    if interps[s]:
                        if s[0] == '_':
                            p[s] = [p[s][0] + interps[s](p[iv][0])]
                        else:
                            p[s] = [p[s][0] - interps[s](p[iv][0])]
                    else:
                        p[s][0] = None
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
    
    
if __name__=="__main__":
    a = Data('../db/117eb3afc127e22e0d3fc74eb8efa3ea.file')
    a.sub(a, 'A3')
    
