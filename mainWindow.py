# -*- coding: utf-8 -*-

# MTTT UI implementation
# Work in progress, inmense room for improvement ;-)
# Authors: MLemos, PEstrella
# 
import textwrap
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

from Ui_mainWindow import Ui_MainWindow
from util import doAlert
from table import MyTable


from migrated_backend_main import *
from differences_module import Differences

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

        self.modified_table_items_coordinates = []
        self.lastChangedTableItemCoordinates = (-1,-1)

        self.post_editing_data = {}
        self.differences_data = {}
        self.modified_references_indices =  []
        self.saved_modified_references = []
        self.unmodified_target = []
        self.modified_target = []
        self.last_changed_item_in_post_edition = None
        self.last_selected_search = None
        self.log = {}
        #self.statistics = None
        self.differences = None
        self.engine = None
        self.progress = None
        self.workdir = workdir
        self.chooseModel = None
        self.migrated_backend_main = MyWindow()


    @pyqtSignature("")
    def on_btnMachineTranslation_clicked(self):
        
        source = self.edit_source_machine_translation_tab.text()
        if not source:
            doAlert("Please choose a source text.")
            return
        self.results_machine_translation.setText("Running decoder, please wait\n\n")  
        text = self.migrated_backend_main._machine_translation(source, self.chooseModel).decode('utf8')
        self.results_machine_translation.setText(text)

    @pyqtSignature("")
    def on_btnChooseTM_clicked(self):
        #self.chooseModel= str(QFileDialog.getExistingDirectory(self, "Select Model"))
        self.chooseModel=str(self.directoryDialog()) 
           

    @pyqtSignature("")
    def on_btnCreateTM_clicked(self):
        self.tabWidget.setCurrentIndex(0)

    @pyqtSignature("")
    def on_btnPostEditing_clicked(self):
        source = self.edit_source_post_editing.text()
        #print source
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
       
        
        self.source_text = []
        self.unchanged_target_text = []
        self.target_text = []

        with open(target) as fp:
                for line in fp:
                    line = line.decode("utf-8")
                    if line != '\n':
                       self.unchanged_target_text.append(line)
                       self.target_text.append(line)
        if self.btn_bilingual_post_edition.isChecked():
            with open(source) as fp:
                    for line in fp:
                        line = line.decode("utf-8")
                        if line != '\n':
                           self.source_text.append(line)
        else:
            self.source_text = self.target_text

        self.post_editing_data["source"] = self.source_text
        self.post_editing_data["target"] = self.target_text
        self.table_offset_PostEdition = 0
        self.table_rows_PostEdition = 100 #delete these vars if nav butons not used <<,>>,+,-
        self.table_rows_Differences = 50
        self.table_offset_Differences = 0
        self.lastChangedSegmentIndex = -1

        self.modified_references_indices =  []
        self.modified_table_items_coordinates = []
        self.lastChangedTableItemCoordinates = (-1,-1)
        #CHECK WHICH OF THE FOLLOWING SHOULD BE CLEARED 
        #TO SHOW DIFFERENCES CORRECTLY AFTER RELOADING FILES FOR PE      
        self.saved_modified_references = []
        self.differences = None
        #self.post_editing_data = {}
        self.differences_data = {}
        self.unmodified_target = []
        self.modified_target = []
        self.last_changed_item_in_post_edition = None
        self.last_selected_search = None
        self.log = {}
        self.update_table_PostEdition()
        #THE FOLLOWING CODE CREATES A NICE SIMPLE TABLE WITH WRAPPED 
        #TEXT IN THE CELLS, COULD BE USED AS REFERENCE TO REFACTOR CODE
       #P self.table_post_editing.clear()
        #Pfor y, key in enumerate(sorted(self.post_editing_data.keys())):            
          #P  for x, item in enumerate(self.post_editing_data[key]):
            #P    
              #P  newitem = QTableWidgetItem(textwrap.fill(item, width=70))
                #Pif key != "Post-edited":
                  #P  newitem.setReadOnly(True)
              
              #P  self.table_post_editing.setItem(x, y, newitem)

        #P self.table_post_editing.setTextElideMode(QtCore.Qt.ElideNone)
        #P self.table_post_editing.resizeColumnsToContents()
        #P self.table_post_editing.resizeRowsToContents()
        #P self.table_post_editing.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)             
        self.PE_table_controls_groupBox.show()
        self.PE_search_groupBox.show()
        self.table_post_editing.show()

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

    @pyqtSignature("")
    def on_btnDiff_clicked(self):
        self.save_using_log();
        self.tabWidget.setTabEnabled(5,True)
        self.tabWidget.setCurrentIndex(5)
        self.get_modified_and_unmodified_target()
        self.differences = Differences(self.unmodified_target, self.modified_target) 
        self.differences_data["source"], self.differences_data["target"] = self.differences.get_insertion_and_deletions(self.unmodified_target, self.modified_target)
        self.table_differences.set_differences_table_data(self.differences_data)

        self.btnNextDifferences.show()
        self.btnBackDifferences.show()
        self.btnAddRowsDifferences.show()
        self.btnLessRowsDifferences.show()
        self.table_differences.show()

    def update_table_Differences(self):
        start = self.table_offset_Differences
        end = self.table_offset_Differences + + self.table_rows_Differences
        self.differences_data["source"] = self.enriched_target_text_original[start:end]
        self.differences_data["target"] = self.enriched_target_text_modified[start:end]
        self.table_differences.set_differences_table_data(self.differences_data)

    def showDiffs(self):
        self.table_offset_Differences = 0
        #self.update_table_Differences() 
        self.btnNextDifferences.show()
        self.btnBackDifferences.show()
        self.btnAddRowsDifferences.show()
        self.btnLessRowsDifferences.show()
        self.table_differences.show()

    def load_log(self):
        log = {}
        log_filepath = os.path.abspath(str(self.edit_output_post_editing.text() + "/log.json"))
        try:
            with open(log_filepath) as json_data:
                log = json.load(json_data)
        except:
            pass
        return log

    def get_latest_modifications (self):
        log = self.load_log()
        last_modifications = {}
        for a in sorted(log.keys()):
            for b in log[a]:
                last_modifications[b] = log[a][b]
        return last_modifications

    def get_modified_and_unmodified_target(self):
        self.unmodified_target = []
        self.modified_target = []
        with open(self.original_target_path) as fp:
            for line in fp:
                if line != '\n':
                    line = line.decode('utf-8')
                    self.unmodified_target.append(line)
        latest_modifications = self.get_latest_modifications()
        for index, line in enumerate(self.unmodified_target):
            if str(index) in latest_modifications:
                self.modified_target.append(latest_modifications[str(index)])
            else:
                self.modified_target.append(line)

    @pyqtSignature("")
    def on_btnSave_clicked(self):
        self.original_target_path = str(self.edit_target_post_editing.text())
        target_filename = self.original_target_path[self.original_target_path.rfind('/'):]
        unmodified_target = self.edit_target_post_editing.text()
        self.save_using_log()
        self.get_modified_and_unmodified_target()

    @pyqtSignature("")
    def on_btnNextPostEditing_clicked(self):
        self.table_offset_PostEdition += 1
        self.update_table_PostEdition()

    @pyqtSignature("")
    def on_btnBackPostEditing_clicked(self):
        self.table_offset_PostEdition -= 1
        if self.table_offset_PostEdition < 0: self.table_offset_PostEdition = 0
        self.update_table_PostEdition()

    @pyqtSignature("")
    def on_btnLessRowsPostEditing_clicked(self):
        if self.table_rows_PostEdition:
            self.table_rows_PostEdition -= 1
            self.table_post_editing.removeRow(0)
            self.update_table_PostEdition()

    @pyqtSignature("")
    def on_btnAddRowsPostEditing_clicked(self):
        if self.table_rows_PostEdition < len(self.target_text):
            self.table_rows_PostEdition += 1
            self.table_post_editing.insertRow(self.table_post_editing.rowCount())
            self.update_table_PostEdition()

    @pyqtSignature("")
    def on_btnNextDifferences_clicked(self):
        self.table_offset_Differences += 1
        self.update_table_Differences()

    @pyqtSignature("")
    def on_btnBackDifferences_clicked(self):
        self.table_offset_Differences -= 1
        if self.table_offset_Differences < 0: self.table_offset_Differences = 0
        self.update_table_Differences()

    @pyqtSignature("")
    def on_btnLessRowsDifferences_clicked(self):
        if self.table_rows_Differences:
            self.table_rows_Differences -= 1
            self.table_differences.removeRow(0)
            self.update_table_Differences()

    @pyqtSignature("")
    def on_btnAddRowsDifferences_clicked(self):
        if self.table_rows_Differences< len(self.target_text):
            self.table_rows_Differences += 1
            self.table_differences.insertRow(self.table_differences.rowCount())
            self.update_table_Differences()

    @pyqtSignature("")
    def on_btnSearchDifferences_clicked(self):
        if self.toggled_search_differences:
            self.toggled_search_differences = False
            self.search_table_differences.show()
            self.edit_search_differences.show()
        else:
            self.toggled_search_differences = True
            self.search_table_differences.hide()
            self.edit_search_differences.hide()

    @pyqtSignature("")
    def on_btnSearchPostEditing_clicked(self):
        if self.toggled_search_post_editing:
            self.toggled_search_post_editing = False
            self.search_table_post_editing.show()
            self.edit_search_post_editing.show()
        else:
            self.toggled_search_post_editing = True
            self.table_offset_PostEdition= 0
            self.update_table_PostEdition()
            self.search_table_post_editing.hide()
            self.edit_search_post_editing.hide()

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
        
        text = self.migrated_backend_main._train()
        
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
            cmd = "perl "+ os.path.abspath("evaluation_scripts") + "/WER.pl" + " -t " + hyp + " -r " + ref
            proc = subprocess.Popen([cmd],
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        shell=True)
                
            out, err = proc.communicate()
           
            output += "WER: %s (Execution errors: %s)\n" % (out, err)
            #print cmd

        if self.btn_check_PER.isChecked():
            cmd = "perl "+ os.path.abspath("evaluation_scripts") + "/PER.pl" + " -t " + hyp + " -r " + ref
            proc = subprocess.Popen([cmd],
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        shell=True)
                
            out, err = proc.communicate()
            output += "PER: %s (Execution errors: %s)\n" % (out, err)   
            #print cmd

        if self.btn_check_HTER.isChecked():
            cmd = "perl "+ os.path.abspath("evaluation_scripts") + "/tercom_v6b.pl" + " -h " + hyp + " -r " + ref + " -o sum_doc "
            proc = subprocess.Popen([cmd],
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        shell=True)
            out, err = proc.communicate()
            output += "HTER: %s (Execution errors: %s)\n" % (out, err)
            #print cmd

        if self.btn_check_BLEU.isChecked():
            cmd = "perl "+ os.path.abspath("evaluation_scripts") + "/BLEU.pl " +  ref + " < " + hyp
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
            text = self.migrated_backend_main._prepare_corpus(output, source_language,target_language,source,target,lm_text)
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

    #@pyqtSignature("")
   # def on_btn_output_dir_evaluation_tab_clicked(self):
        """
        Slot documentation goes here.
        """
       # self.edit_output_evaluation_tab.setText(str(self.directoryDialog()))
       
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
           return None #os.pathdirname(os.path.abspath(__file__))

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
        #self.edit_output_preprocessing_tab.setText(str(QFileDialog.getExistingDirectory(self, "Select Directory")))

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

    def changeQTextEditColor(self, tableItem, color):
        try:
            tableItem.setStyleSheet('background-color:'+ color.name())
        except: pass


    def on_tableItemDifferences_selected(self, event, tableItem, x, y):
        pass

    def on_tableItemPostEdition_selected(self, event, tableItem, x, y):
        try:
            if (self.last_changed_item_in_post_editionCoordinates not in self.modified_table_items_coordinates):
                self.changeQTextEditColor(self.last_changed_item_in_post_edition, QColor( 255, 255, 255,255))
            else:
                self.changeQTextEditColor(self.last_changed_item_in_post_edition, QColor( 51, 255, 153,255))
        except: pass
        self.last_changed_item_in_post_edition = tableItem
        self.last_changed_item_in_post_editionCoordinates = (x,y)
        self.changeQTextEditColor(self.last_changed_item_in_post_edition, QColor( 153, 255, 255,255))

    def on_tableItemDifferencestextChanged(self, tableItem, x, y):
        pass

    def on_tableItemPostEditing_textChanged(self, tableItem, row_index,column_index):
        row_index += self.table_offset_PostEdition
        self.last_change_timestamp = int(time.time() * 1000)
        self.modified_table_items_coordinates.append((row_index,0))
        self.modified_table_items_coordinates.append((row_index,1))
        self.modified_table_items_coordinates.append((row_index,2))
        self.PE_diff_and_stats_groupBox.show()
        self.PE_save_groupBox.show()
        self.target_text[row_index] = (str(tableItem.toPlainText().toUtf8())).decode('utf8')
        self.lastChangedSegmentIndex = row_index
        if row_index not in self.modified_references_indices:
            self.modified_references_indices.append(row_index)

    def save_using_log(self):
        for modified_reference_index in self.modified_references_indices:
            modified_segment = self.target_text[modified_reference_index]
            self.saved_modified_references.append(modified_segment)
            if self.last_change_timestamp not in self.log:
                self.log[self.last_change_timestamp] = {}
            self.log[self.last_change_timestamp][modified_reference_index] = modified_segment
        with open(self.edit_output_post_editing.text() + "/log.json", 'w+') as outfile: #CHANGED OUTPUT_DIR
            json.dump(self.log, outfile)