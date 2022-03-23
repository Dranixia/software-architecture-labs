from flask import Flask, request
from requests import get, post
import uuid

app = Flask(__name__)


@app.route('/facade', methods=['GET', 'POST'])
def requests():
    if request.method == 'GET':
        l_url = "http://localhost:8081/logging"
        m_url = "http://localhost:8082/messages"

        r_l = get(l_url).content.decode("utf-8")
        r_m = get(m_url).content.decode("utf-8")

        return "Logging-service response: " + r_l + "\nMessages-service response: " + r_m + '\n'

    if request.method == 'POST':
        message = request.get_data()

        m_uuid = str(uuid.uuid4())

        logging_url = "http://localhost:8081/logging"
        r = post(logging_url, data={m_uuid: message})

        return r.status_code


if __name__ == '__main__':
    app.run(port=8080)
