import os
import sys
import prochandler

from PyQt5 import QtCore, QtGui,QtWidgets
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import (
    QMainWindow, QApplication,
    QLabel, QToolBar, QAction, QStatusBar,QTableWidget,
    QMessageBox,QWidget,QVBoxLayout,QHBoxLayout,QPushButton,QCheckBox,QLineEdit,QDialog,QDialogButtonBox
)
from PyQt5.uic import loadUi

class TaskManager(QMainWindow):
    def __init__(self):
        super(TaskManager,self).__init__()
        loadUi('ui/taskmgrwindow.ui',self)

        self.setWindowTitle("Taskman by @raqdrox")

        self.actionExit.triggered.connect(self.exitApp)
        
        self.showAllCheckbox.stateChanged.connect(self.loadProcessData)


        self.updateSpeedSelector.currentTextChanged.connect(self.SelectUpdateSpeed)

        self.actionUpdateSlow.triggered.connect(lambda: self.SelectUpdateSpeed("Slow"))
        self.actionUpdateNormal.triggered.connect(lambda: self.SelectUpdateSpeed("Normal"))
        self.actionUpdateRealtime.triggered.connect(lambda: self.SelectUpdateSpeed("Realtime"))
        self.actionUpdateNoUpdate.triggered.connect(lambda: self.SelectUpdateSpeed("No Update"))



        #Table Context Menu
        self.procTableWidget.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.sendSignalAction=QtWidgets.QAction("Send Signal",self)
        self.procTableWidget.addAction(self.sendSignalAction)

        #Signal menu
        self.signalMenu=QtWidgets.QMenu(self)
        self.signalMenu.addAction("SIGTERM",lambda: self.SendSignalToSelectedProcess("SIGTERM"))
        self.signalMenu.addAction("SIGKILL",lambda: self.SendSignalToSelectedProcess("SIGKILL"))
        self.signalMenu.addAction("SIGSTOP",lambda: self.SendSignalToSelectedProcess("SIGSTOP"))
        self.signalMenu.addAction("SIGCONT",lambda: self.SendSignalToSelectedProcess("SIGCONT"))
        self.signalMenu.addAction("SIGINT",lambda: self.SendSignalToSelectedProcess("SIGINT"))
        self.signalMenu.addAction("SIGQUIT",lambda: self.SendSignalToSelectedProcess("SIGQUIT"))
        self.signalMenu.addAction("SIGTSTP",lambda: self.SendSignalToSelectedProcess("SIGTSTP"))
        self.signalMenu.addAction("SIGUSR1",lambda: self.SendSignalToSelectedProcess("SIGUSR1"))
        self.signalMenu.addAction("SIGUSR2",lambda: self.SendSignalToSelectedProcess("SIGUSR2"))
        self.sendSignalAction.setMenu(self.signalMenu)

        #Menu for send signal button in menu bar
        self.menuSendSignal.setMenu(self.signalMenu)



        #unselect when clicked on header
        self.procTableWidget.horizontalHeader().sectionClicked.connect(lambda: self.procTableWidget.clearSelection())

        #expand table to fill parent
        self.procTableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)


        
        



        #Delete key shortcut
        self.deleteShortcut=QtWidgets.QShortcut(QtGui.QKeySequence("Delete"),self)
        self.deleteShortcut.activated.connect(lambda: self.SendSignalToSelectedProcess("SIGKILL"))

        #Force Delete key shortcut
        self.forceDeleteShortcut=QtWidgets.QShortcut(QtGui.QKeySequence("Shift+Delete"),self)
        self.forceDeleteShortcut.activated.connect(lambda: self.SendSignalToSelectedProcess("SIGTERM"))

        
        self.tick_timer = QTimer(self)
        self.tick_timer.timeout.connect(self.tick)
        self.tick_timer.start(1000)

        self.actionAbout.triggered.connect(self.ShowAboutDialog)




    def SendSignalToSelectedProcess(self,signal):
        selectedRows=self.procTableWidget.selectionModel().selectedRows()


        if len(selectedRows)==0:
            #show error dialog
            dialog=QMessageBox()
            dialog.setWindowTitle("Error")
            dialog.setText("No process selected")
            dialog.setIcon(QMessageBox.Critical)
            dialog.setStandardButtons(QMessageBox.Ok)
            dialog.setModal(True)
            dialog.exec_()

            return
        
        selectedPids=[]
        selectedNames=[]
        for row in selectedRows:
            selectedPids.append(int(self.procTableWidget.item(row.row(),1).text()))
            selectedNames.append(self.procTableWidget.item(row.row(),2).text())
        
        if self.ShowStopProcessDialog(selectedNames,signal):
            for pid in selectedPids:
                prochandler.send_signal_to_pid(int(pid),signal)
            self.loadProcessData(self.showAllCheckbox.isChecked())

    def SelectUpdateSpeed(self,speed):

        updateSpeedDict={"Slow":5000,"Normal":1000,"Realtime":100 ,"No Update":0}

        if speed in updateSpeedDict:
            if speed=="No Update":
                self.tick_timer.stop()
            else:
                self.tick_timer.start(updateSpeedDict[speed])
                self.tick_timer.setInterval(updateSpeedDict[speed])
                self.updateSpeedSelector.setCurrentText(speed)



    def ShowStopProcessDialog(self,proc_names,signal):
        dialog=QMessageBox()
        dialog.setDetailedText("\n".join(proc_names))


        #show warning dialog according to signal
        wintitle=""
        description=""
        if signal=="SIGKILL":
            wintitle="Kill Process"
            description="Are you sure you want to kill the following processes?"
        elif signal=="SIGTERM":
            wintitle="Terminate Process"
            description="Are you sure you want to terminate the following processes?"
        elif signal=="SIGSTOP":
            wintitle="Pause Process"
            description="Are you sure you want to pause the following processes?"
        elif signal=="SIGCONT":
            wintitle="Resume Process"
            description="Are you sure you want to resume the following processes?"
        elif signal=="SIGINT":
            wintitle="Interrupt Process"
            description="Are you sure you want to interrupt the following processes?"
        elif signal=="SIGQUIT":
            wintitle="Quit Process"
            description="Are you sure you want to quit the following processes?"
        elif signal=="SIGTSTP":
            wintitle="Stop Process"
            description="Are you sure you want to stop the following processes?"
        elif signal=="SIGUSR1":
            wintitle="User Defined Signal 1"
            description="Are you sure you want to send user defined signal 1 to the following processes?"
        elif signal=="SIGUSR2":
            wintitle="User Defined Signal 2"
            description="Are you sure you want to send user defined signal 2 to the following processes?"
        else:
            return False

        dialog.setWindowTitle(wintitle)
        dialog.setText(description)



        dialog.setIcon(QMessageBox.Question)
        dialog.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
        dialog.setDefaultButton(QMessageBox.No)
        dialog.setEscapeButton(QMessageBox.No)
        dialog.setModal(True)
        dialog.exec_()
        return dialog.result()==QMessageBox.Yes

    def exitApp(self):
        self.close()

    def loadProcessData(self,all):
        if all:
            data=prochandler.get_procs_dict()
        else:
            data=prochandler.get_procs_dict_for_current_user()
        
        if data:
            self.populateProcessTable(data)

    def populateProcessTable(self,data):
        self.procTableWidget.setSortingEnabled(False)
        self.procTableWidget.setRowCount(len(data))
        row=0
        for pid,info in data.items():
            self.procTableWidget.setItem(row,0,QtWidgets.QTableWidgetItem(str(info['username'])))
            self.procTableWidget.setItem(row,1,QtWidgets.QTableWidgetItem(str(pid)))
            self.procTableWidget.setItem(row,2,QtWidgets.QTableWidgetItem(str(info["name"])))
            self.procTableWidget.setItem(row,3,QtWidgets.QTableWidgetItem(format(info["cpu_percent"],'.2f')))
            self.procTableWidget.setItem(row,4,QtWidgets.QTableWidgetItem(format(info["memory_percent"],'.2f')))
            self.procTableWidget.setItem(row,5,QtWidgets.QTableWidgetItem(str(info["status"])))
            self.procTableWidget.setItem(row,6,QtWidgets.QTableWidgetItem(' '.join(info["cmdline"])))
            row+=1

        self.procTableWidget.setSortingEnabled(True)        


    def ShowAboutDialog(self):
        dialog=QDialog()
        dialog.setWindowTitle("About")
        dialog.setModal(True)
        dialog.setLayout(QVBoxLayout())
        dialog.layout().addWidget(QLabel("Taskman"))
        dialog.layout().addWidget(QLabel("Author: @raqdrox"))
        dialog.layout().addWidget(QLabel("Version: 0.1"))
        link=QLabel("<a href='https://github.com/raqdrox/taskman'>https://github.com/raqdrox/taskman</a>")
        link.setOpenExternalLinks(True)
        dialog.layout().addWidget(link)
        dialog.resize(300,100)
        dialog.exec_()


    def tick(self):
        self.loadProcessData(self.showAllCheckbox.isChecked())
        



    



app= QApplication(sys.argv)
mainwindow=TaskManager()

mainwindow.show()

app.exec_()


