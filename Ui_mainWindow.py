"""@brief    GUI for MTTT."""
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
from PyQt4 import QtCore, QtGui
from constants import languages
import sys
from PyQt4.QtCore import QSize, Qt
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *

_fromUtf8 = getattr(QtCore.QString, 'fromUtf8', lambda s: s)


def _translate(context, text, disambig):
    return QtGui.QApplication.translate(
        context, text, disambig,
        getattr(
            QtGui.QApplication, 'UnicodeUTF8',
            QtCore.QCoreApplication.Encoding))

class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
       
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(705, 491)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon(":/icon/mttt.png")
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icon/mttt.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setLayoutDirection(QtCore.Qt.LeftToRight)
        MainWindow.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedKingdom))
        self.centralWidget = QtGui.QWidget(MainWindow)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralWidget.sizePolicy().hasHeightForWidth())
        self.centralWidget.setSizePolicy(sizePolicy)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        verticalLayout = QtGui.QVBoxLayout(self.centralWidget)
        verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tabWidget = QtGui.QTabWidget(self.centralWidget)
        self.tabWidget.setAutoFillBackground(True)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))

        self.background_color_palette = QtGui.QPalette()
        self.background_color_palette.setColor(QtGui.QPalette.Background,QColor("#edf2f6"))

        self.initialize_preprocessing_tab()
        self.initialize_tab_machine_translation()
        self.initialize_training_tab()
        self.initialize_tab_evaluation()
        self.initialize_post_editing_tab()
        self.initialize_tab_differences()


        self.tabWidget.addTab(self.tab_corpus_preparation, _fromUtf8(""))
        self.tabWidget.addTab(self.tab_training, _fromUtf8(""))
        self.tabWidget.addTab(self.tab_machine_translation, _fromUtf8(""))
        self.tabWidget.addTab(self.tab_evaluation, _fromUtf8(""))
        self.tabWidget.addTab(self.tab_post_editing, _fromUtf8(""))
        self.tabWidget.addTab(self.tab_differences, _fromUtf8(""))

        verticalLayout.addWidget(self.tabWidget)
        self.labelInfo = QtGui.QLabel(self.centralWidget)
        self.labelInfo.setTextFormat(QtCore.Qt.AutoText)
        self.labelInfo.setAlignment(
            QtCore.Qt.AlignRight |
            QtCore.Qt.AlignTrailing |
            QtCore.Qt.AlignVCenter)
        self.labelInfo.setObjectName(_fromUtf8("labelInfo"))
        verticalLayout.addWidget(self.labelInfo)
        MainWindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def choose_language(self, tab, source_or_target, language):
       # print language
        if tab == "preprocessing":
            if source_or_target == "source":
                self.preprocessing_source_language = language
            elif source_or_target == "target":
                self.preprocessing_target_language = language

    def initialize_tab_differences(self):
        self.tab_differences = QtGui.QWidget()
        self.tab_differences.setAutoFillBackground(True)
        self.tab_differences.setPalette(self.background_color_palette)
        self.tab_differences.setObjectName(_fromUtf8("tab_differences"))


        groupBox= QtGui.QGroupBox(self.tab_differences)
        groupBox.setObjectName(_fromUtf8("groupBox"))
        gridLayout = QtGui.QGridLayout(groupBox)
        gridLayout.setObjectName(_fromUtf8("gridLayout"))
        groupBox.setMaximumSize((QtCore.QSize(600, 60)))

       
        verticalLayout_2 = QtGui.QVBoxLayout(self.tab_differences)
        verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        verticalLayout_2.addWidget(groupBox)
       
        splitter = QtGui.QSplitter(self.tab_differences)
        splitter.setOrientation(QtCore.Qt.Horizontal)
        splitter.setObjectName(_fromUtf8("splitter"))

        self.table_differences = QtGui.QTableWidget()  
        self.table_differences.setColumnCount(2)        
        splitter.addWidget(self.table_differences)
        self.table_differences.hide()
        verticalLayout_2.addWidget(splitter)

        self.search_table_differences = QtGui.QTableWidget()  
        self.search_table_differences.setColumnCount(1)  
        self.search_table_differences.setHorizontalHeaderLabels(QtCore.QString("Results;").split(";"))
        self.search_table_differences.hide()
        splitter.addWidget(self.search_table_differences)

        self.btnSearchDifferences = QtGui.QPushButton(groupBox)
        self.btnSearchDifferences.setEnabled(True)
        self.btnSearchDifferences.setFlat(False)
        self.btnSearchDifferences.setObjectName(_fromUtf8("btnSearchDifferences"))
        self.btnSearchDifferences.setMaximumSize((QtCore.QSize(100, 30)))
        self.btnSearchDifferences.setText(_translate("Dialog", "Search", None))
        gridLayout.addWidget(self.btnSearchDifferences, 1, 3, 1, 1, Qt.AlignLeft)

        #edit_target_differences
        self.edit_search_differences = QtGui.QLineEdit(groupBox)
        self.edit_search_differences.setReadOnly(False)
        self.edit_search_differences.setObjectName(_fromUtf8("edit_search_differences"))
        gridLayout.addWidget(self.edit_search_differences, 1, 4, 1, 1)

        self.toggled_search_differences = True
        self.search_table_differences.hide()
        self.edit_search_differences.hide()

    def initialize_tab_evaluation(self):
        self.tab_evaluation = QtGui.QWidget()
        self.tab_evaluation.setAutoFillBackground(True)
        self.tab_evaluation.setPalette(self.background_color_palette)
        self.tab_evaluation.setObjectName(_fromUtf8("tab_evaluation"))
        verticalLayout_2 = QtGui.QVBoxLayout(self.tab_evaluation)
        verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        groupBox_evaluation = QtGui.QGroupBox(self.tab_evaluation)
        groupBox_evaluation.setObjectName(_fromUtf8("groupBox_evaluation"))
        groupBox_evaluation.setTitle(_translate("MainWindow", "Evaluation", None))
        gridLayout = QtGui.QGridLayout(groupBox_evaluation)
        gridLayout.setObjectName(_fromUtf8("gridLayout"))

        #label_source_evaluation_tab
        self.label_hyp_evaluation_tab = QtGui.QLabel(groupBox_evaluation)
        self.label_hyp_evaluation_tab.setObjectName(_fromUtf8("label_hyp_evaluation_tab"))
        gridLayout.addWidget(self.label_hyp_evaluation_tab, 1, 1, 1, 1)
        #btn_source_evaluation_tab
        self.btn_hyp_evaluation_tab = QtGui.QPushButton(groupBox_evaluation)
        self.btn_hyp_evaluation_tab.setObjectName(_fromUtf8("btn_hyp_evaluation_tab"))
        gridLayout.addWidget(self.btn_hyp_evaluation_tab, 1, 3, 1, 1)
        #edit_source_evaluation_tab
        self.edit_hyp_evaluation_tab = QtGui.QLineEdit(groupBox_evaluation)
        self.edit_hyp_evaluation_tab.setReadOnly(True)
        self.edit_hyp_evaluation_tab.setObjectName(_fromUtf8("edit_hyp_evaluation_tab"))
        gridLayout.addWidget(self.edit_hyp_evaluation_tab, 1, 2, 1, 1)

        #label_target_evaluation_tab
        self.label_ref_evaluation_tab = QtGui.QLabel(groupBox_evaluation)
        self.label_ref_evaluation_tab.setObjectName(_fromUtf8("label_ref_evaluation_tab"))
        gridLayout.addWidget(self.label_ref_evaluation_tab, 2, 1, 1, 1)
        #btn_target_evaluation_tab
        self.btn_ref_evaluation_tab = QtGui.QPushButton(groupBox_evaluation)
        self.btn_ref_evaluation_tab.setObjectName(_fromUtf8("btn_ref_evaluation_tab"))
        gridLayout.addWidget(self.btn_ref_evaluation_tab, 2, 3, 1, 1)
        #edit_target_evaluation_tab
        self.edit_ref_evaluation_tab = QtGui.QLineEdit(groupBox_evaluation)
        self.edit_ref_evaluation_tab.setReadOnly(False)
        self.edit_ref_evaluation_tab.setObjectName(_fromUtf8("edit_ref_evaluation_tab"))
        gridLayout.addWidget(self.edit_ref_evaluation_tab, 2, 2, 1, 1)

        verticalLayout_2.addWidget(groupBox_evaluation)
        splitter = QtGui.QSplitter(self.tab_evaluation)
        splitter.setOrientation(QtCore.Qt.Horizontal)
        splitter.setObjectName(_fromUtf8("splitter"))
        self.results_evaluation = QtGui.QTextEdit(splitter)
        self.results_evaluation.setObjectName(_fromUtf8("results_evaluation"))
        verticalLayout_2.addWidget(splitter)
        verticalLayout_2.setStretch(0, 2)
        verticalLayout_2.setStretch(1, 8)
        self.tab_evaluation.setAutoFillBackground(True)
        self.tab_evaluation.setObjectName(_fromUtf8("tab_evaluation"))

        #btnEvaluation
        self.btnEvaluation = QtGui.QPushButton(groupBox_evaluation)
        self.btnEvaluation.setEnabled(True)
        self.btnEvaluation.setMinimumSize(QtCore.QSize(120, 30))
        self.btnEvaluation.setFlat(False)
        self.btnEvaluation.setObjectName(_fromUtf8("btnEvaluation"))
        gridLayout.addWidget(self.btnEvaluation, 4, 1, 1, 8)

        self.btn_check_WER = QtGui.QCheckBox(groupBox_evaluation)
        self.btn_check_WER.setEnabled(True)
        self.btn_check_WER.setText("WER")
        self.btn_check_WER.setObjectName(_fromUtf8("btn_check_WER"))
        gridLayout.addWidget(self.btn_check_WER, 1, 5, 1, 1)

        self.btn_check_PER = QtGui.QCheckBox(groupBox_evaluation)
        self.btn_check_PER.setEnabled(True)
        self.btn_check_PER.setText("PER")
        self.btn_check_PER.setObjectName(_fromUtf8("btn_check_PER"))
        gridLayout.addWidget(self.btn_check_PER, 1, 6, 1, 1)

        self.btn_check_HTER = QtGui.QCheckBox(groupBox_evaluation)
        self.btn_check_HTER.setEnabled(True)
        self.btn_check_HTER.setText("HTER")
        self.btn_check_HTER.setObjectName(_fromUtf8("btn_check_HTER"))
        gridLayout.addWidget(self.btn_check_HTER, 1, 7, 1, 1)


        self.btn_check_BLEU = QtGui.QCheckBox(groupBox_evaluation)
        self.btn_check_BLEU.setEnabled(True)
        self.btn_check_BLEU.setText("BLEU")
        self.btn_check_BLEU.setMinimumSize(QtCore.QSize(5, 5))
        self.btn_check_BLEU.setObjectName(_fromUtf8("btn_check_BLEU"))
        gridLayout.addWidget(self.btn_check_BLEU, 2, 5, 1, 1)

        self.label_hyp_evaluation_tab.setText(_translate("MainWindow", "MT (Hyp)", None))
        self.btn_hyp_evaluation_tab.setText(_translate("Dialog", "...", None))
        self.label_ref_evaluation_tab.setText(_translate("MainWindow", "Reference", None))
        self.btn_ref_evaluation_tab.setText(_translate("Dialog", "...", None))
        self.btnEvaluation.setText(_translate("MainWindow", "Start Evaluation", None))
        groupBox_evaluation.setTitle(_translate("MainWindow", "Evaluation", None))        


    def initialize_tab_machine_translation(self):
        self.tab_machine_translation = QtGui.QWidget()
        self.tab_machine_translation.setAutoFillBackground(True)
        self.tab_machine_translation.setPalette(self.background_color_palette)
        self.tab_machine_translation.setObjectName(_fromUtf8("tab_machine_translation"))
        verticalLayout_2 = QtGui.QVBoxLayout(self.tab_machine_translation)
        verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        groupBox= QtGui.QGroupBox(self.tab_machine_translation)
        groupBox.setMaximumSize(QtCore.QSize(800, 80))
        groupBox.setObjectName(_fromUtf8("groupBox"))
        gridLayout = QtGui.QGridLayout(groupBox)
        gridLayout.setObjectName(_fromUtf8("gridLayout"))

        #label_source_machine_translation_tab
        self.label_source_machine_translation_tab = QtGui.QLabel(groupBox)
        self.label_source_machine_translation_tab.setObjectName(_fromUtf8("label_source_machine_translation_tab"))
        gridLayout.addWidget(self.label_source_machine_translation_tab, 1, 1, 1, 1)
        #btn_source_machine_translation_tab
        self.btn_source_machine_translation_tab = QtGui.QPushButton(groupBox)
        self.btn_source_machine_translation_tab.setObjectName(_fromUtf8("btn_source_machine_translation_tab"))
        gridLayout.addWidget(self.btn_source_machine_translation_tab, 1, 3, 1, 1)
        #edit_source_machine_translation_tab
        self.edit_source_machine_translation_tab = QtGui.QLineEdit(groupBox)
        self.edit_source_machine_translation_tab.setReadOnly(True)
        self.edit_source_machine_translation_tab.setObjectName(_fromUtf8("edit_source_machine_translation_tab"))
        gridLayout.addWidget(self.edit_source_machine_translation_tab, 1, 2, 1, 1)

        verticalLayout_2.addWidget(groupBox)
        splitter = QtGui.QSplitter(self.tab_machine_translation)
        splitter.setOrientation(QtCore.Qt.Horizontal)
        splitter.setObjectName(_fromUtf8("splitter"))
        self.results_machine_translation = QtGui.QTextEdit(splitter)
        self.results_machine_translation.setObjectName(_fromUtf8("results_machine_translation"))
        verticalLayout_2.addWidget(splitter)
        verticalLayout_2.setStretch(0, 2)
        verticalLayout_2.setStretch(1, 8)
        self.tab_machine_translation.setAutoFillBackground(True)
        self.tab_machine_translation.setObjectName(_fromUtf8("tab_machine_translation"))

        #btnMachineTranslation
        self.btnMachineTranslation = QtGui.QPushButton(groupBox)
        self.btnMachineTranslation.setEnabled(True)
        self.btnMachineTranslation.setMinimumSize(QtCore.QSize(120, 30))
        self.btnMachineTranslation.setFlat(False)
        self.btnMachineTranslation.setObjectName(_fromUtf8("btnMachineTranslation"))
        gridLayout.addWidget(self.btnMachineTranslation, 2, 1, 1, 3)


        #btnChooseTM ---> pre-trained translation model
        self.btnChooseTM = QtGui.QPushButton(groupBox)
        self.btnChooseTM.setEnabled(True)
        self.btnChooseTM.setMinimumSize(QtCore.QSize(120, 60))
        self.btnChooseTM.setFlat(False)
        self.btnChooseTM.setObjectName(_fromUtf8("btnChooseTM"))
        self.btnChooseTM.setText(_translate("MainWindow", "Choose a Model", None))
        gridLayout.addWidget(self.btnChooseTM, 1, 4, 2, 1)
        #btnCreateTM
        self.btnCreateTM = QtGui.QPushButton(groupBox)
        self.btnCreateTM.setEnabled(True)
        self.btnCreateTM.setMinimumSize(QtCore.QSize(120, 60))
        self.btnCreateTM.setFlat(False)
        self.btnCreateTM.setObjectName(_fromUtf8("btnCreateTM"))
        self.btnCreateTM.setText(_translate("MainWindow", "Create a Model", None))
        gridLayout.addWidget(self.btnCreateTM, 1, 5, 2, 1)

        self.label_source_machine_translation_tab.setText(_translate("MainWindow", "Source text", None))
        self.btn_source_machine_translation_tab.setText(_translate("Dialog", "...", None))
        self.btnMachineTranslation.setText(_translate("MainWindow", "Start Machine Translation", None))

    def initialize_post_editing_tab(self):
        self.tab_post_editing = QtGui.QWidget()
        self.tab_post_editing.setAutoFillBackground(True)
        self.tab_post_editing.setPalette(self.background_color_palette)
        self.tab_post_editing.setObjectName(_fromUtf8("tab_post_editing"))
        verticalLayout_2 = QtGui.QVBoxLayout(self.tab_post_editing)
        verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))


        groupBox = QtGui.QGroupBox(self.tab_post_editing)
        groupBox.setMaximumSize((QtCore.QSize(1000, 250)))
        groupBox.setObjectName(_fromUtf8("groupBox"))
        groupBox.setStyleSheet("""#groupBox
        {
        border: none;
        background-color: none;
        }""")
        gridLayout = QtGui.QGridLayout(groupBox)
        gridLayout.setObjectName(_fromUtf8("gridLayout"))

        post_editing_files_settings_groupBox = QtGui.QGroupBox(groupBox)
        post_editing_files_settings_groupBox.setObjectName(_fromUtf8("post_editing_files_settings_groupBox"))
        post_editing_files_settings_groupBox.setMaximumSize((QtCore.QSize(1000, 250)))
        PE_files_gridLayout = QtGui.QGridLayout(post_editing_files_settings_groupBox)
        PE_files_gridLayout.setObjectName(_fromUtf8("PE_files_gridLayout"))
        gridLayout.addWidget(post_editing_files_settings_groupBox, 1, 0, 2, 1)
        #label_target_post_editing
        self.label_target_post_editing = QtGui.QLabel(groupBox)
        self.label_target_post_editing.setObjectName(_fromUtf8("label_target_post_editing"))
        PE_files_gridLayout.addWidget(self.label_target_post_editing, 1, 1, 1, 1)
        #btn_target_post_editing
        self.btn_target_post_editing = QtGui.QPushButton(groupBox)
        self.btn_target_post_editing.setObjectName(_fromUtf8("btn_target_post_editing"))
        PE_files_gridLayout.addWidget(self.btn_target_post_editing, 1, 3, 1, 1)
        #edit_target_post_editing
        self.edit_target_post_editing = QtGui.QLineEdit(groupBox)
        self.edit_target_post_editing.setReadOnly(True)
        self.edit_target_post_editing.setObjectName(_fromUtf8("edit_target_post_editing"))
        PE_files_gridLayout.addWidget(self.edit_target_post_editing, 1, 2, 1, 1)

        #label_source_post_editing
        self.label_source_post_editing = QtGui.QLabel(groupBox)
        self.label_source_post_editing.setObjectName(_fromUtf8("label_source_post_editing"))
        PE_files_gridLayout.addWidget(self.label_source_post_editing, 2, 1, 1, 1)
        self.label_source_post_editing.hide()
        #btn_source_post_editing
        self.btn_source_post_editing = QtGui.QPushButton(groupBox)
        self.btn_source_post_editing.setObjectName(_fromUtf8("btn_source_post_editing"))
        PE_files_gridLayout.addWidget(self.btn_source_post_editing, 2, 3, 1, 1)
        self.btn_source_post_editing.hide()
        #edit_source_post_editing
        self.edit_source_post_editing = QtGui.QLineEdit(groupBox)
        self.edit_source_post_editing.setReadOnly(True)
        self.edit_source_post_editing.setObjectName(_fromUtf8("edit_source_post_editing"))
        PE_files_gridLayout.addWidget(self.edit_source_post_editing, 2, 2, 1, 1)
        self.edit_source_post_editing.hide()

        #label_output_post_editing
        self.label_output_post_editing = QtGui.QLabel(groupBox)
        self.label_output_post_editing.setObjectName(_fromUtf8("label_output_post_editing"))
        PE_files_gridLayout.addWidget(self.label_output_post_editing, 3, 1, 1, 1)
        #btn_output_post_editing
        self.btn_output_post_editing = QtGui.QPushButton(groupBox)
        self.btn_output_post_editing.setObjectName(_fromUtf8("btn_output_post_editing"))
        PE_files_gridLayout.addWidget(self.btn_output_post_editing, 3, 3, 1, 1)
        #edit_output_post_editing
        self.edit_output_post_editing = QtGui.QLineEdit(groupBox)
        self.edit_output_post_editing.setReadOnly(True)
        self.edit_output_post_editing.setObjectName(_fromUtf8("edit_output_post_editing"))
        PE_files_gridLayout.addWidget(self.edit_output_post_editing, 3, 2, 1, 1)

        self.btnPostEditing = QtGui.QPushButton(groupBox)
        self.btnPostEditing.setEnabled(True)
        self.btnPostEditing.setMinimumSize(QtCore.QSize(120, 30))
        self.btnPostEditing.setFlat(False)
        self.btnPostEditing.setText(_translate("Dialog", "Start Post-Editing", None))
        self.btnPostEditing.setObjectName(_fromUtf8("btnPostEditing"))
        PE_files_gridLayout.addWidget(self.btnPostEditing, 5, 1, 1, 2)

        self.btn_bilingual_post_edition= QtGui.QCheckBox(groupBox)
        self.btn_bilingual_post_edition.setEnabled(True)
        self.btn_bilingual_post_edition.setText("Bilingual post-editing")
        self.btn_bilingual_post_edition.setObjectName(_fromUtf8("btn_bilingual_post_edition"))
        PE_files_gridLayout.addWidget(self.btn_bilingual_post_edition, 4, 3, 1, 1)
        
        self.PE_diff_and_stats_groupBox = QtGui.QGroupBox(groupBox)
        self.PE_diff_and_stats_groupBox.setObjectName(_fromUtf8("PE_diff_and_stats_groupBox"))
        self.PE_diff_and_stats_groupBox.setMaximumSize((QtCore.QSize(300, 200)))
        self.PE_diff_and_stats_groupBox.hide()
        gridLayout4 = QtGui.QGridLayout(self.PE_diff_and_stats_groupBox)
        gridLayout4.setObjectName(_fromUtf8("gridLayout4"))
        gridLayout.addWidget(self.PE_diff_and_stats_groupBox, 1, 2, 1, 1)

        self.btnDiff = QtGui.QPushButton(groupBox)
        self.btnDiff.setEnabled(True)
        self.btnDiff.setMaximumSize(QtCore.QSize(120, 30))
        self.btnDiff.setFlat(False)
        self.btnDiff.setText(_translate("Dialog", "See changes", None))
        self.btnDiff.setObjectName(_fromUtf8("btnDiff"))
        gridLayout4.addWidget(self.btnDiff, 1, 4, 1, 1)

        self.PE_save_groupBox = QtGui.QGroupBox(groupBox)
        self.PE_save_groupBox.setObjectName(_fromUtf8("PE_save_groupBox"))
        self.PE_save_groupBox.setMinimumSize((QtCore.QSize(120, 80)))
        self.PE_save_groupBox.hide()
        gridLayout5 = QtGui.QGridLayout(self.PE_save_groupBox)
        gridLayout5.setObjectName(_fromUtf8("gridLayout5"))
        gridLayout.addWidget(self.PE_save_groupBox, 1, 1, 1, 1)

        self.btnSave = QtGui.QPushButton(groupBox)
        self.btnSave.setEnabled(True)
        self.btnSave.setMaximumSize(QtCore.QSize(120, 30))
        self.btnSave.setFlat(False)
        self.btnSave.setText(_translate("Dialog", "Save", None))
        self.btnSave.setObjectName(_fromUtf8("btnSave"))
        gridLayout5.addWidget(self.btnSave, 1,1, 1, 1)
       

        self.PE_search_groupBox = QtGui.QGroupBox(groupBox)
        self.PE_search_groupBox.setObjectName(_fromUtf8("self.PE_search_groupBox"))
        self.PE_search_groupBox.hide()
        gridLayout6 = QtGui.QGridLayout(self.PE_search_groupBox)
        gridLayout6.setObjectName(_fromUtf8("gridLayout6"))
        gridLayout.addWidget(self.PE_search_groupBox, 3, 1, 2, 2)

        #edit_target_post_editing
        self.edit_search_post_editing = QtGui.QLineEdit(groupBox)
        self.edit_search_post_editing.setReadOnly(False)
        self.edit_search_post_editing.setObjectName(_fromUtf8("edit_search_post_editing"))
        gridLayout6.addWidget(self.edit_search_post_editing, 5, 6, 1, 2)

        self.btnSearchPostEditing = QtGui.QPushButton(groupBox)
        self.btnSearchPostEditing.setEnabled(True)
        self.btnSearchPostEditing.setFlat(False)
        self.btnSearchPostEditing.setObjectName(_fromUtf8("btnSearchPostEditing"))
        self.btnSearchPostEditing.setText(_translate("Dialog", "Search", None))
        gridLayout6.addWidget(self.btnSearchPostEditing, 5, 5, 2, 1)
        self.toggled_search_post_editing = True
        self.edit_search_post_editing.hide()

        verticalLayout_2.addWidget(groupBox)
        splitter = QtGui.QSplitter(self.tab_post_editing)
        splitter.setOrientation(QtCore.Qt.Horizontal)
        splitter.setObjectName(_fromUtf8("splitter"))

        self.table_post_editing = QtGui.QTableWidget()
        self.table_post_editing.setEditTriggers(QAbstractItemView.CurrentChanged)       
        self.table_post_editing.setColumnCount(2)        
        self.table_post_editing.hide()
        splitter.addWidget(self.table_post_editing)
        verticalLayout_2.addWidget(splitter)

        self.search_table_post_editing = QtGui.QTableWidget()     
        self.search_table_post_editing.setColumnCount(1)
        self.search_table_post_editing.setHorizontalHeaderLabels(QtCore.QString("Results;").split(";"))
        self.search_table_post_editing.hide()
        splitter.addWidget(self.search_table_post_editing)

        self.tab_post_editing.setAutoFillBackground(True)
        self.tab_post_editing.setObjectName(_fromUtf8("tab_post_editing"))

        self.label_source_post_editing.setText(_translate("MainWindow", "Source text", None))
        self.btn_source_post_editing.setText(_translate("Dialog", "...", None))
        self.label_target_post_editing.setText(_translate("MainWindow", "MT", None))
        self.btn_target_post_editing.setText(_translate("Dialog", "...", None))
        self.label_output_post_editing.setText(_translate("MainWindow", "Output Directory", None))
        self.btn_output_post_editing.setText(_translate("Dialog", "...", None))



    def initialize_preprocessing_tab(self):
        self.tab_corpus_preparation = QtGui.QWidget()
        self.tab_corpus_preparation.setAutoFillBackground(True)
        self.tab_corpus_preparation.setPalette(self.background_color_palette)
        self.tab_corpus_preparation.setObjectName(_fromUtf8("tab_corpus_preparation"))
        verticalLayout_2 = QtGui.QVBoxLayout(self.tab_corpus_preparation)
        verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))


        groupBox = QtGui.QGroupBox(self.tab_corpus_preparation)
        groupBox.setObjectName(_fromUtf8("groupBox"))
        groupBox.setStyleSheet("""#groupBox
        {
        border: none;
        background-color: none;
        }""")
        gridLayout = QtGui.QGridLayout(groupBox)
        gridLayout.setObjectName(_fromUtf8("gridLayout"))


        languages_groupBox = QtGui.QGroupBox(groupBox)
        languages_groupBox.setObjectName(_fromUtf8("languages_groupBox"))
        languages_groupBox.setTitle(_translate("MainWindow", "Languages", None))
        languages_gridLayout = QtGui.QGridLayout(languages_groupBox)
        languages_gridLayout.setObjectName(_fromUtf8("languages_gridLayout"))
        gridLayout.addWidget(languages_groupBox, 1, 0, 1, 1)


        groupBox3 = QtGui.QGroupBox(groupBox)
        groupBox3.setObjectName(_fromUtf8("groupBox3"))
        groupBox3.setTitle(_translate("MainWindow", "Translation Model", None))
        gridLayout3 = QtGui.QGridLayout(groupBox3)
        gridLayout3.setObjectName(_fromUtf8("gridLayout3"))
        gridLayout.addWidget(groupBox3, 1, 1, 1, 1)

        groupBox4 = QtGui.QGroupBox(groupBox)
        groupBox4.setObjectName(_fromUtf8("groupBox4"))
        groupBox4.setTitle(_translate("MainWindow", "Language Model", None))
        gridLayout4 = QtGui.QGridLayout(groupBox4)
        gridLayout4.setObjectName(_fromUtf8("gridLayout4"))
        gridLayout.addWidget(groupBox4, 2, 1, 1, 1)

        groupBox5 = QtGui.QGroupBox(groupBox)
        groupBox5.setObjectName(_fromUtf8("groupBox5"))
        groupBox5.setTitle(_translate("MainWindow", "Settings", None))
        gridLayout5 = QtGui.QGridLayout(groupBox5)
        gridLayout5.setObjectName(_fromUtf8("gridLayout5"))
        gridLayout.addWidget(groupBox5, 3, 1, 1, 1)

        groupBox6 = QtGui.QGroupBox(groupBox)
        groupBox6.setObjectName(_fromUtf8("groupBox6"))
        groupBox6.setTitle(_translate("MainWindow", "Results", None))
        gridLayout6 = QtGui.QGridLayout(groupBox6)
        gridLayout6.setObjectName(_fromUtf8("gridLayout6"))
        gridLayout.addWidget(groupBox6, 2, 0, 4, 1)


        #btn_choose_source_lang_preprocessing
        self.comboSrc = QtGui.QComboBox(self)
        for x in languages:
            self.comboSrc.addItem(x)
        self.comboSrc.activated[str].connect(self.onActivatedSrc)
        self.srcLabel = QLabel("Source")
        languages_gridLayout.addWidget(self.comboSrc, 1, 1, 1, 1)
        languages_gridLayout.addWidget(self.srcLabel, 1, 0, 1, 1)

        #btn_choose_source_lang_preprocessing
        self.tgtLabel = QLabel("Target")
        self.comboTgt = QtGui.QComboBox(self)
        for x in languages:
            self.comboTgt.addItem(x)
        self.comboTgt.activated[str].connect(self.onActivatedTgt)
        languages_gridLayout.addWidget(self.comboTgt, 2, 1, 1, 1)
        languages_gridLayout.addWidget(self.tgtLabel, 2, 0, 1, 1)


        #label_source_preprocessing_tab
        self.label_source_preprocessing_tab = QtGui.QLabel(groupBox)
        self.label_source_preprocessing_tab.setObjectName(_fromUtf8("label_source_preprocessing_tab"))
        gridLayout3.addWidget(self.label_source_preprocessing_tab, 1, 1, 1, 1)
        #btn_source_preprocessing_tab
        self.btn_source_preprocessing_tab = QtGui.QPushButton(groupBox)
        self.btn_source_preprocessing_tab.setObjectName(_fromUtf8("btn_source_preprocessing_tab"))
        gridLayout3.addWidget(self.btn_source_preprocessing_tab, 1, 3, 1, 1)
        #edit_source_preprocessing_tab
        self.edit_source_preprocessing_tab = QtGui.QLineEdit(groupBox)
        self.edit_source_preprocessing_tab.setReadOnly(True)
        self.edit_source_preprocessing_tab.setObjectName(_fromUtf8("edit_source_preprocessing_tab"))
        gridLayout3.addWidget(self.edit_source_preprocessing_tab, 1, 2, 1, 1)

        #label_target_preprocessing_tab
        self.label_target_preprocessing_tab = QtGui.QLabel(groupBox)
        self.label_target_preprocessing_tab.setObjectName(_fromUtf8("label_target_preprocessing_tab"))
        gridLayout3.addWidget(self.label_target_preprocessing_tab, 2, 1, 1, 1)
        #btn_target_preprocessing_tab
        self.btn_target_preprocessing_tab = QtGui.QPushButton(groupBox)
        self.btn_target_preprocessing_tab.setObjectName(_fromUtf8("btn_target_preprocessing_tab"))
        gridLayout3.addWidget(self.btn_target_preprocessing_tab, 2, 3, 1, 1)
        #edit_target_preprocessing_tab
        self.edit_target_preprocessing_tab = QtGui.QLineEdit(groupBox)
        self.edit_target_preprocessing_tab.setReadOnly(True)
        self.edit_target_preprocessing_tab.setObjectName(_fromUtf8("edit_target_preprocessing_tab"))
        gridLayout3.addWidget(self.edit_target_preprocessing_tab, 2, 2, 1, 1)

        #label_lm_text_preprocessing_tab
        self.label_lm_text_preprocessing_tab = QtGui.QLabel(groupBox)
        self.label_lm_text_preprocessing_tab.setObjectName(_fromUtf8("label_lm_text_preprocessing_tab"))
        gridLayout4.addWidget(self.label_lm_text_preprocessing_tab, 3, 1, 1, 1)
        #btn_lm_text_preprocessing_tab
        self.btn_lm_text_preprocessing_tab = QtGui.QPushButton(groupBox)
        self.btn_lm_text_preprocessing_tab.setObjectName(_fromUtf8("btn_lm_text_preprocessing_tab"))
        gridLayout4.addWidget(self.btn_lm_text_preprocessing_tab, 3, 3, 1, 1)
        #edit_lm_text_preprocessing_tab
        self.edit_lm_text_preprocessing_tab = QtGui.QLineEdit(groupBox)
        self.edit_lm_text_preprocessing_tab.setReadOnly(True)
        self.edit_lm_text_preprocessing_tab.setObjectName(_fromUtf8("edit_lm_text_preprocessing_tab"))
        gridLayout4.addWidget(self.edit_lm_text_preprocessing_tab, 3, 2, 1, 1)

        #label_output_dir_preprocessing_tab
        self.label_output_dir_preprocessing_tab = QtGui.QLabel(groupBox)
        self.label_output_dir_preprocessing_tab.setObjectName(_fromUtf8("label_output_dir_preprocessing_tab"))
        gridLayout5.addWidget(self.label_output_dir_preprocessing_tab, 4, 1, 1, 1)
        #btn_output_dir_preprocessing_tab
        self.btn_output_dir_preprocessing_tab = QtGui.QPushButton(groupBox)
        self.btn_output_dir_preprocessing_tab.setObjectName(_fromUtf8("btn_output_dir_preprocessing_tab"))
        gridLayout5.addWidget(self.btn_output_dir_preprocessing_tab, 4, 3, 1, 1)
        #edit_output_preprocessing_tab
        self.edit_output_preprocessing_tab = QtGui.QLineEdit(groupBox)
        self.edit_output_preprocessing_tab.setReadOnly(True)
        self.edit_output_preprocessing_tab.setObjectName(_fromUtf8("edit_output_preprocessing_tab"))
        gridLayout5.addWidget(self.edit_output_preprocessing_tab, 4, 2, 1, 1)

        verticalLayout_2.addWidget(groupBox)
        splitter = QtGui.QSplitter(self.tab_corpus_preparation)
        splitter.setOrientation(QtCore.Qt.Horizontal)
        splitter.setObjectName(_fromUtf8("splitter"))

        self.results_preprocessing = QtGui.QTextEdit(groupBox)
        self.results_preprocessing.setObjectName(_fromUtf8("results_preprocessing"))
        gridLayout6.addWidget(self.results_preprocessing , 5, 1, 1, 1)

        verticalLayout_2.addWidget(splitter)
        verticalLayout_2.setStretch(0, 2)
        verticalLayout_2.setStretch(1, 8)

        self.tab_corpus_preparation.setAutoFillBackground(True)
        self.tab_corpus_preparation.setObjectName(_fromUtf8("tab_corpus_preparation"))

        #btnPreProccess
        self.btnPreProccess = QtGui.QPushButton(groupBox)
        self.btnPreProccess.setEnabled(True)
        self.btnPreProccess.setMinimumSize(QtCore.QSize(120, 30))
        self.btnPreProccess.setFlat(False)
        self.btnPreProccess.setObjectName(_fromUtf8("btnPreProccess"))
        gridLayout.addWidget(self.btnPreProccess, 5, 1, 1, 1)

        self.label_source_preprocessing_tab.setText(_translate("MainWindow", "Source text", None))
        self.btn_source_preprocessing_tab.setText(_translate("Dialog", "...", None))
        self.label_target_preprocessing_tab.setText(_translate("MainWindow", "Target text", None))
        self.btn_target_preprocessing_tab.setText(_translate("Dialog", "...", None))
        self.label_lm_text_preprocessing_tab.setText(_translate("MainWindow", "Text (target lang)", None))
        self.btn_lm_text_preprocessing_tab.setText(_translate("Dialog", "...", None))
        self.label_output_dir_preprocessing_tab.setText(_translate("MainWindow", "Output Directory", None))
        self.btn_output_dir_preprocessing_tab.setText(_translate("Dialog", "...", None))
        self.btnPreProccess.setText(_translate("MainWindow", "Start corpus preprocessing", None))

    def onActivatedSrc(self, text):      
        self.choose_language("preprocessing","source",text)

    def onActivatedTgt(self, text):      
        self.choose_language("preprocessing","target",text)

    def initialize_training_tab(self):
        self.tab_training = QtGui.QWidget()
        self.tab_training.setAutoFillBackground(True)
        self.tab_training.setPalette(self.background_color_palette)
        self.tab_training.setObjectName(_fromUtf8("tab_training"))
        verticalLayout_2 = QtGui.QVBoxLayout(self.tab_training)
        verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        groupBox = QtGui.QGroupBox(self.tab_training)
        groupBox.setObjectName(_fromUtf8("groupBox"))
        groupBox.setMaximumSize(QtCore.QSize(500, 60))
        gridLayout = QtGui.QGridLayout(groupBox)
        gridLayout.setObjectName(_fromUtf8("gridLayout"))
        verticalLayout_2.addWidget(groupBox)
        splitter = QtGui.QSplitter(self.tab_training)
        splitter.setOrientation(QtCore.Qt.Horizontal)
        splitter.setObjectName(_fromUtf8("splitter"))
        self.results_training = QtGui.QTextEdit(splitter)
        self.results_training.setObjectName(_fromUtf8("results_training"))
        verticalLayout_2.addWidget(splitter)
        verticalLayout_2.setStretch(0, 2)
        verticalLayout_2.setStretch(1, 8)
        self.tab_training.setAutoFillBackground(True)
        self.tab_training.setObjectName(_fromUtf8("tab_training"))
        self.btnTraining = QtGui.QPushButton(groupBox)
        self.btnTraining.setEnabled(True)
        self.btnTraining.setMinimumSize(QtCore.QSize(120, 30))
        self.btnTraining.setFlat(False)
        self.btnTraining.setObjectName(_fromUtf8("btnTraining"))
        gridLayout.addWidget(self.btnTraining, 4, 1, 1, 1)

        self.btnTraining.setText(_translate("MainWindow", "Start Training", None))

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Machine Translation Training Tool", None))

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_corpus_preparation), _translate("MainWindow", "Corpus Preparation", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_training), _translate("MainWindow", "Model training", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_evaluation), _translate("MainWindow", "Evaluation", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_machine_translation), _translate("MainWindow", "Machine Translation", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_post_editing), _translate("MainWindow", "Post-Editing", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_differences), _translate("MainWindow", "Diff - Stats", None))
        self.tabWidget.setTabEnabled(5,False)
        self.tabWidget.setTabEnabled(6,False)
       

import icons_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
