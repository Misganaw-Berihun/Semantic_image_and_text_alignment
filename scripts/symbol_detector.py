from PIL import Image
import base64
from io import BytesIO

class SymbolDetection:
    """
    A class used to reprsent a Symbol detector
    """
    def __init__(self, model, conf):
        """
        constructs a symbol detector object
        
        parameters:
            model: symbol-detector model
            conf: NMS confidence threshold
        """
        self.model = model
        self.conf = conf

    def query(self, filename):
        """
        Query the symbol-detector object to detect our image

        parameters:
            filename: Path of the input image
        """

        # inference with test time augmentation
        results = self.model(filename)
        objects = results.crop(save=False)
        output = []
        for obj in objects:
            if (self.conf <= float(obj['conf'])):
                output.append( {
                    "Box": {
                        "x": int(obj['box'][0]),
                        "y": int(obj['box'][1]),
                        "width": int(obj['box'][2]),
                        "height": int(obj['box'][3])
                    },
                    "conf": float(obj['conf']),
                    "label": self.model.names[int(obj['cls'])]
                })
        return output