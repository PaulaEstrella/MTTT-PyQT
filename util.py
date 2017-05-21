"""@brief     A few aux functions."""
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

import sys

from PyQt4.QtGui import (
    QApplication,
    QMessageBox,
    )


def doAlert(text):
    msgBox = QMessageBox()
    msgBox.setText(text)
    msgBox.setWindowTitle("Message")
    msgBox.setIcon(QMessageBox.Warning)
    msgBox.exec_()


def doQuestion(text):
    reply = QMessageBox.question(
        None, 'Message', text, QMessageBox.Yes, QMessageBox.No)
    if reply == QMessageBox.Yes:
        return True
    else:
        return False


if __name__ == '__main__':
    app = QApplication(sys.argv)
    doAlert("doAlert")
    print doQuestion("doQuestion")
