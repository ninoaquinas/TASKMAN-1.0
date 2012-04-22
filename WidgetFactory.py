import wx
import wx.calendar
import operator
import wx.lib.inspection
from wx.lib.mixins.listctrl import CheckListCtrlMixin, ListCtrlAutoWidthMixin, TextEditMixin, ColumnSorterMixin
from Template import *
from Define import *

class AbstractWidgetFactory():
	@staticmethod
	def getWidgetFactory(factory):
		if factory == "MainTask":
			return MainTaskWidgetFactory
		elif factory == "CompleteTask":
			return CompleteTaskWidgetFactory
		elif factory == "AddEditTask":
			return AddTaskWidgetFactory
		elif factory == "Welcome":
			return WelcomeWidgetFactory
		else:
			 return None

class AbstractWidget():
	@staticmethod
	def getWidget(self,widget,parent,mediator): pass

class WelcomeWidgetFactory(AbstractWidget):
	@staticmethod
	def getWidget(widget,parent,mediator):
		if widget == "Login":
			return LoginWidget(parent,mediator)
		elif widget == "Banner":
			return BannerWidget(parent,mediator)
		else:
			 return None

class MainTaskWidgetFactory(AbstractWidget):
	@staticmethod
	def getWidget(widget,parent,mediator):
		if widget == "TaskListBox":
			return TaskListBoxWidget(parent,mediator)
		elif widget == "TaskButton":
			return TaskButtonWidget(parent,mediator)
		elif widget == "SortButton":
			return SortButtonWidget(parent,mediator)
		elif widget == "MileStoneBox":
			return MileStoneBoxWidget(parent,mediator)
		elif widget == "CompleteTask":
			return CompleteTaskWidget(parent,mediator)
		elif widget == "Logout":
			return LogoutWidget(parent,mediator)
		else:
			 return None

class CompleteTaskWidgetFactory(AbstractWidget):
	@staticmethod
	def getWidget(widget,parent,mediator):
		if widget == "TaskListBox":
			return TaskListBoxWidget(parent,mediator)
		elif widget == "SortButton":
			return SortButtonWidget(parent,mediator)
		elif widget == "MileStoneBox":
			return CompletedMileStoneBoxWidget(parent,mediator)
		elif widget == "CloseButton":
			return CloseButtonWidget(parent,mediator)
		else:
			 return None

class AddTaskWidgetFactory(AbstractWidget):
	@staticmethod
	def getWidget(widget,parent,mediator):
		if widget == "Name":
			return AddTaskNameWidget(parent,mediator) 
		elif widget == "Priority":
			return AddTaskPriorityWidget(parent,mediator) 
		elif widget == "Duedate":
			return AddTaskDuedateWidget(parent,mediator) 
		elif widget == "MilestoneBox":
			return AddTaskMilestoneBoxWidget(parent,mediator) 
		elif widget == "EditMilestoneBox":
			return EditTaskMilestoneBoxWidget(parent,mediator) 
		elif widget == "Category":
			return AddTaskCategoryWidget(parent,mediator)
		elif widget == "MilestoneCtrl":
			return AddTaskMilestoneButtonWidget(parent,mediator)
		elif widget == "Decision":
			return AddTaskDecisionWidget(parent,mediator)
		else:
			return None

class BannerWidget:
	def __init__(self,parent,mediator):
		self.panel = wx.Panel(parent)
		self.mediator = mediator
		self.command = dict()
		
		self.banner = wx.StaticText(self.panel, wx.ID_ANY, label="TASKMAN 1.0")
		self.subBanner = wx.StaticText(self.panel, wx.ID_ANY, label="(Quora)")

		font = wx.Font(28, wx.SWISS, wx.NORMAL, wx.BOLD)
		font2 = wx.Font(20, wx.SWISS, wx.NORMAL, wx.BOLD)
		self.banner.SetFont(font)		
		self.subBanner.SetFont(font2)		
	
		self.sizer = wx.BoxSizer(wx.VERTICAL)
		self.sizer.Add(self.banner, 0, flag=wx.ALL|wx.CENTER, border=10)
		self.sizer.Add(self.subBanner, 0, flag=wx.ALL|wx.CENTER, border=10)

		self.panel.SetSizer(self.sizer)

