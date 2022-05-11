from flask import Flask
import hazelcast
import sys

app = Flask(__name__)

client = hazelcast.HazelcastClient(cluster_members=["172.17.0.2:5701", "172.17.0.3:5701", "172.17.0.4:5701"])
message_q = client.get_queue("message-queue").blocking()
message_data = []


@app.route('/messages', methods=['GET'])
def mess_requests():
    while not message_q.is_empty():
        message_data.append(message_q.take())
        print(f"New message: {message_data[-1]}")
    return " ".join(message_data)


if __name__ == '__main__':
    app.run(port=int(sys.argv[1]))
