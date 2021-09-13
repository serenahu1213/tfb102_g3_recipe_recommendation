from flask import Flask, request, abort, render_template

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

from ast import literal_eval

import pymysql

from recomm_recipes_carousel import *
from recomm_recipes import *
from check_inventory import *
from deposit import *
from call_md import *
from check_recipe_ingredient import *
from jaccard_similarity_recommender import *

import tempfile, os, random, string
import datetime
import time
import re


app = Flask(__name__)
line_bot_api = LineBotApi('Dlow55NwMhUOqXBgYlZuekbQ9nvZLJd/M7SR1SNIDN/t/hYYD8kV1hILjwb2irfVRZTGiBzdquXcdNPTe8uBHXUe1yl1qB6tTOpv/u+CPsx58YwuGEM1yRkqyS98beU5DAUhjACw5R+vSizOV4UorwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('1ee56998faf23a84ff21c58a9e829d02')
image_tmp_path = os.path.join(os.getcwd(), 'static').replace('\\','/')

connect = pymysql.connect(
                host="127.0.0.1",
                user="spark",
                passwd="1qaz@wsX",
                port=3306,
                database="recipe_db",
                charset='utf8mb4',
        )

cursor = connect.cursor()

def save_recomm_dishIDs(user_id, dishIDs):
    cursor.execute(f'select * from recommened_dishIDs where user_id = "{user_id}"')
    result = cursor.fetchall()

    if len(result) == 0:
        command = f'insert into recommened_dishIDs (user_id, dishIDs) values ("{user_id}", "{dishIDs}")'
        cursor.execute(command)
        connect.commit()

    else:
        command = f'update recommened_dishIDs set dishIDs = "{dishIDs}" WHERE user_id = "{user_id}"'
        cursor.execute(command)
        connect.commit()

        
def load_recomm_dishIDs(user_id):
    cursor.execute(f'select * from recommened_dishIDs where user_id = "{user_id}"')
    dishIDs = cursor.fetchall()[0][1]
    dishIDs = literal_eval(dishIDs)
        
    return dishIDs


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
def handle_message_1(event):
    
    user_id = event.source.user_id
    user_name = line_bot_api.get_profile(user_id).display_name
    print(user_id)
    print(user_name)
    
    # for testing purpose
#     dishIDs = [13962, 13966, 13981, 14004, 14005]

    if event.message.type=='text':
        msg = event.message.text
        
        if msg in ['哈囉', '你好']:
            text='哈囉~ 歡迎使用食譜底呷啦！\n請至功能選單中填寫喜好問卷，讓我們為您推薦最適合您的菜色 :)'
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text))
            
            # =========================================================
            try:
#              # 連接MySQL
#              def get_conn():
#                  return pymysql.connect(
#                      host='127.0.0.1',
#                      user='spark',
#                      passwd='1qaz@wsX',
#                      port=3306,
#                      db='recipe_db',
#                      charset='utf8'
#              )
#              # insert
                def insert_or_update_data(sql):
                    conn = connect
                    try:
                        cursor = conn.cursor()
                        cursor.execute(sql)
                        conn.commit()
                    finally:
                        print('OK MySQL')
                # 填寫標單 ngrok+/cooklike 網址
                @app.route("/cooklike", methods=['GET'])
                def cookuser():
                    user = user_name #參數帶進去HTML
                    userid = user_id

                    return render_template("cooklike-01.html",user_Id = user, name_Id = userid)
            
                # 完成填寫表單，寫進MySQL
                @app.route("/do_add_user", methods=["POST"])
                def do_add_user():
                    print(request.form)
                    name = request.form.get("name")
                    like1 = int(request.form.get("like1"))
                    like2 = int(request.form.get("like2"))
                    like3 = int(request.form.get("like3"))
                    like4 = int(request.form.get("like4"))
                    like5 = int(request.form.get("like5"))
                    like6 = int(request.form.get("like6"))
                    like7 = int(request.form.get("like7"))
                    like8 = int(request.form.get("like8"))
                    like9 = int(request.form.get("like9"))
                    like10 = int(request.form.get("like10"))
            
                    cluster0 = (like1+like2)
                    cluster1 = (like3+like4)
                    cluster2 = (like5+like6)
                    cluster3 = (like7+like8)
                    cluster4 = (like9+like10)
            
                    sql = f"""
                        insert into user_scores (name, cluster_0, cluster_1, cluster_2, cluster_3, cluster_4)
                        values ('{name}', '{cluster0}', '{cluster1}', '{cluster2}', '{cluster3}', '{cluster4}')
                    """
                    insert_or_update_data(sql)
                    print(sql)
                    return "已完成填寫"
            finally:
                print("OK")
            # =========================================================           
        elif msg == '清冰箱模式':
            """
            code that can turn all ingres into a list
            """
            inventory = check_inventory(user_id)
            input_list = [_[0] for _ in inventory]

            dishIDs = recommender(input_list, user_id, 2)
            
            save_recomm_dishIDs(user_id, dishIDs)

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
            input_list = [_ for _ in msg.split(' ')[0:-1]]

            dishIDs = recommender(input_list, user_id, 2)
           
            save_recomm_dishIDs(user_id, dishIDs)

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
            dishIDs = load_recomm_dishIDs(user_id)

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

            dishIDs = load_recomm_dishIDs(user_id)

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
            
        elif msg == '上傳食材照片': 
            text='請上傳您的食材照片'
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text))
            
        elif msg == '輸入食材名稱': 
            text='請輸入正確食材名稱及重量(g)，並以空白鍵隔開\n\n例如: 番茄 100g'
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
            
        elif re.match(r'^[\u4E00-\u9FA5]+\s-\d+g$', msg):
            msg = msg.split(' ')
            ing = msg[0]
            amount = float(msg[1].replace('g',''))
            deposit_ing(user_id,ing,amount)
            """
            code that can calculate the remaining amount in fridge
            """
            text = f'deleted'
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
    app.run(host='127.0.0.1', port=12345)
