import seaborn as sns
import matplotlib.pyplot as plt
from urlextract import URLExtract
from wordcloud import WordCloud
extractor=URLExtract()
import pandas as pd
from collections import Counter
import emoji
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
import os
import streamlit as st
def fetch_stats(selected_user, df):
    if selected_user == "Overall":
        links=[]
        for messesge in df['messeges']:
            links.extend(extractor.find_urls(messesge))
        lenmed=len(df[df['messeges']=='<Media omitted> '])
        words=[]
        for message in df['messeges']:
            words.extend(message.split())
        num_messeges = df.shape[0]
        total_words = len(words)
        return num_messeges, total_words,lenmed,links
    else:
        links=[]
        for messesge in df[df['users'] == selected_user]['messeges']:
            links.extend(extractor.find_urls(messesge))
        lenmed = len(df[(df['users'] == selected_user) & (df['messeges'] == '<Media omitted> ')])
        user_df = df[df['users'] == selected_user]
        num_messeges = user_df.shape[0]
        words = []
        for message in user_df['messeges']:
            words.extend(message.split())
        total_words = len(words)
        return num_messeges, total_words,lenmed,links
def plot_pie( df):
    pie_data = df['users'].value_counts()
    return pie_data.plot.pie(autopct='%1.1f%%', figsize=(14, 5), title='User Distribution').get_figure()

import seaborn as sns
import matplotlib.pyplot as plt

def density_plot(selected_user, df):
    if selected_user == "Overall":
        print("Overall user selected, please select a specific user for density plot.")
        return None

    # Filter data for the selected user
    user_df = df[df['users'] == selected_user]

    if user_df.empty:
        print("No data available for the selected user.")
        return None

    hours = user_df['hour']
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.kdeplot(hours, fill=True, bw_adjust=0.8, ax=ax)
    ax.set_title(f"Activity Density Plot for {selected_user}")
    ax.set_xlabel("Hour of Day")
    ax.set_ylabel("Density")
    ax.set_xticks(range(0, 25))
    ax.grid(True)

    return fig


import matplotlib.pyplot as plt

def color(background_color):
    return "yellow"
def plot_bar(df,background_color):
    
    data = df['users'].value_counts().head(10)
    x = data.index
    y = data.values
    fig, ax = plt.subplots()
    ax.bar(x, y, color='blue',width=0.8)
    ax.set_xlabel('Users-->',color=color(background_color))
    ax.set_ylabel('Number of Messages-->',color=color(background_color))
    ax.set_title('Most Active Users', color=color(background_color))
    ax.set_xticklabels(x, rotation=90, ha='right', color=color(background_color))
    fig.patch.set_alpha(0.0)  
    ax.patch.set_alpha(0.0)
    ax.tick_params(colors=color(background_color))
    for spine in ax.spines.values():
        spine.set_color(color(background_color)) 
    return fig,round((df['users'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={"users":"name","count":"percent"}) # Return the figure object

def create_wordcloud(selected_user, df):
    if selected_user != "Overall":
        df = df[df['users'] == selected_user]
    
    wc = WordCloud(width=800, height=400, background_color='white', colormap='viridis').generate(' '.join(df['messeges']))
    return wc
def most_common_words(selected_user,df):
    f=open('stop_hinglish.txt','r')
    stop_words=f.read()
    if selected_user != "Overall":
        df = df[df['users'] == selected_user]
    temp=df[df['users'] != 'group_notification']
    temp=temp[temp['messeges'] != '<Media omitted>\n']
    words=[]
    for message in temp['messeges']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
    return pd.DataFrame(Counter(words).most_common(20),columns=['word','count'])
def plot_most_common_bar(df):
    x = df['word']
    y = df['count']
    fig, ax = plt.subplots()
    ax.bar(x, y, color='blue')
    ax.set_xlabel('Words',color="yellow")
    ax.set_ylabel('Number of Messages-->',color="yellow")
    ax.set_title('Most common Words', color="yellow")
    ax.set_xticklabels(x, rotation=90, ha='right', color="yellow")
    fig.patch.set_alpha(0.0)  # Entire figure
    ax.patch.set_alpha(0.0)
    ax.tick_params(colors="yellow")
    # Set border (spines) color to white
    for spine in ax.spines.values():
        spine.set_color("yellow")
    return fig
def emoji_helper(selected_user,df):
    if selected_user != "Overall":
        df = df[df['users'] == selected_user]
    emojis=[]
    for message in df['messeges']:
        emojis.extend([char for char in message if emoji.is_emoji(char)])
    return pd.DataFrame(Counter(emojis).most_common(20),columns=['emoji','count'])
def plot_monthly_timeline(selected_user,df):
    if selected_user != "Overall":
        df = df[df['users'] == selected_user]
    timeline=df.groupby(['year','month_num','month']).count()['messeges'].reset_index()
    time=[]
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i]+"-"+str(timeline['year'][i]))
    timeline['time']=time
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(timeline['time'], timeline['messeges'], marker='o', linestyle='-', color='blue')
    ax.set_title('Monthly Timeline of Messages', color="yellow")
    ax.set_xlabel('Time', color="yellow")
    ax.set_ylabel('Number of Messages', color="yellow")
    ax.tick_params(colors="yellow")
    plt.xticks(rotation=45)
    fig.patch.set_alpha(0.0)  
    ax.patch.set_alpha(0.0)
    for spine in ax.spines.values():
        spine.set_color("yellow")
    return fig
