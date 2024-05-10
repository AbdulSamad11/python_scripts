# main libraries are mysql-connector-python==8.4.0 streamlit==1.34.0
"""
database look like this
+---------------------+-----------+-------------------+-------+
| date_time           | device_id | feature_type      | score |
+---------------------+-----------+-------------------+-------+
| 2024-05-09 12:17:16 |      1212 | df_5_sec_pkt_rate |     1 |
| 2024-05-09 12:17:16 |      1212 | df_data_ofs       |     2 |
| 2024-05-09 12:17:16 |      1212 | df_dst_ip         |     1 |
| 2024-05-09 12:17:16 |      1212 | df_dst_ports      |     1 |
| 2024-05-09 12:17:16 |      1212 | df_fft_time_diff  |     8 |

"""
import streamlit as st
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import plotly.graph_objects as go 
import plotly.express as px

# Connect to MySQL
def connect_to_mysql():
    return mysql.connector.connect(
        host="localhost",
        user="vm",
        password="samad123",
        database="dp_events"
    )
table_name = "dp_events"
# Connect to MySQL
conn = connect_to_mysql()
cursor = conn.cursor()
# cursor.execute("SELECT * FROM {} limit 10".format(table_name))
cursor.execute("SELECT * FROM dp_events WHERE DATE(date_time) = '2024-05-10';")
rows = cursor.fetchall()
# st.title (f"Device Profiler Dashboard for {pd.Timestamp.today().date()}")


data = pd.DataFrame(rows, columns=["date_time", "device_id","feature_type","score"])
# st.dataframe(data)

# Convert date_time column to datetime format
data['date_time'] = pd.to_datetime(data['date_time'])

# Filter data for today
today_data = data[data['date_time'].dt.date == pd.Timestamp.today().date()]

# Display the data
devices = data['device_id'].unique().tolist()

chart_visual = st.sidebar.selectbox('Select From Menu', 
									('Home', 'Risk Score Over Time', 'Analyze Risk Score in Detail', 'Bubble Chart')) 




fig = go.Figure() 
today_risk = data[(data['feature_type'] == "var_cols")]
# today_risk = data[(data['feature_type'] == "var_cols") & (data['date_time'].dt.date == datetime.now().date())]
# st.dataframe(today_risk)


def device_activity():
    df = (
        today_risk[['device_id', 'score']].groupby("device_id")
        .count()
        .reset_index()
        .rename(columns={"score": "Activity"})
    )
    # st.dataframe(df)
    # st.progress(int(len(today_risk)*100/len(data)))
    fig = px.bar(
        df,
        x="device_id",
        y="Activity",
        color="Activity",
        text="device_id",
    )
    st.title(f'Device Activity Summary')
    st.plotly_chart(fig)
# Plotting
def plot_risk_over_time(device):
    
    # st.dataframe(today_risk_1212[['date_time', 'score']].head())
    chart_data = pd.DataFrame(
        today_risk[(today_risk['device_id'] == device)],
        columns=['date_time', 'score']
        )
    # st.subheader(f'Risk score over time for device {device}')
    st.subheader(device)
    st.line_chart(chart_data, x='date_time', y='score')



def plot_risk_in_detail(device):
    
    feature_scores = (
        data[data['device_id'] == device][['feature_type', 'score']].groupby("feature_type")
        .mean()
        .reset_index()
    )
 
    feature_scores = pd.DataFrame(feature_scores, columns=['feature_type', 'score'])
    fig = px.bar(
        feature_scores,
        x="feature_type",
        y="score",
        color="score",
        text="feature_type",
    )
    st.subheader(device)
    st.plotly_chart(fig)
    # # st.dataframe(today_risk_1212[['date_time', 'score']].head())
    # chart_data = pd.DataFrame(
    #     today_risk[(today_risk['device_id'] == device)],
    #     columns=['date_time', 'score']
    #     )
    # # st.subheader(f'Risk score over time for device {device}')
    # st.subheader(device)
    # st.line_chart(chart_data, x='date_time', y='score')

if chart_visual == 'Home': 
    # st.title ("Device Profiler Dashboard")
    
    device_activity()
    # 
    # st.balloons()

elif chart_visual == 'Risk Score Over Time': 
    st.title(f'Risk score over time')
    # for device in devices:
    # st.progress(len(data) - len(today_risk))
    options = ['all'] + devices
    selected_status = st.sidebar.selectbox('Select device',options = options) 



    if selected_status == 'all':
        for device in devices:
            plot_risk_over_time(device)
    else:
        plot_risk_over_time(selected_status)


elif chart_visual == 'Analyze Risk Score in Detail': 
    st.title(f'Individual feature set scores')
    # for device in devices:
    # st.progress(len(data) - len(today_risk))
    options = ['all'] + devices
    selected_status = st.sidebar.selectbox('Select device',options = options) 
    if selected_status == 'all':
        for device in devices:
            plot_risk_in_detail(device)
    else:
        plot_risk_in_detail(selected_status)

