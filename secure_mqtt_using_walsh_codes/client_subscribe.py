import logging
import asyncio
import time

from amqtt.client import MQTTClient, ClientException
from amqtt.mqtt.constants import QOS_1, QOS_2


#
# This sample shows how to subscbribe a topic and receive data from incoming messages
# It subscribes to '$SYS/broker/uptime' topic and displays the first ten values returned
# by the broker.
#

logger = logging.getLogger(__name__)


async def uptime_coro():
    C = MQTTClient()
    print("Connection process started at ", time.time())	
    await C.connect("mqtt://172.17.34.5:1884/")
    print("Connection process ended at ", time.time())
    print("Subscription process with network latency started at: ", time.time())
    await C.subscribe(
        [
            ("default", QOS_1),
        ]
    )
    logger.info("Subscribed")
    a = 1
    count = 0
    try:
        while True:
            message = await C.deliver_message()
            packet = message.publish_packet	
            print(
                "%s => %s"
                % (packet.variable_header.topic_name, str(packet.payload.data))
            )
            if (packet.payload.data[4] == 'c' and count == 0):
                print("Subscription process with network latency ended at: ", time.time())	
                count = count + 1
        await C.unsubscribe(["default"])
        logger.info("UnSubscribed")
        await C.disconnect()
    except ClientException as ce:
        logger.error("Client exception: %s" % ce)


if __name__ == "__main__":
    formatter = "[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.CRITICAL, format=formatter)
    asyncio.get_event_loop().run_until_complete(uptime_coro())
