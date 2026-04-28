import streamlit as st
import seaborn as sns
import preprocessor, helper
import matplotlib.pyplot as plt
import pandas as pd
st.markdown("""
<style>
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

st.sidebar.title("Whatsapp Chat Analyzer")
theme = st.sidebar.selectbox("🎨 Select Theme", ["Light", "Dark", "Multicolor"])

if theme == "Dark":
    st.markdown("""
    <style>
    .stApp {
        background-color: #0E1117;
        color: white;
    }
    section[data-testid="stSidebar"] {
        background-color: #161B22;
    }
    </style>
    """, unsafe_allow_html=True)

elif theme == "Light":
    # Light theme
    st.markdown("""
       <style>
       .stApp {
           background-color: white;
           color: black;
           font_color: black;
       }
       </style>
       """, unsafe_allow_html=True)
#Default multicolor theme
else:
    st.markdown("""
        <style>

        /* Animated Gradient Background */
        .stApp {
            background: linear-gradient(-45deg, #667eea, #764ba2, #ff758c, #43cea2);
            background-size: 400% 400%;
            animation: gradientBG 10s ease infinite;
            color: white;
            transition: all 0.5s ease;
        }

        @keyframes gradientBG {
            0% {background-position: 0% 50%;}
            50% {background-position: 100% 50%;}
            100% {background-position: 0% 50%;}
        }

        /* Sidebar */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #141E30, #243B55);
            transition: all 0.4s ease;
        }

        /* Buttons (gesture-like hover effect) */
        .stButton > button {
            background: linear-gradient(90deg, #ff7e5f, #feb47b);
            color: white;
            border-radius: 10px;
            border: none;
            padding: 10px 18px;
            transition: all 0.3s ease;
        }

        .stButton > button:hover {
            transform: scale(1.05);
            background: linear-gradient(90deg, #43cea2, #185a9d);
        }

        /* Cards / Metrics hover effect */
        [data-testid="metric-container"] {
            background: linear-gradient(135deg, #ff9a9e, #fad0c4);
            padding: 15px;
            border-radius: 12px;
            transition: transform 0.3s ease;
            color: black;
        }

        [data-testid="metric-container"]:hover {
            transform: translateY(-5px);
        }

        /* Smooth text */
        h1, h2, h3, p {
            transition: all 0.3s ease;
        }

        </style>
        """, unsafe_allow_html=True)


# 🔥 Header (TOP)
st.markdown("""
<style>
.header {
    background: linear-gradient(90deg, #6a11cb, #2575fc);
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    color: white;
    margin-bottom: 20px;
}
</style>

<div class="header">
    <h1>📊 WhatsApp Chat Analyzer</h1>
    <p>Analyze chats • Visualize data • Gain insights</p>
</div>
""", unsafe_allow_html=True)

# Theme


# st.title("📊 WhatsApp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")

# ✅ Welcome screen
if uploaded_file is None:
    st.markdown("""
    <div style="
        padding:20px;
        border-radius:12px;
        background: rgba(0,0,0,0.2);
        text-align:center;
        backdrop-filter: blur(10px);
    ">
        <h2>👋 Welcome!</h2>
        <p>..Go to the side bar..<p>
        <p>Upload your WhatsApp chat file to get started.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="
        margin-top:20px;
        padding:15px;
        border-radius:10px;
        background: rgba(0,0,0,0.2);
    ">
    <b>✨ Features:</b><br>
    📅 Monthly & Daily Timeline<br>
    📊 Activity Map<br>
    ☁️ Word Cloud<br>
    😂 Emoji Analysis<br>
    👤 Most Busiest User<br>
    🔤 Most Common Words
    </div>
    """, unsafe_allow_html=True)




# uploaded_file = st.sidebar.file_uploader("Choose a file")
else:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    #st.text(data)
    df = preprocessor.preprocess(data)

    # Date filter
    st.sidebar.subheader("📅 Filter by Date")
    start_date = st.sidebar.date_input("Start Date")
    end_date = st.sidebar.date_input("End Date")

    df["only_date"] = pd.to_datetime(df["only_date"])

    if start_date and end_date:
        df = df[(df["only_date"] >= pd.to_datetime(start_date)) &
                (df["only_date"] <= pd.to_datetime(end_date))]

    # fetch unique users
    user_list = df["user"].unique().tolist()
    user_list = [user for user in user_list if user != "group_notification"]
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Select a user", user_list)

    if st.sidebar.button("Show Analysis"):
        num_messages, words, num_media_messages, num_links, = helper.fetch_stats(selected_user, df)
        st.title(f"Top Statistics of {selected_user}")
        col1, col2, col3, col4 =st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)

        with col3:
            st.header("Total Media Messages")
            st.title(num_media_messages)

        with col4:
            st.header("Total Links")
            st.title(num_links)

        # monthly timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline["time"], timeline["message"], color="purple", marker='o')
        plt.xticks(rotation=90)
        plt.xlabel("Months")
        plt.ylabel("No of Messages")
        plt.title("Month wise message Data")
        st.pyplot(fig)


        # daily timeline
        st.title("Daily Timeline")

        daily_data = helper.daily_timeline(selected_user, df)

        if daily_data.empty:
            st.warning("No data available")
        else:
            fig, ax = plt.subplots(figsize=(10, 5))

            ax.plot(daily_data["only_date"], daily_data["message"], marker='o')

            plt.xticks(rotation=45)
            plt.xlabel("Days")
            plt.ylabel("No of Messages")
            plt.title("Day wise message Data")

            plt.tight_layout()

            st.pyplot(fig)


        # weekly activity map
        st.title("Activity Map")
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most Busiest Day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, width=0.8, color="gray")

            plt.tight_layout()
            plt.xticks(rotation=45)
            plt.xlabel("Days")
            plt.ylabel("No of Messages")
            st.pyplot(fig)

        with col2:
            st.header("Most Busiest Month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, width=0.8, color="#67c9c6")

            plt.tight_layout()
            plt.xticks(rotation=45)
            plt.xlabel("Month")
            plt.ylabel("No of Messages")
            st.pyplot(fig)

        st.title("Weekly Activity Heatmap")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap, annot=False, cmap="YlOrRd")
        st.pyplot(fig)


        # finding the busiest users in the group (Group level)
        if selected_user == "Overall":
            st.title("Most Busiest User")
            x, new_df = helper.most_busy_user(df)
            fig, ax = plt.subplots()
            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, width=0.8)
                plt.title("Most Busiest User")
                plt.xticks(rotation=45)
                plt.tight_layout()
                plt.xlabel("Detail of User")
                plt.ylabel("No of Messages")
                plt.tight_layout()
                plt.show()
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df, height=260, use_container_width=350)

        # WordCoud
        st.title("Word Cloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)


        # Most Common Words
        most_common_df= helper.most_common_words(selected_user, df)
        fig, ax = plt.subplots(figsize=(6, 4))

        ax.barh(most_common_df["word"], most_common_df["count"])

        ax.set_ylabel("Words")
        ax.set_xlabel("Frequency")
        ax.set_title("Most Common Words")

        plt.xticks(rotation=45)

        st.pyplot(fig)

        # emoji Analysis

        emoji_df = helper.emoji_helper(selected_user, df)
        st.title("Emoji Analysis")

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df, use_container_width=300, height=350)

        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")
            st.pyplot(fig)



        # Download section
        st.markdown("""
        <style>
        div.stDownloadButton > button {
            background: linear-gradient(90deg, #ff7e5f, #feb47b);
            color: white;
            border-radius: 10px;
            padding: 10px 20px;
            border: none;
            font-size: 16px;
            transition: all 0.3s ease;
        }
        div.stDownloadButton > button:hover {
            transform: scale(1.05);
            background: linear-gradient(90deg, #43cea2, #185a9d);
        }
        </style>
        """, unsafe_allow_html=True)

        csv = df.to_csv(index=False).encode('utf-8')

        st.download_button(
            "⬇️ Download Data",
            data=csv,
            file_name="chat_analysis.csv",
            mime="text/csv"
        )



        # divider line
        st.markdown("""
        <div style="
            margin-top:40px;
            padding:10px;
            border-radius:10px;
            text-align:center;
            background: rgba(255,255,255,0.1);
            font-weight:bold;
        ">
            📊 End of Analysis
        </div>
        """, unsafe_allow_html=True)


# Footer stylin
st.markdown("""
<style>
.footer {
    margin-top: 60px;
    padding: 15px;
    text-align: center;
    font-size: 14px;
    color: #3C2C40;
}
</style>

<div class="footer">
    Made with ❤️ by <b>Shahnwaz</b><br>
    📊 WhatsApp Chat Analyzer
</div>
""", unsafe_allow_html=True)