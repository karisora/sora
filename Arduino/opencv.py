import cv2
import numpy as np

corn_pic = r"C:\Users\taiso\Documents\nakazesougen-7.jpg"

img = cv2.imread(corn_pic, cv2.IMREAD_COLOR)

height, width = img.shape[:2]

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV_FULL)
h = hsv[:,:,0]
s = hsv[:,:,1]
v = hsv[:,:,2]

img_corn = np.zeros((height,width,3), np.uint8)

img_corn[(h <= 10) & (h >= 0) & (150 < h) & (h < 180) & (s >= 127) & (s <= 255) & (v > 100)] = 255

img_gray = cv2.imread(corn_pic, cv2.IMREAD_GRAYSCALE)
M = cv2.moments(img_gray, False)
contours, hierarchy= cv2.findContours(img_gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
x,y= int(M["m10"]/M["m00"]) , int(M["m01"]/M["m00"])
cv2.circle(img, (x,y), 20, 100, 2, 4)
cv2.drawContours(img, contours, -1, color=(0, 0, 0), thickness=5)
print(x,y)                    #求めたカラーコーンの色の重心のピクセル座標
cv2.imshow('img',img)
cv2.waitKey(0)