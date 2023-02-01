from random import random
from datetime import datetime, timezone, timedelta
import os
import pandas as pd
import time
from prisma import Prisma
from dateutil import tz, parser

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
    # print('ok1')
    store_hours_data['start_time_local'] = store_hours_data['start_time_local'].map(datetime_string_processing_StoreHours)
    store_hours_data['end_time_local'] = store_hours_data['end_time_local'].map(datetime_string_processing_StoreHours)
    store_hours_data = store_hours_data.to_dict('records')
    # print('ok2')
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


# ############################# Report making
def norm_to_schema(dayofweek):
    res = dayofweek - 1
    return res
def local_to_utc(date, local_tzinfo):
    return date.replace(tzinfo=local_tzinfo).astimezone(tz=timezone.utc)
def utc_to_local(date, local_tzinfo):
    return date.astimezone(tz=local_tzinfo)
def upt_dwt_last_hour(storehours_data_arr,poll_data_arr, local_tzinfo):
    latest_poll_time = poll_data_arr[-1].timestamp_utc
    latest_poll_time = utc_to_local(latest_poll_time, local_tzinfo)
    if len(storehours_data_arr) == 0:
        end_time = datetime.now().astimezone(tz=local_tzinfo)
        # current_time_local = datetime.now().astimezone(tz=local_tzinfo)
        # temporary current time local !!!!!!!!!!!!!!!
        current_time_local = latest_poll_time + timedelta(hours=4*random())
    else:
        # current_time_local = datetime.now().astimezone(tz=local_tzinfo)
        # temporary current time local !!!!!!!!!!!!!!!
        current_time_local = latest_poll_time + timedelta(hours=4*random())
        day = norm_to_schema(latest_poll_time.isoweekday())
        end_time = storehours_data_arr[day].end_time_local
        end_time = end_time.replace(day=latest_poll_time.day, month=latest_poll_time.month, year=latest_poll_time.year, tzinfo=local_tzinfo)
    if current_time_local > end_time:
        return 'Store is past closing.'
    else:
        delta_one = current_time_local - latest_poll_time
        # set leeway here for last hour uptime/downtime
        temp = timedelta(hours=2)
        if delta_one - temp < timedelta(hours=1) and poll_data_arr[-1].status != 'inactive':
            downtime_last_hour = delta_one - temp
            uptime_last_hour = timedelta(hours=1) - downtime_last_hour
        else:
            uptime_last_hour = timedelta(hours=0)
            downtime_last_hour = timedelta(hours=1)

        # return [end_time, latest_poll_time, end_time - latest_poll_time]
        return [uptime_last_hour, downtime_last_hour, delta_one]
def upt_dwt_last_day(storehours_data_arr, poll_data_arr, local_tzinfo):

    return
def uptime_downtime(storehours_data_arr, poll_data_arr, local_tzinfo):
    # return format: [uptime last hour, uptime last day, uptime last week, downtime last hour, downtime last day, downtime last week]
    upt_dwt_last_hour_final = upt_dwt_last_hour(storehours_data_arr, poll_data_arr, local_tzinfo)

    return upt_dwt_last_hour_final

async def generate_report():
    prisma = Prisma()
    await prisma.connect()
    report = {'store_id' : [], 'uptime_last_hour' : [], 'uptime_last_day' : [], 'update_last_week' : [], 'downtime_last_hour' : [], 'downtime_last_day' : [], 'downtime_last_week' : []}
    store_timestamp_data = await prisma.storetimezone.find_many()
    df = pd.DataFrame(store_timestamp_data, columns=['store_id', 'timezone_str'])
    try:
        df['store_id'] = df['store_id'].map(lambda x : x[1])
        df['timezone_str'] = df['timezone_str'].map(lambda x : x[1])
    except Exception as e:
        print(e)
    # print(df)

    # for ind in df.index :
    date_now = datetime(2023,1,26)
    delta = timedelta(days=-7)
    date_week_before = date_now + delta
    for ind in range(50):
        # print(df['store_id'][ind])
        store_id = df['store_id'][ind]
        try:
            poll_data = await prisma.storestatus.find_many(
                where={'store_id' : str(store_id), 'timestamp_utc' : {
                    'gt' : date_week_before
                } },
                order={
                    'timestamp_utc' : 'asc' 
                }
            )
        except Exception as e:
            print(e)
        try : 
            store_schedule_data = await prisma.storehours.find_many(
                where={
                    'store_id' : str(store_id),
                },
                order={
                    'day_of_week' : 'asc'
                }
            )
        except Exception as e:
            print(e)
        # print(poll_data)
        # print(ind)
        # print(store_schedule_data)
        try:
            local_tzinfo = tz.gettz(str(df['timezone_str'][ind]))
            # print(local_tzinfo, df['timezone_str'][ind])
            print(uptime_downtime(store_schedule_data, poll_data, local_tzinfo))
        except Exception as e:
            print(e)

    await prisma.disconnect()
    return store_timestamp_data