class LoginWidget:
	def __init__(self,parent,mediator):
		self.panel = wx.Panel(parent)
		self.mediator = mediator
		self.command = dict()
		
		self.nameLabel = wx.StaticText(self.panel, wx.ID_ANY, label="What is your name?")
		self.username = wx.TextCtrl(self.panel, wx.ID_ANY,style = wx.TE_CENTRE,  size=(300,40))
		self.passwordLabel = wx.StaticText(self.panel, wx.ID_ANY, label="Password please")
		self.password = wx.TextCtrl(self.panel, wx.ID_ANY,style= wx.ALIGN_CENTRE, size=(300,40))
		self.login = wx.Button(self.panel, wx.ID_ANY, "Login Now")

		font = wx.Font(14, wx.SWISS, wx.NORMAL, wx.NORMAL)
		self.nameLabel.SetFont(font)		
		self.username.SetFont(font)		
		self.passwordLabel.SetFont(font)		
		self.password.SetFont(font)		
		self.login.SetFont(font)		
	
		#event binding
		self.login.Bind (wx.EVT_BUTTON, self.onLogin)
		
		self.sizer = wx.BoxSizer(wx.VERTICAL)
		self.sizer.Add(self.nameLabel, 0, flag=wx.ALL|wx.CENTER, border=10)
		self.sizer.Add(self.username, 0, flag=wx.ALL|wx.CENTER, border=10)
		self.sizer.Add(self.passwordLabel, 0, flag=wx.ALL|wx.CENTER, border=10)
		self.sizer.Add(self.password, 0, flag=wx.ALL|wx.CENTER, border=10)
		self.sizer.AddSpacer(60)
		self.sizer.Add(self.login, 0, flag=wx.ALL|wx.CENTER, border=10)

		self.panel.SetSizer(self.sizer)

	def onLogin(self, event):
		self.command["type"] = "Login"
		self.command["user"] = self.username.GetValue()
		self.command["password"] = self.password.GetValue()
		return self.mediator.response(self.command)

	def setValue(self, val):
		self.password.SetValue(val)

class CloseButtonWidget:
	def __init__(self,parent,mediator):
		self.panel = wx.Panel(parent)
		self.mediator = mediator
		self.command = dict()
		
		self.close = wx.Button(self.panel, wx.ID_ANY, "Close")

		#event binding
		self.close.Bind (wx.EVT_BUTTON, self.onClose)
		
		self.sizer = wx.BoxSizer(wx.VERTICAL)
		self.sizer.Add(self.close, 0, flag=wx.ALL|wx.RIGHT, border=2)

		self.panel.SetSizer(self.sizer)

	def onClose(self, event):
		self.command["type"] = "Close"
		return self.mediator.response(self.command)

class LogoutWidget:
	def __init__(self,parent,mediator):
		self.panel = wx.Panel(parent)
		self.mediator = mediator
		self.command = dict()
		
		self.logout = wx.Button(self.panel, wx.ID_ANY, "Logout")

		#event binding
		self.logout.Bind (wx.EVT_BUTTON, self.onLogout)
		
		self.sizer = wx.BoxSizer(wx.VERTICAL)
		self.sizer.Add(self.logout, 0, flag=wx.ALL|wx.RIGHT, border=2)

		self.panel.SetSizer(self.sizer)

	def onLogout(self, event):
		self.command["type"] = "Logout"
		return self.mediator.response(self.command)

class CompleteTaskWidget:
	def __init__(self,parent,mediator):
		self.panel = wx.Panel(parent)
		self.mediator = mediator
		self.command = dict()
		
		self.completeButton = wx.Button(self.panel, wx.ID_ANY, "Completed Task")

		#event binding
		self.completeButton.Bind (wx.EVT_BUTTON, self.onComplete)
		
		self.sizer = wx.BoxSizer(wx.VERTICAL)
		self.sizer.Add(self.completeButton, 0, flag=wx.ALL|wx.CENTER, border=2)

		self.panel.SetSizer(self.sizer)

	def onComplete(self, event):
		self.command["type"] = "ShowComplete"
		return self.mediator.response(self.command)

class AddTaskDecisionWidget:
	def __init__(self,parent,mediator):
		self.panel = wx.Panel(parent)
		self.mediator = mediator
		self.command = dict()
		
		#self.save = wx.Button(self.panel, wx.ID_ANY, "Save")
		self.delete = wx.Button(self.panel, wx.ID_ANY, "Delete")
		self.post = wx.Button(self.panel, wx.ID_ANY, "Post")
		
		#event binding
		#self.save.Bind(wx.EVT_BUTTON, self.onSave)
		self.delete.Bind(wx.EVT_BUTTON, self.onDelete)
		self.post.Bind(wx.EVT_BUTTON, self.onPost)
		
		self.sizer = wx.BoxSizer(wx.HORIZONTAL)
		self.sizer.Add(self.delete, 0, flag=wx.ALL|wx.EXPAND, border=10)
		#self.sizer.Add(self.save, 0, flag=wx.ALL|wx.EXPAND, border=10)
		self.sizer.Add(self.post, 0, flag=wx.ALL|wx.EXPAND, border=10)

		self.panel.SetSizer(self.sizer)
	
	def onSave(self, event):
		self.command["type"] = "SaveTask"
		return self.mediator.response(self.command)
	
	def onPost(self, event):
		self.command["type"] = "PostTask"
		return self.mediator.response(self.command)

	def onDelete(self, event):
		self.command["type"] = "DeleteTask"
		self.mediator.response(self.command)

