from flask import Flask, request
from requests import get, post
from random import choice
import uuid
import sys
import hazelcast
import consul

try:
    port = int(sys.argv[1])
except:
    raise AttributeError("Must specify port (int) before running the app!\n")

session = consul.Consul(host='localhost', port=8500)
session.agent.service.register('facade-service', port=port, service_id=f"facade-{str(uuid.uuid4())}")

app = Flask(__name__)

services = session.agent.services()

logging_clients = []
messages_clients = []

for key, value in services.items():
    service_type = key.split("-")[0]
    if service_type == "logging":
        logging_clients.append(f"http://localhost:{value['Port']}/logging")
    elif service_type == "messages":
        messages_clients.append(f"http://localhost:{value['Port']}/messages")

client = hazelcast.HazelcastClient(cluster_name="dev",
                                   cluster_members=session.kv.get('hazel_ports')[1]['Value'].decode("utf-8").split()
                                   )

message_q = client.get_queue(session.kv.get('queue')[1]['Value'].decode("utf-8")).blocking()


@app.route('/facade', methods=['GET', 'POST'])
def requests():
    print(logging_clients)
    if request.method == 'GET':
        return "Logging-service response: " + get(choice(logging_clients)).text + "\nMessages-service response: " \
               + get(choice(messages_clients)).text + '\n'

    if request.method == 'POST':
        message_q.put(f"{request.get_json()}")

        message = request.get_json()
        m_uuid = str(uuid.uuid4())
        r = post(choice(logging_clients), data={"id": m_uuid, "msg": message})

        return r.text


if __name__ == '__main__':
    app.run(port=port)
