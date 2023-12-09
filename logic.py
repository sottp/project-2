from PyQt6.QtWidgets import *
from gui import *
from letterdoer import *
import re
import csv
import os


class Logic(QMainWindow, Ui_MainWindow):

    def __init__(self) -> None:
        """
        initializes the application and sets up the usuable file
        """
        self.current_high: float = -1
        self.old_high: float = self.current_high
        super().__init__()
        self.setupUi(self)

        with open('temp.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            rt = ['Students:', 'Score: x/-1', 'Letter Grade:']  # row title
            writer.writerow(rt)

        self.limitchange.clicked.connect(lambda: self.newhigh())
        self.load.clicked.connect(lambda: self.doload())
        self.save.clicked.connect(lambda: self.dosave())
        self.add.clicked.connect(lambda: self.addto())
        self.edit.clicked.connect(lambda: self.doedit())
        self.remove.clicked.connect(lambda: self.doremove())

    def newhigh(self) -> None:
        """
        changes the score needed to get a 100 percent or A++
        it also clears the grades
        """
        try:
            self.old_high = self.current_high
            self.current_high = float(self.limitscore.text())
            if self.current_high == self.old_high:
                raise ChildProcessError
            elif 0 >= self.current_high:
                raise ZeroDivisionError
            else:
                self.addname.setEnabled(True)
                self.addscore.setEnabled(True)
                self.add.setEnabled(True)

                self.errorthing.setText('')
            with open('temp.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                rt = ['Students:', 'Score:', 'Letter Grade:']  # row title
                if len(str(self.current_high/1).strip()) > 4:
                    rt[1] = f'Score: x/{float(self.current_high)}'
                    if len(str(self.current_high/1).strip()) > 5:
                        raise MemoryError
                else:
                    rt[1] = f'Score: x/{float(self.current_high)}'
                self.scorecolm.setText(rt[1])
                self.lettercolm.setText(f'Letter\nGrade:')
                self.studentcolm.setText('Students:\n')
                writer.writerow(rt)
        except ValueError:
            self.errorthing.setText('Enter number')
        except ZeroDivisionError:
            self.errorthing.setText('Enter positive number')
        except MemoryError:
            self.errorthing.setText('Only use up to 3 digits')
        except ChildProcessError:
            self.errorthing.setText(f'{self.current_high} is already highest number')
        finally:
            self.limitscore.clear()

    def doload(self) -> None:
        """
        loads saved gradebook if found in stored.csv
        """
        try:
            self.lettercolm.setText('Letter Grade:')
            self.studentcolm.setText('Students:')
            with open('temp.csv', 'w', newline='') as file:
                with open('stored.csv', 'r') as otherfile:
                    reader = csv.reader(otherfile)
                    writer = csv.writer(file)
                    for line in reader:
                        writer.writerow(line)
                        if line[0] == 'Students:':
                            bing: str = 'Students: \n'
                            ding: str = f'Score: x/{self.current_high}'
                            ring: str = 'Letter Grade:'
                            if not re.search('Score: x/-1', line[1]):
                                findscore = line[1]
                                self.current_high = float(findscore[9:])
                                self.scorecolm.setText(line[1])
                            else:
                                self.current_high = -1
                            if self.current_high == -1:
                                self.addname.setEnabled(False)
                                self.addscore.setEnabled(False)
                                self.add.setEnabled(False)
                                self.editname.setEnabled(False)
                                self.editscore.setEnabled(False)
                                self.edit.setEnabled(False)
                                self.removename.setEnabled(False)
                                self.remove.setEnabled(False)
                                self.scorecolm.setText('Score:')
                                self.studentcolm.setText('Students:')
                                self.lettercolm.setText('Letter Grade:')
                            elif self.current_high != -1:
                                self.addname.setEnabled(True)
                                self.addscore.setEnabled(True)
                                self.add.setEnabled(True)
                                ding = f'Score: x/{float(self.current_high)}'
                            continue
                        else:
                            self.editname.setEnabled(True)
                            self.editscore.setEnabled(True)
                            self.edit.setEnabled(True)
                            self.removename.setEnabled(True)
                            self.remove.setEnabled(True)
                        bing = bing + '\n' + line[0]
                        ding = ding + '\n' + line[1]
                        ring = ring + '\n' + line[2]
                        self.studentcolm.setText(bing)
                        self.scorecolm.setText(ding)
                        self.lettercolm.setText(ring)
            self.errorthing.setText('File loaded')
        except FileNotFoundError:
            self.errorthing.setText('No file')

    def dosave(self) -> None:
        """
        saves the current gradebook to the file stored.csv
        """
        try:
            with open('stored.csv', 'w', newline='') as file:
                with open('temp.csv', 'r') as otherfile:
                    reader = csv.reader(otherfile)
                    writer = csv.writer(file)
                    for line in reader:
                        writer.writerow(line)
        finally:
            self.errorthing.setText('File saved')

    def addto(self) -> None:
        """
        adds name, score, and letter grade to the gradebook
        doesn't add a new student if thier name is already in gradebook
        """
        try:
            newname: str = self.addname.text()
            newscore: float = float(self.addscore.text())
            found: bool = False

            with open('temp.csv', 'r') as file:
                for line in file:
                    line = line.rstrip()
                    if re.search(newname, line[0]):
                        self.errorthing.setText(f'{line[0]} is already here')
                        found = True

            if not found:
                with open('temp.csv', 'a+', newline='') as file:
                    writer = csv.writer(file)
                    rt = [newname, newscore, lettergetter(newscore, self.current_high)]
                    bing = 'Students:'
                    writer.writerow(rt)

                    self.editname.setEnabled(True)
                    self.editscore.setEnabled(True)
                    self.edit.setEnabled(True)
                    self.removename.setEnabled(True)
                    self.remove.setEnabled(True)

                    self.errorthing.setText('')

                with open('temp.csv', 'r', newline='') as file:
                    reader = csv.reader(file)
                    for line in reader:
                        if line[0] == bing:
                            bing = 'Students: \n'
                            ding = f'Score: x/{self.current_high}'
                            ring = 'Letter Grade:'
                            continue
                        bing = bing + '\n' + line[0]
                        ding = ding + '\n' + line[1]
                        ring = ring + '\n' + line[2]
                        self.studentcolm.setText(bing)
                        self.scorecolm.setText(ding)
                        self.lettercolm.setText(ring)

        except ValueError:
            self.errorthing.setText('Score must be number')
        finally:
            self.addname.clear()
            self.addscore.clear()

    def doedit(self) -> None:
        """
        edits the intputted student's score if they are in the gradebook
        """
        try:
            float(self.editscore.text())
            with open('temp.csv', 'r', newline='') as rfile:
                with open('edit.csv', 'w', newline='')as afile:
                    found = False
                    reader = csv.reader(rfile)
                    writer = csv.writer(afile)
                    for line in reader:
                        if re.search(self.editname.text(), line[0]):
                            found = True
                            line[1] = str(float(self.editscore.text()))
                            line[2] = lettergetter(float(line[1]), self.current_high)
                            writer.writerow([line[0], line[1], line[2]])
                        else:
                            writer.writerow(line)
                    if not found:
                        raise NameError
                    pass
                pass
            os.remove('temp.csv')
            os.renames('edit.csv', 'temp.csv')
            with open('temp.csv', 'r', newline='') as file:
                reader = csv.reader(file)
                bing = 'Students:'
                for line in reader:
                    if line[0] == bing:
                        bing = 'Students: \n'
                        ding = f'Score: x/{self.current_high}'
                        ring = 'Letter Grade:'
                        continue
                    bing = bing + '\n' + line[0]
                    ding = ding + '\n' + line[1]
                    ring = ring + '\n' + line[2]
                    self.studentcolm.setText(bing)
                    self.scorecolm.setText(ding)
                    self.lettercolm.setText(ring)
        except ValueError:
            self.errorthing.setText('Score must be number')
        except NameError:
            self.errorthing.setText('Enter a name on the list')
        finally:
            self.editname.clear()
            self.editscore.clear()
        pass

    def doremove(self) -> None:
        """
        removes the student from the gradebook
        """
        try:
            with open('temp.csv', 'r', newline='') as rfile:
                with open('edit.csv', 'w', newline='')as afile:
                    found = False
                    reader = csv.reader(rfile)
                    writer = csv.writer(afile)
                    for line in reader:
                        if re.search(self.removename.text(), line[0]):
                            found = True
                            continue
                        else:
                            writer.writerow(line)
                    if not found:
                        raise NameError
                    pass
                pass
            os.remove('temp.csv')
            os.renames('edit.csv', 'temp.csv')
            with open('temp.csv', 'r', newline='') as file:
                reader = csv.reader(file)
                counter = 0
                for line in reader:
                    counter += 1
                    if line[0] == 'Students:':
                        bing = 'Students: \n'
                        ding = f'Score: x/{self.current_high}'
                        ring = 'Letter Grade:'
                        # continue
                    if counter > 1:

                        bing = bing + '\n' + line[0]  # students
                        ding = ding + '\n' + line[1]  # score
                        ring = ring + '\n' + line[2]  # letter grade
                        self.studentcolm.setText(bing)
                        self.scorecolm.setText(ding)
                        self.lettercolm.setText(ring)
                    else:
                        self.studentcolm.setText(bing)
                        self.scorecolm.setText(ding)
                        self.lettercolm.setText(ring)
                        # self.editname.setEnabled(False)
                        # self.editscore.setEnabled(False)
                        # self.edit.setEnabled(False)
                        # self.removename.setEnabled(False)
                        # self.remove.setEnabled(False)

        except NameError:
            self.errorthing.setText('Enter a name on the list')
        finally:
            self.removename.clear()
        pass
