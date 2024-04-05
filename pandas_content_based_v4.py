#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
from functools import reduce
import pymongo
import pickle


# In[2]:


client = pymongo.MongoClient("mongodb://localhost:27017")


# In[3]:


db = client["project"]


# In[4]:


mycollection = db["games"]


# In[5]:


#print(mycollection)


# In[6]:


all_records = mycollection.find()


# In[7]:


#print(all_records)


# In[8]:


list_cursor = list(all_records)


# In[9]:


games = pd.DataFrame(list_cursor)


# In[10]:


#games.head(5)


# In[11]:


#games[games["name"] == 'Call of Duty: Ghosts']


# ### Data is used for popular tab

# In[12]:


popular_forever = games.sort_values(by=['positive'],ascending=False).head(2000)

popular_forever.reset_index(inplace = True, drop = True)

pickle.dump(popular_forever,open('/home/sooloow/game-recommender-system/popular_forever.pkl','wb'))


# In[13]:


popular_lastWeek = games.sort_values(by=['average_2weeks'],ascending=False).head(20)

popular_lastWeek.reset_index(inplace = True, drop = True)

pickle.dump(popular_lastWeek,open('/home/sooloow/game-recommender-system/popular_lastWeek.pkl','wb'))


# In[ ]:





# In[14]:


games = games.infer_objects()


# In[15]:


#games.dtypes


# In[16]:


games = games.sort_values(by=['positive'],ascending=False).head(2000)


# In[17]:


games.reset_index(inplace = True, drop = True)


# In[18]:


games['total_reviews'] = games['positive'] + games['negative']


# In[19]:


games = games[['appid', 'name','review_score', 'ccu', 'developer','positive', 'negative','total_reviews', 'genre', 'tags', 'review']]


# In[20]:


#games.head()


# In[21]:


#games.info()


# In[22]:


#games.isnull().sum()


# In[23]:


games.dropna(axis=0,inplace=True)


# In[24]:


#games[games['name'].duplicated()]


# In[25]:


games = games.drop_duplicates(subset='name',keep='first')


# In[26]:


games = games.loc[games['tags'].apply(len).gt(0)]
games = games.loc[games['review'].apply(len).gt(0)]


# In[27]:


#games.shape


# In[28]:


games.reset_index(inplace = True, drop = True)


# In[29]:


#games['review']


# In[30]:


#games.iloc[2].review


# In[31]:


import ast
def convert(obj):
    lst = []
    obj = ast.literal_eval(obj)
    for word in obj:
        lst.append(word.split(" "))
    return lst


# In[32]:


def convert2(obj):
    lst = obj.split(",")
    
    return lst


# In[33]:


import ast
def convert3(obj):
    lst = []
    obj = ast.literal_eval(obj)
    for words in obj:
           lst.append(words)
    return lst


# In[34]:


def convert4(obj):
    for i in obj:
        lst = []
        for j in i:
            lst.append(j)
    return lst


# In[35]:


#games['tags']


# In[36]:


games['review'].apply(convert4)


# In[37]:


games['tags'] = games['tags'].apply(convert3)
games['developer'] = games['developer'].apply(convert2)
games['genre'] = games['genre'].apply(convert2)
games['review'] = games['review'].apply(convert)
games['review'] = games['review'].apply(convert4)


# In[38]:


#games.head()


# In[39]:


games['review'].apply(lambda x:[i.replace(" ","") for i in x ])


# In[40]:


games['developer'] = games['developer'].apply(lambda x:[i.replace(" ","") for i in x ])
games['genre'] = games['genre'].apply(lambda x:[i.replace(" ","") for i in x ])
games['tags'] = games['tags'].apply(lambda x:[i.replace(" ","") for i in x ])
games['review'] = games['review'].apply(lambda x:[i.replace(" ","") for i in x ])


# In[41]:


#games.head()


# In[42]:


games['tag'] = games['developer'] + games['genre'] + games['tags'] + games['review']


# In[43]:


#games.head()


# #### Data is used for trending tab

# In[44]:


trending_games = games.sort_values(by=['ccu'],ascending=False).head(20)


# In[45]:


trending_games.reset_index(inplace = True, drop = True)


# In[46]:


trending_games = trending_games[["appid", "name", "review_score" ]]


# In[47]:


pickle.dump(trending_games,open('/home/sooloow/game-recommender-system/trending_games.pkl','wb'))


# In[ ]:





# In[48]:


new_df = games[['appid', 'name', 'tag']]


# In[49]:


#new_df.head()


# In[50]:


new_df['tag'] = new_df['tag'].apply(lambda x:" ".join(x))


# In[51]:


#new_df.head()


# In[52]:


#new_df['tag']


# In[53]:


new_df['tag'] = new_df['tag'].apply(lambda x:x.lower())


# In[54]:


#new_df.head()


# In[55]:


from nltk.stem.porter import PorterStemmer
ps = PorterStemmer()


# In[56]:


def stem(text):
    y = []
    for i in text.split():
        y.append(ps.stem(i))
    return " ".join(y)


# In[57]:


new_df['tag'] = new_df['tag'].apply(stem)


# In[58]:


#new_df['tag']


# In[59]:


#new_df['tag'][1]


# In[60]:


from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features=2000,stop_words='english')


# In[61]:


vectors = cv.fit_transform(new_df['tag']).toarray()


# In[ ]:





# In[62]:


#vectors[0]


# In[63]:


#cv.get_feature_names()


# In[64]:


from sklearn.metrics.pairwise import cosine_similarity


# In[65]:


similarity = cosine_similarity(vectors)


# In[66]:


sorted(list(enumerate(similarity[0])),reverse=True,key=lambda x:x[1])[1:6]


# In[67]:


def recommend(game):
    game_index = new_df[new_df['appname'] == game ].index[0]
    distances = similarity[game_index]
    games_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    for i in games_list:
        print(new_df.iloc[i[0]].appname)


# In[68]:


new_df.rename(columns = {'name':'appname'}, inplace = True)


# In[69]:


#new_df


# In[70]:


#recommend('Fallout: New Vegas')


# In[71]:


#new_df.iloc[999].appname


# In[72]:


pickle.dump(new_df,open('/home/sooloow/game-recommender-system/games.pkl','wb'))


# In[73]:


new_df['appname'].values


# In[74]:


pickle.dump(similarity,open('/home/sooloow/game-recommender-system/similarity.pkl','wb'))

