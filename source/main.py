import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import numpy as np
import math as mth
# https://tutorials-raspberrypi.com/raspberry-pi-measure-humidity-temperature-dht11-dht22/
# import Adaruit_DHT

 
class App(QDialog):
<<<<<<< HEAD
	# temperatura powietrza
	airTemperature = 20.0
	# temperatura radiacji
	radTemperature = 20.0
	# prędkosć powietrza
	airSpeed = 0.1
	# wilgotność
	humidity = 50
	# współczynnik metabolizu
	metabolicRate = 1.1
	# współczynnik ubioru
	clothingLevel = 0.5
	# praca zewnętrzna
	extWork = 50
	#ciśnienie cząsteczkowe pary wodnej
	steamPressure = 1000 #[Pa], 1 hPa na biegunach, 20-30 hPa na równiku
	#temperatura powierzchnii odzieży
	clothingTemperature = 15.0

	## wyniki
	# PMV - współczynnik komfortu (PMV = (0.303 e^(-0.036metabolicRate^ + 0.028) clothingLevel  )
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
		self.width = 800
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

	# Ustawia pracę zewnetrzna
	def setExtWork(self):
		self.extWork = int(self.qExtWork.text())
		self.calculateParams()

	# Ustawia ciśnienie cząsteczkowe pary wodnej
	def setSteamPressure(self):
		self.steamPressure = int(self.qSteamPressure.text())
		self.calculateParams()

	# Ustawia temperaturę powietrza
	def setClothingTemperature(self):
		try:
			self.clothingTemperature = float(self.qClothingTemperature.text().replace(",", "."))
		except:
			self.clothingTemperature = 0.0
		self.calculateParams()
		
	# Tworzenie listy dla metabolizmu
	# Uwaga - zachować format przy wpisywaniu nowych pozycji!
	# (zakres 0,0 - 9,9; 1 miejsce po przecinku)
	def initMetabolicRateElementList(self):
		self.qMetaRateList.addItem("1,1 - Pisanie na klawiaturze")
		self.qMetaRateList.addItem("1,2 - Stanie, relaks")
		self.qMetaRateList.addItem("1,0 - Siedzenie, spokojnie")
		self.qMetaRateList.addItem("0,7 - Spanie")
		self.qMetaRateList.addItem("0,8 - Leżenie")
		self.qMetaRateList.addItem("2,0 - Powolny chód (3km/h)")
		self.qMetaRateList.addItem("2,6 - Normalny chód (4,5km/h)")
		self.qMetaRateList.addItem("3,8 - Szybki chód (6km/h)")
		self.qMetaRateList.addItem("1,0 - Czytanie, na siedząco")
		self.qMetaRateList.addItem("1,0 - Pisanie")
		self.qMetaRateList.addItem("1,2 - Odkładanie dokumentów, na siedząco")
		self.qMetaRateList.addItem("1,4 - Odkładanie dokumentów, na stojąco")
		self.qMetaRateList.addItem("1,7 - Chodzenie bez celu")
		self.qMetaRateList.addItem("2,1 - Podnoszenie / pakowanie")
		self.qMetaRateList.addItem("1,5 - Prowadzenie samochodu")
		self.qMetaRateList.addItem("1,2 - Latanie samolotem, pasażer")
		self.qMetaRateList.addItem("2,4 - Latanie samolotem bojowym")
		self.qMetaRateList.addItem("3,2 - Prowadzenie ciężkiego pojazdu")
		self.qMetaRateList.addItem("1,8 - Gotowanie")
		self.qMetaRateList.addItem("2,7 - Sprzątanie domu")
		self.qMetaRateList.addItem("2,2 - Siedzenie, intensywny ruch kończyn")
		self.qMetaRateList.addItem("1,8 - Piłowanie")
		self.qMetaRateList.addItem("2,2 - Lekka praca przy maszynie")
		self.qMetaRateList.addItem("4,0 - Ciężka praca przy maszynie")
		self.qMetaRateList.addItem("4,0 - Dźwiganie bagażu o wadze 45kg")
		self.qMetaRateList.addItem("4,0 - Praca łopatą")
		self.qMetaRateList.addItem("3,4 - Tańcowanie")
		self.qMetaRateList.addItem("3,5 - Ćwiczenia bez przyrządów (pompki itp.)")
		self.qMetaRateList.addItem("3,8 - Tenis")
		self.qMetaRateList.addItem("6,3 - Koszykówka")
		self.qMetaRateList.addItem("7,8 - Wrestling")

	# Tworzenie listy dla stopnia ubioru
	# Uwaga - zachować format przy wpisywaniu nowych pozycji!
	# (zakres 0,00 - 9,99; 2 miejsca po przecinku)
	def initClothingLevelElementList(self):
		self.qCloLevelList.addItem(str("0,50 - Typowy ubiór letni"))
		self.qCloLevelList.addItem(str("1,00 - Typowy zimowy ubiór (w budynku)"))
		self.qCloLevelList.addItem(str("0,57 - T-shirt, spodnie"))
		self.qCloLevelList.addItem(str("0,61 - Koszula, spodnie"))
		self.qCloLevelList.addItem(str("0,96 - Kurtka, koszula, spodnie"))
		self.qCloLevelList.addItem(str("0,54 - Spódniczka do kolan, koszulka"))
		self.qCloLevelList.addItem(str("0,36 - Spodenki, T-shirt"))
		self.qCloLevelList.addItem(str("0,74 - Dres, długi rękaw"))
		
	def getMetaRateFromList(self):
		# Trzy pierwsze znaki z nazwy elementu listy jako wartość
		temp = float(self.qMetaRateList.currentText()[:3].replace(",", "."))
		self.metabolicRate = temp
		self.getValues()
		self.calculateParams()
		
	def getCloLevelFromList(self):
		# Trzy pierwsze znaki z nazwy elementu listy jako wartość
		temp = float(self.qCloLevelList.currentText()[:4].replace(",", "."))
		self.clothingLevel = temp
		self.getValues()
		self.calculateParams()
		
	# Zapis wartości ze zmiennych do pól tekstowych - może się przyda
	def getValues(self):
		self.qAirTemperature.setText(str(self.airTemperature))
		self.qRadTemperature.setText(str(self.radTemperature))
		self.qAirSpeed.setText(str(self.airSpeed))
		self.qHumidity.setText(str(self.humidity))
		self.qMetabolicRate.setText(str(self.metabolicRate))
		self.qClothingLevel.setText(str(self.clothingLevel))
		self.qExtWork.setText(str(self.extWork))
		self.qSteamPressure.setText(str(self.steamPressure))
		self.qClothingTemperature.setText(str(self.clothingTemperature))

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
		if self.clothingLevel*0.155 > 0.078:
			f_cl = 1.05+0.645*self.clothingLevel*0.155
		else:
			f_cl = 1+1.29*self.clothingLevel*0.155

		if (2.38*mth.pow(mth.fabs(self.clothingTemperature-self.airTemperature),0.25)) > (12.1*mth.sqrt(self.airSpeed)):
			h_c = 12.1*mth.sqrt(self.airSpeed)
		else:
			h_c = 2.38*mth.pow(mth.fabs(self.clothingTemperature-self.airTemperature),0.25)

		a = 0.303*mth.exp(-0.036*self.metabolicRate*58)+0.028
		b = (self.metabolicRate*58-self.extWork)-0.00305*(5773-6.99*(self.metabolicRate*58-self.extWork)-self.steamPressure)-0.42*((self.metabolicRate*58-self.extWork)-58.15)
		c = -1.7*mth.pow(10,-5)*self.metabolicRate*58*(5867-self.steamPressure)-0.0014*self.metabolicRate*58*(34-self.airTemperature)
		d = -3.96*mth.pow(10,-8)*f_cl*(mth.pow((self.clothingTemperature+273),4)-mth.pow((self.radTemperature+273),4)) - f_cl*h_c*(self.clothingTemperature-self.radTemperature)
		pmv = a*(b+c+d)	# tu wstawić wzór
		self.pmv = pmv
		res = str(pmv)
		return res

	# Tutaj będzie liczone PPD
	def calculatePPD(self):
		ppd = mth.fabs(1-95*mth.exp(-0.03353*mth.pow(self.pmv,4)-0.2179*mth.pow(self.pmv,2)))	# tu wstawić wzór
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
		self.qMetaRateList = QComboBox()
		self.initMetabolicRateElementList()
		self.qMetabolicRate.setAlignment(Qt.AlignCenter)
		qValMetabolicRate = QDoubleValidator(0.0, 30.0, 2)
		qValMetabolicRate.setNotation(QDoubleValidator.StandardNotation)
		qValMetabolicRate.setLocale(locale)
		self.qMetabolicRate.setValidator(qValMetabolicRate)
		
		self.qClothingLevel = QLineEdit()
		self.qCloLevelList = QComboBox()
		self.initClothingLevelElementList()
		self.qClothingLevel.setAlignment(Qt.AlignCenter)
		qValClothingLevel = QDoubleValidator(0.0, 30.0, 2)
		qValClothingLevel.setNotation(QDoubleValidator.StandardNotation)
		qValClothingLevel.setLocale(locale)
		self.qClothingLevel.setValidator(qValClothingLevel)

		self.qExtWork = QLineEdit()
		self.qExtWork.setAlignment(Qt.AlignCenter)
		self.qExtWork.setValidator(QIntValidator(0, 500, self))

		self.qSteamPressure = QLineEdit()
		self.qSteamPressure.setAlignment(Qt.AlignCenter)
		self.qSteamPressure.setValidator(QIntValidator(100, 3000, self))

		self.qClothingTemperature = QLineEdit()
		self.qClothingTemperature.setAlignment(Qt.AlignCenter)
		qCloTemperature = QDoubleValidator(0, 100.0, 2)
		qCloTemperature.setNotation(QDoubleValidator.StandardNotation)
		qCloTemperature.setLocale(locale)
		self.qClothingTemperature.setValidator(qCloTemperature)

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
		layout.addWidget(self.qMetaRateList,4,3)
