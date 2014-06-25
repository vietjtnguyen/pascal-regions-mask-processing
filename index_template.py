#!/usr/bin/env python




##################################################
## DEPENDENCIES
import sys
import os
import os.path
try:
    import builtins as builtin
except ImportError:
    import __builtin__ as builtin
from os.path import getmtime, exists
import time
import types
from Cheetah.Version import MinCompatibleVersion as RequiredCheetahVersion
from Cheetah.Version import MinCompatibleVersionTuple as RequiredCheetahVersionTuple
from Cheetah.Template import Template
from Cheetah.DummyTransaction import *
from Cheetah.NameMapper import NotFound, valueForName, valueFromSearchList, valueFromFrameOrSearchList
from Cheetah.CacheRegion import CacheRegion
import Cheetah.Filters as Filters
import Cheetah.ErrorCatchers as ErrorCatchers

##################################################
## MODULE CONSTANTS
VFFSL=valueFromFrameOrSearchList
VFSL=valueFromSearchList
VFN=valueForName
currentTime=time.time
__CHEETAH_version__ = '2.4.4'
__CHEETAH_versionTuple__ = (2, 4, 4, 'development', 0)
__CHEETAH_genTime__ = 1403707268.905518
__CHEETAH_genTimestamp__ = 'Wed Jun 25 07:41:08 2014'
__CHEETAH_src__ = 'index_template.tmpl'
__CHEETAH_srcLastModified__ = 'Wed Jun 25 07:41:06 2014'
__CHEETAH_docstring__ = 'Autogenerated by Cheetah: The Python-Powered Template Engine'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class index_template(Template):

    ##################################################
    ## CHEETAH GENERATED METHODS


    def __init__(self, *args, **KWs):

        super(index_template, self).__init__(*args, **KWs)
        if not self._CHEETAH__instanceInitialized:
            cheetahKWArgs = {}
            allowedKWs = 'searchList namespaces filter filtersLib errorCatcher'.split()
            for k,v in KWs.items():
                if k in allowedKWs: cheetahKWArgs[k] = v
            self._initCheetahInstance(**cheetahKWArgs)
        

    def respond(self, trans=None):



        ## CHEETAH: main method generated for this template
        if (not trans and not self._CHEETAH__isBuffering and not callable(self.transaction)):
            trans = self.transaction # is None unless self.awake() was called
        if not trans:
            trans = DummyTransaction()
            _dummyTrans = True
        else: _dummyTrans = False
        write = trans.response().write
        SL = self._CHEETAH__searchList
        _filter = self._CHEETAH__currentFilter
        
        ########################################
        ## START - generated method body
        
        write(u'''<html>
<head>
  <title>Label Index</title>
  <style>
    tr:nth-child(even) { background: #eee; }
    tr:nth-child(odd) { background: #fff; }
  </style>
</head>
<body>
  <center>
  <table cellpadding="4" cellspacing="0" border="0">
''')
        for label_name in VFFSL(SL,"label_names",True): # generated from line 12, col 3
            write(u'''    <tr>
      <td><a href="/query/''')
            _v = VFFSL(SL,"label_name",True) # u'${label_name}' on line 14, col 27
            if _v is not None: write(_filter(_v, rawExpr=u'${label_name}')) # from line 14, col 27.
            write(u'''">''')
            _v = VFFSL(SL,"label_name",True) # u'${label_name}' on line 14, col 42
            if _v is not None: write(_filter(_v, rawExpr=u'${label_name}')) # from line 14, col 42.
            write(u'''</a></td>
      <td><a href="/query/''')
            _v = VFFSL(SL,"label_name",True) # u'${label_name}' on line 15, col 27
            if _v is not None: write(_filter(_v, rawExpr=u'${label_name}')) # from line 15, col 27.
            write(u'''?num=100">100</a></td>
      <td><a href="/query/''')
            _v = VFFSL(SL,"label_name",True) # u'${label_name}' on line 16, col 27
            if _v is not None: write(_filter(_v, rawExpr=u'${label_name}')) # from line 16, col 27.
            write(u'''?num=100&set=trainval">100 + trainval only</a></td>
      <td><a href="/query/''')
            _v = VFFSL(SL,"label_name",True) # u'${label_name}' on line 17, col 27
            if _v is not None: write(_filter(_v, rawExpr=u'${label_name}')) # from line 17, col 27.
            write(u'''?num=100&set=test">100 + test only</a></td>
      <td><a href="/query/''')
            _v = VFFSL(SL,"label_name",True) # u'${label_name}' on line 18, col 27
            if _v is not None: write(_filter(_v, rawExpr=u'${label_name}')) # from line 18, col 27.
            write(u'''?num=100&nochanges=true">100 + no changes</a></td>
    </tr>
''')
        write(u'''  </table>
  </center>
</body>
</html>
''')
        
        ########################################
        ## END - generated method body
        
        return _dummyTrans and trans.response().getvalue() or ""
        
    ##################################################
    ## CHEETAH GENERATED ATTRIBUTES


    _CHEETAH__instanceInitialized = False

    _CHEETAH_version = __CHEETAH_version__

    _CHEETAH_versionTuple = __CHEETAH_versionTuple__

    _CHEETAH_genTime = __CHEETAH_genTime__

    _CHEETAH_genTimestamp = __CHEETAH_genTimestamp__

    _CHEETAH_src = __CHEETAH_src__

    _CHEETAH_srcLastModified = __CHEETAH_srcLastModified__

    _mainCheetahMethod_for_index_template= 'respond'

## END CLASS DEFINITION

if not hasattr(index_template, '_initCheetahAttributes'):
    templateAPIClass = getattr(index_template, '_CHEETAH_templateClass', Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(index_template)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://www.CheetahTemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=index_template()).run()


