import requests
import os

os.environ["OPENBLAS_NUM_THREADS"] = "1"
import numpy as np
import pandas as pd
import psycopg2
import csv
import zipfile
import io
import shutil

from urllib.request import urlopen

BASEPATH = "clients.wwlengineering.com/public_html/"
# BASEPATH = os.getcwd()+"/"

# for every node and piezometer
A, B, C = 1.4051 * 10**-3, 2.369 * 10**-4, 1.019 * 10**-7

dbname = "wwlengineering_rossing"
user = "WWL_ADMIN"
password = "WWL#2023"
host = "wwl-rossing.crnkanilun4m.ap-southeast-2.rds.amazonaws.com"
dev = True


def save_last_features(nodes_df, cur):
    # base = os.getcwd()+"/"

    cdf = pd.read_csv(os.path.abspath("data/calibration_data.csv"), index_col="SNumber")
    query = ""
    # calculate temperature and pressure by piezometer
    for i in range(len(nodes_df)):
        # for i in range(1):
        idf = nodes_df[i][0]
        k = nodes_df[i][1]
        sub = nodes_df[i][2]
        # sub2 = sub.copy()
        # print(sub)
        # sub = sub['TIMESTAMP'].max()
        # print(sub)

        if sub.size > 0:
            t = sub.index[-1]
            sub = sub.iloc[-1, :]
            feat = cdf.loc[(cdf["Logger"] == idf) & (cdf["Channel"] == k)].fillna(0)
            if feat.size > 0:
                # we suppose the last sensor is the newest one
                feat = feat.to_dict("records")[-1]
                # get temperature
                # print(sub)
                sub["Temperature"] = get_temp(sub["thermRes"], A, B, C)

                if feat["G"] != 0:
                    # get pressure
                    sub["Pressure"] = polynomial2(
                        sub["freq"], sub["Temperature"], sub["AtmPressure"], feat
                    )
                else:
                    # get pressure
                    sub["Pressure"] = polynomial1(
                        sub["freq"], sub["Temperature"], sub["AtmPressure"], feat
                    )
            else:
                # get temperature
                sub["Temperature"] = np.nan
                # get pressure
                sub["Pressure"] = np.nan
            row = np.array(sub)

            try:
                data1 = tuple([idf, k, t, row[-1], row[-2]])
                query += f" INSERT INTO last_readings VALUES ('{data1[0]}','{data1[1]}','{data1[2]}','{data1[3]}','{data1[4]}') ON CONFLICT(node, channel) DO NOTHING; "  # +\

                data2 = tuple([t, row[-1], row[-2], idf, k])
                query += f" UPDATE last_readings SET time = '{data2[0]}', pressure = '{data2[1]}', temperature = '{data2[2]}' WHERE node='{data2[3]}' AND channel='{data2[4]}' ; "
                # "ON CONFLICT() DO NOTHING;"

            except:
                data = tuple([t, row[-1], row[-2], idf, k])
                query += f" UPDATE last_readings SET time = '{data[0]}', pressure = '{data[1]}', temperature = '{data[2]}' WHERE node='{data[3]}' AND channel='{data[4]}' ; "

                # "ON CONFLICT() DO NOTHING;"

    return query


def update_status():
    """
    Update the status according to 2 conditions:
       Longer than 7 days (disconnected:3)
       Wrong measures (damaged:2)
       Active (1)
    """

    query = """
    UPDATE piezometer_details
    SET status = CASE
	    WHEN (CURRENT_DATE - last_readings.time) > INTERVAL '7 days' THEN 3
	    WHEN last_readings.pressure > 0 AND last_readings.pressure / 10 > piezometer_details.depth * 1.1 THEN 2
	    ELSE 1
	    END
    FROM last_readings
    WHERE piezometer_details.datalogger=last_readings.node AND piezometer_details.channel=last_readings.channel;
    """
    return query


def create_table(id, k, cur):
    try:
        query = ""
        # sub = pd.read_csv('download\\node_'+str(id)+'_'+str(k)+'_'+str(year)+'_'+str(month)+'.csv',parse_dates=['TIMESTAMP'])
        table_name = "node_" + str(id) + "_" + str(k)
        query += f" CREATE TABLE IF NOT EXISTS {table_name} (time timestamp NOT NULL PRIMARY KEY, atmpres numeric(10,4), freq numeric(20,5), thermR numeric(20,5), Temperature numeric(12,6), Pressure numeric(12,6)); "
        return query
    except Exception as e:
        print("error in file %d %d - %s" % (id, k, e))


