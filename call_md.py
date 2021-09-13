# # CNN model
# import tensorflow as tf
# import os 
# import numpy as np

# class_dict = {'高麗菜':0,'紅蘿蔔':1,'花椰菜':2,'雞腿':3,'茄子':4,'洋蔥':5,'鳳梨':6,'鮭魚':7,'蝦子':8,'番茄':9}

# model = tf.keras.models.load_model('/home/spark/Desktop/models/CNN_model.h5')


# def call_md(path):


#     image_path = path
#     test_image = tf.keras.preprocessing.image.load_img(path, target_size = (150, 150)) 
#     test_image = tf.keras.preprocessing.image.img_to_array(test_image)
#     test_image = test_image /255.0
#     # (150, 150, 3)

#     test_image = np.expand_dims(test_image, axis = 0)
#     # (1, 150, 150, 3)

#     #predict the result
#     result = model.predict(test_image)
    
#     for key in class_dict:
#         if result.argmax() == class_dict[key]:
#             return key

# # inception v3 model
# import tensorflow as tf
# import os 
# import numpy as np
# from tensorflow import keras

# class_dict = {'高麗菜':0,'紅蘿蔔':1,'花椰菜':2,'雞腿':3,'茄子':4,'洋蔥':5,'鳳梨':6,'鮭魚':7,'蝦子':8,'番茄':9}


# with open('/home/spark/Desktop/models/model_config.json') as json_file: # load model
#     json_config = json_file.read()
# model = keras.models.model_from_json(json_config)
 
# model.load_weights('/home/spark/Desktop/models/inceptionv3_model.h5') # load variables
# model.compile(optimizer=keras.optimizers.Adam(),
#              loss=keras.losses.SparseCategoricalCrossentropy(),
#              metrics=['accuracy'])


# def call_md(path):


#     image_path = path
#     test_image = tf.keras.preprocessing.image.load_img(path, target_size = (150, 150)) 
#     test_image = tf.keras.preprocessing.image.img_to_array(test_image)
#     test_image = test_image /255.0
#     # (150, 150, 3)

#     test_image = np.expand_dims(test_image, axis = 0)
#     # (1, 150, 150, 3)

#     #predict the result
#     result = model.predict(test_image)
    
#     for key in class_dict:
#         if result.argmax() == class_dict[key]:
#             return key



# VGG16 model
# import tensorflow as tf
# import os 
# import numpy as np
# from tensorflow import keras

# class_dict = {'高麗菜':0,'紅蘿蔔':1,'花椰菜':2,'雞腿':3,'茄子':4,'洋蔥':5,'鳳梨':6,'鮭魚':7,'蝦子':8,'番茄':9}


# with open('/home/spark/Desktop/models/vgg16_model_config.json') as json_file: # load model
#     json_config = json_file.read()
# model = keras.models.model_from_json(json_config)
 
# model.load_weights('/home/spark/Desktop/models/vgg16_model.h5') # load variables
# model.compile(optimizer=keras.optimizers.Adam(),
#              loss=keras.losses.SparseCategoricalCrossentropy(),
#              metrics=['accuracy'])


# def call_md(path):


#     image_path = path
#     test_image = tf.keras.preprocessing.image.load_img(path, target_size = (150, 150)) 
#     test_image = tf.keras.preprocessing.image.img_to_array(test_image)
#     test_image = test_image /255.0
#     # (150, 150, 3)

#     test_image = np.expand_dims(test_image, axis = 0)
#     # (1, 150, 150, 3)

#     #predict the result
#     result = model.predict(test_image)
    
#     for key in class_dict:
#         if result.argmax() == class_dict[key]:
#             return key


#'============================================================================================================'

# Yolov5 model
#pip install -r requirements.txt
from PIL import Image
import torch
from matplotlib import pyplot as plt
import numpy as np
from torch._C import Value

class_dict = {'番茄':0,'紅蘿蔔':1,'花椰菜':2,'茄子':3,'高麗菜':4,'洋蔥':5,'鳳梨':6,'蝦子':7,'雞腿':8,'鮭魚':9}

# path = with open("C:\Users\Tibame_25\Downloads\lineBot_TFB102_withModel and Inv\lineBot_TFB102\static", "r") as file:
# image_path = path
model = torch.hub.load('ultralytics/yolov5','custom',path=r"/home/spark/Desktop/models/yolov5/runs/train/exp13/weights/best.pt",force_reload=True)

def call_md(path):
    image_path = path
    img = Image.open(path)
    results = model(img)  
    resultss = results.pandas().xyxy[0]['class'][0]  # print classnumber

    for key, value in class_dict.items():
        if resultss == value:
            return key