=======
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
    # praca zewnętrzna
    extWork = 50
    #ciśnienie cząsteczkowe pary wodnej
    steamPressure = 1000 #[Pa], 1 hPa na biegunach, 20-30 hPa na równiku
    #temperatura powierzchnii odzieży
    clothingTemperature = 15.0

    ## wyniki
    # PMV - współczynnik komfortu (PMV = (0.303 e^(-0.036metabolicRate^ + 0.028) clothingLevel  )
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

    # Ustawia pracę zewnetrzna
    def setExtWork(self):
        self.extWork = int(self.qExtWork.text())
        self.calculateParams()

    # Ustawia ciśnienie cząsteczkowe pary wodnej
    def setSteamPressure(self):
        self.steamPressure = int(self.qSteamPressure.text())
        self.calculateParams()

    # Ustawia temperaturę powietrza
    def setClothingTemperature(self):
        try:
            self.clothingTemperature = float(self.qClothingTemperature.text().replace(",", "."))
        except:
            self.clothingTemperature = 0.0
        self.calculateParams()

        
	
    # Zapis wartości ze zmiennych do pól tekstowych - może się przyda
    def getValues(self):
        self.qAirTemperature.setText(str(self.airTemperature))
        self.qRadTemperature.setText(str(self.radTemperature))
        self.qAirSpeed.setText(str(self.airSpeed))
        self.qHumidity.setText(str(self.humidity))
        self.qMetabolicRate.setText(str(self.metabolicRate))
        self.qClothingLevel.setText(str(self.clothingLevel))
        self.qExtWork.setText(str(self.extWork))
        self.qSteamPressure.setText(str(self.steamPressure))
        self.qClothingTemperature.setText(str(self.clothingTemperature))

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
        if self.clothingLevel*0.155 > 0.078:
            f_cl = 1.05+0.645*self.clothingLevel*0.155
        else:
            f_cl = 1+1.29*self.clothingLevel*0.155

        if (2.38*mth.pow(mth.fabs(self.clothingTemperature-self.airTemperature),0.25)) > (12.1*mth.sqrt(self.airSpeed)):
            h_c = 12.1*mth.sqrt(self.airSpeed)
        else:
            h_c = 2.38*mth.pow(mth.fabs(self.clothingTemperature-self.airTemperature),0.25)

        a = 0.303*mth.exp(-0.036*self.metabolicRate*58)+0.028
        b = (self.metabolicRate*58-self.extWork)-0.00305*(5773-6.99*(self.metabolicRate*58-self.extWork)-self.steamPressure)-0.42*((self.metabolicRate*58-self.extWork)-58.15)
        c = -1.7*mth.pow(10,-5)*self.metabolicRate*58*(5867-self.steamPressure)-0.0014*self.metabolicRate*58*(34-self.airTemperature)
        d = -3.96*mth.pow(10,-8)*f_cl*(mth.pow((self.clothingTemperature+273),4)-mth.pow((self.radTemperature+273),4)) - f_cl*h_c*(self.clothingTemperature-self.radTemperature)
        pmv = a*(b+c+d)    # tu wstawić wzór
        self.pmv = pmv
        res = str(pmv)
        return res

    # Tutaj będzie liczone PPD
    def calculatePPD(self):
        ppd = mth.fabs(1-95*mth.exp(-0.03353*mth.pow(self.pmv,4)-0.2179*mth.pow(self.pmv,2)))    # tu wstawić wzór
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

        self.qExtWork = QLineEdit()
        self.qExtWork.setAlignment(Qt.AlignCenter)
        self.qExtWork.setValidator(QIntValidator(0, 500, self))

        self.qSteamPressure = QLineEdit()
        self.qSteamPressure.setAlignment(Qt.AlignCenter)
        self.qSteamPressure.setValidator(QIntValidator(100, 3000, self))

        self.qClothingTemperature = QLineEdit()
        self.qClothingTemperature.setAlignment(Qt.AlignCenter)
        qCloTemperature = QDoubleValidator(0, 100.0, 2)
        qCloTemperature.setNotation(QDoubleValidator.StandardNotation)
        qCloTemperature.setLocale(locale)
        self.qClothingTemperature.setValidator(qCloTemperature)

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

        layout.addWidget(QLabel("Praca zewnętrzna"),6,0)
        layout.addWidget(self.qExtWork,6,1)
        layout.addWidget(QLabel("[W/m2]"),6,2)

        layout.addWidget(QLabel("Ciśnienie cząsteczkowe pary wodnej"),7,0)
        layout.addWidget(self.qSteamPressure,7,1)
        layout.addWidget(QLabel("[Pa]"),7,2)

        layout.addWidget(QLabel("Temperatura powierzchni odzieży"),8,0)
        layout.addWidget(self.qClothingTemperature,8,1)
        layout.addWidget(QLabel("[°C]"),8,2)

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
        self.qExtWork.setText(str(self.extWork))
        self.qSteamPressure.setText(str(self.steamPressure))
        self.qClothingTemperature.setText(str(self.clothingTemperature))
