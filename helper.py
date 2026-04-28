import pandas as pd
from urlextract import URLExtract
extract = URLExtract()
from wordcloud import WordCloud
from collections import Counter
import emoji

def fetch_stats(selected_user, df):

    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    # fetch no of messages
    num_messages = df.shape[0]

    # fetch no of words
    words = []
    for message in df["message"]:
        words.extend(message.split())

    # fetch media omitted
    num_media_messages = df[df["message"] == "<Media omitted>\n"].shape[0]

    # fetch no of links
    links = []
    for message in df["message"]:
        links.extend(extract.find_urls(message))
    return num_messages, len(words), num_media_messages, len(links)


def most_busy_user(df):
    x = df["user"].value_counts().head()
    df = round((df["user"].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={"index": "Name", "user": "Percent"})
    return x,df

# WordCloud
def create_wordcloud(selected_user, df):
    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    wc = WordCloud(width=500, height=500, background_color="white", max_words=500, min_font_size=10)
    df_wc = wc.generate(df["message"].str.cat(sep=" "))

    return df_wc

# Most common words
def most_common_words(selected_user, df):

    with open("stopwords.txt", "r", encoding="utf-8") as f:
        stop_words = set(f.read().split())

    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    temp = df[df["user"] != "group_notification"]
    temp = temp[temp["message"] != "<Media omitted>\n"]

    words = []
    for message in temp["message"]:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(
        Counter(words).most_common(20),
        columns=["word", "count"]
    )

    return most_common_df

def emoji_helper(selected_user, df):
    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    emojis = []
    for message in df["message"]:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df

def monthly_timeline(selected_user, df):
    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    timeline = df.groupby(["year", "month_num", "month"]).count()["message"].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline["month"][i] + "-" + str(timeline["year"][i]))

    timeline["time"] = time
    return timeline


# daily timeline
def daily_timeline(selected_user, df):
    if selected_user != "Overall":
        df = df[df["user"] == selected_user]


    daily_df = df.groupby("only_date").size().reset_index(name="message")

    daily_df["only_date"] = pd.to_datetime(daily_df["only_date"])
    daily_df = daily_df.sort_values("only_date")

    return daily_df

def week_activity_map(selected_user, df):
    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    return df["day_name"].value_counts()

def month_activity_map(selected_user, df):
    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    return df["month"].value_counts()

def activity_heatmap(selected_user, df):
    if selected_user != "Overall":
        df = df[df["user"] == selected_user]

    user_heatmap = df.pivot_table(
        index="day_name",
        columns="period",
        values="message",
        aggfunc="count"
    ).fillna(0)

    return user_heatmap