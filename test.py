import pandas as pd
import os
from datetime import datetime, timezone
from prisma import Prisma
import asyncio
import pytz
import time

# def datetime_string_processing(string) :
#     format = f'%Y-%m-%d %H:%M:%S.%f'
#     string = string.split(' ')[0] + " " + string.split(' ')[1]
#     try :
#         res = datetime.strptime(string, format).replace(tzinfo=timezone.utc).isoformat()
#     except Exception as e:
#         print(string, e)
#         res = 'f'
#     return res
# store_status = pd.read_csv('./controllers/data/raw/store status-1.csv')
# store_status['timestamp_utc'] = store_status['timestamp_utc'].map(datetime_string_processing)
# temp = store_status.iloc[1:10,:].to_dict('r')
# print(temp)
# print('1')
# temp = set(temp)
# print('2')
# print(temp)

# path = './data/reports/'
# filename = 'testfile.txt'
# print(os.path.exists(path+filename))

# string = str(datetime.now().year) + '-' + str(datetime.now().month) + '-' + str(datetime.now().day) + '-' + str(datetime.now().hour)
# print(string, type(string))

# a = datetime(2023,1,27,20)
# b = datetime(2023,4,25,20)
# print(a>b)

# prisma = Prisma( )

# store_status_data = pd.read_csv('./data/raw/store status.csv')
# print(store_status_data)
# print(len(store_status_data))
# for i in range(4):
#     print(store_status_data.iloc[i,0], store_status_data.iloc[i,1], store_status_data.iloc[i,2])

# async def store_status_update():
#     prisma = Prisma()
#     await prisma.connect()
#     store_status_data = pd.read_csv('./data/raw/store status-1.csv')
#     for i in range(len(store_status_data)):
#         # print(i)
#         format = f'%Y-%m-%d %H:%M:%S.%f'
#         string = '2023-01-21 02:03:58.311087 UTC'
#         string = string.split(' ')[0] + " " + string.split(' ')[1]   
#         date_object = datetime.strptime(string, format)
#         date_object = date_object.replace(tzinfo=timezone.utc) 
#         await prisma.storestatus.upsert(
#             where={
#                 'store_id' : int(store_status_data.iloc[i,0]),
#             },
#             data= {
#                 'create' : {
#                     'store_id' : int(store_status_data.iloc[i,0]),
#                     'timestamp_utc' : date_object.isoformat(),
#                     'status' : str(store_status_data.iloc[i,1])
#                 },
#                 'update' : {
#                     'status' : str(store_status_data.iloc[i,1]),
#                     'timestamp_utc' : date_object.isoformat()
#                 },
#             }
#         )
#     await prisma.disconnect()
# start = time.time()
# if __name__ == '__main__' :
#     asyncio.run(store_status_update())
# end = time.time()
# print('execution time is : ', end-start)


# format = f'%Y-%m-%d %H:%M:%S.%f'
# string = '2023-01-21 02:03:58.311087 UTC'
# string = string.split(' ')[0] + " " + string.split(' ')[1]
# # print(string)
# date_object = datetime.strptime(string, format)
# date_object = date_object.replace(tzinfo=timezone.utc)
# print(date_object, date_object.isoformat())
# # print(timezone.tzname('America/Denver'))