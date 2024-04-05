#!/usr/bin/env python
# coding: utf-8

# In[1]:


from pyspark.sql import SparkSession


# In[2]:


spark = SparkSession \
    .builder \
    .appName("game-recommender-system") \
    .config("spark.mongodb.input.uri", "mongodb://127.0.0.1/project.games") \
    .config("spark.mongodb.output.uri", "mongodb://127.0.0.1/project.games") \
    .config('spark.jars.packages', 'org.mongodb.spark:mongo-spark-connector_2.12:3.0.1')\
    .config('spark.driver.memory', '3g')\
    .getOrCreate()


# In[3]:


# games = spark.read.json("/home/omkar/project/game-recommender-system/games/games.json")


# In[4]:


# games = spark.read.json("/home/omkar/project/game-recommender-system/games/games.json")
# tags = spark.read.json("/home/omkar/project/game-recommender-system/tags/tags.json")
# reviews = spark.read.json("/home/omkar/project/game-recommender-system/reviews/reviews.json")


# #### Temporary using pandas dataframe to spark dataframe

# In[5]:


import pandas as pd
games_df = pd.read_json("/home/sooloow/game-recommender-system/games/games.json")
tags_df = pd.read_json("/home/sooloow/game-recommender-system/tags/tags.json")
reviews_df = pd.read_json("/home/sooloow/game-recommender-system/reviews/reviews.json")
games_df = games_df.T
tags_df = tags_df.T
reviews_df = reviews_df.T
games_df.reset_index(drop=True, inplace=True)
tags_df.reset_index(drop=True, inplace=True)
reviews_df.reset_index(drop=True, inplace=True)
games_df[['score_rank']] = games_df[['score_rank']].astype(str)
tags_df[['tags']] = tags_df[['tags']].astype(str)
tags_df[['genre']] = tags_df[['genre']].astype(str)
reviews_df[['review_score']] = reviews_df[['review_score']].astype(str)
reviews_df[['review']] = reviews_df[['review']].astype(str)
tags_df = tags_df[['appid', 'genre', 'tags']]
reviews_df = reviews_df[["appid", "review_score", "review"]]
games = spark.createDataFrame(games_df)
tags = spark.createDataFrame(tags_df)
reviews = spark.createDataFrame(reviews_df)


# In[6]:


#games.show(1)


# In[7]:


games = games.drop("score_rank")
games = games.drop("userscore")


# In[8]:


#games.count()


# In[9]:


chcekNullValues = {col:games.filter(games[col].isNull()).count() for col in games.columns}
print(chcekNullValues)


# In[10]:


games = games.na.drop()


# In[11]:


#games.count()


# In[12]:


games.drop_duplicates()


# In[13]:


#games.count()


# In[14]:


#tags.show(15)


# In[15]:


#tags.count()


# In[16]:


chcekNullValues = {col:tags.filter(tags[col].isNull()).count() for col in tags.columns}
print(chcekNullValues)


# In[17]:


tags = tags.na.drop()


# In[18]:


#reviews.show(15)


# In[19]:


#reviews.select("review").filter(reviews.appid == 730).head()


# In[20]:


# reviews = reviews.drop("total_reviews")
# reviews = reviews.drop("total_negative")
# reviews = reviews.drop("total_positive")


# In[21]:


chcekNullValues = {col:reviews.filter(reviews[col].isNull()).count() for col in reviews.columns}
print(chcekNullValues)


# In[22]:


games = games.join(tags,["appid"]) \
     .join(reviews,["appid"])


# In[23]:


#games.show()


# In[24]:


#games.count()


# In[25]:


chcekNullValues = {col:games.filter(games[col].isNull()).count() for col in games.columns}
print(chcekNullValues)


# In[26]:


# games.sort(["review"], ascending=False).show(250)


# In[27]:


games = games.where(games.review != '[]')


# In[28]:


#games.count()


# In[29]:


games.where(games.tags != '[]').count()


# In[30]:


#games.show()


# In[31]:


#games.printSchema()


# In[32]:


from pyspark.sql.types import LongType


# In[33]:


games = games \
  .withColumn("price",
              games["price"]
              .cast(LongType()))    \
  .withColumn("initialprice"  ,
              games["initialprice"]
              .cast(LongType())) \
  .withColumn("discount"  ,
              games["discount"]
              .cast(LongType())) \
  .withColumn("review_score"  ,
              games["review_score"]
              .cast(LongType())) 


# In[34]:


games.write.format("mongo").mode("overwrite").option("database",
"project").option("collection", "games").save()


# In[35]:


spark.sparkContext.stop()
spark.stop()

