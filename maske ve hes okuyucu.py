# -*- coding: utf-8 -*-
"""
Created on Fri Oct 30 20:20:43 2020

@author: yazılım
"""


from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
from imutils.video import VideoStream
import numpy as np
import imutils
import time
import cv2
import os

#benim kodlar
import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar

import selenium
from  selenium import webdriver
import time

#hes kodum

global TC,sifre
TC=""
sifre=""


driver_path = "chromedriver"
#tarayıcıyı açıyoruz

browser = webdriver.Chrome(executable_path=driver_path)
#boyut değiştirdim

#e devlet girişi
browser.get("https://giris.turkiye.gov.tr/Giris/gir")
time.sleep(1)
#tc no yazma
browser.find_element_by_xpath('//*[@id="tridField"]').send_keys(TC)

            #şifre yazma
browser.find_element_by_xpath('//*[@id="egpField"]').send_keys("sifre")

kod_okudum_qr=""
try:
    time.sleep(1)
    browser.find_element_by_xpath('//*[@id="loginForm"]/div[2]/input[4]').click()
except:
    time.sleep(1)
    browser.find_element_by_xpath('//*[@id="loginForm"]/div[2]/input[4]').click()
global sayac
global Hes_kod
global Hes_tc
global Ekran_Yazisi
global Ekran_Yazisi_tc
Ekran_Yazisi="Hes okut"
Ekran_Yazisi_tc=""
cap = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_PLAIN
decodedObjects=""
obj=""
adam=False
Hes_tc=""
Hes_kod=""
sayac=""
bakayim_mi=""
Ekran_Yazisi_tc_deneme=""




















def detect_and_predict_mask(frame, faceNet, maskNet):

	(h, w) = frame.shape[:2]
	blob = cv2.dnn.blobFromImage(frame, 1.0, (224, 224),
		(104.0, 177.0, 123.0))

	
	faceNet.setInput(blob)
	detections = faceNet.forward()


	faces = []
	locs = []
	preds = []


	for i in range(0, detections.shape[2]):
		
		confidence = detections[0, 0, i, 2]

		if confidence > 0.5:
			
			box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
			(startX, startY, endX, endY) = box.astype("int")

		
			(startX, startY) = (max(0, startX), max(0, startY))
			(endX, endY) = (min(w - 1, endX), min(h - 1, endY))

			
			face = frame[startY:endY, startX:endX]
			face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
			face = cv2.resize(face, (224, 224))
			face = img_to_array(face)
			face = preprocess_input(face)

			
			faces.append(face)
			locs.append((startX, startY, endX, endY))

	if len(faces) > 0:

		faces = np.array(faces, dtype="float32")
		preds = maskNet.predict(faces, batch_size=32)

	
	return (locs, preds)


prototxtPath = r"face_detector\deploy.prototxt"
weightsPath = r"face_detector\res10_300x300_ssd_iter_140000.caffemodel"
faceNet = cv2.dnn.readNet(prototxtPath, weightsPath)


maskNet = load_model("mask_detector.model")


print("[INFO] starting video stream...")

#Kamera kaynağını seçin

vs = VideoStream(src=0).start()
global maske,qr,sonuc,tc
maske="once maskeni tak"
qr="qr kodu okut"
sonuc="Sonuc"
tc="Tc"

