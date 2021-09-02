import asyncio
import os
import json
from random import randrange
from numpy import random
from datetime import datetime
import time as mod_time
from pathlib import Path


class Sensor(object):
    def __init__(self, deviceId, location, temperature, time):
        self.temperature = temperature
        self.time = time
        self.location = location
        self.deviceId = deviceId

    async def run(self):
        self.time = int((mod_time.mktime(datetime.now().timetuple())))

        jsonStr = json.dumps({"data": self.__dict__})

        filename = self.deviceId + '-' + str(self.time) + '.json'
        # writing the json file to current directory
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(jsonStr)
        # when writing is done, move it to other directory to be read by publisher
        path = os.path.dirname(os.path.realpath(__file__)) + '/../weatherfiles/' + filename
        Path(filename).rename(path)
        print(path)


def makeData(c):
    a = randrange((c * 10) - 3, (c * 10) + 2)
    r = random.uniform(-3, 2)
    if r >= 1.9:
        r = r + 10
    elif r < (-2.8):
        r = r + (- 10)
    return int(a) + int(r)


async def main():
    sensors = [
        Sensor('7d869758-d54a-4daf-a625-a9a94ca15b22',
               {'latitude': 52.14691120000001, 'longitude': 11.658838699999933},
               0,
               '0'),
        Sensor('6b4f4a32-a7f5-4ec2-8820-6581468ef36b',
               {'latitude': 152.14691120000001, 'longitude': 111.658838699999933},
               0, '0'),
        Sensor('889b0221-4b4b-4094-b6ae-7d647264f23b',
               {'latitude': 252.14691120000001, 'longitude': 211.658838699999933},
               0, '0')]

    while 1:
        climate = 0
        for sensor in sensors:
            sensor.temperature = makeData(climate)
            task = asyncio.create_task(sensor.run())
            climate += 1
            await task
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())