class AddTaskNameWidget:
	def __init__(self,parent,mediator):
		self.panel = wx.Panel(parent)
		self.mediator = mediator

		self.taskNameLabel = wx.StaticText(self.panel, wx.ID_ANY, label="Task Name")
		self.taskNameBox = wx.TextCtrl(self.panel, wx.ID_ANY, size=(300,10))

		self.sizer = wx.BoxSizer(wx.HORIZONTAL)
		self.sizer.Add(self.taskNameLabel, 0, flag=wx.ALL|wx.EXPAND, border=10)
		self.sizer.Add(self.taskNameBox, 0, flag=wx.RIGHT|wx.EXPAND, border=10)

		self.panel.SetSizer(self.sizer)

	def setValue(self, name):
		self.taskNameBox.SetValue(name)

	def getValue(self):
		return self.taskNameBox.GetValue()

class AddTaskPriorityWidget:
	def __init__(self,parent,mediator):
		self.panel = wx.Panel(parent)
		self.mediator = mediator

		self.priority = wx.StaticBox(self.panel, wx.ID_ANY, label="Task Priority")
		self.command["type"] = "PostTask"
		return self.mediator.response(self.command)

	def onDelete(self, event):
		self.command["type"] = "DeleteTask"
		self.mediator.response(self.command)

class AddTaskNameWidget:
	def __init__(self,parent,mediator):
		self.panel = wx.Panel(parent)
		self.mediator = mediator

		self.taskNameLabel = wx.StaticText(self.panel, wx.ID_ANY, label="Task Name")
		self.taskNameBox = wx.TextCtrl(self.panel, wx.ID_ANY, size=(300,10))

		self.sizer = wx.BoxSizer(wx.HORIZONTAL)
		self.sizer.Add(self.taskNameLabel, 0, flag=wx.ALL|wx.EXPAND, border=10)
		self.sizer.Add(self.taskNameBox, 0, flag=wx.RIGHT|wx.EXPAND, border=10)

		self.panel.SetSizer(self.sizer)

	def setValue(self, name):
		self.taskNameBox.SetValue(name)

	def getValue(self):
		return self.taskNameBox.GetValue()

class AddTaskPriorityWidget:
	def __init__(self,parent,mediator):
		self.panel = wx.Panel(parent)
		self.mediator = mediator

		self.priority = wx.StaticBox(self.panel, wx.ID_ANY, label="Task Priority")
		self.command["type"] = "PostTask"
		return self.mediator.response(self.command)

	def onDelete(self, event):
		self.command["type"] = "DeleteTask"
		self.mediator.response(self.command)

class AddTaskNameWidget:
	def __init__(self,parent,mediator):
		self.panel = wx.Panel(parent)
		self.mediator = mediator

		self.taskNameLabel = wx.StaticText(self.panel, wx.ID_ANY, label="Task Name")
		self.taskNameBox = wx.TextCtrl(self.panel, wx.ID_ANY, size=(300,10))

		self.sizer = wx.BoxSizer(wx.HORIZONTAL)
		self.sizer.Add(self.taskNameLabel, 0, flag=wx.ALL|wx.EXPAND, border=10)
		self.sizer.Add(self.taskNameBox, 0, flag=wx.RIGHT|wx.EXPAND, border=10)

		self.panel.SetSizer(self.sizer)

	def setValue(self, name):
		self.taskNameBox.SetValue(name)

	def getValue(self):
		return self.taskNameBox.GetValue()

class AddTaskPriorityWidget:
	def __init__(self,parent,mediator):
		self.panel = wx.Panel(parent)
		self.mediator = mediator

		self.priority = wx.StaticBox(self.panel, wx.ID_ANY, label="Task Priority")
		self.priorityButton1 = wx.RadioButton(self.panel, wx.ID_ANY, label='Urgent', style=wx.RB_GROUP)
		self.priorityButton2 = wx.RadioButton(self.panel, wx.ID_ANY, label='Immediate')
		self.priorityButton3 = wx.RadioButton(self.panel, wx.ID_ANY, label='Fixed')
		self.priorityButton4 = wx.RadioButton(self.panel, wx.ID_ANY, label='Tentative')

		self.v_sizer = wx.StaticBoxSizer(self.priority, wx.VERTICAL)
		self.v_sizer.Add(self.priorityButton1, 0, flag=wx.ALL|wx.EXPAND, border=3)
		self.v_sizer.Add(self.priorityButton2, 0, flag=wx.ALL|wx.EXPAND, border=3)
		self.v_sizer.Add(self.priorityButton3, 0, flag=wx.ALL|wx.EXPAND, border=3)
		self.v_sizer.Add(self.priorityButton4, 0, flag=wx.ALL|wx.EXPAND, border=3)

		self.panel.SetSizer(self.v_sizer)

	def setValue(self, priority):
		if (priority == "Urgent"):
			self.priorityButton1.SetValue(True)
		elif (priority == "Immediate"):
			self.priorityButton2.SetValue(True)
		elif (priority == "Fixed"):
			self.priorityButton3.SetValue(True)
		elif (priority == "Tentative"):
			self.priorityButton4.SetValue(True)
		else:
			return None

	def getValue(self):
		if(self.priorityButton1.GetValue()): 
			return "Urgent"
		elif(self.priorityButton2.GetValue()): 
			return "Immediate"
		elif(self.priorityButton3.GetValue()): 
			return "Fixed"
		elif(self.priorityButton4.GetValue()): 
			return "Tentative"
		else:
			return ""	
		