font = cv2.FONT_HERSHEY_PLAIN
renk_kod=(255, 255, 255)
while True:
    sayac=0
    adana=""
    frame = vs.read()
    #logomu koyuyorum
    android = cv2.imread("beyaz logo.png")
    android_gri= cv2.cvtColor(android,cv2.COLOR_BGR2GRAY)
    yukseklik,genislik=android_gri.shape
    roi=frame[0:yukseklik,0:genislik]
    ret,mask=cv2.threshold(android_gri,10,255,cv2.THRESH_BINARY)
    mask_inver=cv2.bitwise_not(mask)
    frame_arka= cv2.bitwise_or(roi,roi,mask = mask_inver)
    renkli= cv2.add(frame_arka,android)
    frame[0:yukseklik,0:genislik]=renkli
    
    #frame = imutils.resize(frame, width=400)
    decodedObjects = pyzbar.decode(frame)
    (locs,preds) = detect_and_predict_mask(frame,faceNet,maskNet)
    
    
    #sonuc için güzel yazı
    
    if sonuc == "Riskli Değil":
        print("güvenli 1212")
        sonuc= "Riskli Degil"
        renk_kod=(255, 0, 0)
    try:
        if sonuc !="Riskli Değil":
            sonuc=browser.find_element_by_xpath('//*[@id="contentStart"]/div/dl/dd[3]').text
            if sonuc == "Riskli Değil":
                print("güvenli 105")
                sonuc= "Riskli Degil"
                renk_kod=(255, 0, 0)
    except:
        print("hello 12")
    if sonuc == "Riskli":
        sonuc= "Riskli"
        renk_kod=(0, 0, 255)
    #frame için yazı

    

    cv2.putText(frame, str(maske), (0, 150), font, 2,(255, 255, 255), 2)
    cv2.putText(frame, str(qr), (0, 250), font, 2,(255, 255, 255), 2)
    cv2.putText(frame, str(tc), (0, 350), font, 2,(255, 255, 255), 2)
    cv2.putText(frame, str(sonuc), (0, 450), font, 2,(renk_kod), 2)

    
    
    
    for (box,pred) in zip(locs, preds):
        (startX,startY,endX,endY) = box
        (mask, withoutMask) = pred
        label ="Maskeli" if mask > withoutMask else "maske yok"
        color = (0,255,0) if label == "Maskeli" else (0,0,255)
        label2 = "{}: {:.2f}%".format(label,max(mask,withoutMask) * 100)
        cv2.putText(frame,label2,(startX,startY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.45, color,2)
        cv2.rectangle(frame, (startX,startY),(endX,endY), color,2)
        if label==("maske yok"):
            maske="Maske tak"
            cv2.putText(frame, str(maske), (0, 150), font, 2,(255, 255, 255), 2)
        elif label==("Maskeli"):
            print("maske takıldı")
            maske="Maskeli"
            cv2.putText(frame, str(maske), (0, 150), font, 2,(255, 255, 255), 2)
            for obj in decodedObjects:
                try:
                    print("Data", obj.data)
                    Hes1=obj.data
                    Hes1=str(Hes1)
                    Hes1=Hes1.split("|")
                    Hes_tc=Hes1[0]
                    Hes_tc=Hes_tc[2:]
                    Hes_kod=Hes1[1]
                    Hes_kod=Hes_kod[0:10]
                    print("[+] tc: %s | kod= %s"% (Hes_tc,Hes_kod))
                except :
                    Hes_kod="qr kodu hatali"
                    Hes_tc="qr kodu hatali"
                
                qr=Hes_kod
                tc=Hes_tc
                cv2.putText(frame, str(qr), (0, 250), font, 2,(255, 255, 255), 2)
                cv2.putText(frame, str(tc), (0, 350), font, 2,(255, 255, 255), 2)
                
            for obj in decodedObjects:
    
                print("okudum")
                Hes1=obj.data
                Hes1=str(Hes1)
                Hes1=Hes1.split("|")
                Hes_tc=Hes1[0]
                Hes_tc=Hes_tc[2:]
                Hes_tc=str(Hes_tc)
                if str(Ekran_Yazisi_tc_deneme)==Hes_tc:
                    sayac==0
                else:
                    if len(Hes_tc)==11:
                        sayac=1
                    else:
                        sayac=0
            if sayac ==0:
                bakayim_mi==1
            if sayac == 1:
                for obj in decodedObjects:
                    bakayim_mi==0
                    kod_okudum_qr="dogru"
                    adam=True
                    print("Data", obj.data)
                    Hes1=obj.data
                    Hes1=str(Hes1)
                    Hes1=Hes1.split("|")
                    Hes_tc=Hes1[0]
                    Hes_tc=Hes_tc[2:]
                    Hes_kod=Hes1[1]
                    Hes_kod=Hes_kod[0:10]
                    print("[+] tc: %s | kod= %s"% (Hes_tc,Hes_kod))
                    #selammmmm
                    decodedObjects=""
                    obj=""
                    
                    try:

                        browser.get("https://www.turkiye.gov.tr/saglik-bakanligi-hes-kodu-sorgulama")
    
                        #Hes kodu girişi
                        Hes_kod = Hes_kod
                        Hes_kod= Hes_kod.upper()
                        browser.find_element_by_xpath('//*[@id="hes_kodu"]').send_keys(Hes_kod)
                        print("hes kodu girildi")
                        #sorgula
                        try:
                            time.sleep(1)
                            browser.find_element_by_xpath('//*[@id="contentStart"]/div[3]/form/div/input[1]').click()
                        except:
                            time.sleep(1)
                            browser.find_element_by_xpath('//*[@id="contentStart"]/div[3]/form/div/input[1]').click()
                        #hes doğru mu değil mi?
                        print("sorgula butonuna basıldı")
    
    
                        try:
                            time.sleep(2)
    
                            HesDogruluk=browser.find_element_by_xpath('//*[@id="contentStart"]/div').text
                            print(HesDogruluk)
                            if HesDogruluk == "Girilen HES Kodu geçersizdir.":
                                print("hes geçersiz")
                            elif HesDogruluk != "Girilen HES Kodu geçersizdir.":
                                sonuc=browser.find_element_by_xpath('//*[@id="contentStart"]/div/dl/dd[3]').text
                                tcNo=browser.find_element_by_xpath('//*[@id="contentStart"]/div/dl/dd[1]').text
    
                                if sonuc == "Riskli Değil" :
                                    print("guvenli")
                                    Ekran_Yazisi_tc="tc:"+str(Hes_tc)
                                    Ekran_Yazisi_tc_deneme=str(Hes_tc)
                                    Ekran_Yazisi=("guvenli")
    
                                else:
                                    print("riskli")
                                    Ekran_Yazisi=("riskli")
                                    Ekran_Yazisi_tc="tc:"+str(Hes_tc)
                                    Ekran_Yazisi_tc_deneme=str(Hes_tc)
    
    
                                #sonuc
                        except:
                            print("hes geçersiz (hata 1)")
                            Ekran_Yazisi=("hes geçersiz (hata 1)")
    
    
    
    
    
    
                    except:
                        try:
                            browser.get("https://giris.turkiye.gov.tr/Giris/gir")
                            time.sleep(1)
    
                            #tc no yazma
                            browser.find_element_by_xpath('//*[@id="tridField"]').send_keys(TC)
    
                            #şifre yazma
                            browser.find_element_by_xpath('//*[@id="egpField"]').send_keys("sifre")
    
                            #giriş
    
                            try:
                                time.sleep(1)
                                browser.find_element_by_xpath('//*[@id="loginForm"]/div[2]/input[4]').click()
                            except:
                                time.sleep(1)
                                browser.find_element_by_xpath('//*[@id="loginForm"]/div[2]/input[4]').click()
    
                            #hes sorgulama ekranı
                            browser.get("https://www.turkiye.gov.tr/saglik-bakanligi-hes-kodu-sorgulama")
    
                            #Hes kodu girişi
                            HesKodu = Hes_kod
                            HesKodu= HesKodu.upper()
                            browser.find_element_by_xpath('//*[@id="hes_kodu"]').send_keys(HesKodu)
                            print("hes kodu girildi")
                            #sorgula
                            try:
                                time.sleep(1)
                                browser.find_element_by_xpath('//*[@id="contentStart"]/div[3]/form/div/input[1]').click()
                            except:
                                time.sleep(1)
                                browser.find_element_by_xpath('//*[@id="contentStart"]/div[3]/form/div/input[1]').click()
                            #hes doğru mu değil mi?
                            print("sorgula butonuna basıldı")
    
    
                            try:
                                time.sleep(2)
    
                                HesDogruluk=browser.find_element_by_xpath('//*[@id="contentStart"]/div').text
                                print(HesDogruluk)
                                if HesDogruluk == "Girilen HES Kodu geçersizdir.":
                                    print("hes geçersiz")
                                elif HesDogruluk != "Girilen HES Kodu geçersizdir.":
                                    sonuc=browser.find_element_by_xpath('//*[@id="contentStart"]/div/dl/dd[3]').text
                                    tcNo=browser.find_element_by_xpath('//*[@id="contentStart"]/div/dl/dd[1]').text
    
    
                                    if sonuc == "Riskli Değil" :
                                        print("guvenli")
                                        Ekran_Yazisi_tc="tc:"+str(Hes_tc)
                                        Ekran_Yazisi=("guvenli")
                                        sonuc=Ekran_Yazisi
                                        Ekran_Yazisi_tc_deneme=str(Hes_tc)
    
                                    else:
                                        print("riskli")
                                        Ekran_Yazisi=("riskli")
                                        sonuc=Ekran_Yazisi
                                        Ekran_Yazisi_tc_deneme=str(Hes_tc)
    
    
                                    #sonuc
                            except:
                                print("hes geçersiz (hata 1)")
                                Ekran_Yazisi=("hes geçersiz (hata 1) tekrar deneyin")
                                sonuc=Ekran_Yazisi
    
    
                        except:
                            print("hata 2")
                            Ekran_Yazisi=("hata 2 tekrar deneyin")
                            sonuc=Ekran_Yazisi
                
        
        
        
    cv2.imshow("frame",frame)
    key= cv2.waitKey(1) & 0xFF
    
    if key == ord("q"):
        break
cv2.destroyAllWindows()
vs.stop()












