import streamlit as st
from streamlit_option_menu import option_menu
import pickle

st.set_page_config(layout="wide")


def fetch_poster(game_id):
    return "https://cdn.cloudflare.steamstatic.com/steam/apps/{}/header.jpg".format(game_id)


def fetch_storePage(game_name):
    game_id = games_list[games_list['appname'] == game_name].index[0]
    return game_id


def recommend(game):
    game_index = games_list[games_list['appname'] == game].index[0]
    distances = similarity[game_index]
    games_list1 = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:2]

    recommended_games = []
    recommended_games_posters = []
    for i in games_list1:
        game_id = games_list.iloc[i[0]].appid
        recommended_games.append(games_list.iloc[i[0]].appname)
        recommended_games_posters.append(fetch_poster(game_id))
    return recommended_games, recommended_games_posters


def recommend_for_single(game):
    game_index = games_list[games_list['appname'] == game].index[0]
    distances = similarity[game_index]
    games_list1 = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_games = []
    recommended_games_posters = []
    for i in games_list1:
        game_id = games_list.iloc[i[0]].appid
        recommended_games.append(games_list.iloc[i[0]].appname)
        recommended_games_posters.append(fetch_poster(game_id))
    return recommended_games, recommended_games_posters


def recommend_for_double(game):
    game_index = games_list[games_list['appname'] == game].index[0]
    distances = similarity[game_index]
    games_list1 = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:3]

    recommended_games = []
    recommended_games_posters = []
    for i in games_list1:
        game_id = games_list.iloc[i[0]].appid
        recommended_games.append(games_list.iloc[i[0]].appname)
        recommended_games_posters.append(fetch_poster(game_id))
    return recommended_games, recommended_games_posters


games_list = pickle.load(open('games.pkl', 'rb'))
games = games_list['appname'].values

similarity = pickle.load(open('similarity.pkl', 'rb'))

trending = pickle.load(open('trending_games.pkl', 'rb'))

forever = pickle.load(open('popular_forever.pkl', 'rb'))

lastWeek = pickle.load(open('popular_lastWeek.pkl', 'rb'))

with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu",
        options=["Game Recommendation", "Trending", "Popular Games"],
    )

if selected == "Trending":
    st.title('Trending')
    for i in range(5):
        col1, col2, col3 = st.columns(3)
        if i == 0:
            cols = {0: col1, 1: col2, 2: col3}
        elif i == 1:
            cols = {3: col1, 4: col2, 5: col3}
        elif i == 2:
            cols = {6: col1, 7: col2, 8: col3}
        elif i == 3:
            cols = {9: col1, 10: col2, 11: col3}
        else:
            cols = {12: col1, 13: col2, 14: col3}
        for key in cols:
            with cols[key]:
                appid = trending["appid"][key]
                poster = fetch_poster(trending["appid"][key])
                st.markdown("[![Foo]({0})](https://store.steampowered.com/app/{1})".format(poster, appid))
                st.text(trending["name"][key])

if selected == "Popular Games":
    st.title('Popular Games')
    selected_category = st.selectbox(
        "Select Category",
        ["All Time Popular", "Popular Last Week"]
    )
    if st.button('Enter'):
        if selected_category == "All Time Popular":
            for i in range(20):
                col1, col2 = st.columns(2)
                cols = {0: col1, 1: col2}
                for key in cols:
                    with cols[key]:
                        if key == 0:
                            poster = fetch_poster(forever["appid"][i])
                            st.markdown("[![Foo]({0})](https://store.steampowered.com/app/{1})".format(poster,
                                                                                                       forever["appid"][
                                                                                                           i]))
                        else:
                            st.text("Developer: " + forever["developer"][i])
                            st.text("Publisher: " + forever["publisher"][i])
                            st.text("Genre: " + forever["genre"][i])
                            st.text("Rating: " + str(forever["review_score"][i]))
        if selected_category == "Popular Last Week":
            for i in range(20):
                col1, col2 = st.columns(2)
                cols = {0: col1, 1: col2}
                for key in cols:
                    with cols[key]:
                        if key == 0:
                            poster = fetch_poster(lastWeek["appid"][i])
                            st.markdown("[![Foo]({0})](https://store.steampowered.com/app/{1})".format(poster, lastWeek[
                                "appid"][i]))
                        else:
                            st.text("Developer: " + lastWeek["developer"][i])
                            st.text("Publisher: " + lastWeek["publisher"][i])
                            st.text("Genre: " + lastWeek["genre"][i])
                            st.text("Rating: " + str(lastWeek["review_score"][i]))