class AddTaskDuedateWidget:
	def __init__(self,parent,mediator):
		self.panel = wx.Panel(parent)
		self.mediator = mediator

		self.calendar = wx.calendar.CalendarCtrl(self.panel, -1, wx.DateTime_Now())
		self.hourLabel = wx.StaticText(self.panel, wx.ID_ANY, label="Hour")
		self.minuteLabel = wx.StaticText(self.panel, wx.ID_ANY, label="Minute")
		self.dueDate = wx.StaticBox(self.panel, wx.ID_ANY, label="Task Deadline")
		self.hourCtrl = wx.SpinCtrl(self.panel, wx.ID_ANY, value='9', size=(50,25))
		self.hourCtrl.SetRange(0, 23)
		self.minuteCtrl = wx.SpinCtrl(self.panel, wx.ID_ANY, value='0', size=(50,25))
		self.minuteCtrl.SetRange(0, 59)

		self.h_sizer = wx.BoxSizer(wx.HORIZONTAL)
		self.h_sizer.Add(self.hourLabel, 0, flag=wx.ALL|wx.EXPAND, border=5)
		self.h_sizer.Add(self.hourCtrl, 0, flag=wx.RIGHT|wx.EXPAND, border=3)
		self.h_sizer.Add(self.minuteLabel, 0, flag=wx.ALL|wx.EXPAND, border=3)
		self.h_sizer.Add(self.minuteCtrl, 0, flag=wx.ALL|wx.EXPAND, border=3)
		self.sizer = wx.StaticBoxSizer(self.dueDate, wx.VERTICAL)
		self.sizer.Add(self.h_sizer, 0, flag=wx.ALL|wx.EXPAND, border=10)
		self.sizer.Add(self.calendar, 0, flag=wx.ALL|wx.EXPAND, border=10)
		self.panel.SetSizer(self.sizer)

	def getValue(self):
		wxdate =  self.calendar.GetDate()
		if(wxdate.Year < 1900):
			wxdate.Year = 1900
		date = datetime(year=wxdate.Year, day=wxdate.Day, month=wxdate.Month+1, minute=self.minuteCtrl.GetValue(), hour=self.hourCtrl.GetValue())
		return date

	def setValue(self, date):
		self.calendar.SetDate(wx.DateTimeFromDMY(day=date.day, month=date.month-1, year=date.year))
		self.minuteCtrl.SetValue(date.minute)
		self.hourCtrl.SetValue(date.hour)

class AddTaskCategoryWidget:
	def __init__(self,parent,mediator):
		self.panel = wx.Panel(parent)
		self.mediator = mediator
		self.command = dict()

		self.category = wx.StaticBox(self.panel, wx.ID_ANY, label="Task Category")
		self.categoryBox = wx.ListBox(self.panel, wx.ID_ANY)
		self.addCategoryButton = wx.Button(self.panel, wx.ID_ANY, "Add Category")
		self.removeCategoryButton = wx.Button(self.panel, wx.ID_ANY, "Remove Category")

		self.sizer_v = wx.BoxSizer(wx.VERTICAL)
		self.sizer_h = wx.BoxSizer(wx.HORIZONTAL)
		self.sizer = wx.StaticBoxSizer(self.category, wx.VERTICAL)
		self.sizer_v.Add(self.addCategoryButton, 0, flag=wx.ALL|wx.EXPAND, border=10)
		self.sizer_v.Add(self.removeCategoryButton, 0, flag=wx.ALL|wx.EXPAND, border=10)
		self.sizer_h.Add(self.categoryBox, 0, flag=wx.ALL|wx.EXPAND, border=10)
		self.sizer_h.Add(self.sizer_v, 0, flag=wx.ALL|wx.EXPAND, border=10)
		self.sizer.Add(self.sizer_h, 1, flag=wx.ALL|wx.EXPAND, border=0)

		self.panel.SetSizer(self.sizer)

		self.addCategoryButton.Bind (wx.EVT_BUTTON, self.onAddCategory)
		self.removeCategoryButton.Bind (wx.EVT_BUTTON, self.onRemoveCategory)

	def setValue(self, data):	
		index = 0
		for i in range(len(data[TASK_USER_CATEGORY])):
			self.categoryBox.Insert(data[TASK_USER_CATEGORY][i], index)
			if(data[TASK_USER_CATEGORY][i] == data[TASK_CATEGORY]):
				self.categoryBox.SetSelection(index)
			index += 1

	def onAddCategory(self, event):
		text = wx.GetTextFromUser('Enter a new category', 'Insert dialog')
		if text != '':
			self.categoryBox.Append(text)
			data = self.onLoadCategory()
			data.append(text)
			self.onSaveCategory(data)
	
	def onRemoveCategory(self, event):
		sel = self.categoryBox.GetSelection()
		if sel != -1:
			self.categoryBox.Delete(sel)
			data = self.onLoadCategory()
			del(data[sel])
			self.onSaveCategory(data)

	def onLoadCategory(self):
		self.command["type"] = "LoadCategory"
		return self.mediator.response(self.command)

	def onSaveCategory(self, data):
		self.command["type"] = "SaveCategory"
		self.command["data"] = data
		self.mediator.response(self.command)

	def getValue(self):
		index = self.categoryBox.GetSelection()
		if index != -1:
			return self.categoryBox.GetString(index)	

