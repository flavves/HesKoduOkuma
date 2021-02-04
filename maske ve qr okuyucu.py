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























def detect_and_predict_mask(frame, faceNet, maskNet):
	# grab the dimensions of the frame and then construct a blob
	# from it
	(h, w) = frame.shape[:2]
	blob = cv2.dnn.blobFromImage(frame, 1.0, (224, 224),
		(104.0, 177.0, 123.0))

	# pass the blob through the network and obtain the face detections
	faceNet.setInput(blob)
	detections = faceNet.forward()
	#print(detections.shape)

	# initialize our list of faces, their corresponding locations,
	# and the list of predictions from our face mask network
	faces = []
	locs = []
	preds = []

	# loop over the detections
	for i in range(0, detections.shape[2]):
		# extract the confidence (i.e., probability) associated with
		# the detection
		confidence = detections[0, 0, i, 2]

		# filter out weak detections by ensuring the confidence is
		# greater than the minimum confidence
		if confidence > 0.5:
			# compute the (x, y)-coordinates of the bounding box for
			# the object
			box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
			(startX, startY, endX, endY) = box.astype("int")

			# ensure the bounding boxes fall within the dimensions of
			# the frame
			(startX, startY) = (max(0, startX), max(0, startY))
			(endX, endY) = (min(w - 1, endX), min(h - 1, endY))

			# extract the face ROI, convert it from BGR to RGB channel
			# ordering, resize it to 224x224, and preprocess it
			face = frame[startY:endY, startX:endX]
			face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
			face = cv2.resize(face, (224, 224))
			face = img_to_array(face)
			face = preprocess_input(face)

			# add the face and bounding boxes to their respective
			# lists
			faces.append(face)
			locs.append((startX, startY, endX, endY))

	# only make a predictions if at least one face was detected
	if len(faces) > 0:
		# for faster inference we'll make batch predictions on *all*
		# faces at the same time rather than one-by-one predictions
		# in the above `for` loop
		faces = np.array(faces, dtype="float32")
		preds = maskNet.predict(faces, batch_size=32)

	# return a 2-tuple of the face locations and their corresponding
	# locations
	return (locs, preds)

# load our serialized face detector model from disk
prototxtPath = r"face_detector\deploy.prototxt"
weightsPath = r"face_detector\res10_300x300_ssd_iter_140000.caffemodel"
faceNet = cv2.dnn.readNet(prototxtPath, weightsPath)

# load the face mask detector model from disk
maskNet = load_model("mask_detector.model")

# initialize the video stream
print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
global maske,qr,sonuc,tc
maske="once maskeni tak"
qr="qr kodu okut"
sonuc="Sonuc"
tc="Tc"

font = cv2.FONT_HERSHEY_PLAIN

while True:
    frame = vs.read()
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
    #frame için yazı
    
    cv2.putText(frame, str(maske), (0, 150), font, 2,(255, 255, 255), 2)
    cv2.putText(frame, str(qr), (0, 250), font, 2,(255, 255, 255), 2)
    cv2.putText(frame, str(tc), (0, 350), font, 2,(255, 255, 255), 2)
    cv2.putText(frame, str(sonuc), (0, 450), font, 2,(0, 0, 255), 2)
    #Deneme= cv2.imread("siyah.png")
    
    
    
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
            #cv2.imwrite("frame.jpg", frame)
            
            #cv2.imwrite("frame.jpg", frame) 
            cv2.putText(frame, str(maske), (0, 150), font, 2,(255, 255, 255), 2)
            for obj in decodedObjects:               
                print("Data", obj.data)
                Hes1=obj.data
                Hes1=str(Hes1)
                Hes1=Hes1.split("|")
                Hes_tc=Hes1[0]
                Hes_tc=Hes_tc[2:]
                Hes_kod=Hes1[1]
                Hes_kod=Hes_kod[0:10]
                print("[+] tc: %s | kod= %s"% (Hes_tc,Hes_kod))
                
                
                qr=Hes_kod
                tc=Hes_tc
                cv2.putText(frame, str(qr), (0, 250), font, 2,(255, 255, 255), 2)
                cv2.putText(frame, str(tc), (0, 350), font, 2,(255, 255, 255), 2)
            
        
        
        
        
    #cv2.imshow("maskeliler", Deneme)
    cv2.imshow("frame",frame)
    key= cv2.waitKey(1) & 0xFF
    
    if key == ord("q"):
        break
cv2.destroyAllWindows()
vs.stop()











