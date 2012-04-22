from operator import itemgetter, attrgetter
from datetime import datetime, timedelta
from Define import *

class TemplatePopulate:
	def populate(self,listbox, data):
		box = listbox
		box.DeleteAllItems()
		totalData = len(data)
		for i in range(totalData):
			item = data[i]
			self.insertData(box,item,i)
			"""
			box.InsertStringItem(i, item[TASK_NAME])
			for j in range(totalField):
				if j==0: continue
				else: box.SetStringItem(i, j, item[j])
			"""
			box.SetItemData(i, i)

class TemplatePopulateTask(TemplatePopulate):
	def insertData(self,box,item,row):
		box.InsertStringItem(row, item[TASK_NAME])
		box.SetStringItem(row,TASK_POSTDATE_INDEX,item[TASK_POSTDATE]) 
		box.SetStringItem(row,TASK_PRIORITY_INDEX,item[TASK_PRIORITY]) 
		box.SetStringItem(row,TASK_PROGRESS_INDEX,item[TASK_PROGRESS]) 
		box.SetStringItem(row,TASK_CATEGORY_INDEX,item[TASK_CATEGORY]) 
		box.SetStringItem(row,TASK_DUEDATE_INDEX,item[TASK_DUEDATE]) 

class TemplatePopulateMilestone(TemplatePopulate):
	def insertData(self,box,item,row):
		box.InsertStringItem(row, item[MILESTONE_NAME])
		box.SetStringItem(row,MILESTONE_WEIGHT_INDEX,item[MILESTONE_WEIGHT]) 
		box.SetStringItem(row,MILESTONE_DETAILS_INDEX,item[MILESTONE_DETAILS]) 

class TemplatePopulateCheckedMilestone(TemplatePopulate):
	def insertData(self,box,item,row):
		box.InsertStringItem(row, item[MILESTONE_NAME])
		box.SetStringItem(row,MILESTONE_WEIGHT_INDEX,item[MILESTONE_WEIGHT]) 
		box.SetStringItem(row,MILESTONE_DETAILS_INDEX,item[MILESTONE_DETAILS]) 
		if(item.has_key(MILESTONE_CHECKED)):
			box.CheckItem(row, item[MILESTONE_CHECKED])

class TemplateSort:
	def __init__(self, data):
		self.data = data

	def sort(self):
		self.sortData()
		return self.data

class SortName(TemplateSort):
	def sortData(self):
		self.data = sorted(self.data, key = itemgetter(TASK_NAME))

class SortPostDate(TemplateSort):
	def sortData(self):
		self.modifyData()
		self.data = sorted(self.data, key = itemgetter(TASK_POSTDATE))
		self.recoverData()

	def recoverData(self):
		for i in range(len(self.data)):
			item = self.data[i]
			self.data[i][TASK_POSTDATE] = TemplateDate.formatDate(item[TASK_POSTDATE])		

	def modifyData(self):
		for i in range(len(self.data)):
			item = self.data[i]
			self.data[i][TASK_POSTDATE] = TemplateDate.unformatDate(item[TASK_POSTDATE])		

class SortPriority(TemplateSort):
	def sortData(self):
		self.modifyData()
		self.data = sorted(self.data, key = itemgetter(TASK_PRIORITY))
		self.recoverData()

	def recoverData(self):
		ref = dict()
		ref[1] = "Urgent"
		ref[2] = "Immediate"
		ref[3] = "Fixed"
		ref[4] = "Tentative"

		for i in range(len(self.data)):
			item = self.data[i]
			self.data[i][TASK_PRIORITY] = ref[item[TASK_PRIORITY]]			

	def modifyData(self):
		ref = dict()
		ref["Urgent"] = 1
		ref["Immediate"] = 2
		ref["Fixed"] = 3
		ref["Tentative"] = 4

		for i in range(len(self.data)):
			item = self.data[i]
			self.data[i][TASK_PRIORITY] = ref[item[TASK_PRIORITY]]

class SortProgress(TemplateSort):
	def sortData(self):
		self.modifyData()
		self.data = sorted(self.data, key = itemgetter(TASK_PROGRESS))
		self.recoverData()

	def recoverData(self):
		for i in range(len(self.data)):
			item = self.data[i]
			self.data[i][TASK_PROGRESS] = str(item[TASK_PROGRESS])+"%"		

	def modifyData(self):
		for i in range(len(self.data)):
			item = self.data[i]
			self.data[i][TASK_PROGRESS] = int(item[TASK_PROGRESS][:-1])		

class SortCategory(TemplateSort):
	def sortData(self):
		self.data = sorted(self.data, key = attrgetter(TASK_CATEGORY))

class SortDueDate(TemplateSort):
	def sortData(self):
		self.modifyData()
		self.data = sorted(self.data, key = itemgetter(TASK_DUEDATE))
		self.recoverData()

	def recoverData(self):
		for i in range(len(self.data)):
			item = self.data[i]
			self.data[i][TASK_DUEDATE] = TemplateDate.formatDate(item[TASK_DUEDATE])		

	def modifyData(self):
		for i in range(len(self.data)):
			item = self.data[i]
			self.data[i][TASK_DUEDATE] = TemplateDate.unformatDate(item[TASK_DUEDATE])		

class SortSuggestion(TemplateSort):
	def sortData(self):
		self.data = sorted(self.data, key = itemgetter(2))

class TemplateDate:
	@staticmethod
	def now():
		date = datetime.now()
		date = TemplateDate.formatDate(date)
		return date	

	@staticmethod
	def formatDate(date):
		return datetime.strftime(date,"%d-%m-%y %H:%M")

	@staticmethod
	def unformatDate(date):
		return datetime.strptime(date,"%d-%m-%y %H:%M")
	
	@staticmethod
	def initDueDate():
		date = datetime.now() + timedelta(2,0)
		date = TemplateDate.formatDate(date)
		return date	

	@staticmethod
	def compareDate(date1,date2,diff):
		if( (TemplateDate.unformatDate(date1)-TemplateDate.unformatDate(date2)) > timedelta(minutes = diff)):
			return True
		else:
			return False

class Template:
	@staticmethod
	def getProgress(milestone):
		total = 0
		progress = 0
		for i in range(len(milestone)):
			if(milestone[i].has_key(MILESTONE_CHECKED)):
				if (milestone[i][MILESTONE_CHECKED]):
					try:
						progress += int(milestone[i][MILESTONE_WEIGHT])
					except ValueError:
						return "not int"
			try:
				total += int(milestone[i][MILESTONE_WEIGHT])
			except ValueError:
				return "not int"
		if(total > 0):
			val = progress*100/total
		else:
			val = 0
		return str(val)+"%"
	
	@staticmethod
	def sort(data, field):
		if field == "NameSort":
			value = SortName(data).sort()
		elif field == "PrioritySort":
			value = SortPriority(data).sort()
		elif field == "PostDateSort":
			value = SortPostDate(data).sort()
		elif field == "DueDateSort":
			value = SortDueDate(data).sort()
		elif field == "ProgressSort":
			value = SortProgress(data).sort()
		elif field == "CategorySort":
			value = SortCategory(data).sort()
		elif field == "SuggestionSort":
			value = SortSuggestion(data).sort()
		else : 
			value = data
		return value
