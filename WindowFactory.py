import wx
from MediatorFactory import *
from Template import *
from WidgetFactory import *
from DataManager import *
from Define import *

class WindowFactory():
	@staticmethod
	def GetMainWindow(self,parent) : pass

class WelcomeWindowFactory(WindowFactory):
	@staticmethod
	def GetMainWindow(parent):
		return WelcomeMainWindow(parent)

class TodoListWindowFactory(WindowFactory):
	@staticmethod
	def GetWindow(parent,window):
		if window == "Main":
			return MainTaskWindow(parent)
		elif window == "Add":
			return AddTaskWindow(parent)
		elif window == "Edit":
			return EditTaskWindow(parent)
		elif window == "Complete":
			return CompleteTaskWindow(parent)
		else:
			return None

class WelcomeMainWindow:
	def __init__(self,parent):
		self.panel = wx.Panel(parent)
		self.parent = parent
		self.windowName = "Welcome!"
		
		panel_v = wx.BoxSizer(wx.VERTICAL)
		
		Mediator = FactoryMediator.getMediator(self,"Login")

		widgetFactory = AbstractWidgetFactory.getWidgetFactory("Welcome")

		self.loginWidget = widgetFactory.getWidget("Login",self.panel,Mediator)
		self.bannerWidget = widgetFactory.getWidget("Banner",self.panel,Mediator)

		panel_v.Add(self.bannerWidget.panel, 0, flag=wx.ALL|wx.EXPAND|wx.CENTER, border=5)
		panel_v.AddSpacer(30)
		panel_v.Add(self.loginWidget.panel, 0, flag=wx.ALL|wx.EXPAND|wx.CENTER, border=5)

		self.panel.SetSizer(panel_v)
		parent.addPage(self.panel,self.windowName)

	def init(self):
		self.loginWidget.setValue("")

	def destroy(self):  
		self.panel.Destroy()
		self.parent.removePage(self.parent.notebook.GetSelection())

class MainTaskWindow:

	def __init__(self,parent):
		self.panel = wx.Panel(parent)
		self.parent = parent
		self.data = dict()
		self.dataHandler = None	
		self.windowName = parent.username + "'s Task"

		panel_h = wx.BoxSizer(wx.HORIZONTAL)
		panel_h2 = wx.BoxSizer(wx.HORIZONTAL)
		panel_v = wx.BoxSizer(wx.VERTICAL)

		Mediator = FactoryMediator.getMediator(self,"Main")

		widgetFactory = AbstractWidgetFactory.getWidgetFactory("MainTask")

		self.taskListBoxWidget = widgetFactory.getWidget("TaskListBox",self.panel,Mediator)
		self.taskButtonWidget = widgetFactory.getWidget("TaskButton",self.panel,Mediator)
		self.sortButtonWidget = widgetFactory.getWidget("SortButton",self.panel,Mediator)
		self.mileStoneBoxWidget = widgetFactory.getWidget("MileStoneBox",self.panel,Mediator)
		self.updateButtonWidget = widgetFactory.getWidget("UpdateButton",self.panel,Mediator)
		self.completeButtonWidget = widgetFactory.getWidget("CompleteTask",self.panel,Mediator)
		self.logoutButtonWidget = widgetFactory.getWidget("Logout",self.panel,Mediator)

		panel_h.Add(self.taskListBoxWidget.panel, 4, flag=wx.ALL|wx.EXPAND, border=5)
		panel_h.Add(self.taskButtonWidget.panel, 1, flag=wx.ALL|wx.EXPAND, border=5)
		panel_h2.Add(self.updateButtonWidget.panel, 0, flag=wx.ALL|wx.EXPAND, border=5)
		panel_h2.Add((0,0), 1, flag=wx.ALL|wx.EXPAND, border=5)
		panel_h2.Add(self.completeButtonWidget.panel, 0, flag=wx.ALL|wx.EXPAND, border=5)
		panel_h2.Add(self.logoutButtonWidget.panel, 0, flag=wx.ALL|wx.EXPAND|wx.RIGHT, border=5)
		panel_v.Add(panel_h, 1, flag=wx.ALL|wx.EXPAND, border=5)
		panel_v.Add(self.sortButtonWidget.panel, 0, flag=wx.ALL|wx.EXPAND, border=5)
		panel_v.Add(self.mileStoneBoxWidget.panel, 1, flag=wx.ALL|wx.EXPAND, border=5)
		panel_v.Add(panel_h2, 0, flag=wx.ALL|wx.EXPAND, border=5)
		self.panel.SetSizer(panel_v)
		parent.addPage(self.panel,self.windowName)

	def init(self):
		self.dataHandler = DataManager.getInstance()
		self.data = self.dataHandler.load()
		self.taskListBoxWidget.setValue(self.data[USER_DATA])
		self.mileStoneBoxWidget.setValue(list())

	def destroy(self):  
		self.panel.Destroy()
		self.parent.removePage(self.parent.notebook.GetSelection())