# basic functions
def clean_name(name):
    tmp = "".join([j for j in name if not j.isdigit()])
    tmp = tmp.replace("InDigit", "")
    tmp = tmp.replace("in-mbar", "")
    tmp = tmp.replace("InOhms", "")
    tmp = tmp.replace("InHz", "")
    tmp = tmp.replace("VW", "")
    tmp = tmp.replace("Ch", "")
    tmp = tmp.replace("-", "")
    return tmp


def get_node_id(name):
    n = [int(s) for s in name.split("-") if s.isdigit()][0]
    return n


def get_temp(thermR, A, B, C):
    return 1 / (A + B * np.log(thermR) + C * (np.log(thermR) ** 3)) - 273.2


def linear1(R, T, S, df):
    CF, Tk, R0, Tm, S0 = df["CF"], df["Tk"], df["R0"], df["Tm"], df["S0"]
    Rf = (R**2) / 1000
    val = CF * (R0 - Rf) - Tk * (Tm - T) + 0.05 * (S - S0) / 10000
    return val


def polynomial1(R, T, S, df):
    Tk, Tm, S0 = df["Tk"], df["Tm"], df["S0"]
    A, B, C = df["A"], df["B"], df["C"]
    Rf = (R**2) / 1000
    val = A * (Rf**2) + B * Rf + C - Tk * (Tm - T) + 0.05 * (S - S0) / 10000
    return val


def linear2(R, T, S, df):
    G, Tk, R0, Tm, S0 = df["G"], df["Tk"], df["R0"], df["Tm"], df["S0"]
    Rf = (R**2) / 1000
    val = G * (R0 - Rf) + Tk * (T - Tm) - 0.05 * (S - S0) / 10000
    return val


def polynomial2(R, T, S, df):
    Tk, Tm, S0 = df["Tk"], df["Tm"], df["S0"]
    A, B, C = df["A"], df["B"], df["C"]
    Rf = (R**2) / 1000
    val = A * (Rf**2) + B * Rf + C + Tk * (T - Tm) - 0.05 * (S - S0) / 10000
    return val


def copy_data(id, k, year, month, cur):
    try:
        query = ""
        # sub = pd.read_csv('download\\node_'+str(id)+'_'+str(k)+'_'+str(year)+'_'+str(month)+'.csv',parse_dates=['TIMESTAMP'])
        query += create_table(id, k, cur)
        table_name = "node_" + str(id) + "_" + str(k)

        file = os.path.abspath("download/node_%d_%d_%d_%02d.csv" % (id, k, year, month))
        print("FILE", file)
        sub = pd.read_csv(file, parse_dates=["TIMESTAMP"])
        for _, row in sub.iterrows():
            tuple_row = tuple(row)
            query += f" INSERT INTO {table_name} VALUES ('{tuple_row[0]}','{tuple_row[1]}','{tuple_row[2]}','{tuple_row[3]}','{tuple_row[4]}','{tuple_row[5]}') ON CONFLICT (time) DO NOTHING; "
        return query
    except Exception as e:
        print("error in file %d %d - %s" % (id, k, e))


# def update_tables(mysql, id, k, year, month):
#     try:
#         sub = pd.read_csv(
#             os.path.abspath(
#                 "download/node_"
#                 + str(id)
#                 + "_"
#                 + str(k)
#                 + "_"
#                 + str(year)
#                 + "_"
#                 + str(month)
#                 + ".csv"
#             ),
#             parse_dates=["TIMESTAMP"],
#         )
#         conn = mysql.connect()
#         cursor = conn.cursor()
#         query = (
#             "CREATE TABLE IF NOT EXISTS node_"
#             + str(id)
#             + "_"
#             + str(k)
#             + " (timestamp datetime not null primary key,atmpres decimal(10,4),freq decimal(20,5),thermR decimal(20,5),Temperature decimal(10,5),Pressure decimal(10,5));"
#         )
#         cursor.execute(query)
#         conn.commit()
#         table_name = "node_" + str(id) + "_" + str(k)
#         for i, row in sub.iterrows():
#             query = "INSERT IGNORE INTO " + table_name + " VALUES (%s,%s,%s,%s,%s,%s)"
#             cursor.execute(query, tuple(row))
#             conn.commit()
#         print("updated table %d %d" % (id, k))
#     except Exception as e:
#         print("error in file %d %d - %s" % (id, k, e))


