import logging
import asyncio
import time

from amqtt.client import MQTTClient, ClientException
from amqtt.mqtt.constants import QOS_1, QOS_2


#
# This file can be used to demonstrate the REM criteria in the paper 
# Analysis and Implementation of Lightweight Key Exchange Algorithms for MQTT Security
# Connect all clients to the broker.
# Connect and disconnect this client 100 times to get average time required by the
# client to eshtablish an connection with the broker
#

logger = logging.getLogger(__name__)


async def uptime_coro():
    C = MQTTClient()
    time1 = 0
    time2 = 0
    avg_time = 0
    time1 = time.time()*1000
    print("Connection process started at ", time.time())	
    await C.connect("mqtt://192.168.0.198:1884/")
    time2 = time.time()*1000
    print("Connection process ended at ", time.time())	
    await C.disconnect()

if __name__ == "__main__":
    formatter = "[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.CRITICAL, format=formatter)
    asyncio.get_event_loop().run_until_complete(uptime_coro())