def plot_daily_timeline(selected_user,df):
    if selected_user != "Overall":
        df = df[df['users'] == selected_user]
    timeline=df.groupby('day').count()['messeges'].reset_index()
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(timeline['day'], timeline['messeges'], marker='o', linestyle='-', color='blue')
    ax.set_title('Daily Timeline of Messages', color="yellow")
    ax.set_xlabel('Day', color="yellow")
    ax.set_ylabel('Number of Messages', color="yellow")
    ax.tick_params(colors="yellow")
    plt.xticks(rotation=45)
    fig.patch.set_alpha(0.0)  
    ax.patch.set_alpha(0.0)
    for spine in ax.spines.values():
        spine.set_color("yellow")
    return fig
def plot_yearly_timeline(selected_user,df):
    if selected_user != "Overall":
        df = df[df['users'] == selected_user]
    timeline=df.groupby('year').count()['messeges'].reset_index()
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(timeline['year'], timeline['messeges'], marker='o', linestyle='-', color='blue')
    ax.set_title('Yearly Timeline of Messages', color="yellow")
    ax.set_xlabel('Year', color="yellow")
    ax.set_ylabel('Number of Messages', color="yellow")
    ax.tick_params(colors="yellow")
    plt.xticks(rotation=45)
    fig.patch.set_alpha(0.0)  
    ax.patch.set_alpha(0.0)
    for spine in ax.spines.values():
        spine.set_color("yellow")
    return fig
def plot_most_busy_day(selected_user,df):
    if selected_user != "Overall":
        df = df[df['users'] == selected_user]
    df['day_name'] = df['dates'].dt.day_name()
    busy_day=df['day_name'].value_counts().reset_index()
    busy_day.columns=['day_name','count']
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(busy_day['day_name'], busy_day['count'], color='blue')
    ax.set_title('Most Busy Day', color="yellow")
    ax.set_xlabel('Day Name', color="yellow")
    ax.set_ylabel('Number of Messages', color="yellow")
    ax.tick_params(colors="yellow")
    plt.xticks(rotation=45)
    fig.patch.set_alpha(0.0)  
    ax.patch.set_alpha(0.0)
    for spine in ax.spines.values():
        spine.set_color("yellow")
    return fig
def plot_most_busy_month(selected_user,df):
    if selected_user != "Overall":
        df = df[df['users'] == selected_user]
    busy_month=df['month'].value_counts().reset_index()
    busy_month.columns=['month','count']
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(busy_month['month'], busy_month['count'], color='blue')
    ax.set_title('Most Busy Month', color="yellow")
    ax.set_xlabel('Month', color="yellow")
    ax.set_ylabel('Number of Messages', color="yellow")
    ax.tick_params(colors="yellow")
    plt.xticks(rotation=45)
    fig.patch.set_alpha(0.0)  
    ax.patch.set_alpha(0.0)
    for spine in ax.spines.values():
        spine.set_color("yellow")
    return fig




api_key = st.secrets["GOOGLE_API_KEY"]
def gemini_character_analysis(df, selected_user="Overall"):
   
    if selected_user == "Overall":
        return "Cannot show analysis for all users together. Please select a specific user."

    
    messages = df[df['users'] == selected_user]['messeges'].astype(str).tolist()

   
    text_input = " ".join(messages[:200]) 

    
    chat = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash", 
        temperature=0.7,
        google_api_key=api_key
    )

  
    response = chat.invoke([
        HumanMessage(content=f"Analyze this person's communication style and traits based on these messages(explain in brief):\n{text_input}")
    ])

    return response.content