def dict_helper(objlist):
    result2 = [item.obj_to_dict() for item in objlist]
    return result2


def download_data(gateway, year, month, option=False):
    # user log to server
    adm = ("admin", "Aeros4uav")
    # url server
    if option:
        base_url = (
            "https://loadsensing.wocs3.com/"
            + str(gateway)
            + "/dataserver/csv/compacted/compacted-readings-"
            + str(gateway)
            + "-"
        )
        url = base_url + str(year) + "-" + "%02d" % (month) + ".dat"

        print("LINK1", url)
    else:
        url = (
            "https://loadsensing.wocs3.com/"
            + str(gateway)
            + "/dataserver/current/comp/"
            + str(gateway)
        )
        print("LINK2", url)
    # conecting to server
    response = requests.get(url=url, auth=adm, allow_redirects=True)

    # download data and save it as csv
    print("CONTENT", response.content)
    open(os.path.abspath("data/data_compacted.csv"), "wb").write(response.content)

    # url = 'https://loadsensing.wocs3.com/21545/dataserver/csv/compacted/compacted-readings-21545-2022-06.zip'
    # print("connecting to server")
    # print(url)
    # res = requests.get(url=url, stream=True, auth=adm, allow_redirects=True)

    # print("STATUS",res.status_code)
    # if res.status_code == 200:
    #     with open(os.path.abspath("data/zipped.zip"), 'wb') as fh:
    #         res.raw.decode_content
    #         shutil.copyfileobj(res.raw, fh)

    # z = zipfile.ZipFile(os.path.abspath("data/zipped.zip"))
    # z.extractall(os.path.abspath("data"))
    # # # print("RESPONSE", r.content)
    # print("downloaded data from server")

    # df = open(os.path.abspath("data/compacted-readings-21545-2022-06.dat")).read().encode()
    # # print(df)
    # open(os.path.abspath("data/data_compacted.csv"), "wb").write(df)

    print("downloaded data to local")