class CompleteTaskWindow:

	def __init__(self,parent):
		self.panel = wx.Panel(parent)
		self.parent = parent
		self.data = dict()
		self.dataHandler = None	
		self.windowName = parent.username + "'s Completed Task"

		panel_v = wx.BoxSizer(wx.VERTICAL)

		Mediator = FactoryMediator.getMediator(self,"Complete")

		widgetFactory = AbstractWidgetFactory.getWidgetFactory("CompleteTask")

		self.taskListBoxWidget = widgetFactory.getWidget("TaskListBox",self.panel,Mediator)
		self.sortButtonWidget = widgetFactory.getWidget("SortButton",self.panel,Mediator)
		self.mileStoneBoxWidget = widgetFactory.getWidget("MileStoneBox",self.panel,Mediator)
		self.closeButtonWidget = widgetFactory.getWidget("CloseButton",self.panel,Mediator)

		panel_v.Add(self.taskListBoxWidget.panel, 4, flag=wx.ALL|wx.EXPAND, border=5)
		panel_v.Add(self.sortButtonWidget.panel, 0, flag=wx.ALL|wx.EXPAND, border=5)
		panel_v.Add(self.mileStoneBoxWidget.panel, 4, flag=wx.ALL|wx.EXPAND, border=5)
		panel_v.Add(self.closeButtonWidget.panel, 0, flag=wx.ALL|wx.EXPAND, border=5)
		
		self.panel.SetSizer(panel_v)
		parent.addPage(self.panel,self.windowName)

	def init(self, data):
		self.dataHandler = DataManager.getInstance()
		self.data = data
		self.taskListBoxWidget.setValue(self.data)
		self.mileStoneBoxWidget.setValue(list())

	def destroy(self):  
		self.panel.Destroy()
		self.parent.removePage(self.parent.notebook.GetSelection())

class AddTaskWindow:
	def __init__(self,parent):
		self.panel = wx.Panel(parent)
		self.parent = parent
		self.windowName = "add Task"
		self.data = dict()
		self.dataHandler = None
		Mediator = FactoryMediator.getMediator(self,"AddEdit")
		
		widgetFactory = AbstractWidgetFactory.getWidgetFactory("AddEditTask")
				
		self.nameWidget = widgetFactory.getWidget("Name",self.panel,Mediator)
		self.priorityWidget = widgetFactory.getWidget("Priority",self.panel,Mediator)
		self.duedateWidget = widgetFactory.getWidget("Duedate",self.panel,Mediator)
		self.milestoneBoxWidget = widgetFactory.getWidget("MilestoneBox",self.panel,Mediator)
		self.categoryWidget = widgetFactory.getWidget("Category",self.panel,Mediator)
		self.milestoneCtrlWidget = widgetFactory.getWidget("MilestoneCtrl",self.panel,Mediator)
		self.decisionWidget = widgetFactory.getWidget("Decision",self.panel,Mediator)

		sizer_v = wx.BoxSizer(wx.VERTICAL)
		sizer_h1 = wx.BoxSizer(wx.HORIZONTAL)
		sizer_h2 = wx.BoxSizer(wx.HORIZONTAL)

		sizer_h1.Add(self.duedateWidget.panel, 5, flag=wx.TOP|wx.EXPAND, border=10)
		sizer_h1.Add(self.priorityWidget.panel, 2, flag=wx.ALL|wx.EXPAND, border=10)
		sizer_h1.Add(self.categoryWidget.panel, 4, flag=wx.ALL|wx.EXPAND, border=10)
		sizer_h2.Add(self.milestoneBoxWidget.panel, 1, flag=wx.ALL|wx.EXPAND, border=10)
		sizer_h2.Add(self.milestoneCtrlWidget.panel, 0, flag=wx.ALL|wx.EXPAND, border=10)
		sizer_v.Add(self.nameWidget.panel, 0, flag=wx.ALL|wx.CENTER, border=5)
		sizer_v.Add(sizer_h1, 6, flag=wx.ALL|wx.EXPAND, border=5)
		sizer_v.Add(sizer_h2, 5, flag=wx.ALL|wx.EXPAND, border=5)
		sizer_v.Add(self.decisionWidget.panel, 0, flag=wx.ALL|wx.EXPAND, border=5)

		self.panel.SetSizer(sizer_v)
		parent.addPage(self.panel,self.windowName)

	def init(self):
		self.dataHandler = DataManager.getInstance()
		self.data = self.dataHandler.initTask()
		self.nameWidget.setValue(self.data[TASK_NAME])
		self.priorityWidget.setValue(self.data[TASK_PRIORITY])
		self.duedateWidget.setValue(TemplateDate.unformatDate(self.data[TASK_DUEDATE]))
		self.categoryWidget.setValue(self.data)
		
	def destroy(self):  
		self.panel.Destroy()
		self.parent.removePage(self.parent.notebook.GetSelection())

