"""
:filename:                    CheckBoxes.py
:author:                      frederic.gabel@tordivel.no
:requirements:                Scorpion 9.0.0.494 or higher
:copyright:                   2000-2017 Tordivel AS
:license:                     Tordivel AS' Scorpion Python Plugin License

Checkboxes creation plugin - To quickly integrate checkboxes with callback to custom function

::
  1.0.0.3, 07oct2017, FG: Checkbox add, remove, update functions
  1.0.0.2, 03oct2017, FG: Name change, add verbose + printdebug
  1.0.0.1, 02oct2017, FG: requirements : Scorpion 9.0.0.493 or higher
"""

__version__ = '1.0.0.3'
import os
from Scorpion import PluginNotify,GetControlByHandle,ExecuteCmd,GetTool,SelectTagname,SpbDialog,PluginChanged

class CheckBoxes(object):
  ''' CameraSetup - panel with a button for camera configuration '''
  def __init__(self,cntr,name):
    self.name = name
    self.cntr = cntr
    self.init()


  def __str__(self):
    ''' return a unique persistance name for host application storage '''
    return '%s_%s'%(self.__class__.__name__,self.name)

    
  def init(self):
    """ reset all content """
    self.cntr.deleteControls()                  #delete previous added controls if any
    self.count = 1                              #number of checkboxes
    self.checkboxes=[]                          #list of buttons
    self.cmds=[]                                #list of commands
    self.params=[]                              #list of commands
    self.checkboxWidth = 100                    #width of each checkbox
    self.verbose = 1                            #debug level - null by default
    self.addCheckBox('Show picking', 'script', 'showPicking()')
    

  def getConfig(self):
    ''' return plugin configuration as xml '''
    from SPB import CreateSpb
    self.printDebug(2, '---getConfig')
    spb=CreateSpb()
    spb.setText('type',self.__class__.__name__)
    spb.setInt('version', 1)
    spb.setInt('count',len(self.checkboxes))
    spb.setInt('verbose', self.verbose)
    spb.setInt('checkbox.width', self.checkboxWidth)
    for i in range(len(self.checkboxes)):
      spb.setText('checkbox%d.caption'%(i+1),self.checkboxes[i].caption)
      spb.setText('checkbox%d.command'%(i+1),self.cmds[i])
      spb.setText('checkbox%d.params'%(i+1),self.params[i])
    self.printDebug(2, 'End getConfig---')
    return spb.xml


  def setConfig(self,value):
    ''' set plugin configuration from string '''
    from SPB import CreateSpb
    self.printDebug(2, '---setConfig')
    spb=CreateSpb(value)
    if spb.getText('type') == self.__class__.__name__:
      if spb.isEntry('checkbox.width'):
        self.checkboxWidth = spb.getInt('checkbox.width')
      if spb.isEntry('verbose'):
        self.verbose = spb.getInt('verbose')
      # If the count entered is greater than the current count - ADD checkboxes
      if spb.getInt('count') > self.count:                  
        for j in range (self.count, spb.getInt('count')):
          checkbox = self.addCheckBox('checkbox%i'%(j+1),'a','b')
          self.printDebug(1, '\tadd checkbox %s'%checkbox.name)
      # If the count entered is less than the current count - DELETE checkboxes
      elif spb.getInt('count') < self.count:                
        for k in range(self.count, spb.getInt('count'), -1):
          self.printDebug(1,'delete checkbox : %s'%self.checkboxes[k-1].name)
          self.cntr.deleteControl(self.checkboxes[k-1].name)
          del self.checkboxes[k-1]
          self.count = spb.getInt('count')
    # Update the current controls
    for l in range(self.count):
      self.checkboxes[l].caption = spb.getText('checkbox%d.caption'%(l+1))
      self.cmds[l] = spb.getText('checkbox%d.command'%(l+1))
      self.params[l] = spb.getText('checkbox%d.params'%(l+1))
    self.count = spb.getInt('count')
    self.printDebug(2,'End setConfig---')
  
    
  def configure(self):
    ''' configure the plugin, return bool whether changed or not '''
    import SPB
    self.printDebug(2, '---configure')
    ok,cfg = SpbDialog('Plugin configuration', self.getConfig())
    if ok:
      self.setConfig(cfg)
      PluginChanged(self)
      self.cntr.update()


  def addCheckBox(self,caption,cmd,params):
    """ add a checkbox """
    self.printDebug(2, '+ add checkbox')
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
    ''' button click handler '''
    if sender in self.checkboxes:
      self.printDebug(1, 'checkbox clicked : %s'%self.checkboxes[sender.tag].caption)
      self.printDebug(1, '\t\tcmd: %s'%self.cmds[sender.tag])
      self.printDebug(1, '\t\tparam: %s'%self.params[sender.tag])
      ExecuteCmd(self.cmds[sender.tag],self.params[sender.tag])

  def printDebug(self,level,msg):
    ''' prints a debug message when verbose is less equal level '''
    if level<=self.verbose: print '<%s> %s'%(self.__class__.__name__,msg)


def CreatePlugin(hWnd, name=''):
  '''
  Scorpion Plugin Stub - Required
  '''
  cntr=GetControlByHandle(hWnd)
  return CheckBoxes(cntr,name)
