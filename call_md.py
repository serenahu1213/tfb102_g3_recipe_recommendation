# CNN model
# import tensorflow as tf
# import os 
# import numpy as np

# class_dict = {'高麗菜':0,'紅蘿蔔':1,'花椰菜':2,'雞腿':3,'茄子':4,'洋蔥':5,'鳳梨':6,'鮭魚':7,'蝦子':8,'番茄':9}

# model = tf.keras.models.load_model('C:/Users/Tibame_25/TFB102專案/lineBot_TFB102/models/CNN_model.h5')


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

# inception v3 model
# import tensorflow as tf
# import os 
# import numpy as np
# from tensorflow import keras

# class_dict = {'高麗菜':0,'紅蘿蔔':1,'花椰菜':2,'雞腿':3,'茄子':4,'洋蔥':5,'鳳梨':6,'鮭魚':7,'蝦子':8,'番茄':9}


# with open('C:/Users/Tibame_25/TFB102專案/lineBot_TFB102/models/model_config.json') as json_file: # load model
#     json_config = json_file.read()
# model = keras.models.model_from_json(json_config)
 
# model.load_weights('C:/Users/Tibame_25/TFB102專案/lineBot_TFB102/models/inceptionv3_model.h5') # load variables
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
import tensorflow as tf
import os 
import numpy as np
from tensorflow import keras

class_dict = {'高麗菜':0,'紅蘿蔔':1,'花椰菜':2,'雞腿':3,'茄子':4,'洋蔥':5,'鳳梨':6,'鮭魚':7,'蝦子':8,'番茄':9}


with open('C:/Users/Tibame_25/TFB102專案/lineBot_TFB102/models/vgg16_model_config.json') as json_file: # load model
    json_config = json_file.read()
model = keras.models.model_from_json(json_config)
 
model.load_weights('C:/Users/Tibame_25/TFB102專案/lineBot_TFB102/models/vgg16_model.h5') # load variables
model.compile(optimizer=keras.optimizers.Adam(),
             loss=keras.losses.SparseCategoricalCrossentropy(),
             metrics=['accuracy'])


def call_md(path):


    image_path = path
    test_image = tf.keras.preprocessing.image.load_img(path, target_size = (150, 150)) 
    test_image = tf.keras.preprocessing.image.img_to_array(test_image)
    test_image = test_image /255.0
    # (150, 150, 3)

    test_image = np.expand_dims(test_image, axis = 0)
    # (1, 150, 150, 3)

    #predict the result
    result = model.predict(test_image)
    
    for key in class_dict:
        if result.argmax() == class_dict[key]:
            return key
