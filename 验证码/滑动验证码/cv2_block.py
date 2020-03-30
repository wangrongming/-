import cv2
import numpy as np


def show(name):
    cv2.imshow('Show', name)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def main():
    otemp = 'small_code.png'
    oblk = 'code.png'

    # 读取图片
    code = cv2.imread(otemp, 0)
    small_code = cv2.imread(oblk, 0)
    small_code_jpg = 'small_code_jpg.jpg'
    code_jpg = 'code_jpg.jpg'
    cv2.imwrite(small_code_jpg, small_code)
    cv2.imwrite(code_jpg, code)
    w, h = code.shape[::-1]

    target = cv2.imread(code_jpg)
    target = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)
    target = abs(255 - target)

    cv2.imwrite(code_jpg, target)
    target = cv2.imread(code_jpg)

    template = cv2.imread(small_code_jpg)

    result = cv2.matchTemplate(target, template, cv2.TM_CCOEFF_NORMED)

    x, y = np.unravel_index(result.argmax(), result.shape)

    # 展示圈出来的区域
    # cv2.rectangle(template, (y, x), (y + w, x + h), (7, 249, 151), 2)
    # show(template)
    print(y)
    return y


def main_two():
    otemp = 'small_code.png'
    oblk = 'code.png'

    # 读取图片
    img_rgb = cv2.imread(otemp)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(oblk, 0)
    run = 1
    w, h = template.shape[::-1]
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    x, y = np.unravel_index(res.argmax(), res.shape)

    # cv2.rectangle(template, (y, x), (y + w, x + h), (7, 249, 151), 2)
    # show(template)

    print(x, y)


if __name__ == '__main__':
    main()