class EditTaskWindow:
	def __init__(self,parent):
		self.panel = wx.Panel(parent)
		self.parent = parent
		self.windowName = "edit Task"
		self.data = dict()
		self.dataHandler = None
		Mediator = FactoryMediator.getMediator(self,"AddEdit")
		
		widgetFactory = AbstractWidgetFactory.getWidgetFactory("AddEditTask")
				
		self.nameWidget = widgetFactory.getWidget("Name",self.panel,Mediator)
		self.priorityWidget = widgetFactory.getWidget("Priority",self.panel,Mediator)
		self.duedateWidget = widgetFactory.getWidget("Duedate",self.panel,Mediator)
		self.milestoneBoxWidget = widgetFactory.getWidget("EditMilestoneBox",self.panel,Mediator)
		self.categoryWidget = widgetFactory.getWidget("Category",self.panel,Mediator)
		self.milestoneCtrlWidget = widgetFactory.getWidget("MilestoneCtrl",self.panel,Mediator)
		self.decisionWidget = widgetFactory.getWidget("Decision",self.panel,Mediator)

		sizer_v = wx.BoxSizer(wx.VERTICAL)
		sizer_h1 = wx.BoxSizer(wx.HORIZONTAL)
		sizer_h2 = wx.BoxSizer(wx.HORIZONTAL)

		sizer_h1.Add(self.duedateWidget.panel, 5, flag=wx.TOP|wx.EXPAND, border=10)
		sizer_h1.Add(self.priorityWidget.panel, 2, flag=wx.ALL|wx.EXPAND, border=10)
		sizer_h1.Add(self.categoryWidget.panel, 4, flag=wx.ALL|wx.EXPAND, border=10)
		sizer_h2.Add(self.milestoneBoxWidget.panel, 1, flag=wx.ALL|wx.EXPAND, border=10)
		sizer_h2.Add(self.milestoneCtrlWidget.panel, 0, flag=wx.ALL|wx.EXPAND, border=10)
		sizer_v.Add(self.nameWidget.panel, 0, flag=wx.ALL|wx.CENTER, border=5)
		sizer_v.Add(sizer_h1, 6, flag=wx.ALL|wx.EXPAND, border=5)
		sizer_v.Add(sizer_h2, 5, flag=wx.ALL|wx.EXPAND, border=5)
		sizer_v.Add(self.decisionWidget.panel, 0, flag=wx.ALL|wx.EXPAND, border=5)

		self.panel.SetSizer(sizer_v)
		parent.addPage(self.panel,self.windowName)

	def init(self, data):
		self.dataHandler = DataManager.getInstance()
		self.data = data
		self.windowName = self.data[TASK_NAME]
		self.nameWidget.setValue(self.data[TASK_NAME])
		self.priorityWidget.setValue(self.data[TASK_PRIORITY])
		self.duedateWidget.setValue(TemplateDate.unformatDate(self.data[TASK_DUEDATE]))
		self.milestoneBoxWidget.setValue(self.data[TASK_MILESTONE])
		self.categoryWidget.setValue(self.data)
		
	def destroy(self):  
		self.panel.Destroy()
		self.parent.removePage(self.parent.notebook.GetSelection())
