import streamlit as st
import pandas as pd
import numpy as np
from preprocessor import preprocess
import newhelper as helper
import matplotlib.pyplot as plt

st.sidebar.title("WhatsApp Chat Analyzer")
file = st.sidebar.file_uploader("Upload your WhatsApp chat file", type=["txt"])
background_color=st.get_option("theme.backgroundColor")

if 'emojidf' not in st.session_state:
    st.session_state.emojidf = None
if 'most_common_df' not in st.session_state:
    st.session_state.most_common_df = None
if 'dataframe' not in st.session_state:
    st.session_state.dataframe = None
if 'selected_user' not in st.session_state:
    st.session_state.selected_user = None
if 'urls' not in st.session_state:
    st.session_state.urls = []

if file is not None:
    data = file.read().decode("utf-8")
    st.sidebar.text("File uploaded successfully!")
    st.session_state.dataframe = preprocess(data)


if st.session_state.dataframe is not None:
    st.dataframe(st.session_state.dataframe)
    unique_users = st.session_state.dataframe['users'].unique().tolist()
    if 'group_notification' in unique_users:
          unique_users.remove('group_notification')  
    unique_users.sort()  
    unique_users.append("Overall")  

    
    st.session_state.selected_user = st.sidebar.selectbox("Show analysis for user", unique_users)
    st.title("Monthly Activity Timeline:")
    fig = helper.plot_monthly_timeline(st.session_state.selected_user,st.session_state.dataframe)
    st.pyplot(fig)
    col1, col2 = st.columns(2)
    with col1:
        st.title("Daily Timeline:")
        fig = helper.plot_daily_timeline(st.session_state.selected_user,st.session_state.dataframe)
        st.pyplot(fig)
    with col2:
        st.title("Yearly Timeline:")
        fig = helper.plot_yearly_timeline(st.session_state.selected_user,st.session_state.dataframe)
        st.pyplot(fig)
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Most Busy Day:")
        fig = helper.plot_most_busy_day(st.session_state.selected_user, st.session_state.dataframe)
        st.pyplot(fig)
    with col2:
        st.subheader("Most Busy Month:")
        fig = helper.plot_most_busy_month(st.session_state.selected_user, st.session_state.dataframe)
        st.pyplot(fig)
    if st.sidebar.button("Show Analysis"):
        num_messages, words, media, urls = helper.fetch_stats(st.session_state.selected_user, st.session_state.dataframe)
        st.session_state.urls = urls  

        col1, col2, col3, col4 = st.columns(4)
        with col1:
                st.markdown(f"""
                    <div style='border:2px solid white;
                                padding:10px;
                                margin-bottom:15px;
                                border-radius:8px;
                                color:white;
                                font-size:18px;
                                width: fit-content'>
                        <b>{"Messages"}:</b> {num_messages}
                    </div>
                """, unsafe_allow_html=True)
                
        with col2:
            st.markdown(f"""
                    <div style='border:2px solid white;
                                padding:10px;
                                margin-bottom:15px;
                                border-radius:8px;
                                color:white;
                                font-size:18px;
                                width: fit-content'>
                        <b>{"All Words"}:</b> {words}
                    </div>
                """, unsafe_allow_html=True)
            
        with col3:
            st.markdown(f"""
                    <div style='border:2px solid white;
                                padding:10px;
                                margin-bottom:15px;
                                border-radius:8px;
                                color:white;
                                font-size:18px;
                                width: fit-content'>
                        <b>{"Media Shared"}:</b> {media}
                    </div>
                """, unsafe_allow_html=True)
            
            
        with col4:
            st.markdown(f"""
                    <div style='border:2px solid white;
                                padding:10px;
                                margin-bottom:15px;
                                border-radius:8px;
                                color:white;
                                font-size:18px;
                                width: fit-content'>
                        <b>{"Links Shared"}:</b> {len(urls)}
                    </div>
                """, unsafe_allow_html=True)
            
        if st.session_state.selected_user == "Overall":
            user_activity,newdf = helper.plot_bar(st.session_state.dataframe,background_color)
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Most Active Users")
                st.pyplot(user_activity)
            with col2:
                st.subheader("Percentage of Messages by User")
                st.dataframe(newdf)
        st.title(f"Word Cloud for {st.session_state.selected_user}")
        df_wc = helper.create_wordcloud(st.session_state.selected_user, st.session_state.dataframe)
        fig,ax= plt.subplots(figsize=(10, 5))
        ax.imshow(df_wc, interpolation='bilinear')
        st.pyplot(fig)

        st.session_state.most_common_df=helper.most_common_words(st.session_state.selected_user, st.session_state.dataframe)
        frequent_words = helper.plot_most_common_bar(st.session_state.most_common_df)
        col1,col2 = st.columns(2)
        with col1:
            st.subheader("Most common words")
            st.pyplot(frequent_words)
        with col2:
            st.subheader("Most common words DataFrame")
            st.dataframe(st.session_state.most_common_df)
        st.session_state.emojidf=helper.emoji_helper(st.session_state.selected_user, st.session_state.dataframe)
       
        
        fig, ax = plt.subplots(figsize=(10,5))

        colors = [
            "#ff4d6d","#ff758f","#ff8fa3","#ffb3c1",
            "#ffc2d1","#ffe5ec","#ffb703","#fb8500",
            "#8ecae6","#219ebc"
        ]

        wedges, texts, autotexts = ax.pie(
            st.session_state.emojidf['count'].head(10),
            labels=st.session_state.emojidf['emoji'].head(10),
            colors=colors,
            autopct='%1.1f%%',
            startangle=90,
            wedgeprops={
                'width':0.4,          
                'edgecolor':'black',
                'linewidth':1
            },
            textprops={'color':"white",'fontsize':12}
        )
        centre_circle = plt.Circle((0,0),0.60,fc='black',linewidth=1)
        ax.add_artist(centre_circle)

        ax.set_title('Most Common Emojis', color="red", fontsize=18)

        fig.patch.set_alpha(0.0)
        ax.patch.set_alpha(0.0)

        st.pyplot(fig)
      
        st.subheader("Emoji Analysis")
        st.dataframe(st.session_state.emojidf)
        text=helper.gemini_character_analysis(st.session_state.dataframe, st.session_state.selected_user)
        st.subheader("Character Analysis of the person:")
        st.write(text)


