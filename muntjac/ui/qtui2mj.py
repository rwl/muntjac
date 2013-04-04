from decimal import Decimal
import sys
import re
import os
import xml.sax.handler
import traceback
from muntjac.api import *
from mjextras import *


class TreeBuilder(xml.sax.handler.ContentHandler):
        def __init__(self,parent):
            self.stack = []
            self.root = DataNode()
            self.current = self.root
            self.text_parts = []
            self.parent=parent
        def startElement(self, name, attrs):
            self.stack.append((self.current, self.text_parts))
            self.current = DataNode()
            self.text_parts = []
            # xml attributes --> python attributes
            for k, v in attrs.items():
                self.current._add_xml_attr(self.parent._name_mangle(k), v)
        def endElement(self, name):
            text = ''.join(self.text_parts).strip()
            if text:
                self.current.data = text
            if self.current._attrs:
                obj = self.current
            else:
                # a text only node is simply represented by the string
                obj = text or ''
            self.current, self.text_parts = self.stack.pop()
            self.current._add_xml_attr(self.parent._name_mangle(name), obj)
        def characters(self, content):
            self.text_parts.append(content)

class DataNode(object):
        def __init__(self):
            self._attrs = {}    # XML attributes and child elements
            self.data = None    # child text data
        def __len__(self):
            # treat single element as a list of 1
            return 1
        def __getitem__(self, key):
            if isinstance(key, basestring):
                return self._attrs.get(key,None)
            else:
                return [self][key]
        def __contains__(self, name):
            return self._attrs.has_key(name)
        def __nonzero__(self):
            return bool(self._attrs or self.data)
        def __getattr__(self, name):
            if name.startswith('__'):
                # need to do this for Python special methods???
                raise AttributeError(name)
            return self._attrs.get(name,None)
        def _add_xml_attr(self, name, value):
            if name in self._attrs:
                # multiple attribute of the same name are represented by a list
                children = self._attrs[name]
                if not isinstance(children, list):
                    children = [children]
                    self._attrs[name] = children
                children.append(value)
            else:
                self._attrs[name] = value
        def __str__(self):
            return self.data or ''
        def __repr__(self):
            items = sorted(self._attrs.items())
            if self.data:
                items.append(('data', self.data))
            return u'{%s}' % ', '.join([u'%s:%s' % (k,repr(v)) for k,v in items])

class xml2obj(object):

    def __init__(self,src):
      self.src=src
      self.non_id_char = re.compile('[^_0-9a-zA-Z]')

    def _name_mangle(self,name):
        return self.non_id_char.sub('_', name)


    def build(self):
      builder = TreeBuilder(self)
      if isinstance(self.src,basestring):
          xml.sax.parseString(self.src, builder)
      else:
          xml.sax.parse(self.src, builder)
      return builder.root._attrs.values()[0]

#see if key exists in an object
def cfkey(theobj,thevar):
  try:
    e=getattr(theobj,thevar)
    if e=="":return False
    else:return True
  except:
    return False

class MuntJacWindow(object):
    def __init__(self):
        pass

#generate QIC code class that will create the code for 
class QT2Muntjac(object):
  
  def __init__(self):
      pass
        
    # check to see if the latest file has been pulled
  def translateUI(self,filename):
      IN=open(filename,"r").read()
      g=xml2obj(IN).build()
      centralwidget=g.widget
      mainWidget=aWidget(None,centralwidget,None,True)
      self.window=mainWidget.mainwidget
      self.ui=mainWidget.mainUI
      #print self.ui.__dict__
           
