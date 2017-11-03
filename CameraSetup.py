"""
:filename:               Checkboxes.py
:author:                  frederic.gabel@tordivel.no
:requirements:       Scorpion 9.0.0.494 or higher
:copyright:             2000-2017 Tordivel AS
:license:                 Tordivel AS' Scorpion Python Plugin License

Checkboxes creation plugin - To quickly integrate checkboxes with callback to custom function

::
  1.0.0.1, 02oct2017, FG: requirements : Scorpion 9.0.0.493 or higher
"""

__version__ = '1.0.0.1'
import os
from Scorpion import PluginNotify,GetControlByHandle,ExecuteCmd,GetTool,SelectTagname,SpbDialog,PluginChanged

class CameraSetup(object):
  '''
  CameraSetup - panel with a button for camera configuration
  '''
  def __init__(self,cntr,name):
    self.name=name
    self.cntr = cntr
    self.init()

    
  def init(self):
    """
    reset all content
    """
    self.cntr.deleteControls()                  #delete previous added controls if any
    self.checkboxes=[]                           #list of buttons
    self.cmds=[]                                     #list of commands
    self.params=[]                                  #list of commands
    self.checkboxWidth = 100
    self.addCheckBox('Show picking', 'script', 'showPicking()')
    

  def __str__(self):
    '''
    return a unique persistance name for host application storage
    '''
    return '%s_%s'%(self.__class__.__name__,self.name)


  def getConfig(self):
    '''
    return plugin configuration as xml
    '''
    print '---getConfig'
    from SPB import CreateSpb
    spb=CreateSpb()
    spb.setText('type',self.__class__.__name__)
    spb.setInt('version', 1)
    spb.setInt('count',len(self.checkboxes))
    spb.setInt('checkbox.width', self.checkboxWidth)
    for i in range(len(self.checkboxes)):
      spb.setText('checkbox%d.caption'%(i+1),self.checkboxes[i].caption)
      spb.setText('checkbox%d.command'%(i+1),self.cmds[i])
      spb.setText('checkbox%d.params'%(i+1),self.params[i])
    return spb.xml


  def setConfig(self,value):
    '''
    set plugin configuration from string
    '''
    print'---setConfig'
    self.init()
    from SPB import CreateSpb
    spb=CreateSpb(value)
    if spb.getText('type') == self.__class__.__name__:
      if spb.isEntry('checkbox.width'):
        self.checkboxWidth = spb.getInt('checkbox.width')
        print '\tNew checkboxWidth = ',self.checkboxWidth
      if spb.isEntry('count'):
        print 'Count is an entry'
      for i in range(spb.getInt('count')-1):
        print '\t\t',spb.getText('checkbox%d.caption'%(i+1))
        #checkbox = self.addCheckBox(spb.getText('checkbox%d.caption'%(i+1)), spb.getText('checkbox%d.command'%(i+1)), spb.getText('checkbox%.params'%(i+1)))
        checkbox = self.addCheckBox(str(i+1), str(10*i+1), str(20*i+1))
    print 'End setConfig---'
    
    
  def configure(self):
    '''
    configure the plugin, return bool whether changed or not
    '''
    print '---configure'
    import SPB
    ok,cfg = SpbDialog('Plugin configuration', self.getConfig())
    if ok:
      self.setConfig(cfg)
      PluginChanged(self)
      self.cntr.update()


  def addCheckBox(self,caption,cmd,params):
    print 'adding checkbox'
    checkbox = self.cntr.addControl('CheckBox',10+len(self.checkboxes)*self.checkboxWidth,20)
    checkbox.width = self.checkboxWidth
    checkbox.onClick = self.buttonClick
    checkbox.caption = caption
    checkbox.tag = len(self.checkboxes)
    self.checkboxes.append(checkbox)                               #append bttn
    if cmd:self.cmds.append(cmd)                                       #append bttn command
    else:   self.cmds.append('')
    if params:self.params.append(params)                          #append bttn command porameters
    else:     self.params.append('')
    return checkbox
    

  def buttonClick(self,sender,args):
    '''
    button click handler
    '''
    print 'The button has been clicked!'
    if sender in self.checkboxes:
      print 'sender in checkboxes list'
      print '\ttag: ',sender.tag
      print '\tcmd: ',self.cmds[sender.tag]
      print '\tparam: ',self.params[sender.tag]
      ExecuteCmd(self.cmds[sender.tag],self.params[sender.tag])


def CreatePlugin(hWnd, name=''):
  '''
  Scorpion Plugin Stub - Required
  '''
  cntr=GetControlByHandle(hWnd)
  return CameraSetup(cntr,name)
