import cv2 as cv
import pytesseract
from PIL import Image
import logging
from random import randint
from math import floor

DEBUG = False

def capture_from_image():
    cap = cv.VideoCapture(0)
    while cap.isOpened():
        
        ret, frame = cap.read()
        if ret is False:
            return(ret)
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
   
        cap.release()
        cv.destroyAllWindows()
        return gray

def find_all():
    img1 = capture_from_image()
    if img1 is False:
        return("Camera is not detected")
    h, w = img1.shape
    eighthh = h//8
    halfh = h//2
    halfw = w//2
    full = 618 #pixel count that hopefully chops off extra values, but no information
    reduced_img = img1[eighthh:halfh, halfw:full]
    try:
        text = pytesseract.image_to_string(Image.fromarray(reduced_img))
    except:
        text = "Camera may be disconnected, or the proper dependancies are not installed"
    return text

def capture_decoder():
    '''
            Will return a value in the form of [string, string].
            The return when a value isn't found is ["vessel not found", "0.00"]
    '''
    if DEBUG is True:
        names =[ "PI", "VF" ]
        will_loop = randint(0,1)
        return([names[will_loop],str(floor((randint(1, 450)/4.5)*100)/100)])
    else:
        logging.basicConfig(filename="log_files\ocr_output.log",
                        format='%(asctime)s %(message)s',
                        filemode='a')
        logger = logging.getLogger()
        # Setting the threshold of logger to DEBUG
        logger.setLevel(logging.DEBUG)
        searching_for_text = True
        capture_decoder_return = ["vessel not found", "0.00"]
        while searching_for_text:
            text = find_all()
            logger.info(text)
            split_txt = text.split("\n")
            matchespi = [match for match in split_txt if "PI" in match]
            matchespi += [match for match in split_txt if "PL" in match]
            matchespi += [match for match in split_txt if "Pl" in match]
            matchespi += [match for match in split_txt if "Pi" in match]
            matchesvf = [match for match in split_txt if "Vol Flow" in match]
            array_lengthpi = len(matchespi)
            array_lengthvf = len(matchesvf)
            if (array_lengthvf > 0) or (array_lengthpi > 0):
                if array_lengthvf > 0:
                    for items in matchesvf:
                        matches = items.split()
                    name = "VF"
                    array_lengthvf = len(matches)
                elif array_lengthpi > 0:
                    for items in matchespi:
                        matches = items.split()
                    array_lengthpi = len(matches)
                    name = "PI"
                for items in matches:
                    try:
                        float(items)
                        capture_decoder_return = [name, items]
                    except:
                        pass
                return(capture_decoder_return)
            else:
                return(["value not found", "0.00"])            

if __name__ == "__main__":
    while True:
        print("return_val = ", capture_decoder())