if selected == "Game Recommendation":
    st.title('Game Recommender System')

    games_ = st.multiselect("Select Games", games)

    if st.button('Recommend'):
        if len(games_) == 1:
            names, posters = recommend_for_single(games_[0])

            for i in range(5):
                col1, col2 = st.columns(2)
                cols = {0: col1, 1: col2}
                for key in cols:
                    with cols[key]:
                        if key == 0:
                            appid = fetch_storePage(names[i])
                            store_link = games_list.iloc[appid].appid
                            st.markdown(
                                "[![Foo]({0})](https://store.steampowered.com/app/{1})".format(posters[i], store_link))
                            st.text(games_list.iloc[appid].appname)
                        else:
                            id = games_list["appid"][appid]
                            index = forever.index[forever["appid"] == id].tolist()
                            index = index[0]

                            st.text("Developer: " + forever.loc[index, "developer"])
                            st.text("Publisher: " + forever.loc[index, "publisher"])
                            st.text("Genre: " + forever.loc[index, "genre"])
                            st.text("Rating: " + str(forever.loc[index, "review_score"]))
                            st.text("Upvotes : " + str(forever.loc[index, "positive"]) + "\t" + "Downvotes : " + str(
                                forever.loc[index, "negative"]))

        if len(games_) == 2:
            for game in games_:
                names, posters = recommend_for_double(game)

                for i in range(2):
                    col1, col2 = st.columns(2)
                    cols = {0: col1, 1: col2}
                    for key in cols:
                        with cols[key]:
                            if key == 0:
                                appid = fetch_storePage(names[i])
                                store_link = games_list.iloc[appid].appid
                                st.markdown(
                                    "[![Foo]({0})](https://store.steampowered.com/app/{1})".format(posters[i],
                                                                                                   store_link))
                                st.text(games_list.iloc[appid].appname)
                            else:
                                id = games_list["appid"][appid]
                                index = forever.index[forever["appid"] == id].tolist()
                                index = index[0]

                                st.text("Developer: " + forever.loc[index, "developer"])
                                st.text("Publisher: " + forever.loc[index, "publisher"])
                                st.text("Genre: " + forever.loc[index, "genre"])
                                st.text("Rating: " + str(forever.loc[index, "review_score"]))
                                st.text(
                                    "Upvotes : " + str(forever.loc[index, "positive"]) + "\t" + "Downvotes : " + str(
                                        forever.loc[index, "negative"]))

        if len(games_) > 2:
            for game in games_:
                names, posters = recommend(game)

                col1, col2 = st.columns(2)
                cols = {0: col1, 1: col2}

                for key in cols:
                    with cols[key]:
                        if key == 0:
                            appid = fetch_storePage(names[0])
                            store_link = games_list.iloc[appid].appid
                            st.markdown("[![Foo]({0})](https://store.steampowered.com/app/{1})".format(posters[0],
                                                                                                       store_link))
                            st.text(games_list.iloc[appid].appname)
                        else:
                            id = games_list["appid"][appid]
                            index = forever.index[forever["appid"] == id].tolist()
                            index = index[0]

                            st.text("Developer: " + forever.loc[index, "developer"])
                            st.text("Publisher: " + forever.loc[index, "publisher"])
                            st.text("Genre: " + forever.loc[index, "genre"])
                            st.text("Rating: " + str(forever.loc[index, "review_score"]))
                            st.text("Upvotes : " + str(forever.loc[index, "positive"]) + "\t" + "Downvotes : "
                                    + str(forever.loc[index, "negative"]))
