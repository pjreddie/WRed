from json_parser import read_standards
import copy
def split_det(s):
    a = s
    for i in range(len(s)):
        if ord(s[i]) in range(48,58):
        a = [s[:i]
class Standard:
    def __init__(self, name, units = 'unknown', epsilon = .0001, distinct = False, interpolatable = False, spectator = False, friends = None, plottable = None, metadata = False, _comment = None):
        self.name = name
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
        #self.standards = [1,2,3,4]
        self.standardsN = []
        for s in self.standards:
            self.standardsN.append(s['name'])
        f = file(filename, 'r')

        t = []
        for lines in f:
            lines = lines.split()
            if lines[0] == '#Columns':
                t.append(lines[1:])
                break

        for lines in f:
            if lines[0] == '#': break
            t.append(lines.split())
        f.close()
        self.data = []
        for i in range(1,len(t)):
            self.data.append([[None]] * len(self.standards))
            'Detector', 'AnalyzerBlade','SDC','TDC', 'PSDC','DDC', 'MonoBlade'
            for j in range(len(t[0])):
                if(t[0][j]
                try:
                    ind = self.standardsN.index(t[0][j])
                    self.data[i-1][ind] = [t[i][j]]
                except ValueError:
                    self.standardsN.append(t[0][j])
                    self.standards.append(Standard(t[0][j]).__dict__)
                    self.data[i-1].append([t[i][j]])
        f = file(filename, 'r')
        for lines in f:
            lines = lines.split()
            if lines[0] == '#Columns':
                break
            else:
                try:
                    ind = self.standardsN.index(lines[0][1:])
                    if False:
                        pass
                    elif False:
                        pass
                    else:
                        for row in self.data:
                            row[ind] = lines[1:]
                except ValueError:
                    self.standardsN.append(lines[0][1:])
                    self.standards.append(Standard(lines[0][1:]).__dict__)
                    for row in self.data:
                        row.append(lines[1:])
    def write(self, filename):
        f = file(filename, 'w')
        f.write(self.to_string())
    def to_string(self):
        out = ''
        for s in self.standards:
            if s['metadata']:
                out += ('#' + s['name'].ljust(11))
                for val in self.data[0][self.standardsN.index(s['name'])]:
                    out += (' ' + str(val))
                out += ('\n')
        out += ('#Columns')
        for s in self.standards:
            if not s['metadata']:
                out += (' ' + s['name'].rjust(13))
        for p in self.data:
            out += ('\n        ')
            for i in range(len(p)):
                if not self.standards[i]['metadata'] and p[i] and len(p[i]):
                    valstr = p[i][0]
                    for val in p[i][1:]:
                        valstr+='_' + val
                    out += (' ' + str(valstr).rjust(13))
        return out
    def interpolate(self, iv):
        iv_idx = self.standardsN.index(iv)
        detectors = ['']
    def __add__(self, d):
        def combine(p1, p2):
            pass
        def same_point(p1, p2):
            return False
        out = copy.deepcopy(d)
        out.standards = copy.deepcopy(d.standards)
        out.standardsN = copy.deepcopy(d.standardsN)
        for i in range(len(self.standardsN)):
            if not self.standardsN[i] in out.standardsN:
                out.standardsN.append(self.standardsN[i])
                out.standards.append(self.standards[i])
        for i in range(len(out.standardsN)):
            try:
                sind = self.standardsN.index(out.standardsN[i])
                dind = d.standardsN.index(out.standardsN[i])
                if (not d.standards[i]['metadata']) or (not self.standards[i]['metadata']) or (self.data[0][sind] != d.data[0][dind]):
                    out.standards[i]['metadata'] = False
                else:
                    out.standards[i]['metadata'] = True
            except ValueError:
                out.standards[i]['metadata'] = False
        allpts = []
        for i in range(len(self.data)):
            temp = {}
            for j in range(len(self.data[i])):
                temp[self.standardsN[j]] = self.data[i][j]
            allpts.append(temp)
        for i in range(len(d.data)):
            temp = {}
            for j in range(len(d.data[i])):
                temp[d.standardsN[j]] = d.data[i][j]
            allpts.append(temp)
        out.data = []
        for point in allpts:
            temp = [None]*len(out.standardsN)
            for i in range(len(out.standardsN)):
                try:
                    temp[i] = point[out.standardsN[i]]
                except KeyError:
                    pass
            newpoint = True
            for otherp in out.data:
                if same_point(otherp, temp):
                    newpoint = False
                    combine(otherp, temp)
                    break
            if newpoint:
                out.data.append(temp)
        return out
    
