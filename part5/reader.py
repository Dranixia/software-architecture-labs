import hazelcast
import logging
from time import sleep

logging.basicConfig(level=logging.INFO)

client = hazelcast.HazelcastClient(cluster_members=["172.17.0.2:5701", "172.17.0.3:5701", "172.17.0.4:5701"])
dist_q = client.get_queue("my-distributed-queue").blocking()

for _ in range(1000):
    value = dist_q.take()
    print(f"Read value = {value}")
    sleep(0.01)

client.shutdown()
