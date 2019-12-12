#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt, QEventLoop, QThread, QObject, pyqtSlot, pyqtSignal

import free_hand
import sys, os

path = os.path.abspath(__file__)
curdir = os.path.dirname(path)
sys.path.insert(0, curdir)


class Speech(QObject):
    def __init__(self, widget):
        super(Speech, self).__init__()
        self.widget = widget
        self.run_trigger.connect(self.run)

    run_trigger = pyqtSignal()
    @pyqtSlot()
    def run(self):
        import speech_recognition as sr
        print("[OK]\n"
              "--speach regonition module importes successfuly")
        recognizer = sr.Recognizer()
        microphone = sr.Microphone()

        # check that recognizer and microphone arguments are appropriate type
        if not isinstance(recognizer, sr.Recognizer):
            raise TypeError("`recognizer` must be `Recognizer` instance")

        if not isinstance(microphone, sr.Microphone):
            raise TypeError("`microphone` must be `Microphone` instance")\

        print("Sustem ready for work\n"
              "Speak!")
        self.widget.someTrigger.emit("SPEAK!")
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        # set up the response object
        response = {
            "success": True,
            "error": None,
            "transcription": None
        }

        self.widget.someTrigger.emit("[OK], trying to recognize")
        
        try:
            response["transcription"] = recognizer.recognize_google(audio,
                                                            language="ru-RU").lower()
            self.widget.someTrigger.emit(response["transcription"])
            print(response["transcription"])
        except sr.RequestError:
            print("API was unreachable or unresponsive")
        except sr.UnknownValueError:
            # speech was unintelligible
            print("Unable to recognize speech")
            
        if not response["transcription"] is None:
            if "запусти" in response["transcription"]:
                import subprocess
                if "яндекс" in response["transcription"]:
                    print("statring yandex browser")
                    subprocess.Popen('yandex-browser')

                if "питон" in response["transcription"]:
                    print("statring python idle")
                    subprocess.Popen('idle')

        print("End of progreamm")
        
        
        self.widget.someTrigger.emit("Hello World")
        #self.widget.closing()
        QApplication.instance().quit()
        

class ExampleApp(QtWidgets.QWidget, free_hand.Ui_Form):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self) # Это нужно для инициализации нашего дизайна
        self.label.setText("Fuck every body")
        #self.setWindowFlags(Qt.FramelessWindowHint)
        self.approx_window()

        self.someTrigger.connect(self.gui_response)

        self.thread = QThread()
        self.thread.start()
        self.consume = Speech(self)
        self.consume.moveToThread(self.thread)
        self.consume.run_trigger.emit()

    someTrigger = pyqtSignal(str)

    def approx_window(self):
        screen_geometry = QApplication.desktop().availableGeometry()
        x = int(screen_geometry.width()/2) - 150 # 300/2
        y = int(screen_geometry.height()/2) - 60 # 60/2
        #screen_size = (screen_geometry.width(), screen_geometry.height())
        self.move(x, y)
        self.label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

    def gui_response(self, text):
        self.label.setText(text)

    def closing(self):
        self.close()
        
        


    def start(self):
        import speech_recognition as sr
        print("[OK]\n"
              "--speach regonition module importes successfuly")
        recognizer = sr.Recognizer()
        microphone = sr.Microphone()

        # check that recognizer and microphone arguments are appropriate type
        if not isinstance(recognizer, sr.Recognizer):
            raise TypeError("`recognizer` must be `Recognizer` instance")

        if not isinstance(microphone, sr.Microphone):
            raise TypeError("`microphone` must be `Microphone` instance")\

        print("Sustem ready for work\n"
              "Speak!")
        self.label.setText("SPEAK!")
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        # set up the response object
        response = {
            "success": True,
            "error": None,
            "transcription": None
        }

        self.label.setText("[OK], trying to recognize")
        
        try:
            response["transcription"] = recognizer.recognize_google(audio,
                                                            language="ru-RU").lower()
            print(response["transcription"])
        except sr.RequestError:
            print("API was unreachable or unresponsive")
        except sr.UnknownValueError:
            # speech was unintelligible
            print("Unable to recognize speech")
            
        if not response["transcription"] is None:
            if "запусти" in response["transcription"]:
                import subprocess
                if "яндекс" in response["transcription"]:
                    print("statring yandex browser")
                    subprocess.Popen('yandex-browser')

                if "питон" in response["transcription"]:
                    print("statring python idle")
                    subprocess.Popen('idle')

        print("End of progreamm")
        self.close()

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ExampleApp()
    window.show()
    #window.t1 = threading.Thread(target=window.start)
    #window.daemon = True
    #window.t1.start()
    #window.t1.join()
    sys.exit(app.exec_())
    

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()




        
