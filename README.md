# Steam-Game-Recommendation-Engine

Main aim of this project is to recommend similar games to the user based on his/her choice or preferences.

Problem Statement
A Game user (Gamer) spends lots of his time and efforts to find the best suitable games according to his/her preference. Yet he/she may not find appropriate games to play over the internet. To address this issue we are developing a game recommender system.

Objectives
The objective is to predict and recommend the best suitable games to the user according to the users choice to enhance the user experience and to reduce their time and efforts of searching similar games over the internet.

SYSTEM REQUIREMENTS
Hardware Requirements
● Platform – Ubuntu using wsl
● RAM – At least 8 GB of RAM,
● Peripheral Devices – Mouse, Keyboard
● A network connection for data recovery over the network.

Software Requirements
● Apache Airflow
● Apache Spark
● MongoDB
● Python Pandas (Machine Learning)
● Streamlit

METHODOLOGY
Data Retrieval
The Game data used in this project was obtained from https://steamspy.com/ an open source website. The data retrieval was scheduled using Apache Airflow. The downloaded data was in JSON format.

ETL Process in spark
For project work Spark was used to perform Extract, Transform, Load(ETL) processes on the retrieved data. As the data was obtained in json format the data needed to be cleaned( the process of detecting and correcting corrupt or inaccurate records from record set, tables or database and refers to identifying incomplete, incorrect, inaccurate or irrelevant parts of the data and then replacing, modifying, or deleting the dirty or coarse data). Merging of tables, checking and removing null and duplicate values, and applying a stemming process from the nltk library on the retrieved data was performed here in spark. Later the end result data was dumped directly from Spark into MongoDB.

Dumping Data in MongoDB
Data obtained after ETL process from spark was directly dumped into MongoDB. As the data was in json format we opted for MongoDB.

Machine Learning using Python Pandas
The processed data was used to train an algorithm which will recommend similar games according to users preference or choice. Vectorization algorithm was used to vectorize the games referring to the tags and reviews data with similar gameID. Cosine similarity technique was used to measure the similarity between the vectors so as to recommend the best vectors(games) as an end product. Thus a recommender system model was trained to always perform at maximum efficiency and recommend the best similar games.

Streamlit App Creation
An app for game recommendation system was created using streamlit an opensource app framework which provides a faster way to build and share data apps.

ALGORITHMS AND FORMULAS
Content-Based Filtering
In this type of recommendation system, relevant items are shown using the content of the previously searched items by the users. Here content refers to the attribute/tag of the product that the user likes. In this type of system, products are tagged using certain keywords, then the system tries to understand what the user wants and it looks in its database and finally tries to recommend different products that the user wants.
Let us take an example of the movie recommendation system where every movie is associated with its genres which in the above case is referred to as tag/attributes. Now let assume user A comes and initially the system doesn't have any data about user A. So initially, the system tries to recommend the popular movies to the users or the system tries to get some information about the user by getting a form filled by the user. After some time, users might have given a rating to some of the movies like it gives a good rating to movies based on the action genre and a bad rating to the movies based on the anime genre. So here the system recommends action movies to the users. But here you can’t say that the user dislikes animation movies because maybe the user dislikes that movie due to some other reason like acting or story but actually likes animation movies and needs more data in this case.

CountVectorizer
CountVectorizer is a great tool provided by the scikit-learn library in Python. It is used to transform a given text into a vector on the basis of the frequency (count) of each word that occurs in the entire text. This is helpful when we have multiple such texts, and we wish to convert each word in each text into vectors (for use in further text analysis).
CountVectorizer creates a matrix in which each unique word is represented by a column of the matrix, and each text sample from the document is a row in the matrix. The value of each cell is nothing but the count of the word in that particular text sample.

Cosine Similarity
Cosine similarity measures the similarity between two vectors of an inner product space. It is measured by the cosine of the angle between two vectors and determines whether two vectors are pointing in roughly the same direction. It is often used to measure document similarity in text analysis.

Bag of Words
In this article, we are going to discuss a Natural Language Processing technique of text modeling known as Bag of Words model. Whenever we apply any algorithm in NLP, it works on numbers. We cannot directly feed our text into that algorithm. Hence, the Bag of Words model is used to preprocess the text by converting it into a bag of words, which keeps a count of the total occurrences of most frequently used words. This model can be visualized using a table, which contains the count of words corresponding to the word itself

![image](https://github.com/not-harsh/Steam-Game-Recommendation-Engine/assets/141590635/a41a887e-4019-415b-a454-b9c3eccee01a)

CONCLUSION
The Game Recommender System recommends similar games according to users preferences or choices thus enhancing their user experience and reduces their time and efforts of searching similar games over the internet. The interactive UI developed in steamlit makes it simpler for users to search games.
