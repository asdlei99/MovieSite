# coding=utf-8
from __future__ import division
from PIL import Image
from ms_constants import P_HEIGHT, P_WIDTH, S_HEIGHT, S_WIDTH
import log
import os

LOG = log.Log()


class ImageProcessor(object):

    def __init__(self):
        self.P_RATIO = P_WIDTH / P_HEIGHT
        self.S_RATIO = S_WIDTH / S_HEIGHT

    def edit_poster(self, origin_path, origin_filename, target_path):
        """
        Reduce a poster, cut it and save to the target path
        :param origin_path:
        :param origin_filename:
        :param target_path:
        :return: True or False
        """
        origin_poster = os.path.join(origin_path, origin_filename)
        target_poster = os.path.join(target_path, origin_filename)
        try:
            img = Image.open(origin_poster)
            w, h = img.size
            ratio = w / h
            if ratio < self.P_RATIO:
                # scaled height
                scaled_h = int(h / (w / P_WIDTH))
                img = img.resize((P_WIDTH, scaled_h), Image.ANTIALIAS)
                x = 0
                y = int((scaled_h / 2) - (P_HEIGHT / 2))
                box = (x, y, x + P_WIDTH, y + P_HEIGHT)
                new_img = img.crop(box)
            elif ratio > self.P_RATIO:  # 宽了
                scaled_w = int(w / (h / P_HEIGHT))
                img = img.resize((scaled_w, P_HEIGHT), Image.ANTIALIAS)
                y = 0
                x = int((scaled_w / 2) - (P_WIDTH / 2))
                box = (x, y, x + P_WIDTH, y + P_HEIGHT)
                new_img = img.crop(box)
            else:
                new_img = img.resize((P_WIDTH, P_HEIGHT), Image.ANTIALIAS)

            if not os.path.exists(target_path):
                os.makedirs(target_path)
            # save
            new_img.save(target_poster, 'JPEG', quality=85)
        finally:
            # delete old poster
            self.clean(origin_poster)

    def edit_screenshot(self, origin_path, origin_filename, target_path):
        """
        Reduce a screenshot, cut it and save to the target path
        :param origin_path: a list
        :param origin_filename:
        :param target_path:
        :return: True or False
        """
        origin_poster = os.path.join(origin_path, origin_filename)
        target_poster = os.path.join(target_path, origin_filename)
        try:
            img = Image.open(origin_poster)
            w, h = img.size
            ratio = w / h
            if ratio < self.S_RATIO:
                # scaled height
                scaled_h = int(h / (w / S_WIDTH))
                img = img.resize((S_WIDTH, scaled_h), Image.ANTIALIAS)
                x = 0
                y = int((scaled_h / 2) - (S_HEIGHT / 2))
                box = (x, y, x + S_WIDTH, y + S_HEIGHT)
                new_img = img.crop(box)
            elif ratio > self.S_RATIO:  # 宽了
                scaled_w = int(w / (h / S_HEIGHT))
                img = img.resize((scaled_w, S_HEIGHT), Image.ANTIALIAS)
                y = 0
                x = int((scaled_w / 2) - (S_WIDTH / 2))
                box = (x, y, x + S_WIDTH, y + S_HEIGHT)
                new_img = img.crop(box)
            else:
                new_img = img.resize((S_WIDTH, S_HEIGHT), Image.ANTIALIAS)

            if not os.path.exists(target_path):
                os.makedirs(target_path)
            # save
            new_img.save(target_poster, 'JPEG', quality=85)
        finally:
            # delete old poster
            self.clean(origin_poster)

    @staticmethod
    def clean(image_path):
        try:
            os.remove(image_path)
            pass
        except OSError:
            LOG.error('Failed to remove %s' % image_path)
            raise


if __name__ == '__main__':
    pass
