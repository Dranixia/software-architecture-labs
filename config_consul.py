import consul

session = consul.Consul()

session.kv.put("hazel_ports", "127.0.0.1:5701 127.0.0.1:5702 127.0.0.1:5703")

session.kv.put("map", "logging-map")
session.kv.put("queue", "messages-queue")