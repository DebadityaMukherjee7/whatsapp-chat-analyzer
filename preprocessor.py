import pandas as pd
import re
def preprocess(data):
    print(data)
    pattern='\d{2}/\d{2}/\d{2}, \d{1,2}:\d{2}\u202f(?:am|pm) -\s'
    messeges=re.split(pattern,data)
    messeges=messeges[2:]
    fixed1=[]
    for text in messeges:
        fixed1.append(text.replace("\n", " "))

    dates=re.findall(pattern,data)
    dates=dates[1:]
    fixed2=[]
    for text in dates:
        fixed2.append(text.replace("\u202f", " "))
    df=pd.DataFrame({'dates':fixed2,'user_messeges':fixed1})
    df['dates'] = df['dates'].str.replace('\u202f', ' ', regex=False).str.replace(' - ', '', regex=False)
    df['dates'] = pd.to_datetime(df['dates'], format='%d/%m/%y, %I:%M %p')
    users=[]
    messeges=[]
    for messege in df['user_messeges']:
        entry=re.split('([\w\W]+?):\s',messege)
        if entry[1:]:
            users.append(entry[1])
            messeges.append(entry[2])
        else:
            users.append('group_notification')
            messeges.append(entry[0])
    df['users']=users
    df['messeges']=messeges
    df.drop(columns=['user_messeges'],inplace=True)
    df['year'] = df['dates'].dt.year
    df['month'] = df['dates'].dt.month_name()
    df['day'] = df['dates'].dt.day
    df['hour'] = df['dates'].dt.hour
    df['minute'] = df['dates'].dt.minute
    df['month_num']=df['dates'].dt.month
    return df
f=open('WhatsApp Chat with Asmit.txt','r',encoding='utf-8')
data=f.read()
dataframe=preprocess(data)