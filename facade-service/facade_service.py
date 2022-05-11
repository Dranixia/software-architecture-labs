from flask import Flask, request
from requests import get, post
from random import choice
import uuid
import sys
import hazelcast

app = Flask(__name__)

m_urls = ["http://localhost:8084/messages", "http://localhost:8085/messages"]
l_urls = ["http://localhost:8081/logging", "http://localhost:8082/logging", "http://localhost:8083/logging"]


client = hazelcast.HazelcastClient(cluster_members=["172.17.0.2:5701", "172.17.0.3:5701", "172.17.0.4:5701"])
message_q = client.get_queue("message-queue").blocking()


@app.route('/facade', methods=['GET', 'POST'])
def requests():
    if request.method == 'GET':

        r_l = get(choice(l_urls)).text
        r_m = get(choice(m_urls)).text

        return "Logging-service response: " + r_l + "\nMessages-service response: " + r_m + '\n'

    if request.method == 'POST':

        message_q.put(f"{request.get_json()}")

        message = request.get_json()
        m_uuid = str(uuid.uuid4())

        r = post(choice(l_urls), data={"id": m_uuid, "msg": message})

        return r.text


if __name__ == '__main__':
    app.run(port=int(sys.argv[1]))
