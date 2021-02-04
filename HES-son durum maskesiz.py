# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 12:48:33 2020

@author: yazılım
"""


"""
Hes son durum maskesiz

"""
from pygame import mixer
import pygame
mixer.init()

#benim kodlar
import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar

import imutils
import selenium
from  selenium import webdriver
import time

import time
from datetime import date

#hes kodum
global TC,sifre

TC=""
sifre=""

try:
    
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
    browser.find_element_by_xpath('//*[@id="egpField"]').send_keys(sifre)
    
    kod_okudum_qr=""
    try:
        time.sleep(1)
        browser.find_element_by_xpath('//*[@id="loginForm"]/div[2]/input[4]').click()
    except:
        time.sleep(1)
        browser.find_element_by_xpath('//*[@id="loginForm"]/div[2]/input[4]').click()
except:
    print("internet yok")
    pass
fps = 30
frame_width = 640
frame_height = 480


global sayac
global Hes_kod
global Hes_tc
global Ekran_Yazisi
global Ekran_Yazisi_tc
Ekran_Yazisi="Hes okut"
Ekran_Yazisi_tc=""
cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)
cap.set(cv2.CAP_PROP_FPS, fps)

font = cv2.FONT_HERSHEY_PLAIN
decodedObjects=""
obj=""
adam=False
Hes_tc=""
Hes_kod=""
sayac=""
bakayim_mi=""
Ekran_Yazisi_tc_deneme=""



global maske,qr,sonuc,tc,KisiSayici
maske="MASKE TAK"
qr="qr kodu okut"
sonuc="Sonuc"
tc="Tc"
KisiSayici=0
KisiSayiciYazi=""

font = cv2.FONT_HERSHEY_PLAIN
renk_kod=(0, 91, 255)
sureye_bak=0
log_sayac=0
while True:
    sayac=0
    adana=""
    _, frame = cap.read()
    frame = imutils.resize(frame, width=1000)
    
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

    try:
        
        sonuc=browser.find_element_by_xpath('//*[@id="contentStart"]/div/dl/dd[4]').text
        tc=sonuc=browser.find_element_by_xpath('//*[@id="contentStart"]/div/dl/dd[2]').text
    except:
        pass

    #sonuc için güzel yazı

    if sonuc == "Riskli Değil":
        
        sonuc= "Riskli Degil"
        renk_kod=(0, 255, 0)

    try:
        if sonuc !="Riskli Değil":
            sonuc=browser.find_element_by_xpath('//*[@id="contentStart"]/div/dl/dd[4]').text
            if sonuc == "Riskli Değil":
                
                sonuc= "Riskli Degil"
                renk_kod=(0, 255, 0)

    except:
        pass
    if sonuc == "Riskli":
        sonuc= "Riskli"
        renk_kod=(0, 0, 255)

    #frame için yazı
    


    cv2.putText(frame, str(maske), (0, 150), font, 2,(0, 91, 255), 2)
    cv2.putText(frame, str(qr), (0, 250), font, 2,(0, 91, 255), 2)
    cv2.putText(frame, str(tc), (0, 350), font, 2,(0, 91, 255), 2)
    cv2.putText(frame, str(sonuc), (0, 450), font, 2,(renk_kod), 2)
    cv2.putText(frame, str(KisiSayiciYazi), (0, 550), font, 2,(0, 91, 255), 2)
    
    
    time.localtime()
        
    zaman_ayarlama=time.localtime()
    zaman_ayarlama[4]
    gosterge_dakika=str(zaman_ayarlama[4])
        
    gosterge_dakika=int(gosterge_dakika)
    
        
    if sureye_bak==0:
        sureye_bak=1
        
        gosterge_dakika_kontrol=gosterge_dakika+5
        
    if gosterge_dakika_kontrol==gosterge_dakika:
        sureye_bak=0
        print("oldu")
        try:

                        browser.get("https://www.turkiye.gov.tr/saglik-bakanligi-hes-kodu-sorgulama")

                        #Hes kodu girişi
                        Hes_kod = Hes_kod
                        Hes_kod= Hes_kod.upper()
                        browser.find_element_by_xpath('//*[@id="hes_kodu"]')
        except:
            try:
                            browser.get("https://giris.turkiye.gov.tr/Giris/gir")
                            time.sleep(1)

                            #tc no yazma
                            browser.find_element_by_xpath('//*[@id="tridField"]').send_keys(TC)

                            #şifre yazma
                            browser.find_element_by_xpath('//*[@id="egpField"]').send_keys(sifre)

                            #giriş

                            try:
                                time.sleep(1)
                                browser.find_element_by_xpath('//*[@id="loginForm"]/div[2]/input[4]').click()
                            except:
                                time.sleep(1)
                                browser.find_element_by_xpath('//*[@id="loginForm"]/div[2]/input[4]').click()
            except:
                print("Süreye baglı durumda giris yapamadım")
                pass

    

    for obj in decodedObjects:
                pygame.mixer.music.load("kod_okuma.wav")
                pygame.mixer.music.play()
                print("hello")
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
        try:
        
                print("okudum")
                Hes1=obj.data
                Hes1=str(Hes1)
                Hes1=Hes1.split("|")
                Hes_tc=Hes1[0]
                Hes_tc=Hes_tc[2:]
                Hes_tc=str(Hes_tc)
                Hes_kod=Hes1[1]
                Hes_kod=Hes_kod[0:10]
                Hes_kod=str(Hes_kod)
                print("kontrolculer")
                print(Hes_kod)
                print(Hes_tc)
                if str(Ekran_Yazisi_tc_deneme)==Hes_tc:
                    print(Ekran_Yazisi_tc_deneme)
                    sayac==0
                else:
                    if len(Hes_tc)==32:
                        sayac=1
                    else:
                        sayac=0
        except:
            Hes_kod=""
            Hes_tc=""
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
                    log_bilgisi=("[+] tc: %s | kod= %s"% (Hes_tc,Hes_kod))
                    #selammmmm
                    decodedObjects=""
                    obj=""
                    KisiSayici=int(KisiSayici)
                    KisiSayici=KisiSayici+1
                    KisiSayici=str(KisiSayici)
                    KisiSayiciYazi=("giris sayisi: "+KisiSayici)
                    
                    #Giriş loglama
                    with open("log.txt", "a") as dosya:
                        dosya.write(str(log_sayac))
                        dosya.write(" ")
                        dosya.write(str(log_bilgisi))
                        dosya.write("\n")
                        log_sayac=log_sayac+1
                    dosya.close()

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
                                sonuc=browser.find_element_by_xpath('//*[@id="contentStart"]/div/dl/dd[4]').text
                                
                                tcNo=browser.find_element_by_xpath('//*[@id="contentStart"]/div/dl/dd[2]').text

                                if sonuc == "Riskli Değil" :
                                    print("guvenli")
                                    Ekran_Yazisi_tc="tc:"+str(Hes_tc)
                                    Ekran_Yazisi_tc_deneme=str(tcNo)
                                    Ekran_Yazisi=("guvenli")
                                    pygame.mixer.music.load("dogru.wav")
                                    pygame.mixer.music.play()

                                else:
                                    print("riskli")
                                    Ekran_Yazisi=("riskli")
                                    Ekran_Yazisi_tc="tc:"+str(Hes_tc)
                                    Ekran_Yazisi_tc_deneme=str(tcNo)
                                    pygame.mixer.music.load("riskli.wav")
                                    pygame.mixer.music.play()


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
                            browser.find_element_by_xpath('//*[@id="egpField"]').send_keys(sifre)

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
                                        pygame.mixer.music.load("dogru.wav")
                                        pygame.mixer.music.play()

                                    else:
                                        print("riskli")
                                        Ekran_Yazisi=("riskli")
                                        sonuc=Ekran_Yazisi
                                        Ekran_Yazisi_tc_deneme=str(Hes_tc)
                                        pygame.mixer.music.load("riskli.wav")
                                        pygame.mixer.music.play()


                                    #sonuc
                            except:
                                print("hes geçersiz (hata 1)")
                                Ekran_Yazisi=("hes geçersiz (hata 1) tekrar deneyin")
                                sonuc=Ekran_Yazisi


                        except:
                            print("hata 2")
                            Ekran_Yazisi=("hata 2 tekrar deneyin")
                            sonuc=Ekran_Yazisi




    cv2.imshow("Hes kodu okuyucu",frame)
    key= cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break
cv2.destroyAllWindows()
cap.stop()