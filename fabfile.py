from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm

env.user='yeealex'
env.hosts=['danse.chem.utk.edu'] 
env.root='/home/yeealex/'
env.site='UBmatrixCalculator'

def deploy():
    local('git archive --format=tar HEAD | gzip > %(site)s.tar.gz'%env)
    run('rm -rf %(root)s%(site)s'%env) 
    run('mkdir %(root)s%(site)s'%env) 
    put('%(site)s.tar.gz'%env, '%(root)s%(site)s/%(site)s.tar.gz'%env)
    run('cd %(root)s%(site)s && tar zxf %(site)s.tar.gz'%env)
    local('rm %(site)s.tar.gz'%env)
    #restart()

def restart():
    run('sh $(root)$(site)/restart.sh')



