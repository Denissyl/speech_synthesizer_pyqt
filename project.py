import sqlite3
import sys

import wave
import struct

import pyaudio
import pyttsx3
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.uic.properties import QtCore
from pygame import mixer
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt

import io

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QTableWidgetItem, QMessageBox

from DataBaseForm import Ui_DataBaseForm
from DesiredLettersSyllables import desired_letters_and_syllables
from GetSyllablesAndLetters import get_syllables_and_letters
from SpeechSynthesizerForm import Ui_SpeechSynthesizerForm
from SplitedWords import split_into_syllables


class SpeechRecorderForm(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent, QtCore.Qt.Window)
        self.init_ui()
        self.WAVE_OUTPUT_FILENAME = ''

    def init_ui(self):
        self.setWindowTitle('Запись слога и буквы')
        self.setGeometry(750, 400, 400, 200)

        self.pb_record_syllable = QPushButton(self)
        self.pb_record_syllable.setEnabled(False)
        self.pb_record_syllable.setIcon(QIcon('mic.png'))
        self.pb_record_syllable.setIconSize(QSize(50, 50))
        self.pb_record_syllable.move(125, 120)
        self.pb_listen_record = QPushButton(self)
        self.pb_listen_record.setIcon(QIcon('play.png'))
        self.pb_listen_record.move(205, 120)
        self.pb_listen_record.setIconSize(QSize(50, 50))
        self.pb_listen_record.setEnabled(False)
        self.lbl_add_syllable = QLabel("Введите слог или букву, которую хотите записать", self)
        self.lbl_add_syllable.move(100, 10)
        self.lbl_status = QLabel(self)
        self.lbl_status.setText('Статус: Запись не начата')
        self.lbl_status.setStyleSheet('color: blue')
        self.lbl_status.move(130, 80)
        self.lbl_add_syllable.move(100, 10)
        self.le_add_syllable = QLineEdit(self)
        self.le_add_syllable.move(130, 50)
        self.le_add_syllable.textChanged.connect(self.textchanged)
        self.show()
        self.pb_record_syllable.clicked.connect(self.record_syllable)
        self.pb_listen_record.clicked.connect(self.listen_record)

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        if event.key() == Qt.Key_F5:
            if self.le_add_syllable.text():
                self.record_syllable()
        if event.key() == Qt.Key_F6:
            if self.WAVE_OUTPUT_FILENAME != '':
                self.listen_record()

    def textchanged(self):
        if self.le_add_syllable.text() != '':
            self.pb_record_syllable.setEnabled(True)
        else:
            self.pb_record_syllable.setEnabled(False)

    def record_syllable(self):
        self.WAVE_OUTPUT_FILENAME = ''
        self.lbl_status.setText('Статус: Запись начата')
        self.lbl_status.setStyleSheet('color: red')
        QApplication.processEvents()
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100
        DURATION = 0.8

        p = pyaudio.PyAudio()

        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        frames = []

        for i in range(0, int(RATE / CHUNK * DURATION)):
            data = stream.read(CHUNK)
            frames.append(data)

        stream.stop_stream()
        stream.close()
        p.terminate()

        self.lbl_status.setText('Статус: Запись завершена')
        self.lbl_status.setStyleSheet('color: green')

        self.WAVE_OUTPUT_FILENAME += self.le_add_syllable.text() + ".wav"
        wf = wave.open(self.WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        self.pb_listen_record.setEnabled(True)
        self.bytestring = open(self.WAVE_OUTPUT_FILENAME, 'rb').read()

        self.add_to_get_syllables_and_letters()

    def listen_record(self):
        mixer.init()
        mixer.Sound(self.WAVE_OUTPUT_FILENAME).play()

    def add_to_get_syllables_and_letters(self):
        conn = sqlite3.connect('sounds.db')
        cursor = conn.cursor()

        cursor.execute("""INSERT INTO sounds(letter, sound) VALUES(?, ?)""",
                       (self.le_add_syllable.text(), self.bytestring))
        conn.commit()
        self.le_add_syllable.clear()


class SpeechSynthesizerForm(QWidget, Ui_SpeechSynthesizerForm):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.additionalWin = None
        self.WinDatabase = None
        self.init_ui()
        self.text_k = ''

    def init_ui(self):
        self.pixmap = QPixmap('Speech.png')
        self.image = QLabel(self)
        self.image.move(15, 310)
        self.image.setPixmap(self.pixmap)

        self.le_text.textChanged.connect(self.textchanged)

        self.pb_bd.clicked.connect(self.openWindowDataBase)
        self.pb_play.clicked.connect(self.callSpeechSynthesizer)
        self.pb_add_syllable.clicked.connect(self.openWindow)
        self.pb_delete_one_letter.clicked.connect(self.delete_one_letter)
        self.pb_delete_all.clicked.connect(self.delete_all)
        self.pb_zh.clicked.connect(self.keyboard_on_screen)
        self.pb_a.clicked.connect(self.keyboard_on_screen)
        self.pb_b.clicked.connect(self.keyboard_on_screen)
        self.pb_ch.clicked.connect(self.keyboard_on_screen)
        self.pb_d.clicked.connect(self.keyboard_on_screen)
        self.pb_e.clicked.connect(self.keyboard_on_screen)
        self.pb_f.clicked.connect(self.keyboard_on_screen)
        self.pb_g.clicked.connect(self.keyboard_on_screen)
        self.pb_hs.clicked.connect(self.keyboard_on_screen)
        self.pb_i.clicked.connect(self.keyboard_on_screen)
        self.pb_j.clicked.connect(self.keyboard_on_screen)
        self.pb_k.clicked.connect(self.keyboard_on_screen)
        self.pb_kh.clicked.connect(self.keyboard_on_screen)
        self.pb_l.clicked.connect(self.keyboard_on_screen)
        self.pb_m.clicked.connect(self.keyboard_on_screen)
        self.pb_n.clicked.connect(self.keyboard_on_screen)
        self.pb_o.clicked.connect(self.keyboard_on_screen)
        self.pb_p.clicked.connect(self.keyboard_on_screen)
        self.pb_r.clicked.connect(self.keyboard_on_screen)
        self.pb_s.clicked.connect(self.keyboard_on_screen)
        self.pb_sg.clicked.connect(self.keyboard_on_screen)
        self.pb_sh.clicked.connect(self.keyboard_on_screen)
        self.pb_shch.clicked.connect(self.keyboard_on_screen)
        self.pb_t.clicked.connect(self.keyboard_on_screen)
        self.pb_ts.clicked.connect(self.keyboard_on_screen)
        self.pb_u.clicked.connect(self.keyboard_on_screen)
        self.pb_v.clicked.connect(self.keyboard_on_screen)
        self.pb_y.clicked.connect(self.keyboard_on_screen)
        self.pb_ya.clicked.connect(self.keyboard_on_screen)
        self.pb_ye.clicked.connect(self.keyboard_on_screen)
        self.pb_ye2.clicked.connect(self.keyboard_on_screen)
        self.pb_yu.clicked.connect(self.keyboard_on_screen)
        self.pb_z.clicked.connect(self.keyboard_on_screen)
        self.pb_zh.clicked.connect(self.keyboard_on_screen)

    def openWindow(self):
        if not self.additionalWin:
            self.additionalWin = SpeechRecorderForm(self)
        self.additionalWin.show()

    def openWindowDataBase(self):
        if not self.WinDatabase:
            self.WinDatabase = DataBase(self)
        self.WinDatabase.show()

    def textchanged(self):
        if self.le_text.text() != '':
            self.pb_play.setEnabled(True)
        else:
            self.pb_play.setEnabled(False)
        self.play_one_letter_from_keyboard()

    def keyboard_on_screen(self):
        self.button = self.sender()
        self.text_k += self.button.text()
        self.le_text.setText(self.text_k)

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        if event.key() == Qt.Key_F1:
            self.callSpeechSynthesizer()
        if event.key() == Qt.Key_F2:
            self.openWindow()

    def play_one_letter_from_keyboard(self):
        letters_syllables = get_syllables_and_letters()
        mixer.init()
        if self.checkBox.isChecked():
            if len(self.le_text.text()) != 0:
                mixer.Sound(letters_syllables[self.le_text.text()[-1]]).play()

    def delete_one_letter(self):
        self.le_text.setText(self.le_text.text()[:-1])
        self.text_k = self.text_k[:-1]

    def delete_all(self):
        self.le_text.setText('')
        self.text_k = ''

    def callSpeechSynthesizer(self):
        if self.comboBox.currentText() == 'Denis TTS':
            self.call1 = SpeechSynthesizer()
            self.call1.play_text(self.le_text.text())
        elif self.comboBox.currentText() == 'Google TTS':
            self.call2 = SpeechSynthesizer()
            self.call2.play_google_tts(self.le_text.text())


class SpeechSynthesizer:
    def play_text(self, text):
        splited_words = split_into_syllables(text)
        letters_syllables = get_syllables_and_letters()
        desired_letters_syllables = desired_letters_and_syllables(splited_words, letters_syllables)

        all_frames = io.BytesIO()

        frames_count = 0

        for b in desired_letters_syllables:
            wave_file = wave.open(io.BytesIO(b), mode="rb")
            cnt = wave_file.getnframes()
            frames_count += cnt
            all_frames.write(wave_file.readframes(frames_count))

        first_wave = wave.open(io.BytesIO(desired_letters_syllables[0]), mode="rb")
        output_bytes = io.BytesIO()
        wave_out = wave.open(output_bytes, mode='wb')

        wave_out.setparams(first_wave.getparams())
        wave_out.setnframes(frames_count)

        all_frames.seek(0)
        wave_out.writeframes(all_frames.read())
        wave_out.close()

        output_bytes.seek(0)

        source = wave.open(output_bytes, mode="rb")
        frames_count = source.getnframes()
        data = struct.unpack("<" + str(frames_count) + "h",
                             source.readframes(frames_count))
        data = list(filter(lambda i: i < -35 or i > 35 and not i == 0, data))
        newframes = struct.pack("<" + str(len(data)) + "h", *data)
        source.close()

        mixer.init()
        mixer.Sound(newframes).play()

    def play_google_tts(self, text):
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()


class DataBase(QWidget, Ui_DataBaseForm):
    def __init__(self, parent=None):
        super().__init__(parent, QtCore.Qt.Window)
        self.setupUi(self)

        self.conn = sqlite3.connect('sounds.db')
        self.cursor = self.conn.cursor()

        self.init_ui()

    def init_ui(self):
        self.pb_select.clicked.connect(self.get_sounds)
        self.pb_select_all.clicked.connect(self.get_all_sounds)
        self.pb_delete.clicked.connect(self.delete_sounds)

    def get_sounds(self):

        query = 'SELECT * FROM Sounds WHERE letter = ' + "'" + self.le_condition.text() + "'"

        sounds = self.cursor.execute(query).fetchall()
        columns = list(map(lambda x: x[0], self.cursor.description))

        self.tw_sounds.setRowCount(0)
        self.tw_sounds.setColumnCount(len(columns))
        self.tw_sounds.setHorizontalHeaderLabels(columns)

        for row_index, sound in enumerate(sounds):
            self.tw_sounds.insertRow(row_index)

            for col_index, column in enumerate(sound):
                self.tw_sounds.setItem(row_index, col_index, QTableWidgetItem(str(column)))

    def get_all_sounds(self):
        query = 'SELECT * FROM Sounds'
        sounds = self.cursor.execute(query).fetchall()
        columns = list(map(lambda x: x[0], self.cursor.description))

        self.tw_sounds.setRowCount(0)
        self.tw_sounds.setColumnCount(len(columns))
        self.tw_sounds.setHorizontalHeaderLabels(columns)

        for row_index, sound in enumerate(sounds):
            self.tw_sounds.insertRow(row_index)

            for col_index, column in enumerate(sound):
                self.tw_sounds.setItem(row_index, col_index, QTableWidgetItem(str(column)))

    def delete_sounds(self):
        selected_rows = set([item.row() for item in self.tw_sounds.selectedItems()])

        selected_letters = [self.tw_sounds.item(row, 0).text() for row in selected_rows]

        agreed = QMessageBox.question(self, 'Подтвердите удаление',
                                      'Действительно ли Вы хотите удалить звуки: ' +
                                      ', '.join(map(str, selected_letters)) + '?', QMessageBox.Yes, QMessageBox.No)

        if agreed == QMessageBox.Yes:
            query = "DELETE FROM Sounds WHERE letter IN (" + ", ".join('?' * len(selected_letters)) + ")"
            self.cursor.execute(query, selected_letters)
            self.conn.commit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    wnd = SpeechSynthesizerForm()
    wnd.show()
    sys.exit(app.exec())
