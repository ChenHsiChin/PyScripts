import cv2 as cv
import numpy as np
import random
import math

# pic turn to low pixels, im using it to preprocess material, then material can import to bit game.
img = cv.imread('o.jpg')

if img is None:
    print("cant find picture")
    exit(0)

img_sp = img.shape
img_width = img_sp[0]
img_height = img_sp[1]
thunk_size = 6

mod_width = img_width % thunk_size
mod_height = img_height % thunk_size

correct_img_width = 0
correct_img_height = 0
if mod_width != 0:
    correct_img_width = img_width - mod_width
else:
    correct_img_width = img_width
if mod_height != 0:
    correct_img_height = img_height - mod_height
else:
    correct_img_height = img_height

print("ori ", img_width, img_height)
print("cor ", correct_img_width, correct_img_height)
step_x = 0
step_y = 0

out_image = np.zeros((correct_img_width, correct_img_height, 3), dtype=np.uint8)


def get_thunk(x, y, size):
    pl = []
    for m in range(size):
        for n in range(size):
            # print(x + n, y + m)
            pl.append(img[x + n, y + m])
    return pl


def set_pixel(x, y, size, color):
    for m in range(size):
        for n in range(size):
            out_image[x + n, y + m] = color


def get_thunk_one(x, y):
    return img[x, y]


def choice_pixel(x, y):
    # pixels = get_thunk(x, y, thunk_size)
    # choice_color = pixels[0]  # random.randint(0, int(math.pow(thunk_size, 2) - 1))
    # set_pixel(x, y, thunk_size, choice_color)
    set_pixel(x, y, thunk_size, get_thunk_one(x, y))


while True:
    if correct_img_width - step_x <= 0:
        step_x = 0
        step_y = step_y + thunk_size
    choice_pixel(step_x, step_y)
    step_x = step_x + thunk_size
    if correct_img_width - thunk_size - step_x <= 0 and correct_img_height - thunk_size - step_y <= 0:
        break

# 处理边界问题 最后一个块
step_x = correct_img_width - thunk_size
step_y = correct_img_height - thunk_size
choice_pixel(step_x, step_y)

cv.imwrite("1.jpg", out_image)
print("finish")
cv.waitKey(0)
