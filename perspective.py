import numpy as np
import cv2

points=[]
i=0
cpy=np.array(())
im1=np.array(())
#polygon drawer


def poly(pts):
    #pts=np.array(pts)
    #print('poly')
    global im1,cpy
    im1=cpy.copy()
    #pts=pts.tolist()#.reshape((-1,1,2))
    #print(pts)
    for pt in pts:
        cv2.circle(im1, tuple(pt), 4, (255,0,0),-1)

#point setting(to be optimised)
def point(lst):
    #print('point')
    global points
    dis=[]
    for pt in points:
        d=pow(pow(pt[0]-lst[0],2)+pow(pt[1]-lst[1],2),0.5)
        dis.append(d)
    m=min(dis)
    i=dis.index(m)
    points.pop(i)
    points.insert(i,lst)
    poly(points)

#points arranger
def arg(pts):
    #print('arg')
    x=sorted(pts)
    if x[0][1]>x[1][1]:
        x[1],x[0]=x[0],x[1]
    if x[2][1]>x[3][1]:
        x[2],x[3]=x[3],x[2]

    r=(x[2][0]+x[3][0]-x[0][0]-x[1][0])/2
    c=(x[3][1]+x[1][1]-x[2][1]-x[0][1])/2
    return x,int(r),int(c)


#read function
def read(event,x,y,flags,param):
    if event==cv2.EVENT_LBUTTONDOWN:
        point([x,y])

#image display and mouse invoking
def per(im,pts):
    #print('per')
    global cpy,im1,points
    points=[]
    points.extend(pts)
    im1=im.copy()
    cpy=im1.copy()
    poly(pts)
    cv2.imshow('Image',im1)
    #cv2.waitKey(0)
    cv2.setMouseCallback('Image',read)
    while(True):
        cv2.imshow('Image',im1)
        if cv2.waitKey(1)==13:
            break


#adjusting perception
    im1=cpy.copy()
    pts1,rnew,cnew=arg(points)
    pts2=np.float32([[0,0],[0,cnew],[rnew,0],[rnew,cnew]])
    M=cv2.getPerspectiveTransform(np.float32(pts1),pts2)
    dst = cv2.warpPerspective(im1,M,(rnew,cnew))
    #cv2.destroyWindow('Image')
    return dst,pts1
