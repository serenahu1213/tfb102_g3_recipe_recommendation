import pymysql
import pymysql.cursors
from  datetime import datetime as dt


def deposit_ing(uuid,ing,amount):

    connection = pymysql.connect(host='localhost',
                             user='root',
                             password='root',
                             database='recipe_db',
                             cursorclass=pymysql.cursors.DictCursor)
    cursor=connection.cursor()
    
    if ing[0] != 'I':
        # find ingredient ID
        sql_FindID = f'select ingredientID from ingredient_info where ingredientName = "{ing}"'
        cursor.execute(sql_FindID)
        ingID = cursor.fetchone()['ingredientID']
    else : 
        ingID = ing

    date = dt.today().strftime('%Y/%m/%d %H:%M:%S')

    # check inventory
    sql_inventory = f'select * from refrigerator_info where (uuid = "{uuid}") and (ingredientID = "{ingID}")'
    cursor.execute(sql_inventory)
    inventory_result = cursor.fetchall()
    if len(inventory_result) == 0:
        if amount > 0:
            sql_insert = f'insert into refrigerator_info (uuid, ingredientID, amount, total_amount, date) \
                values ("{uuid}","{ingID}",{amount},"{amount}","{date}")'
            cursor.execute(sql_insert)
            connection.commit()
            connection.close()

            return f'{ing} {amount}克 已被存進您的冰箱 ! '
        else:
            return 'no action executed.'

    else:
        sql_find_last = f'select total_amount from refrigerator_info where  (uuid = "{uuid}") and \
            (ingredientID = "{ingID}") order by id desc limit 1'
        cursor.execute(sql_find_last)
        total_amount_result = cursor.fetchone()
        if total_amount_result['total_amount'] + amount >= 0:
            new_total_amount = amount + total_amount_result['total_amount']
            # insert data into table
            sql_insert = f'insert into refrigerator_info (uuid, ingredientID, amount, total_amount, date) \
                values ("{uuid}","{ingID}",{amount},"{new_total_amount}","{date}")'
            cursor.execute(sql_insert)
            connection.commit()
            connection.close()        

            return f'{ing} {amount}克 庫存更新 ! '
        else:
            new_total_amount = 0
            sql_insert = f'insert into refrigerator_info (uuid, ingredientID, amount, total_amount, date) \
                values ("{uuid}","{ingID}",{amount},"{new_total_amount}","{date}")'
            cursor.execute(sql_insert)
            connection.commit()
            connection.close()   

            diff = abs(total_amount_result['total_amount'] + amount)

            return f'{ing} 不夠 {diff} 克'
    

if __name__ == '__main__':
    print(deposit_ing('U7e21d301d0c71ced924939c2546462c2','蝦子',200))
    print(deposit_ing('U7e21d301d0c71ced924939c2546462c2','藍莓',+100))
    

