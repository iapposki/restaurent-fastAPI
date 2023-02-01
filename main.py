from fastapi import FastAPI
from pydantic import BaseModel
from controllers import restaurantController
from fastapi.responses import FileResponse
from fastapi_utils.tasks import repeat_every
import asyncio

app = FastAPI()

class Item(BaseModel):
    name : str
    price : float
    is_offer : bool = False

@app.get('/')
def read_root():
    return {'hello':'world'}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q }

@app.put('/items/{item_id}')
def update_item(item_id : int, item : Item):
    return {'item_name' : item.name, 'item_id' : item_id}

@app.get('/get-report/')
def get_report(id : str = None):
    """
    gets report with 'id' being the report name. Report naming scheme and url example example : /get-report/?id=2023-01-29
    if no id is given then gives id of the latest report.
    """
    res = restaurantController.get_report(id)
    if id :
        if res['status'] == 'Completed':
            return FileResponse('./data/reports/' + id + '.csv', filename=id+'.csv')
        else: 
            return res
    return res

@app.on_event("startup")
@repeat_every(seconds=60*60)  # 1 hour
async def initiate_report_generation():
    await restaurantController.generate_report()


@app.on_event('startup')
@repeat_every(seconds=60*60)  # 1 hour
async def update_database():
    tasks = [restaurantController.store_hours_update(), restaurantController.store_timezone_update(), restaurantController.store_status_update()]
    execute = []
    for task in tasks:
        execute.append(asyncio.create_task(task))
    await asyncio.gather(*execute)
