from datetime import datetime
from re import S
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.bash_operator import BashOperator

import json
import requests


def get_games(**kwargs):  
    count = 0
    for i in range(0,57):
        try:
            response = requests.get("https://steamspy.com/api.php?request=all&page={}".format(i))
        except:
            continue
        data = response.text
        if(count == 0):
            
            parse_json = json.loads(data)
            count += 1
        else:
            parse_json1 = json.loads(data)
            parse_json.update(parse_json1)
    response = requests.get("https://steamspy.com/api.php?request=top100in2weeks")
    data = response.text
    parse_json1 = json.loads(data)
    parse_json.update(parse_json1)
    parse_json1 = sorted(parse_json.items(), key=lambda x:x[1]["positive"], reverse=True)
    parse_json2 = parse_json1[:2000]
    parse_json3 = {}
    for l in parse_json2:
        parse_json3[l[1]["appid"]] = l[1]
    with open("home/sooloow/game-recommender-system/games/games.json", "w") as outfile:
        json.dump(parse_json3, outfile)
    return parse_json3


def get_tags(**kwargs):
    ti = kwargs['ti']
    parse_json = ti.xcom_pull(task_ids='games')
    for key in parse_json:
        try:
            response = requests.get("https://steamspy.com/api.php?request=appdetails&appid={}".format(key))
        except:
            continue
        data = response.text
        try:
            data = json.loads(data)
        except:
            continue 
        lst = ["appid", "genre", "tags"]
        lst1 =  [parse_json[key]["appid"],data["genre"],data["tags"]]
        dic = dict(zip(lst, lst1))
        parse_json[key] = dic
    with open("home/sooloow/game-recommender-system/tags/tags.json", "w") as outfile:
        json.dump(parse_json, outfile)

        
def get_reviews(**kwargs):
    ti = kwargs['ti']
    parse_json = ti.xcom_pull(task_ids='games')	
    for key in parse_json:
        try:
            response = requests.get("https://store.steampowered.com/appreviews/{}?json=1&num_per_page=100".format(key))
        except:
            continue
        data = response.text
        try:
            data = json.loads(data)
        except:
            continue 
        lst = ["appid","review_score", "total_positive","total_negative","total_reviews", "review"]
        review = []
        for i in range(0,len(data["reviews"])):
            review.append(data["reviews"][i]["review"])
        lst1 = [parse_json[key]["appid"], data["query_summary"]["review_score"], data["query_summary"]["total_positive"], data["query_summary"]["total_negative"], data["query_summary"]["total_reviews"],  review]
        dic = dict(zip(lst, lst1))
        parse_json[key] = dic
    with open("home/sooloow/game-recommender-system/reviews/reviews.json", "w") as outfile:
        json.dump(parse_json, outfile)




dag = DAG('game-recommender-system1', description='Getting game data',
	schedule_interval = '@daily',
	start_date=datetime(2022, 9, 9), catchup=False)


games_operator = PythonOperator(task_id = 'games', python_callable = get_games, provide_context = True, dag = dag)

tags_operator = PythonOperator(task_id = 'tags', python_callable = get_tags, provide_context = True, dag = dag)

reviews_operator = PythonOperator(task_id = 'reviews', python_callable = get_reviews, provide_context = True, dag = dag)

etl_operataor = BashOperator(task_id = 'ETL', bash_command = "python3 /home/sooloow/game-recommender-system/spark_ETL.py", dag = dag)

ml_operataor = BashOperator(task_id = 'ML', bash_command = "python3 /home/sooloow/game-recommender-system/pandas_content_based_v4.py", dag = dag)


start = DummyOperator(task_id = 'start', retries = 0, dag = dag)

end = DummyOperator(task_id = 'end', retries = 0, dag = dag)

start >> games_operator >> [tags_operator, reviews_operator] >> etl_operataor >> ml_operataor >> end
