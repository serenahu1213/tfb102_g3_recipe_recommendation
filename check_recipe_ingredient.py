import pymysql
import pymysql.cursors
import tempfile, os, random, string

def check_recipe_ingredient(dishid,uuid):

    connection = pymysql.connect(host='localhost',
                             user='spark',
                             password='1qaz@wsX',
                             database='recipe_db',
                             port=3306,
                             cursorclass=pymysql.cursors.DictCursor)
    cursor=connection.cursor()

    you_have_list = []
    you_dont_have_list = []
    # look up user's inventory
    sql_refrige_lookup = f'SELECT  S1.INGREDIENTID fi , S2.INGREDIENTID ri FROM \
        (SELECT r1.uuid, r1.ingredientID ,i.ingredientName, r1.total_amount \
            FROM refrigerator_info r1 LEFT JOIN refrigerator_info r2 \
                ON (r1.uuid = r2.uuid and r1.ingredientID = r2.ingredientID and r1.id < r2.id) \
                    join ingredient_info i on r1.ingredientID = i.ingredientID \
                        where (r1.uuid = "{uuid}") and (r2.id IS NULL) and (r1.total_amount>0)) S1 \
                            LEFT JOIN (SELECT DISHID, INGREDIENTID FROM recipe_ingredient WHERE DISHID = {dishid}) S2 ON S1.INGREDIENTID=S2.INGREDIENTID \
                                UNION \
                                    SELECT S1.INGREDIENTID fi , S2.INGREDIENTID ri FROM \
                                        (SELECT r1.uuid, r1.ingredientID ,i.ingredientName, r1.total_amount \
                                            FROM refrigerator_info r1 LEFT JOIN refrigerator_info r2 \
                                                ON (r1.uuid = r2.uuid and r1.ingredientID = r2.ingredientID and r1.id < r2.id) \
                                                    join ingredient_info i on r1.ingredientID = i.ingredientID \
                                                        where (r1.uuid = "{uuid}") and (r2.id IS NULL) and (r1.total_amount>0)) S1 \
                                                            RIGHT JOIN (SELECT DISHID, INGREDIENTID FROM recipe_ingredient WHERE DISHID = {dishid}) S2 ON S1.INGREDIENTID=S2.INGREDIENTID;'

    cursor.execute(sql_refrige_lookup)
    query_inventory = cursor.fetchall()

    for inventory in query_inventory:
        if inventory['fi'] != None and inventory['ri'] != None:
            you_have_list.append(inventory['fi'])
        elif inventory['fi'] == None and inventory['ri'] != None:
            you_dont_have_list.append(inventory['ri'])

    conv_you_have_list = []
    conv_you_dont_have_list = []
    for i in you_have_list:
        convert_ingName = f'select ingredientName from ingredient_info where ingredientID = "{i}"'
        cursor.execute(convert_ingName)
        conv_ingName = cursor.fetchone()
        conv_you_have_list.append(conv_ingName['ingredientName'])
    for i in you_dont_have_list:
        convert_ingName = f'select ingredientName from ingredient_info where ingredientID = "{i}"'
        cursor.execute(convert_ingName)
        conv_ingName = cursor.fetchone()
        conv_you_dont_have_list.append(conv_ingName['ingredientName'])           

    

    return (conv_you_have_list,conv_you_dont_have_list)


if __name__ == '__main__' :
    print(check_recipe_ingredient(13962,'U7e21d301d0c71ced924939c2546462c2'))
