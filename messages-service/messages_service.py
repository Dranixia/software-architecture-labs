from flask import Flask
import hazelcast
import sys
import consul
import uuid


try:
    port = int(sys.argv[1])
except:
    raise AttributeError("Must specify port (int) before running the app!\n")

session = consul.Consul(host='localhost', port=8500)
session.agent.service.register('messages-service', port=port, service_id=f"messages-{str(uuid.uuid4())}")

app = Flask(__name__)

client = hazelcast.HazelcastClient(cluster_name="dev",
                                   cluster_members=session.kv.get('hazel_ports')[1]['Value'].decode("utf-8").split()
                                   )

message_q = client.get_queue(session.kv.get('queue')[1]['Value'].decode("utf-8")).blocking()
message_data = []


@app.route('/messages', methods=['GET'])
def mess_requests():
    while not message_q.is_empty():
        message_data.append(message_q.take())
        print(f"New message: {message_data[-1]}")  # Debug print
    return " ".join(message_data)


if __name__ == '__main__':
    app.run(port=port)
