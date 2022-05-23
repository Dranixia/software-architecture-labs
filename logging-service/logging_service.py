from flask import Flask, request
import hazelcast
import sys
import uuid
import consul

try:
    port = int(sys.argv[1])
except:
    raise AttributeError("Must specify port (int) before running the app!\n")

session = consul.Consul(host='localhost', port=8500)
session.agent.service.register('logging-service', port=port, service_id=f"logging-{str(uuid.uuid4())}")

app = Flask(__name__)

client = hazelcast.HazelcastClient(cluster_name="dev",
                                   cluster_members=session.kv.get('hazel_ports')[1]['Value'].decode("utf-8").split()
                                   )

message_dict = client.get_map(session.kv.get('map')[1]['Value'].decode("utf-8")).blocking()


@app.route('/logging', methods=['GET', 'POST'])
def log_requests():

    if request.method == 'GET':
        return " ".join(message_dict.values())

    if request.method == 'POST':
        uid = request.form["id"]
        msg = request.form["msg"]

        print(f"ID: {uuid}\nMessage: {msg}")  # Test print

        message_dict.lock(uid)
        try:
            message_dict.put(uid, msg)
        finally:
            message_dict.unlock(uid)
        return "logging-return-value"


if __name__ == '__main__':
    app.run(port=port)
