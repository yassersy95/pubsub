import time

import pandas as pd
import pymysql
from sklearn.cluster import KMeans
from numpy import sqrt, array
import matplotlib.pyplot as plt


def findAnamolies():
    tarr = array(df['temperature']).reshape(-1, 1)
    kmeans = KMeans(n_clusters=1).fit(tarr)
    center = kmeans.cluster_centers_
    distance = sqrt((tarr - center) ** 2)
    df_anomalies = df
    df_anomalies['distance'] = pd.DataFrame(distance)
    df_anomalies = df_anomalies.sort_values(by="distance")
    df_anomalies = df_anomalies[
        (df_anomalies['temperature'] > anamoly_max) | (df_anomalies['temperature'] < anamoly_min)]
    return df_anomalies


def flagAnomalies():
    for index, row in df_anomalies.iterrows():
        insert_sql = 'update weather_trans set isanomal= 1 where id=' + str(int(row['id'])) + ';'
        print(insert_sql)
        cur = conn.cursor()
        cur.execute(insert_sql)
        conn.commit()
    for index, row in df_norm.iterrows():
        insert_sql = 'update weather_trans set isanomal= 0 where id=' + str(int(row['id'])) + ';'
        print(insert_sql)
        cur = conn.cursor()
        cur.execute(insert_sql)
        conn.commit()


def plotAnamolies():
    x_ax = range(df.shape[0])  # datasize
    plt.plot(x_ax, df['temperature'])
    plt.scatter(df_anomalies.index, df_anomalies['temperature'], color='r')
    plt.show()


conn = pymysql.connect(host='127.0.0.1', port=3306, user='weather', passwd='weather', db='weather')
while 1:
    devicedf = pd.read_sql("select distinct deviceid from weather_trans where isanomal = -1", conn);
    for index, row in devicedf.iterrows():
        df = pd.read_sql('select id, temperature from weather_trans where isanomal = -1 and deviceid="' + row[
            'deviceid'] + '" order by time limit 60', conn);
        if df.shape[0] < 60:
            continue
        median = df['temperature'].median()
        std = df['temperature'].std()
        anamoly_min = median - std
        anamoly_max = median + std

        df_anomalies = findAnamolies()
        df_norm = df[~df.index.isin(df_anomalies.index)]
        flagAnomalies()
        # time.sleep(60)
        # plotAnamolies(df, df_anomalies)

# conn.close()

