from flask import Flask, request
from requests import get, post
from random import choice
import uuid
import sys

app = Flask(__name__)


@app.route('/facade', methods=['GET', 'POST'])
def requests():
    if request.method == 'GET':
        m_url = "http://localhost:8081/messages"
        l_urls = ["http://localhost:8082/logging", "http://localhost:8083/logging", "http://localhost:8084/logging"]

        r_l = get(choice(l_urls)).text
        r_m = get(m_url).text

        return "Logging-service response: " + r_l + "\nMessages-service response: " + r_m + '\n'

    if request.method == 'POST':
        message = request.get_data()
        m_uuid = str(uuid.uuid4())

        l_urls = ["http://localhost:8082/logging", "http://localhost:8083/logging", "http://localhost:8084/logging"]
        r = post(choice(l_urls), data={"id": m_uuid, "msg": message})

        return r.text


if __name__ == '__main__':
    app.run(port=int(sys.argv[1]))
