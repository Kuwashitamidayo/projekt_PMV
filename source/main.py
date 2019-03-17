import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import numpy as np
# https://tutorials-raspberrypi.com/raspberry-pi-measure-humidity-temperature-dht11-dht22/
# import Adaruit_DHT

 
class App(QDialog):
    # temperatura powietrza
    airTemperature = 20.0
    # temperatura radiacji
    radTemperature = 20.0
    # prędkosć powietrza
    airSpeed = 0.1
    # wilgotność
    humidity = 50
    # współczynnik metabolizu
    metabolicRate = 1.0
    # współczynnik ubioru
    clothingLevel = 0.5


    ## wyniki
    # PMV - współczynnik komfortu (PMV = (0.303 e^(-0.036metabolicRate^ + 0.028) clothigLevel  )
    pmv = 0
    # PPD - odsetek niezadowolonych
    ppd = 0
    # kategoria komfortu
    category = ""

 
    def __init__(self):
        super().__init__()
        self.title = 'Kalkulacja wskaźnika komfortu PMV by K. Talaga & Ł. Pawlik'
        self.left = 10
        self.top = 10
        self.width = 500
        self.height = 300
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
    
        self.createGridLayout()
        
        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.horizontalGroupBox)
        windowLayout.addWidget(self.horizontalGroupBoxResults)
        self.calculateCategory()
        self.setLayout(windowLayout)
    
        self.show()
    #def setValues(self):

    # Określanie kategorii na podstawie wartości PMV
    def calculateCategory(self):
        self.category = "IV"
        if -0.7 < self.pmv < 0.7:
            self.category = "III"
        if -0.5 < self.pmv < 0.5:
            self.category = "II"
        if -0.2 < self.pmv < 0.2:
            self.category = "I"
        return self.category

    # Tutaj będzie liczone PMV
    def calculatePMV(self):
        self.pmv = 0    # tu wstawić wzór
        a = "" + str(self.pmv)
        return a

    # Tutaj będzie liczone PPD
    def calculatePPD(self):
        self.ppd = 0    # tu wstawić wzór
        return self.ppd
    
    def createGridLayout(self):
        self.horizontalGroupBox = QGroupBox("Parametry")
        layout = QGridLayout()
        layout.setColumnStretch(1, 4)
        #layout.setColumnStretch(3, 6)

        self.horizontalGroupBoxResults = QGroupBox("Wyniki")
        layoutRes = QGridLayout()
        layoutRes.setColumnStretch(1, 4)
        
        ## Deklarowanie pól ze zmiennymi do wpisywania
        # Płotek (#) w setInputMask oznacza + lub - przed liczbą
        # QLineEdit - pole do wpisywania wartości
        # QComboBox - rozwijana lista - do zaimplementowania
        qAirTemperature = QLineEdit()
        qAirTemperature.setAlignment(Qt.AlignCenter)
        qAirTemperature.setInputMask('#99.99')  

        qRadTemperature = QLineEdit()
        qRadTemperature.setAlignment(Qt.AlignCenter)
        qRadTemperature.setInputMask('#99.99')

        qAirSpeed = QLineEdit()
        qAirSpeed.setAlignment(Qt.AlignCenter)
        qAirSpeed.setInputMask('#99.99')

        qHumidity = QLineEdit()
        qHumidity.setAlignment(Qt.AlignCenter)
        qHumidity.setValidator(QIntValidator(0, 100, self))

        qMetabolicRate = QLineEdit()
        qMetabolicRate.setAlignment(Qt.AlignCenter)
        qMetabolicRate.setInputMask("99.9")
        
        qClothingLevel = QLineEdit()
        qClothingLevel.setAlignment(Qt.AlignCenter)
        qClothingLevel.setInputMask("99.9")

        qPMV = QLabel(str(self.pmv))
        qPMV.setAlignment(Qt.AlignCenter)
        qPPD = QLabel(str(self.ppd))
        qPPD.setAlignment(Qt.AlignCenter)
        qCategory = QLabel(self.calculateCategory())
        qCategory.setAlignment(Qt.AlignCenter)
        
        ## Dodawaie pól do siatki
        # Dla parametrów
        layout.addWidget(QLabel("Temperatura powietrza"),0,0)
        layout.addWidget(qAirTemperature,0,1)
        layout.addWidget(QLabel("[°C]"),0,2)

        layout.addWidget(QLabel("Średnia temperatura radiacji"),1,0)
        layout.addWidget(qRadTemperature,1,1)
        layout.addWidget(QLabel("[°C]"),1,2)

        layout.addWidget(QLabel("Prędkość powietrza"),2,0)
        layout.addWidget(qAirSpeed,2,1)
        layout.addWidget(QLabel("[m/s]"),2,2)

        layout.addWidget(QLabel("Wilgotność"),3,0)
        layout.addWidget(qHumidity,3,1)
        layout.addWidget(QLabel("[%]"),3,2)

        layout.addWidget(QLabel("Współcznynnik metabolizmu"),4,0)
        layout.addWidget(qMetabolicRate,4,1)
        layout.addWidget(QLabel("[met]"),4,2)
        
        layout.addWidget(QLabel("Współcznynnik ubioru"),5,0)
        layout.addWidget(qClothingLevel,5,1)
        layout.addWidget(QLabel("[clo]"),5,2)

        # Dla wyników
        layoutRes.addWidget(QLabel("PMV (wskażnik komfortu)"),0,0)
        layoutRes.addWidget(qPMV,0,1)

        layoutRes.addWidget(QLabel("PPD (odsetek niezadowolonych)"),1,0)
        layoutRes.addWidget(qPPD,1,1)
        layoutRes.addWidget(QLabel("[%]"),1,2)


        layoutRes.addWidget(QLabel("Kategoria"),2,0)
        layoutRes.addWidget(qCategory, 2,1)

        ## Inicjowanie wartości w polach
        qAirTemperature.setText(str(self.airTemperature))
        qRadTemperature.setText(str(self.radTemperature))
        qAirSpeed.setText(str(self.airSpeed))
        qHumidity.setText(str(self.humidity))
        qMetabolicRate.setText(str(self.metabolicRate))
        qClothingLevel.setText(str(self.clothingLevel))

        
        self.horizontalGroupBox.setLayout(layout)
        self.horizontalGroupBoxResults.setLayout(layoutRes)
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
ex = App()
sys.exit(app.exec_())