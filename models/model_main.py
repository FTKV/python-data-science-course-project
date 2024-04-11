from fastapi import FastAPI, File, UploadFile
import numpy as np
import cv2
import tensorflow as tf
from tensorflow.keras import optimizers
from tensorflow.keras.models import Sequential
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.layers import Dense, Flatten, MaxPooling2D, Dropout, Conv2D
from keras.models import model_from_json

app = FastAPI()


@app.post("/process_image")
async def upload_image(img_file: UploadFile = File(...)):

    img_bytes = await img_file.read()
    np_array = np.frombuffer(img_bytes, np.uint8)

    plate_cascade = cv2.CascadeClassifier("license_plate.xml")

    def detect_plate(img, text=""):
        plate_img = img.copy()
        roi = img.copy()
        plate = None
        plate_rect = plate_cascade.detectMultiScale(
            plate_img, scaleFactor=1.2, minNeighbors=6
        )  # detects numberplates and returns the coordinates and dimensions of detected license plate's contours.
        for x, y, w, h in plate_rect:
            roi_ = roi[
                y : y + h, x : x + w, :
            ]  # extracting the Region of Interest of license plate for blurring.
            plate = roi[y : y + h, x : x + w, :]
            cv2.rectangle(
                plate_img, (x + 2, y), (x + w - 3, y + h - 5), (51, 181, 155), 3
            )  # finally representing the detected contours by drawing rectangles around the edges.
        if text != "":
            plate_img = cv2.putText(
                plate_img,
                text,
                (x - w // 2, y - h // 2),
                cv2.FONT_HERSHEY_COMPLEX_SMALL,
                0.5,
                (51, 181, 155),
                1,
                cv2.LINE_AA,
            )
        if plate is None:
            return None, None
        else:
            return plate_img, plate

    # img = cv2.imread(image_to_process)
    img = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
    output_img, plate = detect_plate(img)

    def find_contours(dimensions, img):

        # Find all contours in the image
        cntrs, _ = cv2.findContours(img.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Retrieve potential dimensions
        lower_width = dimensions[0]
        upper_width = dimensions[1]
        lower_height = dimensions[2]
        upper_height = dimensions[3]

        # Check largest 5 or  15 contours for license plate or character respectively
        cntrs = sorted(cntrs, key=cv2.contourArea, reverse=True)[:15]

        ii = cv2.imread("contour.jpg")

        x_cntr_list = []
        target_contours = []
        img_res = []
        for cntr in cntrs:
            # detects contour in binary image and returns the coordinates of rectangle enclosing it
            intX, intY, intWidth, intHeight = cv2.boundingRect(cntr)

            # checking the dimensions of the contour to filter out the characters by contour's size
            if (
                intWidth > lower_width
                and intWidth < upper_width
                and intHeight > lower_height
                and intHeight < upper_height
            ):
                x_cntr_list.append(
                    intX
                )  # stores the x coordinate of the character's contour, to used later for indexing the contours

                char_copy = np.zeros((44, 24))
                # extracting each character using the enclosing rectangle's coordinates.
                char = img[intY : intY + intHeight, intX : intX + intWidth]
                char = cv2.resize(char, (20, 40))

                cv2.rectangle(
                    ii,
                    (intX, intY),
                    (intWidth + intX, intY + intHeight),
                    (50, 21, 200),
                    2,
                )

                # Make result formatted for classification: invert colors
                char = cv2.subtract(255, char)

                # Resize the image to 24x44 with black border
                char_copy[2:42, 2:22] = char
                char_copy[0:2, :] = 0
                char_copy[:, 0:2] = 0
                char_copy[42:44, :] = 0
                char_copy[:, 22:24] = 0

                img_res.append(
                    char_copy
                )  # List that stores the character's binary image (unsorted)

        # arbitrary function that stores sorted list of character indeces
        indices = sorted(range(len(x_cntr_list)), key=lambda k: x_cntr_list[k])
        img_res_copy = []
        for idx in indices:
            img_res_copy.append(
                img_res[idx]
            )  # stores character images according to their index
        img_res = np.array(img_res_copy)

        return img_res

    # Find characters in the resulting images
    def segment_characters(image):
        if image is None:
            return None
        # Preprocess cropped license plate image
        img_lp = cv2.resize(image, (333, 75))
        img_gray_lp = cv2.cvtColor(img_lp, cv2.COLOR_BGR2GRAY)
        _, img_binary_lp = cv2.threshold(
            img_gray_lp, 200, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )
        img_binary_lp = cv2.erode(img_binary_lp, (3, 3))
        img_binary_lp = cv2.dilate(img_binary_lp, (3, 3))

        LP_WIDTH = img_binary_lp.shape[0]
        LP_HEIGHT = img_binary_lp.shape[1]

        # Make borders white
        img_binary_lp[0:3, :] = 255
        img_binary_lp[:, 0:3] = 255
        img_binary_lp[72:75, :] = 255
        img_binary_lp[:, 330:333] = 255

        # Estimations of character contours sizes of cropped license plates
        dimensions = [LP_WIDTH / 6, LP_WIDTH / 2, LP_HEIGHT / 10, 2 * LP_HEIGHT / 3]

        cv2.imwrite("contour.jpg", img_binary_lp)

        # Get contours within cropped license plate
        char_list = find_contours(dimensions, img_binary_lp)

        return char_list

    # segmented characters
    char = segment_characters(plate)

    # download the model architecture from JSON and weights
    with open("model.json", "r") as json_file:
        loaded_model_json = json_file.read()
    model = model_from_json(loaded_model_json)
    model.load_weights("model.weights.h5")

    # Predicting the output
    def fix_dimension(img):
        new_img = np.zeros((28, 28, 3))
        for i in range(3):
            new_img[:, :, i] = img
        return new_img

    def show_results():
        dic = {}
        characters = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        for i, c in enumerate(characters):
            dic[i] = c

        if char is None:
            return None

        output = []
        for i, ch in enumerate(char):  # iterating over the characters
            img_ = cv2.resize(ch, (28, 28), interpolation=cv2.INTER_AREA)
            img = fix_dimension(img_)
            img = img.reshape(1, 28, 28, 3)  # preparing image for the model
            y_prob = model.predict(img)[0]  # predicting the class
            y_class = np.argmax(y_prob)
            character = dic[y_class]  #
            output.append(character)  # storing the result in a list

        plate_number = "".join(output)

        return plate_number

    license_plate_number = show_results()
    print(f"License plate number: {license_plate_number}")

    return {"result": license_plate_number}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