def get_features_from_data(file):
    # read data and drop last column
    print("cleaning data")
    df = pd.read_csv(file, skiprows=1, parse_dates=["TIMESTAMP"], index_col=0)
    df = df.iloc[:, :-1]
    # counting number of channels per node
    nodes = dict()
    for col in df.columns[1:]:
        n = get_node_id(col)
        if n in nodes.keys():
            nodes[n] += 1
        else:
            nodes[n] = 1
    x = list(nodes.items())
    # saving data per node and per channel
    nodes_df = []
    j = 1
    print("reording")
    for i in range(len(x)):
        mainset = df.iloc[:, j : j + x[i][1]]
        for k in range(0, (x[i][1] - 1) // 3):
            subset = mainset.iloc[:, [0, 3 * k + 1, 3 * k + 3]]
            subset = subset.dropna()
            # cleaning subsets names
            cols = subset.columns
            new_cols = []
            for col in cols:
                new_cols.append(clean_name(col))
            subset.columns = new_cols
            nodes_df.append([x[i][0], k + 1, subset])
        j += x[i][1]
    return nodes_df


def save_features(nodes_df, year, month, cur):
    cdf = pd.read_csv(os.path.abspath("data/calibration_data.csv"), index_col="SNumber")
    query = ""
    # calculate temperature and pressure by piezometer
    for i in range(len(nodes_df)):
        # for i in range(5):
        idf = nodes_df[i][0]
        k = nodes_df[i][1]
        sub = nodes_df[i][2]
        if sub.size > 0:
            feat = cdf.loc[(cdf["Logger"] == idf) & (cdf["Channel"] == k)].fillna(0)
            if feat.size > 0:
                # we suppose the last sensor is the newest one
                feat = feat.to_dict("records")[-1]
                # get temperature
                sub["Temperature"] = sub.apply(
                    lambda row: get_temp(row["thermRes"], A, B, C), axis=1
                )
                if feat["G"] != 0:
                    # get pressure
                    sub["Pressure"] = sub.apply(
                        lambda row: polynomial2(
                            row["freq"], row["Temperature"], row["AtmPressure"], feat
                        ),
                        axis=1,
                    )
                else:
                    # get pressure
                    sub["Pressure"] = sub.apply(
                        lambda row: polynomial1(
                            row["freq"], row["Temperature"], row["AtmPressure"], feat
                        ),
                        axis=1,
                    )
            else:
                # get temperature
                sub["Temperature"] = sub.apply(lambda row: np.nan, axis=1)
                # get pressure
                sub["Pressure"] = sub.apply(lambda row: np.nan, axis=1)

            file = os.path.abspath(
                "download/node_%d_%d_%d_%02d.csv" % (idf, k, year, month)
            )
            sub.to_csv(file, date_format="%Y/%m/%d %H:%M:%S %t")
            query += copy_data(idf, k, year, month, cur)

    return query


# download data and process
# def get_data_from_server(mysql, year, month, option=1, cal_params=True):
#     # read data and drop last column
#     print("cleaning data")
#     if option:
#         df = pd.read_csv(
#             os.path.abspath("data/data_compacted.csv"),
#             skiprows=1,
#             parse_dates=["TIMESTAMP"],
#             index_col=0,
#         )
#     else:
#         name = os.path.abspath(
#             "data/compacted-readings-21545-%d-%02d.dat" % (year, month)
#         )
#         df = pd.read_csv(name, skiprows=1, parse_dates=["TIMESTAMP"], index_col=0)
#     df = df.iloc[:, :-1]
#     # counting number of channels per node
#     nodes = dict()
#     for col in df.columns[1:]:
#         n = get_node_id(col)
#         if n in nodes.keys():
#             nodes[n] += 1
#         else:
#             nodes[n] = 1
#     x = list(nodes.items())
#     # saving data per node and per channel
#     nodes_df = []
#     j = 1
#     print("reording")
#     for i in range(len(x)):
#         mainset = df.iloc[:, j : j + x[i][1]]
#         for k in range(0, (x[i][1] - 1) // 3):
#             subset = mainset.iloc[:, [0, 3 * k + 1, 3 * k + 3]]
#             subset = subset.dropna()
#             # cleaning subsets names
#             cols = subset.columns
#             new_cols = []
#             for col in cols:
#                 new_cols.append(clean_name(col))
#             subset.columns = new_cols
#             nodes_df.append([x[i][0], k + 1, subset])
#         j += x[i][1]
#     # read piezometer features
#     print("calculating parameters")

#     cdf = pd.read_csv(os.path.abspath("data/calibration_data.csv"), index_col="SNumber")
#     # calculate temperature and pressure by piezometer
#     for i in range(len(nodes_df)):
#         idf = nodes_df[i][0]
#         k = nodes_df[i][1]
#         if cal_params:
#             sub = nodes_df[i][2]
#             if sub.size > 0:
#                 feat = cdf.loc[(cdf["Logger"] == idf) & (cdf["Channel"] == k)].fillna(0)
#                 if feat.size > 0:
#                     # we suppose the last sensor is the newest one
#                     feat = feat.to_dict("records")[-1]
#                     # get temperature
#                     sub["Temperature"] = sub.apply(
#                         lambda row: get_temp(row["thermRes"], A, B, C), axis=1
#                     )
#                     if feat["G"] != 0:
#                         # get pressure
#                         sub["Pressure"] = sub.apply(
#                             lambda row: polynomial2(
#                                 row["freq"],
#                                 row["Temperature"],
#                                 row["AtmPressure"],
#                                 feat,
#                             ),
#                             axis=1,
#                         )
#                     else:
#                         # get pressure
#                         sub["Pressure"] = sub.apply(
#                             lambda row: polynomial1(
#                                 row["freq"],
#                                 row["Temperature"],
#                                 row["AtmPressure"],
#                                 feat,
#                             ),
#                             axis=1,
#                         )
#                 else:
#                     # get temperature
#                     sub["Temperature"] = sub.apply(lambda row: np.nan, axis=1)
#                     # get pressure
#                     sub["Pressure"] = sub.apply(lambda row: np.nan, axis=1)
#                 sub.to_csv(
#                     "download/node_"
#                     + str(idf)
#                     + "_"
#                     + str(k)
#                     + "_"
#                     + str(year)
#                     + "_"
#                     + str(month)
#                     + ".csv",
#                     date_format="%Y/%m/%d %H:%M:%S %t",
#                 )
#                 update_tables(mysql, idf, k, year, month)
#         else:
#             copy_data(idf, k, year, month)
