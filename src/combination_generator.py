import cv2
import numpy as np


def make_retangle(image, color_value=None):
    if color_value is None:
        color_value = 255
    # for ss in shape_split[0]:
    if image.shape[0] > image.shape[1]:
        margin = (image.shape[0] - image.shape[1]) // 2
        t = np.zeros((image.shape[0], margin, 3), dtype=np.int32)
        t[:] = color_value
        if image.shape[0] != (t.shape[1] * 2) + image.shape[1]:
            t_ = np.zeros((margin + 1, image.shape[1], 3), dtype=np.int32)
            t_[:] = color_value
            tc = np.concatenate((t, image, t_), axis=1)
        else:
            tc = np.concatenate((t, image, t), axis=1)
        return tc

    elif image.shape[0] < image.shape[1]:
        mg = (image.shape[1] - image.shape[0]) // 2
        t = np.zeros((mg, image.shape[1], 3), dtype=np.int32)
        t[:] = color_value
        if image.shape[1] != (t.shape[0] * 2) + image.shape[0]:
            t_ = np.zeros((mg + 1, image.shape[1], 3), dtype=np.int32)
            t_[:] = color_value
            tc = np.concatenate((t, image, t_), axis=0)
        else:
            tc = np.concatenate((t, image, t), axis=0)
        return tc
    else:
        return image

def make_avg_size(image, avg_shape=None):
    if avg_shape is None:
        avg_shape = (800, 800)

    image = cv2.resize(image, dsize=avg_shape, interpolation=cv2.INTER_AREA)

    return image

def combination(images):
    retangle, long_w, long_h = [], [], []

    for img in images:
        h, w = img.shape[0], img.shape[1]
        if h > w:
            long_h.append(img)
        elif h < w:
            long_w.append(img)
        else:
            retangle.append(img)