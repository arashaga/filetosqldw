#install pyodbc driver from https://docs.microsoft.com/en-us/sql/connect/odbc/windows/system-requirements-installation-and-driver-files?view=sql-server-2017#installing-microsoft-odbc-driver-for-sql-server
import pyodbc
import os
import pandas as pd
import numpy as np
import gzip

server = 'adwsqlserverarash.database.windows.net'
database = 'databasename'
username = 'username'
password = 'password'
driver= '{ODBC Driver 17 for SQL Server}'
cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()

path = './data'
fileList = os.listdir(path)
for file in fileList:
    #print(file)
    path_tofile =path+"/"+file
    with gzip.open(path_tofile, 'rb') as f_in:
        df = pd.read_csv(f_in)
        for index,row in df.iterrows():
            cursor.execute("insert into dbo.Stock(Datet,Openp,High,Low,Closep,AdjClose,Volume) values (?,?,?,?,?,?,?)",
            row['Date'],row['Open'],row['High'],row['Low'],row['Close'],row['Adj Close'],row['Volume'])
            cnxn.commit()
cursor.close()
cnxn.close()