>>>>>>> 7b30cf9188ac020dd5b9a59aee1948814f8feff7
		
		layout.addWidget(QLabel("Współcznynnik ubioru"),5,0)
		layout.addWidget(self.qClothingLevel,5,1)
		layout.addWidget(QLabel("[clo]"),5,2)
		layout.addWidget(self.qCloLevelList,5,3)

		layout.addWidget(QLabel("Praca zewnętrzna"),6,0)
		layout.addWidget(self.qExtWork,6,1)
		layout.addWidget(QLabel("[W/m2]"),6,2)

		layout.addWidget(QLabel("Ciśnienie cząsteczkowe pary wodnej"),7,0)
		layout.addWidget(self.qSteamPressure,7,1)
		layout.addWidget(QLabel("[Pa]"),7,2)

		layout.addWidget(QLabel("Temperatura powierzchni odzieży"),8,0)
		layout.addWidget(self.qClothingTemperature,8,1)
		layout.addWidget(QLabel("[°C]"),8,2)

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
		self.qExtWork.setText(str(self.extWork))
		self.qSteamPressure.setText(str(self.steamPressure))
		self.qClothingTemperature.setText(str(self.clothingTemperature))
		
		## Łączenie zmiennych przechowujących wartości z polami tekstowymi
		self.qAirTemperature.textChanged.connect(self.setAirTemperature)
		self.qAirTemperature.editingFinished.connect(self.getValues)

		self.qRadTemperature.textChanged.connect(self.setRadTemperature)
		self.qRadTemperature.editingFinished.connect(self.getValues)

		self.qAirSpeed.textChanged.connect(self.setAirSpeed)
		self.qAirSpeed.editingFinished.connect(self.getValues)

		self.qHumidity.textChanged.connect(self.setHumidity)
		self.qHumidity.editingFinished.connect(self.getValues)

		self.qMetabolicRate.textChanged.connect(self.setMetabolicRate)
		self.qMetabolicRate.editingFinished.connect(self.getValues)
		self.qMetaRateList.currentTextChanged.connect(self.getMetaRateFromList)
		
		self.qClothingLevel.textChanged.connect(self.setClothingLevel)
		self.qClothingLevel.editingFinished.connect(self.getValues)
		self.qCloLevelList.currentTextChanged.connect(self.getCloLevelFromList)

		self.qExtWork.textChanged.connect(self.setExtWork)
		self.qExtWork.editingFinished.connect(self.getValues)

		self.qSteamPressure.textChanged.connect(self.setSteamPressure)
		self.qSteamPressure.editingFinished.connect(self.getValues)

<<<<<<< HEAD
		self.qClothingTemperature.textChanged.connect(self.setClothingTemperature)
		self.qClothingTemperature.editingFinished.connect(self.getValues)
		
		self.horizontalGroupBox.setLayout(layout)
		self.horizontalGroupBoxResults.setLayout(layoutRes)
=======
        self.qExtWork.textChanged.connect(self.setExtWork)
        self.qExtWork.editingFinished.connect(self.getValues)

        self.qSteamPressure.textChanged.connect(self.setSteamPressure)
        self.qSteamPressure.editingFinished.connect(self.getValues)

        self.qClothingTemperature.textChanged.connect(self.setClothingTemperature)
        self.qClothingTemperature.editingFinished.connect(self.getValues)

        
        self.horizontalGroupBox.setLayout(layout)
        self.horizontalGroupBoxResults.setLayout(layoutRes)
>>>>>>> 7b30cf9188ac020dd5b9a59aee1948814f8feff7

if __name__ == '__main__':
	app = QApplication(sys.argv)
ex = App()
sys.exit(app.exec_())
