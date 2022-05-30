# -*- coding: utf-8 -*-
"""
Project:        image_collage_maker
Creator:        TROY.MAO
Create time:    2020-07-18 23:46 Shanghai, China
Filename:       collage_maker.py
Introduction:   -
"""
# __all__ = ["make_collage"]


import cv2
import numpy as np


class CollageMaker(object):

    def __init__(self):
        self.IMAGE_COLLAGE_MAKER_BORDER_PIX = 3
        self.IMAGE_COLLAGE_MAKER_PIXEL_LIM = 4096


    def _add_color_border_ul(self, image, px=1, color_value=None):
        px = int(px)
        if image.ndim == 2:
            image = np.stack([image, image, image], axis=-1)
            if color_value is None:
                color_value = [255, 255, 255]
            else:
                color_value = [color_value, color_value, color_value]

        if color_value is None:
            if image.shape[-1] == 3:
                color_value = [255, 255, 255]
            else:
                color_value = [255, 255, 255, 255]
        h, w, c = image.shape
        assert c == len(color_value)
        ab = np.ones((px, w + px, c), dtype=np.uint8) * np.array(color_value)
        lr = np.ones((h, px, c), dtype=np.uint8) * np.array(color_value)
        new = np.concatenate([ab, np.concatenate([lr, image], axis=1)], axis=0)
        del ab, lr
        return new


    def _add_color_border_br(self, image, px=1, color_value=None):
        px = int(px)
        if image.ndim == 2:
            image = np.stack([image, image, image], axis=-1)
            if color_value is None:
                color_value = [255, 255, 255]
            else:
                color_value = [color_value, color_value, color_value]

        if color_value is None:
            if image.shape[-1] == 3:
                color_value = [255, 255, 255]
            else:
                color_value = [255, 255, 255, 255]
        h, w, c = image.shape
        assert c == len(color_value)
        ab = np.ones((px, w + px, c), dtype=np.uint8) * np.array(color_value)
        lr = np.ones((h, px, c), dtype=np.uint8) * np.array(color_value)
        new = np.concatenate([np.concatenate([image, lr], axis=1), ab], axis=0)
        del ab, lr
        return new


    def make_collage_(self, images,
                      direction=0,
                      border_px=3,
                      border_color=None):
        """

        Collage is a image combiner to combine lists of arrays.
        This is Collage Maker, it makes the collage with borders.
        You may want to set the ``border_px``, ``border_bg``, ``direction`` to let it work.
        By default, ``border_px=3, border_color=[255, 255, 255, 255]``

        Usage:

        # >>> from collage_maker import make_collage
        # >>> make_collage(images=[
        # ...         [image_a, image_b],
        # ...         [image_c, image_d, [image_f, image_g]]
        # ...    ],
        # ...    direction=0, border_px=1, border_color=[0, 0, 0, 255])

        In this example, ``image_x`` are image np.ndarray with 1 channel, 3 channels, 4 channels.

        :param images: list of (lists of) images
        :param direction: 0/1 to control row first or column first
        :param border_px: border px
        :param border_color: border color rgba
        :return:
        """

        made = self._make(images, direction, border_px, border_color, True)[0]
        return made.astype(np.uint8)


    def _make(self,
            images,
            direction=0,
            border_px=3,
            border_color=None,
            frist=False,
    ):
        """
        TODO: add constant boarder...
        :param images:
        :param direction:
        :param border_px:
        :param border_color:
        :return:
        """

        if isinstance(images, np.ndarray):
            if len(images.shape) == 2:
                images = np.stack([images, images, images, np.ones_like(images) * 255], axis=-1)
            else:
                if images.shape[-1] == 3:
                    images = np.concatenate([images, np.ones_like(images[:, :, :1]) * 255], axis=-1)
            return images, 1
        next_direction = 1 - direction
        assert len(images) != 0, "the image list should have at least one."

        if len(images) == 1:
            if isinstance(images[0], np.ndarray):
                return images[0], 1
        # recursively make collage.
        cats = [
            self._make(
                image,
                direction=next_direction,
                border_px=border_px,
                border_color=border_color,
            )
            for image in images
        ]

        ratio_last = sum([c[1] for c in cats]) / len(cats)
        cats = [c[0] for c in cats]
        # border_px = 0
        ratio = np.array([image.shape[direction] for image in cats], dtype=np.float64)

        sum_border = sum([image.shape[next_direction] for image in cats])
        ratio_v = 1.0
        if sum_border > self.IMAGE_COLLAGE_MAKER_PIXEL_LIM:
            ratio_v = sum_border / self.IMAGE_COLLAGE_MAKER_PIXEL_LIM
        ratio = ratio / np.max(ratio)

        resizes = [
            image
            if r == 1 and ratio_v == 1
            else _cv2.resize(
                image,
                dsize=None,
                fx=1 / r / ratio_v,
                fy=1 / r / ratio_v,
                interpolation=_cv2.INTER_AREA,
            )
            for (image, r) in zip(cats, ratio)
        ]

        if border_px != 0:
            borders = [
                _add_color_border_ul(image, border_px / ratio_last, border_color)
                for image in resizes
            ]
            border_px = border_px if frist else 0
            cats = _add_color_border_br(
                np.concatenate(borders, axis=next_direction), border_px, border_color
            )
        else:
            cats = np.concatenate(resizes, axis=next_direction)
        return cats, ratio_v