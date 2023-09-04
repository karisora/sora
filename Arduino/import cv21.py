import cv2
import numpy as np
import glob

# color definition
RED   = 1
GREEN = 2
BLUE  = 3

def find_rect_of_target_color(image, color_type):
  hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV_FULL)
  h = hsv[:, :, 0]
  s = hsv[:, :, 1]

  # red detection
  if color_type == RED:
    mask = np.zeros(h.shape, dtype=np.uint8)
    mask[((h < 20) | (h > 200)) & (s > 128)] = 255

  # blue detection
  if color_type == BLUE:
    lower_blue = np.array([130, 50, 50])
    upper_blue = np.array([200, 255, 255])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

  # green detection
  if color_type == GREEN:
    lower_green = np.array([75, 50, 50])
    upper_green = np.array([110, 255, 255])
    mask = cv2.inRange(hsv, lower_green, upper_green)

  # 近傍の定義
  neiborhood = np.array([[0, 1, 0],
                         [1, 1, 1],
                         [0, 1, 0]],
                        np.uint8)
  # 収縮
  mask = cv2.dilate(mask,
                    neiborhood,
                    iterations=2)

  # 膨張
  mask = cv2.erode(mask,
                   neiborhood,
                   iterations=2)

  contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  rects = []
  for contour in contours:
    approx = cv2.convexHull(contour)
    rect = cv2.boundingRect(approx)
    rects.append(np.array(rect))
  return rects


if __name__ == "__main__":

  count = 0
  files = glob.glob(r"C:\Users\taiso\Documents\nakazesougen-7.jpg")
  for f in files:

    count += 1
    count_padded = '%05d' % count

    while cv2.waitKey(30) < 0:

      frame = cv2.imread(f)

      # red
      rects = find_rect_of_target_color(frame, RED)
      if len(rects) > 0:
        rect = max(rects, key=(lambda x: x[2] * x[3]))
        if rect[3] > 10: # if red circle is one
          cv2.rectangle(frame, tuple(rect[0:2]), tuple(rect[0:2] + rect[2:4]), (0, 0, 255), thickness=2)
      #for rect in rects:
      #  cv2.rectangle(frame, tuple(rect[0:2]), tuple(rect[0:2] + rect[2:4]), (0, 0, 255), thickness=2)

      # green
      rects = find_rect_of_target_color(frame, GREEN)
      if len(rects) > 0:
        rect = max(rects, key=(lambda x: x[2] * x[3]))
        if rect[3] > 10:
         cv2.rectangle(frame, tuple(rect[0:2]), tuple(rect[0:2] + rect[2:4]), (0, 255, 0), thickness=2)
      #for rect in rects:      
      #  cv2.rectangle(frame, tuple(rect[0:2]), tuple(rect[0:2] + rect[2:4]), (0, 255, 0), thickness=2)

      # blue
      rects = find_rect_of_target_color(frame, BLUE)
      if len(rects) > 0:
        rect = max(rects, key=(lambda x: x[2] * x[3]))
        if rect[3] > 10:
          cv2.rectangle(frame, tuple(rect[0:2]), tuple(rect[0:2] + rect[2:4]), (255, 0, 0), thickness=2)
      #for rect in rects:
      #  cv2.rectangle(frame, tuple(rect[0:2]), tuple(rect[0:2] + rect[2:4]), (255, 0, 0), thickness=2)

      cv2.imshow('frame', frame)
      write_file_name = count_padded + ".png"
      cv2.imwrite(write_file_name, frame)

cv2.destroyAllWindows()