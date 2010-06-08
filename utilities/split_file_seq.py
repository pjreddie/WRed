import re

pattern = re.compile('^(?P<base>[^.]*?)(?P<seq>[0-9]*)(?P<ext>[.].*)?$')
match = pattern.match('Field5T4345.bt7')
dict((a,match.group(a)+"") for a in ['base','seq','ext'])
print match.group('base')