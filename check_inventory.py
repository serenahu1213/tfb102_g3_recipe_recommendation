import pymysql
import pymysql.cursors

def check_inventory(uuid):

    connection = pymysql.connect(host='localhost',
                             user='root',
                             password='root',
                             database='recipe_db',
                             cursorclass=pymysql.cursors.DictCursor)
    cursor=connection.cursor()

    sql = f'SELECT r1.uuid, i.ingredientName, r1.total_amount \
        FROM refrigerator_info r1 LEFT JOIN refrigerator_info r2 \
            ON (r1.uuid = r2.uuid and r1.ingredientID = r2.ingredientID and r1.id < r2.id) \
                join ingredient_info i on r1.ingredientID = i.ingredientID \
                    where (r1.uuid = "{uuid}") and (r2.id IS NULL) and (r1.total_amount>0) ;'
    cursor.execute(sql)

    result = cursor.fetchall()

    ingredientlist = [ (x['ingredientName'],x['total_amount']) for x in result ]
    
    connection.close()

    return ingredientlist

if __name__ == '__main__':
    check_inventory('U7e21d301d0c71ced924939c2546462c2')