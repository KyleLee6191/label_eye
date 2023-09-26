import os
import cv2
import numpy as np

image_path = r"D:\BaiduNetdiskDownload\human3.6mtoolboxprocessed\images\s_01_act_02_subact_01_ca_02"

label_path = r"D:\1LZH\杂物\新建文件夹\label"
dirs = os.listdir(image_path)

def draw_point(img, point, flag, number = 0):
    if flag == 2:
        if number > 0:
            cv2.putText(image, str(number), point, cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 0, 0), 2)
        cv2.circle(img, point, 2, (255, 0, 0), 2)
    elif flag == 1:
        if number > 0:
            cv2.putText(image, str(number), point, cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
        cv2.circle(image, point, 2, (0, 255, 0), 2)
    elif flag == 0:
        if number > 0:
            cv2.putText(image, str(number), point, cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
        cv2.circle(image, point, 2, (0, 0, 255), 2)

    return img

def draw_box(img, p1, p2, label):
    if label == 'l':
        cv2.rectangle(image, p1, p2, (255, 0, 0), thickness=2)
    elif label == 'r':
        cv2.rectangle(image, p1, p2, (0, 255, 0), thickness=2)
    return img


global point1
def on_mouse(event, x, y, flags, param):
    global point1
    image2 = image.copy()
    if event == cv2.EVENT_LBUTTONDOWN:  # 左键点击
        # print("1-EVENT_LBUTTONDOWN")
        point1 = (x, y)
    elif event == cv2.EVENT_MOUSEMOVE and (flags & cv2.EVENT_FLAG_LBUTTON):  # 按住左键拖曳画框
        #print("2-EVENT_FLAG_LBUTTON")
        point2 = (x, y)
        cv2.rectangle(image2, point1, point2, (255, 0, 0), thickness=2)
        cv2.imshow(window_name, image2)
    elif event == cv2.EVENT_LBUTTONUP:  # 左键释放，标可见点或左眼框
        point2 = (x, y)
        if point2 == point1 or np.abs(point2[0] - point1[0]) < 50 or np.abs(point2[1] - point1[1]) < 50:            # 点
            points.append((2, point1))
            # print(str(count) + ' ' +str(point1))
            # print(points)
            draw_point(image, point1, 2, points.__len__())
            cv2.imshow(window_name, image)
        if point1 != point2 and np.abs(point2[0] - point1[0]) > 50 and np.abs(point2[1] - point1[1]) > 50:            # 框
            boxes.append(('l', (point1, point2)))
            draw_box(image, point1, point2, 'l')
            cv2.imshow(window_name, image)

    elif event == cv2.EVENT_RBUTTONDOWN:  # 右键点击
        # print("1-EVENT_LBUTTONDOWN")
        point1 = (x, y)
    elif event == cv2.EVENT_MOUSEMOVE and (flags & cv2.EVENT_FLAG_RBUTTON):  # 按住右键拖曳画框
        # print("2-EVENT_FLAG_LBUTTON")
        point2 = (x, y)
        cv2.rectangle(image2, point1, point2, (0, 255, 0), thickness=2)
        cv2.imshow(window_name, image2)
    elif event == cv2.EVENT_RBUTTONUP:  # 右键释放标隐藏点和右眼框
        point2 = (x, y)
        if point2 == point1 or np.abs(point2[0] - point1[0]) < 50 or np.abs(point2[1] - point1[1]) < 50:
            points.append((1, point1))
            # print(str(count) + ' ' +str(point1))
            # print(points)
            draw_point(image, point1, 1, points.__len__())
            cv2.imshow(window_name, image)
        if point1 != point2 and np.abs(point2[0] - point1[0]) > 50 and np.abs(point2[1] - point1[1]) > 50:
            boxes.append(('r', (point1, point2)))
            draw_box(image, point1, point2, 'r')
            cv2.imshow(window_name, image)

    if event == cv2.EVENT_MBUTTONDOWN:  # 中键点击
        point1 = (x, y)
    elif event == cv2.EVENT_MBUTTONUP:  # 中键释放，标不存在点
        point2 = (x, y)
        if point2 == point1 or np.abs(point2[0] - point1[0]) < 50 or np.abs(point2[1] - point1[1]) < 50:            # 点
            points.append((0, point1))
            draw_point(image, point1, 0, points.__len__())
            cv2.imshow(window_name, image)


with open("error.txt", 'w') as err:
    err.write("error log \n")

for dir in dirs:
    ori_image = cv2.imdecode(np.fromfile(image_path + "/" + dir, dtype=np.uint8), cv2.IMREAD_COLOR)
    image = ori_image.copy()
    n_box = 0
    window_name = "image"
    cv2.namedWindow(window_name, cv2.WINDOW_FREERATIO)
    key = -1
    cv2.setMouseCallback(window_name, on_mouse, key)
    points = []
    boxes = []

    while 1:
        cv2.imshow(window_name, image)
        key = cv2.waitKey(0)
        print(key)
        if key == 8 and points.__len__() > 0:
            print("pop " + str(points.__len__()) + ' ' + str(points.pop()))
            image = ori_image.copy()
            for i, point in enumerate(points):
                draw_point(image, point[1], point[0], i+1)
            for box in boxes:
                draw_box(image, box[1][0], box[1][1], box[0])
            cv2.imshow(window_name, image)
        if key == 27 and boxes.__len__():
            print("pop " + str(boxes.__len__()) + ' ' + str(boxes.pop()))
            image = ori_image.copy()
            for i, point in enumerate(points):
                draw_point(image, point[1], point[0], i+1)
            for box in boxes:
                draw_box(image, box[1][0], box[1][1], box[0])
            cv2.imshow(window_name, image)
        if key == 13:
            break

    with open(label_path + '/' + dir.split('.')[0] + ".txt", 'w') as l:
        height = float(ori_image.shape[0])
        width = float(ori_image.shape[1])
        for i, box in enumerate(boxes):
            line = ""
            if box[0] == 'r':
                line += str(0)
                line += ' '
            elif box[0] == 'l':
                line += str(21)
                line += ' '
            x = float(((box[1][0][0] + box[1][1][0]) / 2.0) / float(width))
            y = float(((box[1][0][1] + box[1][1][1]) / 2.0) / height)
            w = float((np.abs(box[1][0][0] - box[1][1][0])) / width)
            h = float((np.abs(box[1][0][1] - box[1][1][1])) / height)
            line = line + str(x) + ' ' + str(y) + ' ' + str(w) + ' ' + str(h) + ' '

            if (i * 20 + 20) > points.__len__():
                with open("error.txt", 'a+') as err:
                    err.write(dir + "   less than 20 points \n")
            for j in range(i*20, i*20+20):
                if j >= points.__len__():
                    break
                line += str(float(points[j][1][0] / width))
                line += ' '
                line += str(float(points[j][1][1] / width))
                line += ' '
                line += str(int(points[j][0]))
                line += ' '

            line += '\n'
            l.write(line)





