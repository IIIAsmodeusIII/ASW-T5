import numpy as np
import matplotlib.pyplot as plt
import json
import io
import logging
import requests

from PIL import Image
from .logger import Log

from typing import Union
from fastapi import FastAPI, Response
app = FastAPI()

if not hasattr(Image, 'Resampling'):
  Image.Resampling = Image

LOGGER = Log()
logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')

PIXELS = 128

TILE_TRANSFORM = (
    (0, 'blocked'),  
    (1, 'grass'), 
    (2, 'soiledDry'),
    (3, 'seededDry'),
    (4, 'growingDry'),
    (5, 'readyDry'),
    (6, 'soiledWathered'),
    (7, 'seededWathered'),
    (8, 'growingWathered'),
    (9, 'readyWathered')
)

tiles = {}
for _, tile_name in TILE_TRANSFORM:

    tiles[tile_name] = Image.open(f'app/img/{tile_name}.png').convert('RGBA')
    tiles[tile_name].load()



## Server ##
targetConstructionServiceUrl = "http://construct_service/users/"
@app.get("/farms/")
def read_root():
    images = []
    response = requests.get(targetConstructionServiceUrl)
    data     = json.loads(response.content.decode())
    users    = data["users"]

    for _, user in users.items():
        image = getFarm(user)
        images.append(image.decode())

    return {"FarmsImages": "Mundo"}

@app.get("/farms/{id}")
def farm(id: str):

    response = requests.get(targetConstructionServiceUrl + f"{id}")
    data     = json.loads(response.content.decode())    
    imageBytes = getFarm(data)

    ## Send it ##
    return Response(content=imageBytes, media_type="image/png")

def requestConstructionAPI(id=None):
    if id == None:
        LOGGER.log("Users: All", "FARM/", {"farm": []})
        data = open("app/response.json")
        LOGGER.log(f"User: {id}", f"FARM/{id}", data)
        return json.load(data)
    else:
        LOGGER.log(f"User: {id}", f"FARM/{id}", {"farm": []})
        data = open("app/response.json")
        data = json.load(data)
        for key, item in data.items():
            if item["granja"]["userId"] == id:
                LOGGER.log(f"User: {id}", f"FARM/{id} founded", item["granja"])
                return item["granja"]
        LOGGER.log(f"User: {id}", f"FARM/{id} not found. Err404", {"farm": []})

### Farm dict to ImageArray ###
def getFarm(farm):

    print(farm)

    ## Get data ##
    HEIGHT = farm["currentSize"][0]
    WIDTH = farm["currentSize"][1]
    
    MAX_HEIGHT = farm["maxSize"][0]
    MAX_WIDTH = farm["maxSize"][1]

    ## Make data structure of farm ##
    dataset = np.zeros((MAX_HEIGHT, MAX_WIDTH))
    dataset[MAX_HEIGHT-HEIGHT:, 0:WIDTH] = 1
    for construction in farm["constructions"]:
        x = int(construction["posX"])
        y = int(construction["posY"])

        temp = 0
        if(construction["isBuilt"] == 1):
            temp = 2

        if(construction["hasPlant"] == 1 and construction["daysTillDone"] == 0):
            temp = 5

        if(construction["hasPlant"] == 1 and construction["daysTillDone"] >= 1):
            temp = 4

        if(construction["hasPlant"] == 1 and construction["daysTillDone"] >= 5):
            temp = 3

        if(construction["isWatered"] == 1):
            temp += 4

        dataset[MAX_HEIGHT-y-1][x] = temp

    ## Reshape ##
    room = np.reshape(dataset, (MAX_HEIGHT, MAX_WIDTH))

    ## Generate Image ##
    assert room.shape == (MAX_HEIGHT, MAX_WIDTH)
    
    canvas = Image.new('RGBA', (PIXELS*MAX_WIDTH, PIXELS*MAX_HEIGHT))
    
    for i in range(MAX_WIDTH):
        for j in range(MAX_HEIGHT):
            canvas.paste(tiles['blocked'], (i*PIXELS, j*PIXELS))

    for tile_number, tile_name in TILE_TRANSFORM:
        J, I = np.nonzero(room == tile_number)
        for x in range(I.size):
            canvas.alpha_composite(tiles[tile_name], (I[x]*PIXELS, J[x]*PIXELS))
            
    image = canvas.resize((2*PIXELS*MAX_WIDTH, 2*PIXELS*MAX_HEIGHT), resample=Image.Resampling.BOX)

    ## Turn image into bytes ##
    imgByteArr = io.BytesIO()
    image.save(imgByteArr, format="PNG")
    #image.save("output.png")
    imgByteArr = imgByteArr.getvalue()
    
    return imgByteArr