class AddTaskMilestoneButtonWidget:
	def __init__(self,parent,mediator):
		self.panel = wx.Panel(parent)
		self.mediator = mediator
		self.command = dict()

		self.addMilestone = wx.Button(self.panel, wx.ID_ANY, "Add Milestone")
		self.removeMilestone = wx.Button(self.panel, wx.ID_ANY, "Remove Milestone")
		self.copyMilestone = wx.Button(self.panel, wx.ID_ANY, "Copy Milestone")
		
		self.sizer = wx.BoxSizer(wx.VERTICAL)
		self.sizer.Add(self.addMilestone, 0, flag=wx.ALL|wx.EXPAND, border=10)
		self.sizer.Add(self.copyMilestone, 0, flag=wx.ALL|wx.EXPAND, border=10)
		self.sizer.Add(self.removeMilestone, 0, flag=wx.ALL|wx.EXPAND, border=10)

		self.panel.SetSizer(self.sizer)
	
		self.addMilestone.Bind (wx.EVT_BUTTON, self.onAddMilestone)
		self.removeMilestone.Bind (wx.EVT_BUTTON, self.onRemoveMilestone)
		self.copyMilestone.Bind (wx.EVT_BUTTON, self.onCopyMilestone)

	def onAddMilestone(self, event):
		self.command["type"]="AddMilestone"
		self.mediator.response(self.command)

	def onRemoveMilestone(self, event):
		self.command["type"]="RemoveMilestone"
		self.mediator.response(self.command)

	def onCopyMilestone(self, event):
		self.command["type"]="CopyMilestone"
		self.mediator.response(self.command)


class AddTaskMilestoneBoxWidget:
	def __init__(self,parent,mediator):
		self.panel = wx.Panel(parent)
		self.mediator = mediator
		self.milestoneBox = TextEditListCtrl(self.panel)

		self.milestoneBox.InsertColumn(0,"Milestone")
		self.milestoneBox.SetColumnWidth(0,240)
		self.milestoneBox.InsertColumn(1,"Weight")
		self.milestoneBox.SetColumnWidth(1,140)
		self.milestoneBox.InsertColumn(2,"Details")
		
		self.sizer = wx.BoxSizer(wx.HORIZONTAL)
		self.sizer.Add(self.milestoneBox, 1, flag=wx.ALL|wx.EXPAND, border=2)
		
		self.panel.SetSizer(self.sizer)	

	def setValue(self, data):
		TemplatePopulateMilestone().populate(self.milestoneBox, data)
		
	def addMilestone(self):
		index = self.milestoneBox.GetFocusedItem()
		milestone = dict()
		milestone[MILESTONE_NAME] = "untitled"
		milestone[MILESTONE_WEIGHT] = "10"
		milestone[MILESTONE_DETAILS] = "none"
		data = self.getValue()
		data.append(milestone)
		self.setValue(data)
	
	def copyMilestone(self):
		index = self.milestoneBox.GetFocusedItem()
		milestone = dict()
		milestone[MILESTONE_NAME] = self.milestoneBox.GetItem(index,0).GetText()	
		milestone[MILESTONE_WEIGHT] = self.milestoneBox.GetItem(index,1).GetText()			
		milestone[MILESTONE_DETAILS] = self.milestoneBox.GetItem(index,2).GetText()		
		data = self.getValue()
		data.append(milestone)
		self.setValue(data)

	def removeMilestone(self,data):
		index = self.milestoneBox.GetFocusedItem()
		self.milestoneBox.DeleteItem(index)
		del(data[index])

	def saveMilestone(self,data):
		index = self.milestoneBox.GetFocusedItem()
		self.milestoneBox.DeleteItem(index)
		del(data[index])

	def getValue(self):
		data = list()
		for i in range(self.milestoneBox.GetItemCount()):
			rowdata = dict()
			rowdata[MILESTONE_NAME] = self.milestoneBox.GetItem(i,0).GetText()	
			rowdata[MILESTONE_WEIGHT] = self.milestoneBox.GetItem(i,1).GetText()			
			rowdata[MILESTONE_DETAILS] = self.milestoneBox.GetItem(i,2).GetText()		
			rowdata[MILESTONE_CHECKED] = False
			data.append(rowdata)
		return data

