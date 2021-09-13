import pandas as pd
import numpy as np
import pymysql
import logging
import json
from ast import literal_eval
import random

# 連結資料庫
def connectDb(dbName):
    # 資料庫設定
    db_settings = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "spark",
    "password": "1qaz@wsX",
    "db": dbName,
    "charset": "utf8"
    }

    try:
        # 建立Connection物件
        mysqldb = pymysql.connect(**db_settings)
        return mysqldb
    except Exception as e:
        logging.error('Fail to connection mysql {}'.format(str(e)))
    return None


# 獲得 user 對各食譜 cluster 的愛好分數
def user_scores(user_id, method):
    db = connectDb('recipe_db')
    with db.cursor() as cursor:
        command = "SELECT * FROM user_scores where name = '{}'".format(user_id)

        # 執行指令
        cursor.execute(command)

        # 取得 user_id 的 user_scores 資料 (('test1', 2, 0, 1, 1, 0),)
        user_cluster = cursor.fetchall()[0][1:]
    db.close()

    if method == 1 :
        # Method 1
        # 根據 max 的分數，找出對應的 cluster
        cluster = [i for i, score in enumerate(user_cluster) if score == max(user_cluster) ]
    elif method == 2:
        # Method 2
        # 正規化 user_scores
        cluster = [score/sum(user_cluster) for score in user_cluster]
    else:
        print('method Error')

    return cluster

# jaccard 搭配 user 喜好的食譜推薦法
def recommender(input_list, user_id, method):

    # load dish name vs ingredient list as df 
    df = pd.read_csv('dishid_ingredient.csv')

    # jaccard_similarity : "input 食材" 與 "食譜食材" 的 len(交集) / len(聯集) 比 
    def jaccard_similarity(x):
        x = literal_eval(x)
        return len(set(x) & set(input_list)) / len(set(x) | set(input_list))

    # 使用 jaccard_similarity 計算 輸入食材與各食譜間的相似分數
    df['sim_score'] = df['ingredientName'].apply(lambda x: jaccard_similarity(x))
    df = df.drop(columns = 'ingredientName')
    

    if method == 1:
        ### Method 1
        # 找出 user 喜好的群 (user_scores) 的食譜，並依照相似分數 (sim_score) 排序
        df = df[df['cluster'].isin(user_scores(user_id, method))].sort_values('sim_score', ascending=0)
        
        # 根據排序後的結果，取前 5 種食譜返回使用者
        # 若所有比對分數皆 = 0，表示使用者輸入的食材沒有食譜與其相似
        # 此時以 隨機的方式取數種食譜返回給使用者 
        if df['sim_score'][0] == 0:
            output_dish = [ int(df.iloc[random.randint(1, len(df))]['dishId']) for _ in range(5)]
        else:
            df = df.iloc[0:5]['dishId']
            output_dish = [_ for _ in df]

    elif method == 2:
        ### Method 2 
        # 相似度 + user_score (正規化後的)，最後排序分數 = [0 ~ 2] 之間，再進行排序推薦
        for i, scores in enumerate(user_scores(user_id, method)):
            # find which index are same cluster(i)
            cluster_check_df = df['cluster'].isin([i])
            one_cluster_df = df[cluster_check_df]

            # df.['sim_score'][row(index)] = one_cluster_df['sim_score'] + cluster_score
            df['sim_score'].iloc[one_cluster_df.index] = one_cluster_df['sim_score'] + scores   
        
        df = df.sort_values('sim_score', ascending=0)
        df = df.iloc[0:5]['dishId']
        output_dish = [_ for _ in df]
    else:
        print('Method used Error, only 1 or 2.')

    return output_dish


if __name__ == '__main__':
    input_list = ['蒜頭', '西洋芹', '蝦子'] #  ['アジ']
    dish_ingredient = pd.read_csv('dishid_ingredient.csv')
    # dish_ingredient = dish_ingredient.set_index('dishId')

    user_id = 'test3'
    method = 2
    user_cluster = user_scores(user_id, method )
    output_dish = recommender(input_list, user_id, method)
    print(output_dish)