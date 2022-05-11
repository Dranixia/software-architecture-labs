import hazelcast
import logging


logging.basicConfig(level=logging.INFO)

client = hazelcast.HazelcastClient(cluster_members=["172.17.0.2:5701", "172.17.0.3:5701", "172.17.0.4:5701"])

dist_map = client.get_map("my-distributed-map").blocking()

for i in range(1000):
    dist_map.put(f"k-{i}", f"v-{i}")

client.shutdown()
