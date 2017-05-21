"""@brief     This is where everything happens."""
# !/usr/bin/env python
# -*- coding: utf-8 -*-

##############################################################################
#
# Machine Translation Training Tool
# Copyright (C) 2016 Roxana Lafuente <roxana.lafuente@gmail.com>
#                    Miguel Lemos <miguelemosreverte@gmail.com>
#		     Paula Estrella <pestrella@gmail.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from PyQt4.QtCore import (
    pyqtSignature,
    QObject,
    Qt,
    SIGNAL,
    QUrl,
    )

from PyQt4.QtGui import (
    QMainWindow,
    QMessageBox,
    QProgressDialog,
    QDialog,
    QFileDialog,
    QTextEdit,
    QColor,
    QHeaderView,
    QTableWidgetItem,
    QAbstractItemView,
    )
from PyQt4 import QtCore, QtGui
import sys
import time
import threading
import shutil
import codecs
import subprocess
import os
import platform
import textwrap
import difflib

from Ui_mainWindow import Ui_MainWindow
from util import doAlert
from MTTTCore import *


class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    def setupUi(self, mainWindow):
        super(MainWindow, self).setupUi(mainWindow)

    def __init__(self, parent=None, moses=None, workdir=None):
        """
        Constructor
        """
        QMainWindow.__init__(self, parent)

        css = QtCore.QFile('./gui/pyqt.css')
        css.open(QtCore.QIODevice.ReadOnly)
        if css.isOpen():
           self.setStyleSheet(QtCore.QVariant(css.readAll()).toString())
        css.close()

        self.post_editing_data = {'Source/MT':[], 'Post-edited':[]}
        self.log = {}      
        self.core = MTTTCore()
        self.modified_target = []
        self.timestamps = []

        #  self.last_selected_search = None
        self.workdir = workdir
        self.chooseModel = None
        


    @pyqtSignature("")
    def on_btnMachineTranslation_clicked(self):
        
        source = self.edit_source_machine_translation_tab.text()
        if not source:
            doAlert("Please choose a source text.")
            return
        self.results_machine_translation.setText("Running decoder, please wait\n\n")  
        text = self.core._machine_translation(source, self.chooseModel).decode('utf8')
        self.results_machine_translation.setText(text)

    @pyqtSignature("")
    def on_btnChooseTM_clicked(self):       
        self.chooseModel=str(self.directoryDialog())            

    @pyqtSignature("")
    def on_btnCreateTM_clicked(self):
        self.tabWidget.setCurrentIndex(0)

    @pyqtSignature("")
    def on_btnPostEditing_clicked(self):
        self.post_editing_data = {'Source/MT':[], 'Post-edited':[]}
        self.log = {}             
        self.modified_target = []
        self.timestamps = []

        self.table_post_editing.clear()
        self.table_post_editing.blockSignals(True)

        source = self.edit_source_post_editing.text()  
       # print source
        target = self.edit_target_post_editing.text()
        #print target
        output = self.edit_output_post_editing.text()
        if not source and self.btn_bilingual_post_edition.isChecked():
            doAlert("Please choose a source text first.")
            return
        if not target:
            doAlert("Please choose a target text first.")
            return
        if not output:
            doAlert("Please choose an output directory first.")
            return  

        with open(target) as fp:
                for line in fp:
                    line = line.decode("utf-8")
                    if line != '\n':                    
                       self.post_editing_data['Post-edited'].append(line)
                       self.timestamps.append([(0,0)])#initial time for PE timestamps
                       self.modified_target.append(None)
        if self.btn_bilingual_post_edition.isChecked():           
            with open(source) as fp:
                    for line in fp:
                        line = line.decode("utf-8")
                        if line != '\n':
                           self.post_editing_data['Source/MT'].append(line)
        else:
            self.post_editing_data['Source/MT'] = self.post_editing_data['Post-edited']
        
        self.table_post_editing.setRowCount(len(self.post_editing_data['Post-edited']))
        if len(self.post_editing_data['Source/MT']) != len(self.post_editing_data['Post-edited']):
            doAlert("Please choose an output directory first.")
            return

        for y, key in enumerate(['Source/MT','Post-edited']):            
            for x, item in enumerate(self.post_editing_data[key]):                
                newitem = QTableWidgetItem(textwrap.fill(item, width=70))
                #print x, y
                if key == 'Source/MT':     
                    newitem.setFlags(QtCore.Qt.ItemIsEditable)     
                self.table_post_editing.setItem(x, y, newitem)         
        
        self.table_post_editing.setHorizontalHeaderLabels(["Source/MT","Post-edited"])
        self.table_post_editing.setTextElideMode(QtCore.Qt.ElideNone)
        self.table_post_editing.resizeColumnsToContents()
        self.table_post_editing.resizeRowsToContents()
        self.table_post_editing.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)             
        self.table_post_editing.setMouseTracking(True)
         #use the events below to calculate time spent per segment
        self.table_post_editing.show()
        self.table_post_editing.cellChanged.connect(self.endPESeg)
        self.table_post_editing.cellEntered.connect(self.startPESeg)
        self.table_post_editing.blockSignals(False)

    def endPESeg(self, row, col):#only col 1 will be modified, update PE timestamps
        self.leaving_time=int(round(time.time() * 1000))
        #print "LEAVING", self.leaving_time
        self.table_post_editing.item(row,0).setBackground(QColor( 51, 255, 153,255))
        self.table_post_editing.item(row,1).setBackground(QColor( 51, 255, 153,255))
        self.timestamps[row].append((self.enter_time, self.leaving_time))#seconds?
        #self.timestamps[row][1] = self.leaving_time
        self.modified_target[row] = (str(self.table_post_editing.item(row,1).text().toUtf8())).decode('utf8')       
        self.PE_diff_and_stats_groupBox.show()
        self.PE_save_groupBox.show()   

    def startPESeg(self, item):#only col 1 will be modified, update PE timestamps
        self.enter_time=int(round(time.time() * 1000))
        #print "ENTER1 ", self.enter_time

    @pyqtSignature("")
    def on_btnSave_clicked(self):
        self.log = {'MT':[], 'PE':[],'Times':[]}
        for i in range(0, len(self.modified_target)) :
            if self.modified_target[i] is not None:
                self.log['MT'].append(self.post_editing_data['Post-edited'][i].rstrip())#PEd original data, before loading to table
                self.modified_target[i] = self.modified_target[i].replace('\n',' ')
                self.log['PE'].append(self.modified_target[i].rstrip())
                self.log['Times'].append([list(e) for e in set(self.timestamps[i])])

        with open(os.path.abspath(str(self.edit_output_post_editing.text())) + "/log.json", 'w+') as outfile: #CHANGED OUTPUT_DIR
            json.dump(self.log, outfile)
           

    @pyqtSignature("")
    def on_btnDiff_clicked(self):       
        self.tabWidget.setTabEnabled(5,True)
        self.tabWidget.setCurrentIndex(5)
        self.table_differences.clear()
        differences_data = {}
        differences_data["Differences"], differences_data["Stats"] = self.get_diff(self.log['MT'], self.log['PE'])
        differences_data["Stats"] = self.get_timeStats(self.log['Times'], differences_data["Stats"])

        self.table_differences.setRowCount(len(self.log['PE']))
        
        for y, key in enumerate(sorted(differences_data.keys())):            
            for x, item in enumerate(differences_data[key]):                
                tableItem = QtGui.QTextEdit()
                tableItem.setText(textwrap.fill(item, width=70))
                tableItem.setReadOnly(True)
                self.table_differences.setCellWidget(x,y, tableItem)        
        self.table_differences.setHorizontalHeaderLabels(["Differences","Stats"])
        self.table_differences.setTextElideMode(QtCore.Qt.ElideNone)
        self.table_differences.resizeColumnsToContents()
        self.table_differences.resizeRowsToContents()
        self.table_differences.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)  
        self.table_differences.show()

    def get_timeStats(self, timestamps, output):#output collects stats as strings
        for i in range(0, len(timestamps)):
            tspent = 0            
            for j in range(0, len(timestamps[i])):
                tspent += (timestamps[i][j][1] - timestamps[i][j][0])/1000
            if tspent > 60:
                tspent = tspent /60
                output[i] = output[i]+str("\nTimes edited:  %d\n, \nAprox. time spent in minutes: %d\n" % (len(timestamps[i])-1, tspent))
            else:
                output[i] = output[i]+str("\nTimes edited:  %d\n, \nAprox. time spent in seconds: %d\n" % (len(timestamps[i])-1, tspent))
           
        return output

    def get_diff(self, original_segment, modified_segment):
        """Create a tagged diff."""
       
        nl = "<NL>"
        delTag = "<span style=\"background-color:#FE2E2E; font-weight:600\">%s</span>"
        insTag = "<span style=\"background-color:#04B404; font-weight:600\">%s</span>"
        diffs = []
        stats = []
        diffText = None
        for i in range (0, len(original_segment)):
            #print "--"+original_segment[i]+"--"
            #print "--"+modified_segment[i]+"--"
            deleteCount, insertCount, replaceCount = 0, 0, 0
            diffText = ""
            statText = ""
            mt = original_segment[i].replace("\n", "\n%s" % nl).split()
            pe = modified_segment[i].replace("\n", "\n%s" % nl).split()
            s = difflib.SequenceMatcher(None, mt, pe)
            
            outputList = []
            for tag, alo, ahi, blo, bhi in s.get_opcodes():
                if tag == 'replace':
                    # Text replaced = deletion + insertion
                    outputList.append(delTag % " ".join(mt[alo:ahi]))
                    outputList.append(insTag % " ".join(pe[blo:bhi]))
                    replaceCount += 1
                elif tag == 'delete':
                    # Text deleted
                    outputList.append(delTag % " ".join(mt[alo:ahi]))
                    deleteCount += 1
                elif tag == 'insert':
                    # Text inserted
                    outputList.append(insTag % " ".join(pe[blo:bhi]))
                    insertCount += 1
                elif tag == 'equal':
                    # No change
                    outputList.append(" ".join(mt[alo:ahi]))
            diffText = " ".join(outputList)
            diffText = " ".join(diffText.split())
            diffText = diffText.replace(nl, "\n")
            
            statText = str( "Deletions: %d, Insertions: %d, Replacements: %d" % (deleteCount, insertCount, replaceCount))
            diffs.append(diffText)   
            stats.append(statText)  
       
        return (diffs, stats)