class EditTaskMilestoneBoxWidget:
	def __init__(self,parent,mediator):
		self.panel = wx.Panel(parent)
		self.mediator = mediator
		self.milestoneBox = TextCheckEditListCtrl(self.panel)

		self.milestoneBox.InsertColumn(0,"Milestone")
		self.milestoneBox.SetColumnWidth(0,240)
		self.milestoneBox.InsertColumn(1,"Weight")
		self.milestoneBox.SetColumnWidth(1,140)
		self.milestoneBox.InsertColumn(2,"Details")
		
		self.sizer = wx.BoxSizer(wx.HORIZONTAL)
		self.sizer.Add(self.milestoneBox, 1, flag=wx.ALL|wx.EXPAND, border=2)
		
		self.panel.SetSizer(self.sizer)	

	def setValue(self, data):
		TemplatePopulateCheckedMilestone().populate(self.milestoneBox, data)
		
	def addMilestone(self):
		index = self.milestoneBox.GetFocusedItem()
		milestone = dict()
		milestone[MILESTONE_NAME] = "untitled"
		milestone[MILESTONE_WEIGHT] = "10"
		milestone[MILESTONE_DETAILS] = "none"
		data = self.getValue()
		data.append(milestone)
		self.setValue(data)
	
	def copyMilestone(self):
		index = self.milestoneBox.GetFocusedItem()
		milestone = dict()
		milestone[MILESTONE_NAME] = self.milestoneBox.GetItem(index,0).GetText()	
		milestone[MILESTONE_WEIGHT] = self.milestoneBox.GetItem(index,1).GetText()			
		milestone[MILESTONE_DETAILS] = self.milestoneBox.GetItem(index,2).GetText()		
		data = self.getValue()
		data.append(milestone)
		self.setValue(data)

	def removeMilestone(self,data):
		index = self.milestoneBox.GetFocusedItem()
		self.milestoneBox.DeleteItem(index)
		del(data[index])

	def getValue(self):
		data = list()
		for i in range(self.milestoneBox.GetItemCount()):
			rowdata = dict()
			rowdata[MILESTONE_NAME] = self.milestoneBox.GetItem(i,0).GetText()	
			rowdata[MILESTONE_WEIGHT] = self.milestoneBox.GetItem(i,1).GetText()			
			rowdata[MILESTONE_DETAILS] = self.milestoneBox.GetItem(i,2).GetText()		
			if (self.milestoneBox.IsChecked(i)==True):
				rowdata[MILESTONE_CHECKED] = True
				rowdata[MILESTONE_FINISHDATE] = TemplateDate.now()
			else:
				rowdata[MILESTONE_CHECKED] = False
			data.append(rowdata)
		return data

class TaskListBoxWidget:
	def __init__(self,parent,mediator):
		self.panel = wx.Panel(parent)
		self.mediator = mediator 
		self.taskList = AutoWidthListCtrl(self.panel)
		self.command = dict()

		self.taskList.Bind(wx.EVT_LIST_ITEM_SELECTED,self.onSelect)
		self.taskList.InsertColumn(0,"Task Name")
		self.taskList.SetColumnWidth(0,140)
		self.taskList.InsertColumn(1,"Start Date")
		self.taskList.SetColumnWidth(1,140)
		self.taskList.InsertColumn(2,"Priority")
		self.taskList.SetColumnWidth(2,140)
		self.taskList.InsertColumn(3,"Progress")
		self.taskList.SetColumnWidth(3,140)
		self.taskList.InsertColumn(4,"Category")
		self.taskList.SetColumnWidth(4,140)
		self.taskList.InsertColumn(5,"Due Date")
		self.taskList.SetColumnWidth(5,140)

		self.sizer = wx.BoxSizer(wx.HORIZONTAL)
		self.sizer.Add(self.taskList, 1, flag=wx.ALL|wx.EXPAND, border=2)

		self.panel.SetSizer(self.sizer)			

	def onSelect(self, event):
		self.command["type"]="TaskSelect"
		index = self.taskList.GetFocusedItem()
		self.command["index"]=index
		self.mediator.response(self.command)

	def setValue(self, data):
		TemplatePopulateTask().populate(self.taskList, data)

	def setSelect(self, index):
		self.taskList.Focus(index)

	def onEditTask(self):
		index = self.taskList.GetFocusedItem()
		self.command["index"]=index
		self.command["type"]="EditTask2"
		self.mediator.response(self.command)	

	def onUpdateTask(self,command):
		index = self.taskList.GetFocusedItem()
		command["index"]=index
		command["type"]="UpdateTask3"
		self.mediator.response(command)	
	
	def onCopyTask(self):
		index = self.taskList.GetFocusedItem()
		self.command["index"]=index
		self.command["type"]="CopyTask2"
		self.mediator.response(self.command)	

	def onRemoveTask(self):
		index = self.taskList.GetFocusedItem()
		self.command["index"]=index
		self.command["type"]="RemoveTask2"
		self.mediator.response(self.command)	

