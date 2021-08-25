from flask import Flask, request, abort

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

import pymysql

from recomm_recipes_carousel import *
from recomm_recipes import *
from check_inventory import *
from deposit import *
from call_md import *
from check_recipe_ingredient import *


import tempfile, os, random, string
import datetime
import time
import re


app = Flask(__name__)
line_bot_api = LineBotApi('XBKs4QPm4vfsX0qxZd2pyhZMEYVBs1xbv8e+Z4mPRDzK2OqJ4UWVY3g3nUiDgP5iebaaN7xFb8Ks561E8EzAt4hbAozzbHsRMOJXS6eLeUYsEN28bASr13bru49B23xUzBMWeuh1N7vLUBZuCYFXZQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('6538f1908ff5877945040220adaa8253')
image_tmp_path = os.path.join(os.getcwd(), 'static').replace('\\','/')

connect = pymysql.connect(
                host="127.0.0.1",
                user="root",
                passwd="root",
                database="recipe_db",
                charset='utf8mb4',
        )

cursor = connect.cursor()

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        print('receive msg')
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
    return 'OK'

        
        
       

@handler.add(MessageEvent, message=[TextMessage, ImageMessage])
def handle_message(event):
    user_id = event.source.user_id
    user_name = line_bot_api.get_profile(user_id).display_name
    print(user_id)
    print(user_name)
    
    # for testing purpose
    dishIDs = [13962, 13966, 13981, 14004, 14005]

    if event.message.type=='text':
        msg = event.message.text
        
        if msg in ['哈囉', '你好']:
            text='哈囉~ 歡迎使用食譜底呷啦！\n請至功能選單中填寫喜好問卷，讓我們為您推薦最適合您的菜色 :)'
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text))

            
        elif msg == '清冰箱模式':
            """
            code that can turn all ingres into a list
            """
            
            """
            connect to recipe recommendation system
            - the input will be a list of undefined length of ingredients, e.g. ingres = ['麵粉', '奶油', '蘋果']
            - the output should be a list of 5 dishIDs, e.g. dishIDs = [13962, 13966, 13981, 14004, 14005]
            """
            recommRecipes = recommAll(dishIDs)
            message = Carousel_Template(recommRecipes)
            line_bot_api.reply_message(event.reply_token, message)
          
        
        elif msg == '關鍵字模式':
            text = '請輸入食材名稱，並以空白鍵隔開，輸入完畢後，請在最後輸入"完成"\n\n例如: 麵粉 奶油 蘋果 完成'
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text))
            
        elif '完成' in msg:
            """
            code that can turn all ingres into a list
            """
            
            """
            connect to recipe recommendation system
            - the input will be a list of undefined length of ingredients, e.g. ingres = ['麵粉', '奶油', '蘋果']
            - the output should be a list of 5 dishIDs, e.g. dishIDs = [13962, 13966, 13981, 14004, 14005]
            """
            recommRecipes = recommAll(dishIDs)
            message = Carousel_Template(recommRecipes)
            line_bot_api.reply_message(event.reply_token, message)
           
        
        
        elif '所需食材' in msg:
            """
            connect to recipe recommendation system
            - the input will be a list of undefined length of ingredients, e.g. ingres = ['麵粉', '奶油', '蘋果']
            - the output should be a list of 5 dishIDs, e.g. dishIDs = [13962, 13966, 13981, 14004, 14005]
            """
            recommRecipes = recommAll(dishIDs)
            
            if str(recommRecipes[0][1]) in msg:
                inventory_check = check_recipe_ingredient(recommRecipes[0][0],user_id)

                text = '需要以下食材: \n\n'+str(recommRecipes[0][3])
                text += f'\n------------------\n您的冰箱目前有以下食材 : \n\n'
                for i in inventory_check[0]:
                    text += f'{i} \n'

                text += f'------------------\n您目前缺少以下食材 : \n\n'
                for i in inventory_check[1]:
                    text += f'{i} \n'

                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text))

            elif str(recommRecipes[1][1]) in msg:        
                inventory_check = check_recipe_ingredient(recommRecipes[1][0],user_id)

                text = '需要以下食材: \n\n'+str(recommRecipes[1][3])
                text += f'\n------------------\n您的冰箱目前有以下食材 : \n\n'
                for i in inventory_check[0]:
                    text += f'{i} \n'

                text += f'------------------\n您目前缺少以下食材 : \n\n'
                for i in inventory_check[1]:
                    text += f'{i} \n'                   

                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text))

            elif str(recommRecipes[2][1]) in msg:
                inventory_check = check_recipe_ingredient(recommRecipes[2][0],user_id)

                text = '需要以下食材: \n\n'+str(recommRecipes[2][3])
                text += f'\n------------------\n您的冰箱目前有以下食材 : \n\n'
                for i in inventory_check[0]:
                    text += f'{i} \n'

                text += f'------------------\n您目前缺少以下食材 : \n\n'
                for i in inventory_check[1]:
                    text += f'{i} \n'  

                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text))

            elif str(recommRecipes[3][1]) in msg:
                inventory_check = check_recipe_ingredient(recommRecipes[3][0],user_id)

                text = '需要以下食材: \n\n'+str(recommRecipes[3][3])
                text += f'\n------------------\n您的冰箱目前有以下食材 : \n\n'
                for i in inventory_check[0]:
                    text += f'{i} \n'

                text += f'------------------\n您目前缺少以下食材 : \n\n'
                for i in inventory_check[1]:
                    text += f'{i} \n'

                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text))

            elif str(recommRecipes[4][1]) in msg:
                inventory_check = check_recipe_ingredient(recommRecipes[4][0],user_id)

                text = '需要以下食材: \n\n'+str(recommRecipes[4][3])
                text += f'\n------------------\n您的冰箱目前有以下食材 : \n\n'
                for i in inventory_check[0]:
                    text += f'{i} \n'

                text += f'------------------\n您目前缺少以下食材 : \n\n'
                for i in inventory_check[1]:
                    text += f'{i} \n'
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text))
             
            
            
        elif '我要煮' in msg:
            """
            connect to recipe recommendation system
            - the input will be a list of undefined length of ingredients, e.g. ingres = ['麵粉', '奶油', '蘋果']
            - the output should be a list of 5 dishIDs, e.g. dishIDs = [13962, 13966, 13981, 14004, 14005]
            """
            recommRecipes = recommAll(dishIDs)
            
            if str(recommRecipes[0][1]) in msg:

                cursor.execute(f'select ingredientID, ETL_amount from recipe_ingredient where dishID = "{recommRecipes[0][0]}"')
                result = cursor.fetchall()

                for ingredient in result:
                    deposit_ing(user_id,ingredient[0],-ingredient[1])

                inventory = check_inventory(user_id)
                text = '已在冰箱中扣除相關食材，以下是您的剩餘食材:\n'
                for i in inventory:
                    text += f'{i[0]} : {i[1]}克 \n'                
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text))

            elif str(recommRecipes[1][1]) in msg:

                cursor.execute(f'select ingredientID, ETL_amount from recipe_ingredient where dishID = "{recommRecipes[1][0]}"')
                result = cursor.fetchall()

                for ingredient in result:
                    deposit_ing(user_id,ingredient[0],-ingredient[1])

                inventory = check_inventory(user_id)
                text = '已在冰箱中扣除相關食材，以下是您的剩餘食材:\n'
                for i in inventory:
                    text += f'{i[0]} : {i[1]}克 \n'  
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text))

            elif str(recommRecipes[2][1]) in msg:
                cursor.execute(f'select ingredientID, ETL_amount from recipe_ingredient where dishID = "{recommRecipes[2][0]}"')
                result = cursor.fetchall()

                for ingredient in result:
                    deposit_ing(user_id,ingredient[0],-ingredient[1])

                inventory = check_inventory(user_id)
                text = '已在冰箱中扣除相關食材，以下是您的剩餘食材:\n'
                for i in inventory:
                    text += f'{i[0]} : {i[1]}克 \n'  
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text))

            elif str(recommRecipes[3][1]) in msg:

                cursor.execute(f'select ingredientID, ETL_amount from recipe_ingredient where dishID = "{recommRecipes[3][0]}"')
                result = cursor.fetchall()

                for ingredient in result:
                    deposit_ing(user_id,ingredient[0],-ingredient[1])

                inventory = check_inventory(user_id)
                text = '已在冰箱中扣除相關食材，以下是您的剩餘食材:\n'
                for i in inventory:
                    text += f'{i[0]} : {i[1]}克 \n'  
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text))

            elif str(recommRecipes[4][1]) in msg:

                cursor.execute(f'select ingredientID, ETL_amount from recipe_ingredient where dishID = "{recommRecipes[4][0]}"')
                result = cursor.fetchall()

                for ingredient in result:
                    deposit_ing(user_id,ingredient[0],-ingredient[1])

                inventory = check_inventory(user_id)
                text = '已在冰箱中扣除相關食材，以下是您的剩餘食材:\n'
                for i in inventory:
                    text += f'{i[0]} : {i[1]}克 \n'  
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text))
               
 
        
        elif msg == '查看冰箱':

            result = check_inventory(user_id)
            text='以下是您冰箱現有的食材: \n'
            for i in result:
                text += f'{i[0]} : {i[1]}克 \n'

            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text))
            
        elif msg == '上傳圖片': 
            text='請上傳您的食材圖片'
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text))
            
        elif msg == '是':
            text = '請輸入食材重量(g)\n\n例如: 100g'
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text))
            
        elif re.match(r'^\d+g$', msg):

            amount = float(msg.replace('g',""))
            cursor.execute(f'select picture_result from refrigerator_log where uuid = "{user_id}"')
            ing = cursor.fetchone()[0]
            deposit_ing(user_id,ing,amount)
            """
            code that can calculate the remaining amount in fridge
            """
            text = f'已將食材放入冰箱:\n{ing}:{amount}'
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text))
            
        elif msg == '不是':
            text = '請輸入正確食材名稱及重量(g)，並以空白鍵隔開\n\n例如: 番茄 100g'
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text))
        
        # will catch all ingredient name and amount input by the user
        elif re.match(r'^[\u4E00-\u9FA5]+\s\d+g$', msg):
            msg = msg.split(' ')
            ing = msg[0]
            amount = float(msg[1].replace('g',''))
            deposit_ing(user_id,ing,amount)
            """
            code that can calculate the remaining amount in fridge
            """
            text = f'已將食材放入冰箱:\n{ing}:{amount}'
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text))
                
        else:
            text = '無法辨識您的需求，請再輸入一次~'
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text))
            
            
    elif event.message.type=='image':
        img_msg = event.message.id

        message_content = line_bot_api.get_message_content(event.message.id)
        image_name = ''.join(random.choice(string.ascii_letters + string.digits) for A in range(8)) + '.jpg'
        image_path = image_tmp_path + '/' + image_name

        with open(image_path, 'wb') as fd:
            for chunk in message_content.iter_content():
                fd.write(chunk)
                
        start_time = time.time()    
        result = call_md(image_path)
        end_time = time.time()

        print(f'圖片辨識花費時間 : {end_time-start_time}')

        cursor.execute(f'SELECT * FROM refrigerator_log where uuid = "{user_id}"')
        query = cursor.fetchone()
        if query != None: 
            cursor.execute(f'UPDATE refrigerator_log \
                    SET picture_result = "{result}" \
                    WHERE uuid = "{user_id}"')
            connect.commit()
        else : 
            cursor.execute(f'INSERT INTO refrigerator_log(uuid, picture_result) \
                VALUES ("{user_id}","{result}")')
            connect.commit()

        text=f'收到您上傳的照片囉! 請問您上傳食材是{result}? (是/不是)'
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text))
        

@handler.add(PostbackEvent)
def postback_event(event):
    data = event.postback.data
    if data == 'richmenu-changed-to-recomm':
        text = '歡迎使用食譜推薦系統~\n\n若您選擇清冰箱模式，我們會使用您冰箱現有的全部食材做推薦\n\n若您選擇關鍵字模式，您可以透過手動輸入食材名稱做食譜推薦'
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text))
        
    elif data == 'richmenu-changed-to-fridge':
        text = '您已進入到智能冰箱~\n\n您可以查看冰箱現有的食材，或上傳食材圖片來新增食材'
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text)) 
        
    elif data == 'richmenu-changed-to-home':
        text = '回功能選單首頁'
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text)) 
        

        
# run app
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.environ['PORT'])