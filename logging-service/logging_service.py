from flask import Flask, request
import hazelcast
import sys

app = Flask(__name__)


@app.route('/logging', methods=['GET', 'POST'])
def log_requests():

    client = hazelcast.HazelcastClient(cluster_members=["172.17.0.2:5701", "172.17.0.3:5701", "172.17.0.4:5701"])
    message_dict = client.get_map("logging-map").blocking()

    if request.method == 'GET':
        return " ".join(message_dict.values())

    if request.method == 'POST':
        uuid = request.form["id"]
        msg = request.form["msg"]

        print(f"ID:{uuid} Message:{msg}")

        message_dict.lock(uuid)
        try:
            message_dict.put(uuid, msg)
        finally:
            message_dict.unlock(uuid)
        return "logging-return-value"


if __name__ == '__main__':
    app.run(port=int(sys.argv[1]))
