from datetime import datetime, timezone
import os
import pandas as pd
import time
from prisma import Prisma
import asyncio

####################### Getting report id and the report itself
def get_report(report_id : str = None) :
    """
    gets the latest report if no report name is given and if present else returns its status else returns the report with name as report name.
    """
    path = './controllers/data/reports/'
    if report_id:
        fullpath = path + report_id + '.csv'
        # print(os.path.exists(path), path, 'lksajfljsfkj')
        if os.path.exists(fullpath) :
            status = 'Completed'
            return {'status' : status, 'id' : report_id}
        else :
            temp1 = report_id.split('-')
            try:
                temp1 = datetime(int(temp1[0]), int(temp1[1]), int(temp1[2]), int(temp1[3]))
                temp2 = datetime(datetime.now().year, datetime.now().month , datetime.now().day , datetime.now().hour)
                if temp1 > temp2:
                    status = "Can't bring you a future report."
                elif temp1 < temp2:
                    status = "Report hasn't been made for this timestamp."
                else : 
                    status = 'Running'
            except :
                status = "Enter a valid date time."
            return {'status' : status}
    else :
        filename = str(datetime.now().year) + '-' + str(datetime.now().month) + '-' + str(datetime.now().day) + '-' + str(datetime.now().hour)
        fullpath = path + filename + '.csv'
        return {'id' : filename}


######################### Store status update
def datetime_string_processing_StoreStatus(string) :
    format = f'%Y-%m-%d %H:%M:%S.%f'
    string = string.split(' ')[0] + " " + string.split(' ')[1]
    try :
        res = datetime.strptime(string, format).replace(tzinfo=timezone.utc).isoformat()
    except Exception as e:
        print(string, e)
        res = 'f'
    return res
async def store_status_update():
    raw_data_path = './controllers/data/raw/store status.csv'
    try: 
        store_status_data = pd.read_csv(raw_data_path)  
    except Exception as e :
        print('Error while getting file for updating store status.', e)
    # print('ok1')
    store_status_data['timestamp_utc'] = store_status_data['timestamp_utc'].map(datetime_string_processing_StoreStatus)
    # print('ok2')
    store_status_data = store_status_data.to_dict('records')
    print('Started updating the store status.')
    start = time.time()
    prisma = Prisma()
    await prisma.connect()
    try:
        batch_size = 1000
        for i in range(0, len(store_status_data), batch_size):
            batch = store_status_data[i:i + batch_size]
            await prisma.storestatus.create_many(
                data=batch
            )
    except Exception as e :
        message = 'An error occurred while updating store status: ' + str(e)
    else :
        message = 'Store status updated successfully'
    await prisma.disconnect()
    end = time.time()
    print(message, "Time taken: ", (end-start)/60, ' minutes')

################################ Store time zone update
async def store_timezone_update():
    raw_data_path = './controllers/data/raw/bq-results-20230125-202210-1674678181880.csv'
    try: 
        store_timezone_data = pd.read_csv(raw_data_path)  
    except Exception as e :
        print('Error while getting file for updating store status.', e)
    
    store_timezone_data = store_timezone_data.to_dict('records')
    print('Started updating the store timezone.')
    start = time.time()
    prisma = Prisma()
    await prisma.connect()
    try:
        for record in store_timezone_data:
            await prisma.storetimezone.upsert(
                where={
                    'store_id': record['store_id']
                },
                data = {
                    'create' : {
                        'store_id' : record['store_id'],
                        'timezone_str' : record['timezone_str']
                    },
                    'update' : {
                        'timezone_str' : record['timezone_str']
                    }
                }
            )
    except Exception as e :
        message = 'An error occurred while updating store timezone: ' + str(e)
    else :
        message = 'Store timezone updated successfully'
    await prisma.disconnect()
    end = time.time()
    print(message, "Time taken: ", (end-start)/60, ' minutes')


############################## Store Hours update
def datetime_string_processing_StoreHours(string) :
    format = f'%H:%M:%S'
    try :
        # res = datetime.strptime(string, format).replace(tzinfo=timezone.utc).isoformat()
        res = datetime.now().replace(tzinfo=timezone.utc).isoformat()
        # print(res, type(res))
    except Exception as e:
        print(string, e)
        res = 'f'
    return res
async def store_hours_update():
    raw_data_path = './controllers/data/raw/Menu hours.csv'
    try: 
        store_hours_data = pd.read_csv(raw_data_path)  
    except Exception as e :
        print('Error while getting file for updating store status.', e)
    print('ok1')
    store_hours_data['start_time_local'] = store_hours_data['start_time_local'].map(datetime_string_processing_StoreHours)
    store_hours_data['end_time_local'] = store_hours_data['end_time_local'].map(datetime_string_processing_StoreHours)
    store_hours_data = store_hours_data.to_dict('records')
    print('ok2')
    print('Started updating the store hours.')
    start = time.time()
    prisma = Prisma()
    await prisma.connect()
    try:
        batch_size = 1000
        for i in range(0, len(store_hours_data), batch_size):
            batch = store_hours_data[i:i + batch_size]
            await prisma.storehours.create_many(
                data=batch
            )
    except Exception as e :
        message = 'An error occurred while updating store hours: ' + str(e)
    else :
        message = 'Store hours updated successfully'
    await prisma.disconnect()
    end = time.time()
    print(message, "Time taken for store hours update : ", (end-start)/60, ' minutes')


async def generate_report():
    
    return