#=============================================================================   

    @pyqtSignature("QString")
    def on_edit_search_differences_textEdited(self,text):
        self.search_on_table_differences(text)

    @pyqtSignature("QString")
    def on_edit_search_post_editing_textEdited(self,text):
        self.search_on_table_post_editing(text)

    def update_table_PostEdition(self):
        start = self.table_offset_PostEdition
        end = self.table_offset_PostEdition + self.table_rows_PostEdition
        self.post_editing_data["source"] = self.source_text[start:end]
        self.post_editing_data["target"] = self.target_text[start:end]
        self.table_post_editing.set_post_editing_table_data(self.post_editing_data, self.btn_bilingual_post_edition.isChecked())
        
        for y in  self.modified_references_indices:
            y -= start
            if y >= 0 and y < self.table_rows_PostEdition:
                self.setTableRowGreen(y)  

    def setTableRowGreen(self,row_index):
        self.changeQTextEditColor(self.table_post_editing.cellWidget(row_index,0), QColor( 51, 255, 153,255))
        self.changeQTextEditColor(self.table_post_editing.cellWidget(row_index,1), QColor( 51, 255, 153,255))
        if self.btn_bilingual_post_edition.isChecked():
            self.changeQTextEditColor(self.table_post_editing.cellWidget(row_index,2), QColor( 51, 255, 153,255))

    def search_on_table_differences(self, text):
        self.search_table_differences.clear()
        self.search_table_differences.setHorizontalHeaderLabels(QtCore.QString("Results;").split(";"))
        self.search_table_differences.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)#P 
        text = str(text)
        self.search_buttons = []
        if self.differences_data["target"] and self.differences_data["source"]:
            column = 1
            for index,segment in enumerate(self.differences_data["source"]):
                row = index
                if text and (text in segment):
                    self.search_buttons.append(QTextEdit())
                    tableItem = self.search_buttons[-1]
                    tableItem.setMaximumHeight(50)
                    tableItem.setText(segment)
                    tableItem.setReadOnly(True)
                    tableItem.setMinimumHeight(50) 
                    #Following events not available as insertion/deletion function implemetation changed
                    #tableItem.mousePressEvent = (lambda event= tableItem, tableItem= tableItem,x=row, y=column: self.show_selected_segment_from_search_differences(event, tableItem,x,y))
                    self.search_table_differences.setCellWidget(len(self.search_buttons)-1,0, tableItem)
        self.search_table_differences.setTextElideMode(QtCore.Qt.ElideNone)
        self.search_table_differences.resizeRowsToContents()
        self.search_table_differences.resizeColumnsToContents()#P
        self.search_table_differences.show()

    def search_on_table_post_editing(self, text):
        self.search_table_post_editing.clear()
        self.search_table_post_editing.setHorizontalHeaderLabels(QtCore.QString("Results;").split(";"))
        self.search_table_post_editing.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)#P  
        text = str(text)
        self.search_buttons = []
        if self.target_text:
            column = 1
            for index,segment in enumerate(self.target_text):
                row = index
                if text and text in segment:
                   
                    self.search_buttons.append(QTextEdit())
                    tableItem = self.search_buttons[-1]
                    #tableItem.setFixedWidth(250)
                    tableItem.setMaximumHeight(50)
                    tableItem.setText(segment)
                    tableItem.setReadOnly(True)
                    tableItem.mousePressEvent = (lambda event= tableItem, tableItem= tableItem,x=row, y=column: self.show_selected_segment_from_search_post_editing(event, tableItem,x,y))
                    self.search_table_post_editing.setCellWidget(len(self.search_buttons)-1,0, tableItem)
        self.search_table_post_editing.setTextElideMode(QtCore.Qt.ElideNone)
        self.search_table_post_editing.resizeRowsToContents()
        self.search_table_post_editing.resizeColumnsToContents()#P
        self.search_table_post_editing.show()
       

    @pyqtSignature("")
    def show_selected_segment_from_search_differences(self, event, tableItem, x, y):
        try:
            if self.last_selected_search is not None:
                self.changeQTextEditColor(self.last_selected_search, QColor( 255, 255, 255,255))
            self.last_selected_search = tableItem
            self.changeQTextEditColor(tableItem, QColor( 153, 255, 255,255))
        except:pass
        self.table_offset_Differences = x
        self.update_table_Differences()

    @pyqtSignature("")
    def show_selected_segment_from_search_post_editing(self, event, tableItem, x, y):
        try:
            if self.last_selected_search is not None:
                self.changeQTextEditColor(self.last_selected_search, QColor( 255, 255, 255,255))
            self.last_selected_search = tableItem
            self.changeQTextEditColor(tableItem, QColor( 153, 255, 255,255))
        except:pass
        self.table_offset_PostEdition= x
        self.update_table_PostEdition()

   

    def update_table_Differences(self):
        start = self.table_offset_Differences
        end = self.table_offset_Differences + + self.table_rows_Differences
        self.differences_data["source"] = self.enriched_target_text_original[start:end]
        self.differences_data["target"] = self.enriched_target_text_modified[start:end]
        self.table_differences.set_differences_table_data(self.differences_data)  
   
    @pyqtSignature("")
    def on_btnSearchDifferences_clicked(self):
        pass
       # if self.toggled_search_differences:
        #    self.toggled_search_differences = False
         #   self.search_table_differences.show()
         #   self.edit_search_differences.show()
        #else:
         #   self.toggled_search_differences = True
          #  self.search_table_differences.hide()
           # self.edit_search_differences.hide()

    @pyqtSignature("")
    def on_btnSearchPostEditing_clicked(self):
        pass
        #if self.toggled_search_post_editing:
         #   self.toggled_search_post_editing = False
         ##   self.search_table_post_editing.show()
          #  self.edit_search_post_editing.show()
        #else:
        #    self.toggled_search_post_editing = True
        #    self.table_offset_PostEdition= 0
        #    self.update_table_PostEdition()
        #    self.search_table_post_editing.hide()
        #    self.edit_search_post_editing.hide()

    @pyqtSignature("")
    def on_btn_bilingual_post_edition_clicked(self):
        if self.btn_bilingual_post_edition.isChecked():
            self.toggled_bilingual_post_editing = False
            self.label_source_post_editing.show()
            self.edit_source_post_editing.show()
            self.btn_source_post_editing.show()
        else:
            self.toggled_bilingual_post_editing = True
            self.label_source_post_editing.hide()
            self.edit_source_post_editing.hide()
            self.btn_source_post_editing.hide()

    @pyqtSignature("")
    def on_btnTraining_clicked(self):
        """
        Slot documentation goes here.
        """
        
        text = self.core._train()
        
        if text == "ERR":
            text = "ERROR: missing corpus to train model"
            doAlert("Please provide corpus to train model")
            self.tabWidget.setCurrentIndex(0)
            return
        else:
            self.results_training.setText(text)
        

    @pyqtSignature("")
    def on_btnEvaluation_clicked(self):
        """
        Slot documentation goes here.
        """
        hyp = self.edit_hyp_evaluation_tab.text()
        ref = self.edit_ref_evaluation_tab.text()
        output = ""#self.edit_output_evaluation_tab.text()

        if not hyp:
            doAlert("Please choose MTed text.")
            return
        elif not ref:
            doAlert("Please choose reference text.")
            return
        #elif not output:
         ##   doAlert("Please choose an output directory first.")
         #   return
       
        if self.btn_check_WER.isChecked():
            pathEval = (os.path.dirname(os.path.realpath(__file__)))
            cmd = "perl "+ pathEval+ "/evaluation_scripts" + "/WER.pl" + " -t " + hyp + " -r " + ref
            proc = subprocess.Popen([cmd],
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        shell=True)
                
            out, err = proc.communicate()
           
            output += "WER: %s (Execution errors: %s)\n" % (out, err)
            #print cmd

        if self.btn_check_PER.isChecked():
            cmd = "perl "+ pathEval+ "/evaluation_scripts"+ "/PER.pl" + " -t " + hyp + " -r " + ref
            proc = subprocess.Popen([cmd],
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        shell=True)
                
            out, err = proc.communicate()
            output += "PER: %s (Execution errors: %s)\n" % (out, err)   
            #print cmd

        if self.btn_check_HTER.isChecked():
            cmd = "perl "+ pathEval+ "/evaluation_scripts"+ "/tercom_v6b.pl" + " -h " + hyp + " -r " + ref + " -o sum_doc "
            proc = subprocess.Popen([cmd],
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        shell=True)
            out, err = proc.communicate()
            output += "HTER: %s (Execution errors: %s)\n" % (out, err)
            #print cmd

        if self.btn_check_BLEU.isChecked():
            cmd = "perl "+ pathEval+ "/evaluation_scripts" + "/BLEU.pl " +  ref + " < " + hyp
            proc = subprocess.Popen([cmd],
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        shell=True)
            out, err = proc.communicate()
            output += "BLEU: %s (Execution errors: %s)\n" % (out, err) 
            #print cmd 

       
        self.results_evaluation.setText(output)


    @pyqtSignature("")
    def on_btnPreProccess_clicked(self):
        """
        Slot documentation goes here.
        """
        source = self.edit_source_preprocessing_tab.text()
        target = self.edit_target_preprocessing_tab.text()
        lm_text = self.edit_lm_text_preprocessing_tab.text()
        output = self.edit_output_preprocessing_tab.text()
        source_language = self.preprocessing_source_language
        target_language = self.preprocessing_target_language

        if not source:
            doAlert("Please choose a source text first.")
            return
        elif not target:
            doAlert("Please choose a target text first.")
            return
        elif not output:
            doAlert("Please choose an output directory first.")
            return
        elif not source_language:
            doAlert("Please choose an preprocessing_source_language directory first.")
            return
        elif not target_language:
            doAlert("Please choose an preprocessing_target_language directory first.")
            return
        else:
            text = self.core._prepare_corpus(output, source_language,target_language,source,target,lm_text)
            self.results_preprocessing.setText(text)

    @pyqtSignature("")
    def on_btn_hyp_evaluation_tab_clicked(self):
        """
        Slot documentation goes here.
        """
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.ExistingFile)
        dialog.setNameFilter("Machine translated text (*.*)")
        dialog.setViewMode(QFileDialog.Detail)
        if dialog.exec_():
            self.edit_hyp_evaluation_tab.setText(dialog.selectedFiles()[0])

    @pyqtSignature("")
    def on_btn_ref_evaluation_tab_clicked(self):
        """
        Slot documentation goes here.
        """
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.ExistingFile)
        dialog.setNameFilter("Reference file (*.*)")
        dialog.setViewMode(QFileDialog.Detail)
        if dialog.exec_():
            self.edit_ref_evaluation_tab.setText(dialog.selectedFiles()[0])

 
    @pyqtSignature("")
    def on_btn_source_machine_translation_tab_clicked(self):
        """
        Slot documentation goes here.
        """
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.ExistingFile)
        dialog.setNameFilter("Choose a text source (*.*)")
        dialog.setViewMode(QFileDialog.Detail)
        if dialog.exec_():
            self.edit_source_machine_translation_tab.setText(dialog.selectedFiles()[0])

    @pyqtSignature("")
    def on_btn_source_post_editing_clicked(self):
        """
        Slot documentation goes here.
        """
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.ExistingFile)
        dialog.setNameFilter("Choose a text source (*.*)")
        dialog.setViewMode(QFileDialog.Detail)
        if dialog.exec_():
            self.edit_source_post_editing.setText(dialog.selectedFiles()[0])

    @pyqtSignature("")
    def on_btn_target_post_editing_clicked(self):
        """
        Slot documentation goes here.
        """
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.ExistingFile)
        dialog.setNameFilter("Choose a text source (*.*)")
        dialog.setViewMode(QFileDialog.Detail)
        if dialog.exec_():
            self.edit_target_post_editing.setText(dialog.selectedFiles()[0])

    def directoryDialog(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.DirectoryOnly)
        dialog.setViewMode(QFileDialog.Detail)
        if dialog.exec_():
            return(dialog.selectedFiles()[0])
        else:
           return None 

    @pyqtSignature("")
    def on_btn_output_post_editing_clicked(self):
        """
        Slot documentation goes here.
        """        
        self.edit_output_post_editing.setText(str(self.directoryDialog()))
       

    @pyqtSignature("")
    def on_btn_lm_text_preprocessing_tab_clicked(self):
        """
        Slot documentation goes here.
        """
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.ExistingFile)
        dialog.setNameFilter("Choose a text source (*.*)")
        dialog.setViewMode(QFileDialog.Detail)
        if dialog.exec_():
            self.edit_lm_text_preprocessing_tab.setText(dialog.selectedFiles()[0])

    @pyqtSignature("")
    def on_btn_source_preprocessing_tab_clicked(self):
        """
        Slot documentation goes here.
        """
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.ExistingFile)
        dialog.setNameFilter("Choose a text source (*.*)")
        dialog.setViewMode(QFileDialog.Detail)
        if dialog.exec_():
            self.edit_source_preprocessing_tab.setText(dialog.selectedFiles()[0])

    @pyqtSignature("")
    def on_btn_target_preprocessing_tab_clicked(self):
        """
        Slot documentation goes here.
        """
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.ExistingFile)
        dialog.setNameFilter("Choose a text target (*.*)")
        dialog.setViewMode(QFileDialog.Detail)
        if dialog.exec_():
            self.edit_target_preprocessing_tab.setText(dialog.selectedFiles()[0])

    @pyqtSignature("")
    def on_btn_output_dir_preprocessing_tab_clicked(self):
        """
        Slot documentation goes here.
        """
        self.edit_output_preprocessing_tab.setText(str(self.directoryDialog()))
        

    @pyqtSignature("")
    def on_btnTranslate_clicked(self):
        """
        Slot documentation goes here.
        """
        if self.engine is None:
            doAlert("Please load MT model first.")
            return
        self.btnTranslate.setEnabled(False)
        self.editTrg.setText("")
        try:
            texts = str(self.editSrc.toPlainText().toUtf8()).split('\n')
            trans = []
            for text in texts:
                if text.strip() == "":
                    trans.append(text)
                else:
                    trans.append(
                        self.engine.translate(
                            text.replace('\r', ' ').strip()).decode('utf8'))
            self.editTrg.setText('\n'.join(trans))
        except Exception, e:
            print >> sys.stderr, str(e)
            doAlert("Translation failed!")
        
        self.btnTranslate.setEnabled(True)
        self.btnTranslate.setFocus()
