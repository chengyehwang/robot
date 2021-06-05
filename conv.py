import cv2
import numpy as np 
img = cv2.imread('image.jpg')  #read image from system
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)  #Convert to grayscale image
edged = cv2.Canny(gray, 170, 255)            #Determine edges of objects in an image
ret,thresh = cv2.threshold(gray,240,255,cv2.THRESH_BINARY)  
(contours,_) = cv2.findContours(edged,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) #Find contours in an image
def detectShape(c):          #Function to determine type of polygon on basis of number of sides
       shape = 'unknown' 
       peri=cv2.arcLength(cnt,True) 
       vertices = cv2.approxPolyDP(cnt, 0.02 * peri, True)
       return vertices
print("""
$x
$h
G92 X0Y0Z0
G01 X50Y-200F10000
G92 X0Y0Z0
G90
""")
for cnt in contours:
    shape=detectShape(cnt)
    for i in range(len(shape)):
        print("G01 X%dY%dF1000"%(shape[i][0][0]/4,shape[i][0][1]/4))
        if i ==0:
            print("G01 Z-22F1000")
    print("G01 X%dY%dF1000"%(shape[0][0][0]/4,shape[0][0][1]/4))
    print("G01 Z0F1000")
    print("\n")        
print("""
G01 X0Y0F1000
G01 Z0F1000
""")