class TaskButtonWidget:
	def __init__(self,parent,mediator):
		self.panel = wx.Panel(parent)
		self.mediator = mediator
		self.command = dict()		

		self.addTask = wx.Button(self.panel, wx.ID_ANY, "Add Task")
		self.removeTask = wx.Button(self.panel, wx.ID_ANY, "Remove Task")
		self.editTask = wx.Button(self.panel, wx.ID_ANY, "Edit Task")
		self.updateTask = wx.Button(self.panel, wx.ID_ANY, "Update Task")
		self.copyTask = wx.Button(self.panel, wx.ID_ANY, "Copy Task")
		
		#event binding
		self.addTask.Bind (wx.EVT_BUTTON, self.onAddTask)
		self.removeTask.Bind (wx.EVT_BUTTON, self.onRemoveTask)
		self.editTask.Bind (wx.EVT_BUTTON, self.onEditTask)
		self.updateTask.Bind (wx.EVT_BUTTON, self.onUpdateTask)
		self.copyTask.Bind (wx.EVT_BUTTON, self.onCopyTask)
		
		self.taskButtonSizer = wx.BoxSizer(wx.VERTICAL)
		self.taskButtonSizer.Add(self.addTask, 0, flag=wx.ALL|wx.EXPAND, border=5) 
		self.taskButtonSizer.Add(self.editTask, 0, flag=wx.ALL|wx.EXPAND, border=5) 
		self.taskButtonSizer.Add(self.updateTask, 0, flag=wx.ALL|wx.EXPAND, border=5) 
		self.taskButtonSizer.Add(self.copyTask, 0, flag=wx.ALL|wx.EXPAND, border=5) 
		self.taskButtonSizer.Add(self.removeTask, 0, flag=wx.ALL|wx.EXPAND, border=5) 

		self.panel.SetSizer(self.taskButtonSizer)

	def onAddTask(self,event):
		self.command["type"]="AddTask"
		self.mediator.response(self.command)

	def onRemoveTask(self,event):
		self.command["type"]="RemoveTask"
		self.mediator.response(self.command)

	def onEditTask(self, event):
		self.command["type"]="EditTask"
		self.mediator.response(self.command)

	def onUpdateTask(self, event):
		self.command["type"]="UpdateTask"
		self.mediator.response(self.command)

	def onCopyTask(self, event):
		self.command["type"]="CopyTask"
		self.mediator.response(self.command)

class SortButtonWidget:
	def __init__(self,parent,mediator):
		self.panel = wx.Panel(parent)
		self.mediator = mediator
		self.command = dict()

		self.postDateSort = wx.Button(self.panel, wx.ID_ANY, "Post date")
		self.dueDateSort = wx.Button(self.panel, wx.ID_ANY, "Due date")
		self.progressSort = wx.Button(self.panel, wx.ID_ANY, "Progress")
		self.prioritySort = wx.Button(self.panel, wx.ID_ANY, "Priority")
		self.nameSort = wx.Button(self.panel, wx.ID_ANY, "Name")

		#event binding
		self.postDateSort.Bind (wx.EVT_BUTTON, self.onPostDateSort)
		self.dueDateSort.Bind (wx.EVT_BUTTON, self.onDueDateSort)
		self.prioritySort.Bind (wx.EVT_BUTTON, self.onPrioritySort)
		self.progressSort.Bind (wx.EVT_BUTTON, self.onProgressSort)
		self.nameSort.Bind (wx.EVT_BUTTON, self.onNameSort)

		#putting to the sizer
		self.sortText = wx.StaticText(self.panel, wx.ID_ANY, label="Sort task By Field", style=wx.TE_READONLY)	
		self.sortButtonSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.sortButtonSizer.Add(self.postDateSort, 1, flag=wx.ALL|wx.EXPAND, border=5) 
		self.sortButtonSizer.Add(self.dueDateSort, 1, flag=wx.ALL|wx.EXPAND, border=5) 
		self.sortButtonSizer.Add(self.progressSort, 1, flag=wx.ALL|wx.EXPAND, border=5) 
		self.sortButtonSizer.Add(self.prioritySort, 1, flag=wx.ALL|wx.EXPAND, border=5) 
		self.sortButtonSizer.Add(self.nameSort, 1, flag=wx.ALL|wx.EXPAND, border=5) 
		
		self.sizer = wx.BoxSizer(wx.VERTICAL)
		self.sizer.Add(self.sortText, 0, flag=wx.ALL|wx.EXPAND, border=5)
		self.sizer.Add(self.sortButtonSizer, 1, flag=wx.ALL|wx.EXPAND, border=5)

		self.panel.SetSizer(self.sizer)

	def onPostDateSort(self, event):
		self.command["type"]="TaskSort"
		self.command["field"]="PostDateSort"
		self.mediator.response(self.command)
	
	def onDueDateSort(self, event):
		self.command["type"]="TaskSort"
		self.command["field"]="DueDateSort"
		self.mediator.response(self.command)

	def onPrioritySort(self, event):
		self.command["type"]="TaskSort"
		self.command["field"]="PrioritySort"
		self.mediator.response(self.command)

	def onProgressSort(self, event):
		self.command["type"]="TaskSort"
		self.command["field"]="ProgressSort"
		self.mediator.response(self.command)

	def onNameSort(self, event):
		self.command["type"]="TaskSort"
		self.command["field"]="NameSort"
		self.mediator.response(self.command)

