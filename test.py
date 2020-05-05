import os
import numpy as np
import cv2
import tempfile
from fpdf import FPDF
from perspective import per
import paged

orb=cv2.ORB_create()
def setkp(im1):
    kp=orb.detect(im1,None)
    
    #geting the points
    nodes=[]
    for i in kp:
        nodes.append(i.pt)
    
    #getting index
    nodes=np.array(nodes)
    kp_new=[]
    for i in pts:
        #print(pts)
        dist=np.sum((nodes-i)**2,axis=1)
        kp_new.append(kp[np.argmin(dist)])
    dst1=orb.compute(im1,kp_new)[1]
    return kp_new,dst1


def matcher(dst1,dst2):#,im1,kp_new,img2,kp):
    bf=cv2.BFMatcher(cv2.NORM_HAMMING,crossCheck=True)
    matches=bf.match(dst1,dst2)
    #img=cv2.drawMatches(img1, kp_new, img2, kp, matches, img1.copy())
    #cv2.imshow('img', img)
    mat=[]
    for i in matches:
        mat.append(i.trainIdx)
    for i,o in enumerate(mat):
        mat[i]=kp2[o].pt
    #print(mat)
    mat=np.array(mat,np.uint32)
    pts=mat.tolist()
    return pts


#reading the full folder for images
print(os.getcwd())
loc=input('Type Location of containing folder:')
os.chdir(loc)
print('Current Locaion: '+os.getcwd())

print('Available images: ')
l=os.listdir(os.getcwd())
print(l)
pgd=True
name=[]

for file in l:
    print(file)
    if file.endswith('.jpg')==True:
        name.append(file)

name.sort()
del l,file

out=[]
sizex=[]
sizey=[]
for n in name:
    im1=cv2.imread(loc+'/'+n)
    im1=cv2.resize(im1,(0,0),fx=0.15,fy=0.15)
    bp=im1.copy()
    im1=cv2.GaussianBlur(im1, (5,5), 0)
    if pgd==True:
        img1=im1.copy()
        pts=paged.d_page(im1)
        kp_new,dst1=setkp(im1)
        kp2,dst2=orb.detectAndCompute(im1,None)
        pts=matcher(dst1,dst2)
        pim,pts=per(bp,pts)
        kp_new,dst1=setkp(im1)
        pgd=False
        out.append(pim)
        sizex.append(pim.shape[0])
        sizey.append(pim.shape[1])
        continue
        print('asd')
    if pgd==False:
        kp2,dst2=orb.detectAndCompute(im1,None)
        pts=matcher(dst1,dst2)#img1,kp_new,im1,kp2)
        if len(pts)<4:
            pgd=True
            pts=paged.d_page(im1)
            pts=pts.reshape(-1,2)
            pts=pts.tolist()
        pim,pts=per(bp,pts)
    out.append(pim)
    sizex.append(pim.shape[0])
    sizey.append(pim.shape[1])


with tempfile.TemporaryDirectory() as tempdir:
    os.chdir(tempdir)
    o_name=[]
    for i,img in enumerate(out):
        n='temp'+str(i)+'.jpg'
        print(n,os.getcwd())
        cv2.imwrite(n, img)
        o_name.append(n)
    pdf=FPDF(unit='pt',format=np.array([max(sizey),max(sizex)]))
    for n in o_name:
        pdf.add_page()
        pdf.image(n,0,0,0,0)
    os.chdir('/home/thejus/Documents/Project')
    pdf.output('pd.pdf')
cv2.destroyAllWindows()
