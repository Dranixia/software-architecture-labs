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
    dist_map.lock(key)
    try:
        value = dist_map.get(key)
        sleep(0.01)
        value = value + 1
        dist_map.put(key, value)
    finally:
        dist_map.unlock(key)

print(f"Final result: {dist_map.get(key)}")

client.shutdown()