class aWidget(object):
    def __init__(self,parent,widget,mainUI=None,main=False):
        #when the initial widget is passed in main eq true so that A main object can be generated
        if mainUI==None:
            self.mainUI=MuntJacWindow()
        #when child widgets are created the original object reference is passed in.
        else:
            self.mainUI=mainUI
        
        self.main       = main
        self.parent     = parent              # parent
        self.widget     = widget              # current widget
        self.cls        = widget['class']     # for some reason class is a reserved word in python ( :) )
        self.mainwidget = None
        self.isLayout   = False
        
        if self.main==False:
            if self.parent.wHandleSize==False:
                self.wHandleSize=False
            else:
                self.wHandleSize=True
        else:
            self.wHandleSize=False
        
        found, geometry = self.getProperty("geometry")
        if found:
            self.geometry=geometry
        else:
            self.geometry=None
            
        self.makeWidget()
        self.makeChildren()
        
    def makeWidget(self):
        if not self.main:
            #TODO: handle the enabled disabled and readonly properties of all widgets
            
            if self.widget['class']=="QWidget":
                #the qwidget is like an Absolutelayout unless it has a layout defined inside of it
                if self.widget.layout!=None:
                    if self.widget.layout["class"]=="QVBoxLayout":
                        self.mainUI.__dict__[self.widget.layout.name]=VerticalLayout()
                        self.thiswidget = self.mainUI.__dict__[self.widget.layout.name]
                        self.wHandleSize=False
                        self.isLayout=True
                    elif self.widget.layout["class"]=="QHBoxLayout":
                        self.mainUI.__dict__[self.widget.layout.name]=HorizontalLayout()
                        self.thiswidget = self.mainUI.__dict__[self.widget.layout.name]
                        self.wHandleSize=False
                        self.isLayout=True
                        
                elif self.widget.layout==None:
                    self.mainUI.__dict__[self.widget.name]=AbsoluteLayout()
                    self.thiswidget = self.mainUI.__dict__[self.widget.name]
                    self.wHandleSize=True
                #if the parent of this qwidget is the mainwindow then use the geometry from the mainwindow for it
                if self.parent.widget['class']=="QMainWindow":
                    self.parent.mainwidget = self.thiswidget
                    self.mainUI.width      = self.parent.geometry.rect.width
                    self.mainUI.height     = self.parent.geometry.rect.height
                    
            elif self.widget['class']=="QStackedWidget":
                #there is not a stacked widget in munjac.  So in mjextras i made one by removing the 
                #tab headers from a tabsheet
                self.mainUI.__dict__[self.widget.name]=StackedSheet()
                self.thiswidget = self.mainUI.__dict__[self.widget.name]
                
            elif self.widget['class']=="QGroupBox":
                #for muntjac since there is no groupbox I am adding an AbsoluteLayout to a Panel
                title=str(self.getTitle())
                self.mainUI.__dict__[self.widget.name+'Panel']=Panel(title)
                self.thiswidget = self.mainUI.__dict__[self.widget.name+'Panel']
                self.mainUI.__dict__[self.widget.name]=AbsoluteLayout()
                self.thiswidget.setContent(self.mainUI.__dict__[self.widget.name])
                
            elif self.widget['class']=="QLabel":
                #QLabel makes a Label() they are alike
                text=str(self.getText())
                self.mainUI.__dict__[self.widget.name]=Label(text)
                self.thiswidget = self.mainUI.__dict__[self.widget.name]

            elif self.widget['class']=="QLineEdit":
                #conversion about the same only you cannot use the height or textfield gets 
                #automatically converted to a TextArea by muntjac
                text=str(self.getText())
                self.mainUI.__dict__[self.widget.name]=TextField("")
                self.thiswidget = self.mainUI.__dict__[self.widget.name]
                self.thiswidget.setValue(text)

            elif self.widget['class']=="QPushButton":
                #QPushButton converts to Button very well.  In some of the widgetsets height doesnt translate well ie runo
                text=str(self.getText())
                self.mainUI.__dict__[self.widget.name]=Button(text)
                self.thiswidget = self.mainUI.__dict__[self.widget.name]

            elif self.widget['class']=="QTextEdit":
                #the difference with QTextEdit and TextArea is that textarea is resizeable
                #and as well QTextEdit has richtext in it.
                #TODO: convert richtext over to text for TextArea
                #TODO: figure out if richtextarea is needed
                html=str(self.getHtml())
                self.mainUI.__dict__[self.widget.name]=TextArea()
                self.thiswidget = self.mainUI.__dict__[self.widget.name]
                self.thiswidget.setValue(html)

            elif self.widget['class']=="QTabWidget":
                #QTabWidget and TabSheet are very similar
                self.mainUI.__dict__[self.widget.name]=TabSheet()
                self.thiswidget = self.mainUI.__dict__[self.widget.name]

            elif self.widget['class']=="QTableView" or self.widget['class']=="QTableWidget":
                #QTableView is more like Table than QTableWidget.  But I convert both to Table
                self.mainUI.__dict__[self.widget.name]=Table()
                self.thiswidget = self.mainUI.__dict__[self.widget.name]
                
            elif self.widget['class']=="QCheckBox":
                #QCheckBox works pretty much like CheckBox only the state info is different.
                #TODO: set the correct state of the checkbox from the ui file
                self.mainUI.__dict__[self.widget.name]=CheckBox()
                self.thiswidget = self.mainUI.__dict__[self.widget.name]

            else:
                #left in print statement for unhandled widgets
                print "could not handle ",self.widget['class']
                self.wHandleSize=False
                return
            
            if self.wHandleSize:
                self.handleSize()
            
            
            #determine the name and class name of the widget
            
            #handle if it is a layout
            if self.parent.widget['class']=="QWidget":
                if self.parent.widget.layout!=None:
                    pnname=self.parent.widget.layout.name
                    pnclass=self.parent.widget.layout['class']
                else:
                    pnname=self.parent.widget.name
                    pnclass=self.parent.widget['class']
                if self.widget.layout!=None:
                    thname=self.widget.layout.name
                    thclass=self.widget.layout['class']
                else:
                    thname=self.widget.name
                    thclass=self.widget['class']
                    
            #handle if it is not a layout
            else:
                   pnname=self.parent.widget.name
                   pnclass=self.parent.widget['class']
                   thname=self.widget.name
                   thclass=self.widget['class']
            
            
            #handle adding the components to the parent
            #handle containers
            if pnclass=="QVBoxLayout" or \
               pnclass=="QHBoxLayout" or \
               pnclass=="QTabWidget"  or \
               pnclass=="QStackedWidget":
               if pnclass!="QMainWindow":
                   if self.parent.widget['class']=="QStackedWidget" or self.parent.widget['class']=="QTabWidget":
                       self.parent.thiswidget.addTab(self.thiswidget)
                       if thclass=="QGroupBox":
                           self.thiswidget=self.mainUI.__dict__[thname]
                   else:
                       self.parent.thiswidget.addComponent(self.thiswidget)
                       if thclass=="QGroupBox":
                           self.thiswidget=self.mainUI.__dict__[thname]
            #handle widgets
            else:
                if pnclass!="QMainWindow" and pnclass!="QVBoxLayout" and pnclass!="QHBoxLayout":
                    if self.parent.geometry!=None:
                        print "adding",thname,"to",pnname,"is a",pnclass,"is a",type(self.parent.thiswidget)
                        xpos="%.2f" % (((float(self.geometry.rect.x)+.001)/(float(self.parent.geometry.rect.width)+.001))*100)
                        ypos="%.2f" % (((float(self.geometry.rect.y)+.001)/(float(self.parent.geometry.rect.height)+.001))*100)
                        self.parent.thiswidget.addComponent(self.thiswidget, 
                                             "top:"+str(ypos)+"%;left:"+str(xpos)+"%")
                    else:
                        print "adding",thname,"to",pnname,"is a",pnclass,"is a",type(self.parent.thiswidget)
                        self.parent.thiswidget.addComponent(self.thiswidget,
                                             "top:"+str(self.geometry.rect.y)+"%;left:"+str(self.geometry.rect.x)+"%")
                    if thclass=="QGroupBox":
                        self.thiswidget=self.mainUI.__dict__[thname]

    #handle the sizing of the current widget
    def handleSize(self):
        if self.geometry==None:
            self.geometry=self.parent.geometry
            wdth = "%.2f" % ((float(self.parent.geometry.rect.width)/float(self.parent.geometry.rect.width))*100)
            hgth = "%.2f" % ((float(self.parent.geometry.rect.height)/float(self.parent.geometry.rect.height))*100)
            if self.widget.name=="gbValidation":
                print self.widget.name,wdth,hgth
            if self.widget['class']!="QPanel":
                self.thiswidget.setHeight(str(hgth)+"%")
            else:
                self.thiswidget.setHeight(str(self.parent.geometry.rect.height)+"px")
            self.thiswidget.setWidth(str(wdth)+"%")
        else:
            wdth = "%.2f" % ((float(self.geometry.rect.width)/(float(self.parent.geometry.rect.width)-float(self.geometry.rect.x)))*100)
            hgth = "%.2f" % ((float(self.geometry.rect.height)/(float(self.parent.geometry.rect.height)-float(self.geometry.rect.y)))*100)
            if self.widget.name=="gbValidation":
                print self.widget.name,wdth,hgth
            if self.widget['class']!="QLineEdit":
                #if self.widget['class']!="QPanel":
                self.thiswidget.setHeight(str(hgth)+"%")
                #else:
                #    self.thiswidget.setHeight(str(self.geometry.rect.height)+"px")
            self.thiswidget.setWidth(str(wdth)+"%")

    #get title from xml properties
    def getTitle(self):
        found, title=self.getProperty("title")
        if found:title=title.string
        else:title=""
        return title

    #get text from xml properties
    def getText(self):
        found, thetext=self.getProperty("text")
        if found:thetext=thetext.string
        else:thetext=""
        return thetext

    #get html from xml properties
    def getHtml(self):
        found, html=self.getProperty("html")
        if found:html=html.string
        else:html=""
        return html

    #handle creation of the children widgets within this widget
    def makeChildren(self):
        if self.isLayout:
            if not self.widget.layout.item is None:
                for awidget in self.widget.layout.item:
                     aWidget(self,awidget.widget,self.mainUI)
        else:
            if not self.widget.widget is None:
                for awidget in self.widget.widget:
                     aWidget(self,awidget,self.mainUI)
        if self.main:
            #finish up mainwindow commands
            pass

    #get a property from xml of this widget
    def getProperty(self,name,ref="string"):
        widget=self.widget
        if cfkey(widget,"property"):
            if type(widget.property) is list:
                for prop in widget.property:
                    if prop.name==name:
                        return True,prop
                return False,""
            else:
                try:
                    if widget.property.name==name:
                        return True,widget.property
                    else:
                        return False,""
                except:
                    return False,""
        else:
            return False,""

    #get a property from a widget 
    def getSProperty(self,widget,name,ref="string"):
        if cfkey(widget,"property"):
          if type(widget.property) is list:
            for prop in widget.property:
              if prop.name==name:
                ret=str(getattr(prop,ref))
                return ret
            return ""
          else:
            try:
              if widget.property.name==name:
                ret=str(getattr(widget.property,ref))
                return ret
              else:
                return ""
            except:
              return ""
        else:
          return ""        

# test against a test ui file if run as main
if __name__=="__main__":
  conv = QT2Muntjac()
  conv.translateUI('DEMO.ui')

