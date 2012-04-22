#from twisted.internet import wxreactor
#wxreactor.install()
#from twisted.internet import protocol, reactor
#from twisted.protocols import basic
#from widgetFactory import *
#from mediatorFactory import *
from Facade import *

if __name__ == '__main__':
	app = wx.PySimpleApp()
	frame = Main.getInstance(None)
	frame.Show()
	app.MainLoop()
