import pymysql


def recommAll(dishIDs):
    result = []
    for i in dishIDs:
        result.append(recommOne(i))
    return result


def recommOne(dishID):
    conn = pymysql.connect(
                    host="127.0.0.1",
                    port=3306,
                    user="root",
                    passwd="root",
                    database="recipe_db",
                    charset='utf8mb4'
            )

    cursor = conn.cursor()

    sql1 = f'SELECT dishID, dishName, imageUrl \
            FROM recipe_info \
            WHERE dishID = {dishID}'

    sql2 = f'SELECT i.ingredientName, r.original_amount \
            FROM recipe_ingredient r \
            JOIN ingredient_info i ON r.ingredientID = i.ingredientID \
            JOIN nutrition_info n ON i.nutritionID = n.nutritionID \
            WHERE dishID = {dishID}'

    sql3 = f'SELECT format(sum(i.price*r.ETL_amount),0), format(sum(n.calories*r.ETL_amount),2) \
            FROM recipe_ingredient r \
            JOIN ingredient_info i ON r.ingredientID = i.ingredientID \
            JOIN nutrition_info n ON i.nutritionID = n.nutritionID \
            WHERE dishID = {dishID} \
            GROUP BY dishID'


    cursor.execute(sql1)
    result1 = cursor.fetchall()

    cursor.execute(sql2)
    result2 = cursor.fetchall()

    cursor.execute(sql3)
    result3 = cursor.fetchall()

    all_info = []
    for i in result1:
        all_info.append(i[0])
        all_info.append(i[1])
        all_info.append(i[2])

    pair = []    
    for j in result2:
        pair.append(j)
    pair = "\n".join(map(lambda x: x[0] + ': ' + x[1], pair))
    all_info.append(pair)
    
    for k in result3:
        all_info.append(k[0])
        all_info.append(k[1])

    conn.close()

    return all_info

if __name__ == "__main__":
    print(recommAll([13962, 13966, 13981, 14004, 14005]))