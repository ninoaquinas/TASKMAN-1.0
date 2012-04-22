from WindowFactory import *
from MediatorFactory import *
from DataManager import *
from LoginManager import *

class Main(wx.Frame):

	__instance = None

	def __init__(self,parent,id):
		if Main.__instance != None:
			raise Exception("This is a singleton class!")
		else:
			wx.Frame.__init__(self,parent,id,'Taskman 1.0', pos=(0,0), size=(800,600))
			self.notebook = wx.aui.AuiNotebook(self)
			LoginManager(SAVE_STRATEGY)
			GlobalMediator(self)	
			self.welcome = WelcomeWindowFactory.GetMainWindow(self)
			Main.__instance = self

	@staticmethod
	def getInstance(parent):
		if Main.__instance == None:
			Main(parent,-1)
		return Main.__instance
	
	def addPage(self,panel,panelName):
		self.notebook.AddPage(panel,panelName,select=True)
		self.notebook.SetWindowStyle(wx.aui.AUI_NB_CLOSE_ON_ALL_TABS)
		self.notebook.ToggleWindowStyle(wx.aui.AUI_NB_CLOSE_ON_ALL_TABS)
	
	def removePage(self,index):
		self.notebook.RemovePage(index)

	def addTask(self):
		task = TodoListWindowFactory.GetWindow(self,"Add")
		task.init()

	def editTask(self,data):
		task = TodoListWindowFactory.GetWindow(self,"Edit")
		task.init(data)

	def showComplete(self,data):
		complete = TodoListWindowFactory.GetWindow(self, "Complete")
		complete.init(data)

	def logout(self):
		while(self.notebook.GetPageCount()):
			self.notebook.DeletePage(0)		
		self.welcome = WelcomeWindowFactory.GetMainWindow(self)
	
	def login(self, username):
		self.welcome.destroy()
		self.username = username
		DataManager(SAVE_STRATEGY,self.username)
		self.main = TodoListWindowFactory.GetWindow(self,"Main")
		self.main.init()

