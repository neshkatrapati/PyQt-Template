"""
SettingsDialog
--------------
Takes: template file name, parent dialog
Use : 
(i) Create a new SettingsDialog from the template file
(ii) You can see the appropriate fields rendered 
(iii) Call the add_action method to specify an action name, then its call back method and then whether the dialog must be closed after pressing that action or not.

TemplateFile
------------
-> Each line of the template file is a GUI element 
-> Comment with #
-> Each line has atleast three fields seperated by a ':'
-> Fields
   --> The First field is the GUI Label
   --> Second is the reference key
   --> Third is the field type
--> For some fields like Comboboxes, Radiobuttons, Lists, these 3 fields are followed by the respective choices.
--> Run the SettingsDialog with the sample template 'settings.template'

"""

from PyQt4 import QtGui,QtCore
import sys

class RWindow(QtGui.QDialog):
    def __init__(self, template, parent=None,h=350,w=150,title = "Title"):
        QtGui.QWidget.__init__(self, parent)
        
        
        self.template = template
        self.parent = parent
        self.offset = 0
        self.setWindowTitle(title)
        self.wmap = {"text" : QtGui.QLineEdit,
        			 "textbox" : QtGui.QTextEdit,
        			 "combo" : QtGui.QComboBox,
        			 "checkbox": QtGui.QCheckBox,
        			 "slider": QtGui.QSlider,
        			 "calendar":QtGui.QCalendarWidget,
        			 "radio": QtGui.QGroupBox,
        			 "listcheck": QtGui.QListView}
        self.content_area = QtGui.QVBoxLayout()
        self.layout = QtGui.QVBoxLayout()
        self.layout.addLayout(self.content_area)
        self.action_area = QtGui.QHBoxLayout()
        self.action_area.addStretch(1)
        spacer = QtGui.QSpacerItem(20,40,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.layout.addItem(spacer)
        self.layout.addLayout(self.action_area)
        self.setLayout(self.layout)
        self.buttons = {}
        self.widgets = {}


    def relocate(self,w,h):
        he = QtGui.QDesktopWidget.height(QtGui.QDesktopWidget())
        wi = QtGui.QDesktopWidget.width(QtGui.QDesktopWidget())

        self.resize(w, h)
        self.move(wi - w, he - h - 40)
    
    def add_action(self,action_name,callback,close_after = False):
    	b = QtGui.QPushButton(action_name)
    	b.uniqueId = action_name
    	self.action_area.addWidget(b)
    	self.buttons[b.uniqueId] = [callback,close_after]
    	b.connect(b, QtCore.SIGNAL("clicked()"),self.action_handler)

    def get_widget_value(self,widget,wtype):
  	if wtype in ["text"]:
            return widget.text()
        if wtype in ["textbox"]:
            return widget.toPlainText()
        if wtype in ["calendar"]:
            return widget.selectedDate()
        if wtype in ["slider"]:
            return widget.value()
        if wtype in ["checkbox"]:
            return widget.isChecked()
        if wtype in ["combo"]:
            return widget.currentText()
        if wtype in ["radio"]:
            children = widget.children()[1:]
            for child in children:
                if child.isChecked():
                    return child.text()
        if wtype in ["listcheck"]:
            model = widget.model()
            i = 0
            selected = []
            while model.item(i):
                if model.item(i).checkState() == 2:
                    selected.append(model.item(i).text())
                i += 1
            return selected

    def action_handler(self):
    	sender = QtCore.QObject.sender(self)
    	callback = self.buttons[sender.uniqueId][0]
        close_after = self.buttons[sender.uniqueId][1]
    	values = {}
        for widget in self.widgets.keys():
            values[widget] = self.get_widget_value(self.widgets[widget][0],self.widgets[widget][1])	
        
      
  	callback(values)
        if close_after:
            self.done(1)


    def getClosed(self):
        self.deleteLater()

    def do_minimized(self):
        self.getClosed()
        self.parent.do_toggle()

    def render(self):
    	f = open(self.template)
    	for l in f.readlines():
    		l = l.strip("\n")
    		if l not in ["","\n"," "] and l.startswith("#") == False:
    			l = l.split(":")
    			unit = QtGui.QHBoxLayout()
    			label = QtGui.QLabel(l[0])
    			uiel = self.render_widget(l)
    			self.widgets[l[1]] = [uiel,l[2]]
    			unit.addWidget(label)
    			unit.addSpacing(1)
    			unit.addWidget(uiel)
    			self.content_area.addLayout(unit)

    def render_widget(self,l):
    	wtype = l[2]
    	uiel = self.wmap[wtype]()
    	if wtype == "combo" :
    		extra = l[3:]
    		for item in extra:
    			uiel.addItem(item)
    	elif wtype == "slider":
    		if len(l) <= 3 or l[3] == "horizontal":
    			uiel.setOrientation(QtCore.Qt.Horizontal)
    		elif l[3] == "vertical":
    			uiel.setOrientation(QtCore.Qt.Vertical)
    	elif wtype == "calendar":
    		uiel.setGridVisible(True)
    	elif wtype == "radio":
    		extra = l[3:]
    		d = QtGui.QVBoxLayout()
    		i = 0
    		for item in extra:
    			r = QtGui.QRadioButton(item)
    			if i == 0:
    				r.setChecked(True)

    			d.addWidget(r)
    			i += 1
    		uiel.setLayout(d)
    	if wtype == "listcheck" :
    		extra = l[3:]
    		model = QtGui.QStandardItemModel(uiel)
    		for item in extra:
    			i = QtGui.QStandardItem(item)
    			i.setCheckable(True)
    			model.appendRow(i)
    		uiel.setModel(model)

    	return uiel


### Uncomment the Following Lines to see a demo, Otherwise import this file to use the class

def dummy(*args):
	print args

app = QtGui.QApplication(sys.argv)
s = SettingsDialog(sys.argv[1]) 
s.render()
s.add_action("Submit",dummy,True)
s.show()

sys.exit(app.exec_())
