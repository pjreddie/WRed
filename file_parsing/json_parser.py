import json

def read_standards(filename = 'standards.json'):
    filein = file(filename, 'r')
    f = filein.read()
    fout = ''
    for i in range(len(f)):
        if f[i] == "\n":
            pass
        elif f[i] == "\t":
            pass
        elif f[i] == "'":
            fout += '"'
        else:
            fout += f[i]
        
    f = fout[:]
    fout = ''
    for i in range(len(f)):
        if f[i] == ',':
            if f[i+1] == '}':
                pass
            elif f[i+1] == ']':
                pass
            else:
                fout+=f[i]
        else:
            fout += f[i]
    return json.loads(fout)
