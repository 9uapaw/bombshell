from typing import Tuple
import cv2
import os
from PIL import Image as PilImage
import numpy

# methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
#             'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']

class ScreenScuttler:
    width_scale = 9.0112359
    height_scale = 52.6666667

    def try_find_in_screen(self, template: PilImage, screenshot: PilImage, threshold: int = 50) -> Tuple[
        Tuple[int, int], Tuple[int, int], Tuple[int, int], Tuple[int, int]]:
        template_cvf = cv2.cvtColor(numpy.array(template), cv2.COLOR_RGB2GRAY)
        screenshot_cvf = cv2.cvtColor(numpy.array(screenshot), cv2.COLOR_RGB2GRAY)

        w, h = template_cvf.shape[::-1]

        meth = ['cv2.TM_CCOEFF_NORMED']

        method = eval(meth[0])
        res = cv2.matchTemplate(screenshot_cvf, template_cvf, method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        if (max_val*100) <= threshold:
            return None

        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)

        cv2.rectangle(screenshot_cvf, top_left, bottom_right, 255, 2)

        ret = ((top_left[0], top_left[1]), (bottom_right[0], top_left[1]), (bottom_right[0], bottom_right[1]),(top_left[0], bottom_right[1]))

        print("DEBUG: Found coordinates: {}".format(ret))

        return ret

    def find_in_screen(self, template: PilImage, screenshot: PilImage) -> Tuple[
        Tuple[int, int], Tuple[int, int], Tuple[int, int], Tuple[int, int]]:
        template_cvf = cv2.cvtColor(numpy.array(template), cv2.COLOR_RGB2GRAY)
        screenshot_cvf = cv2.cvtColor(numpy.array(screenshot), cv2.COLOR_RGB2GRAY)

        height, width = screenshot_cvf.shape
        template_cvf = cv2.resize(template_cvf,
                                  (int(round(width / self.width_scale)), int(round(height / self.height_scale))))
        w, h = template_cvf.shape[::-1]

        meth = ['cv2.TM_CCOEFF_NORMED']

        method = eval(meth[0])
        res = cv2.matchTemplate(screenshot_cvf, template_cvf, method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        # ha akarunk thresholdot azt ide kell berakni a max_val csekkolásával: pl max_val >= 0.5

        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)

        cv2.rectangle(screenshot_cvf, top_left, bottom_right, 255, 2)

        ret = ((top_left[0], top_left[1]), (bottom_right[0], top_left[1]), (bottom_right[0], bottom_right[1]),
               (top_left[0], bottom_right[1]))

        print("DEBUG: Found coordinates: {}".format(ret))

        return ret

    def find_accept_button(self, screenshot: PilImage) -> Tuple[
        Tuple[int, int], Tuple[int, int], Tuple[int, int], Tuple[int, int]]:

        currdir = os.path.dirname(__file__)
        accept_btn_image = PilImage.open(os.path.join(currdir, '../assets/image/accept_button.png'))
        return self.find_in_screen(accept_btn_image, screenshot)

    def find_release_button(self, screenshot: PilImage) -> Tuple[
        Tuple[int, int], Tuple[int, int], Tuple[int, int], Tuple[int, int]]:

        currdir = os.path.dirname(__file__)
        accept_btn_image = PilImage.open(os.path.join(currdir, '../assets/image/release_button.png'))
        return self.find_in_screen(accept_btn_image, screenshot)

    def find_loot_icon(self, screenshot: PilImage) -> Tuple[
        Tuple[int, int], Tuple[int, int], Tuple[int, int], Tuple[int, int]]:

        currdir = os.path.dirname(__file__)
        loot_icon_image = PilImage.open(os.path.join(currdir, '../assets/image/loot_icon.png'))
        return self.try_find_in_screen(loot_icon_image, screenshot, 70)
