import numpy as np
import cv2

def d_page(page):

    gray=cv2.cvtColor(page,cv2.COLOR_BGR2GRAY)
    edge=cv2.Canny(gray,75,200)
    #cv2.imshow('edge',edge)
    cont,hei=cv2.findContours(edge,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    cnt=sorted(cont, key=cv2.contourArea, reverse=True)[:5]
    c=0
    for i in cnt:
        
        per=cv2.arcLength(i,True)
        approx=cv2.approxPolyDP(i,0.02*per,True)

        if len(approx)==4:
            c=1
            return approx
    if c==0:
        approx=np.array([[10,10],[10,gray.shape[0]-10],[gray.shape[1]-10,gray.shape[0]-10],[gray.shape[1]-10,10]])
        return approx

