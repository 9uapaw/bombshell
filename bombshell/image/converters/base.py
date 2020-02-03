from PIL import Image


class BaseImageToString:

    def image_to_string(self, image: Image) -> str:
        raise NotImplementedError()

    def end(self):
        pass
