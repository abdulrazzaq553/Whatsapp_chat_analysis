import re
import pandas as pd

def start(data):
    # === NEW FEATURE ===
    # Fix multiline messages: join broken lines
    lines = data.split('\n')
    fixed_lines = []
    pattern = re.compile(r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[AP]M\s-\s')

    current_line = ""
    for line in lines:
        if pattern.match(line):
            # New message starts
            if current_line:
                fixed_lines.append(current_line)
            current_line = line
        else:
            # Continuation of previous message
            current_line += ' ' + line
    # Add last message
    if current_line:
        fixed_lines.append(current_line)

    # Convert back to single text
    data = '\n'.join(fixed_lines)
    # === END OF NEW FEATURE ===

    # --- Your existing logic ---
    pattern=('\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[AP]M\s-\s')
    message=re.split(pattern,data)[1:]
 
    dates=re.findall(pattern,data)
    df=pd.DataFrame({
    'Dates':dates,
    'Messages':message})
    user=[]
    message=[]
    for check in df['Messages']:
       entry=re.split('([\w\W]+?):\s',check)
       if entry[1:]:
         user.append(entry[1])
         message.append(entry[2])
       else:
          user.append('Group Notification')
          message.append(entry[0])

    df['User']=user
    df['Message']=message
    df.drop('Messages',axis=1,inplace=True)

    df[['test_time']]=pd.DataFrame(df['Dates'].str.split(', '))
    time=df['test_time'].str[0].str.split('/')

    df['Date']=time.str[1]
    df['Month']=time.str[0]
    df['Year']=time.str[2]
    time=df['test_time'].str[0].str.split(':')
    df['hour']=time.str[0]
    df['Minute']=time.str[1]

    df['Year'].replace({'21':'2021','22':'2022','23':'2023','24':'2024','25':'2025','26':'2026','27':'2027','28':'2028'},inplace=True)
    df['Month_Name']=df['Month'].replace({'1':'Jan','2':'Feb','3':'Mar','4':'Apr','5':'May','6':'Jun','7':'Jul','8':'Aug','9':'Sep','10':'Oct','11':'Nov','12':'Dec'})
    ok=df['Year']+'-'+df['Month']+'-'+df['Date']
    df['Day_Name']=pd.to_datetime(ok).dt.day_name()
    df.drop(['test_time','hour','Minute'],axis=1,inplace=True)
    df['Time'] = df['Dates'].str.split(', ').str[1]
    df['Hour'] = df['Time'].str.split(':').str[0] 
    df['Minute_AM_PM'] = df['Time'].str.split(':').str[1]
    df['Minute'] = df['Minute_AM_PM'].str.split(' ').str[0]
    df['AM_PM'] = df['Minute_AM_PM'].str.split(' ').str[1]

    df.drop(['Dates','Time','Minute_AM_PM','Minute'],axis=1,inplace=True)
    df['Times']=df['Hour']+df['AM_PM']
    df.drop(['Hour','AM_PM'],axis=1,inplace=True)
    df3=df['Times'].str.split(' -')
    df['Times']=df3.str[0]
    df.rename(columns={'Date':'Day','Year':'year','Month_Name':'NEW_Month','Day_Name':'dayss'},inplace=True)

    return df