class MileStoneBoxWidget:
	def __init__(self,parent,mediator):
		self.panel = wx.Panel(parent)
		self.mediator = mediator
		self.command = dict()

		self.detailText = wx.StaticText(self.panel, wx.ID_ANY, label="Task MileStone", style=wx.TE_READONLY)
		self.detailBox = CheckListCtrl(self.panel)

		self.detailBox.Bind(wx.EVT_LIST_ITEM_SELECTED,self.onSelect)
		self.detailBox.InsertColumn(0,"Sub-task Milestone")
		self.detailBox.SetColumnWidth(0,190)
		self.detailBox.InsertColumn(1,"Work Load", wx.LIST_FORMAT_CENTER)
		self.detailBox.SetColumnWidth(1,90)
		self.detailBox.InsertColumn(2,"Notes",wx.LIST_FORMAT_CENTER)		

		self.sizer = wx.BoxSizer(wx.VERTICAL)
		self.sizer.Add(self.detailText, 0, flag=wx.ALL|wx.EXPAND, border=5)
		self.sizer.Add(self.detailBox, 1, flag=wx.ALL|wx.EXPAND, border=5)
		
		self.panel.SetSizer(self.sizer)

	def onSelect(self, event):
		self.command["type"]="MilestoneSelect"
		self.mediator.response(self.command)

	def setValue(self,data):
		TemplatePopulateCheckedMilestone().populate(self.detailBox, data)

	def getValue(self):
		command = dict()
		data = list()
		total = 0
		progress = 0
		for i in range(self.detailBox.GetItemCount()):
			rowdata = dict()	
			rowdata[MILESTONE_NAME]=self.detailBox.GetItem(i,0).GetText()	
			rowdata[MILESTONE_WEIGHT]=self.detailBox.GetItem(i,1).GetText()	
			total += int(rowdata[MILESTONE_WEIGHT])
			rowdata[MILESTONE_DETAILS]=self.detailBox.GetItem(i,2).GetText()	
			if (self.detailBox.IsChecked(i)==True):
				rowdata[MILESTONE_CHECKED] = True
				rowdata[MILESTONE_FINISHDATE] = TemplateDate.now()
				progress += int(rowdata[MILESTONE_WEIGHT])
			else:
				rowdata[MILESTONE_CHECKED] = False
			data.append(rowdata)
		if( total > 0):
			command["progress"] = progress*100/total	
		else:
			command["progress"] = 0	
		command["data"] = data
		return command

class CompletedMileStoneBoxWidget:
	def __init__(self,parent,mediator):
		self.panel = wx.Panel(parent)
		self.mediator = mediator
		self.command = dict()

		self.detailText = wx.StaticText(self.panel, wx.ID_ANY, label="Task MileStone", style=wx.TE_READONLY)
		self.detailBox = AutoWidthListCtrl(self.panel)

		self.detailBox.Bind(wx.EVT_LIST_ITEM_SELECTED,self.onSelect)
		self.detailBox.InsertColumn(0,"Sub-task Milestone")
		self.detailBox.SetColumnWidth(0,190)
		self.detailBox.InsertColumn(1,"Work Load", wx.LIST_FORMAT_CENTER)
		self.detailBox.SetColumnWidth(1,90)
		self.detailBox.InsertColumn(2,"Notes",wx.LIST_FORMAT_CENTER)		

		self.sizer = wx.BoxSizer(wx.VERTICAL)
		self.sizer.Add(self.detailText, 0, flag=wx.ALL|wx.EXPAND, border=5)
		self.sizer.Add(self.detailBox, 1, flag=wx.ALL|wx.EXPAND, border=5)
		
		self.panel.SetSizer(self.sizer)

	def onSelect(self, event):
		self.command["type"]="MilestoneSelect"
		self.mediator.response(self.command)

	def setValue(self,data):
		TemplatePopulateMilestone().populate(self.detailBox, data)

class CheckListCtrl(wx.ListCtrl, CheckListCtrlMixin, ListCtrlAutoWidthMixin):
	def __init__(self, parent):
		wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
		CheckListCtrlMixin.__init__(self)
		ListCtrlAutoWidthMixin.__init__(self)

class AutoWidthListCtrl(wx.ListCtrl, ListCtrlAutoWidthMixin):
	def __init__(self, parent):
		wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
		ListCtrlAutoWidthMixin.__init__(self)

class TextEditListCtrl(wx.ListCtrl, ListCtrlAutoWidthMixin, TextEditMixin):
	def __init__(self, parent):
		wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
		ListCtrlAutoWidthMixin.__init__(self)
		TextEditMixin.__init__(self)

class TextCheckEditListCtrl(wx.ListCtrl, CheckListCtrlMixin, ListCtrlAutoWidthMixin, TextEditMixin):
	def __init__(self, parent):
		wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
		CheckListCtrlMixin.__init__(self)
		ListCtrlAutoWidthMixin.__init__(self)
		TextEditMixin.__init__(self)
