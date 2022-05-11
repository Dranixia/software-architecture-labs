import hazelcast
import logging
from time import sleep

logging.basicConfig(level=logging.INFO)

client = hazelcast.HazelcastClient(cluster_members=["172.17.0.2:5701", "172.17.0.3:5701", "172.17.0.4:5701"])
dist_map = client.get_map("my-distributed-map").blocking()

# The code below is Python interpretation of official example by Hazelcast
key = "1"
value = 0
dist_map.put_if_absent(key, value)


for _ in range(1000):
    while True:
        old_value = dist_map.get(key)
        new_value = old_value
        sleep(0.01)
        new_value += 1
        if dist_map.replace_if_same(key, old_value, new_value):
            break

client.shutdown()
