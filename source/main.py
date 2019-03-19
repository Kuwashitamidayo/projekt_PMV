import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import numpy as np
import math as mth
# https://tutorials-raspberrypi.com/raspberry-pi-measure-humidity-temperature-dht11-dht22/
#import Adaruit_DHT

 
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
    
    # Liczenie wyników (PMV, PPD, kategoria)
    def calculateParams(self):
        self.calculatePMV()
        self.calculatePPD()
        self.calculateCategory()
        self.qPMV.setText(str(self.pmv))
        self.qPPD.setText(str(self.ppd))
        self.qCategory.setText(self.category)

	
    # Ustawia temperaturę powietrza
    def setAirTemperature(self):
        try:
            self.airTemperature = float(self.qAirTemperature.text().replace(",", "."))
        except:
            self.airTemperature = 0.0
        self.calculateParams()
    
    # Ustawia temperaturę radiacji (np. grzanie ścian, szyb)
    def setRadTemperature(self):
        try:
            self.radTemperature = float(self.qRadTemperature.text().replace(",", "."))
        except:
            self.radTemperature = 0.0
        self.calculateParams()

    # Ustawia prędkość powietrza
    def setAirSpeed(self):
        try:
            self.airSpeed = float(self.qAirSpeed.text().replace(",", "."))
        except:
            self.airSpeed = 0.0
        self.calculateParams()

    # Ustawia wilgotność
    def setHumidity(self):
        try:
            self.humidity = int(self.qHumidity.text())
        except:
            self.humidity = 0
        self.calculateParams()

    # Ustawia współczynnik metabolizmu
    def setMetabolicRate(self):
        self.metabolicRate = float(self.qMetabolicRate.text().replace(",", "."))
        self.calculateParams()

    # Ustawia współczynnik ubioru
    def setClothingLevel(self):
        self.clothingLevel = float(self.qClothingLevel.text().replace(",", "."))
        self.calculateParams()
        
	
    # Zapis wartości ze zmiennych do pól tekstowych - może się przyda
    def getValues(self):
        self.qAirTemperature.setText(str(self.airTemperature))
        self.qRadTemperature.setText(str(self.radTemperature))
        self.qAirSpeed.setText(str(self.airSpeed))
        self.qHumidity.setText(str(self.humidity))
        self.qMetabolicRate.setText(str(self.metabolicRate))
        self.qClothingLevel.setText(str(self.clothingLevel))

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
        a = 0.303*mth.exp(-0.036*self.metabolicRate)+0.028
        pmv = a    # tu wstawić wzór
        self.pmv = pmv
        res = str(pmv)
        return res

    # Tutaj będzie liczone PPD
    def calculatePPD(self):
        ppd = 0    # tu wstawić wzór
        self.ppd = ppd
        res = str(ppd)
        return res
    
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
        locale = QLocale("Polish")
        
        self.qAirTemperature = QLineEdit()
        self.qAirTemperature.setAlignment(Qt.AlignCenter)
        qValTemperature = QDoubleValidator(0, 100.0, 2)
        qValTemperature.setNotation(QDoubleValidator.StandardNotation)
        qValTemperature.setLocale(locale)
        self.qAirTemperature.setValidator(qValTemperature)

        self.qRadTemperature = QLineEdit()
        self.qRadTemperature.setAlignment(Qt.AlignCenter)
        self.qRadTemperature.setValidator(qValTemperature)

        self.qAirSpeed = QLineEdit()
        self.qAirSpeed.setAlignment(Qt.AlignCenter)
        qValAirSpeed = QDoubleValidator(0.0, 10.0, 2, self)
        qValAirSpeed.setNotation(QDoubleValidator.StandardNotation)
        qValAirSpeed.setLocale(locale)
        self.qAirSpeed.setValidator(qValAirSpeed)

        self.qHumidity = QLineEdit()
        self.qHumidity.setAlignment(Qt.AlignCenter)
        self.qHumidity.setValidator(QIntValidator(0, 100, self))

        self.qMetabolicRate = QLineEdit()
        self.qMetabolicRate.setAlignment(Qt.AlignCenter)
        qValMetabolicRate = QDoubleValidator(0.0, 30.0, 2)
        qValMetabolicRate.setNotation(QDoubleValidator.StandardNotation)
        qValMetabolicRate.setLocale(locale)
        self.qMetabolicRate.setValidator(qValMetabolicRate)
        
        self.qClothingLevel = QLineEdit()
        self.qClothingLevel.setAlignment(Qt.AlignCenter)
        qValClothingLevel = QDoubleValidator(0.0, 30.0, 2)
        qValClothingLevel.setNotation(QDoubleValidator.StandardNotation)
        qValClothingLevel.setLocale(locale)
        self.qClothingLevel.setValidator(qValClothingLevel)

        self.qPMV = QLabel(str(self.pmv))
        self.qPMV.setAlignment(Qt.AlignCenter)
        self.qPPD = QLabel(str(self.ppd))
        self.qPPD.setAlignment(Qt.AlignCenter)
        self.qCategory = QLabel(self.calculateCategory())
        self.qCategory.setAlignment(Qt.AlignCenter)
        
        ## Dodawaie pól do siatki
        # Dla parametrów
        layout.addWidget(QLabel("Temperatura powietrza"),0,0)
        layout.addWidget(self.qAirTemperature,0,1)
        layout.addWidget(QLabel("[°C]"),0,2)

        layout.addWidget(QLabel("Średnia temperatura radiacji"),1,0)
        layout.addWidget(self.qRadTemperature,1,1)
        layout.addWidget(QLabel("[°C]"),1,2)

        layout.addWidget(QLabel("Prędkość powietrza"),2,0)
        layout.addWidget(self.qAirSpeed,2,1)
        layout.addWidget(QLabel("[m/s]"),2,2)

        layout.addWidget(QLabel("Wilgotność"),3,0)
        layout.addWidget(self.qHumidity,3,1)
        layout.addWidget(QLabel("[%]"),3,2)

        layout.addWidget(QLabel("Współcznynnik metabolizmu"),4,0)
        layout.addWidget(self.qMetabolicRate,4,1)
        layout.addWidget(QLabel("[met]"),4,2)
        
        layout.addWidget(QLabel("Współcznynnik ubioru"),5,0)
        layout.addWidget(self.qClothingLevel,5,1)
        layout.addWidget(QLabel("[clo]"),5,2)

        # Dla wyników
        layoutRes.addWidget(QLabel("PMV (wskażnik komfortu)"),0,0)
        layoutRes.addWidget(self.qPMV,0,1)

        layoutRes.addWidget(QLabel("PPD (odsetek niezadowolonych)"),1,0)
        layoutRes.addWidget(self.qPPD,1,1)
        layoutRes.addWidget(QLabel("[%]"),1,2)


        layoutRes.addWidget(QLabel("Kategoria"),2,0)
        layoutRes.addWidget(self.qCategory, 2,1)

        ## Inicjowanie wartości w polach
        self.qAirTemperature.setText(str(self.airTemperature))
        self.qRadTemperature.setText(str(self.radTemperature))
        self.qAirSpeed.setText(str(self.airSpeed))
        self.qHumidity.setText(str(self.humidity))
        self.qMetabolicRate.setText(str(self.metabolicRate))
        self.qClothingLevel.setText(str(self.clothingLevel))
		
        ## Łączenie zmiennych przechowujących wartości z polami tekstowymi
        self.qAirTemperature.textChanged.connect(self.setAirTemperature)#str(self.airTemperature))
        self.qAirTemperature.editingFinished.connect(self.getValues)

        self.qRadTemperature.textChanged.connect(self.setRadTemperature)
        self.qRadTemperature.editingFinished.connect(self.getValues)

        self.qAirSpeed.textChanged.connect(self.setAirSpeed)
        self.qAirSpeed.editingFinished.connect(self.getValues)

        self.qHumidity.textChanged.connect(self.setHumidity)
        self.qHumidity.editingFinished.connect(self.getValues)

        self.qMetabolicRate.textChanged.connect(self.setMetabolicRate)
        self.qMetabolicRate.editingFinished.connect(self.getValues)

        self.qClothingLevel.textChanged.connect(self.setClothingLevel)
        self.qClothingLevel.editingFinished.connect(self.getValues)

        
        self.horizontalGroupBox.setLayout(layout)
        self.horizontalGroupBoxResults.setLayout(layoutRes)

if __name__ == '__main__':
    app = QApplication(sys.argv)
ex = App()
sys.exit(app.exec_())
