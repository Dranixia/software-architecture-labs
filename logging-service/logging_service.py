from flask import Flask, request

message_dict = dict()
app = Flask(__name__)


@app.route('/logging', methods=['GET', 'POST'])
def log_requests():
    if request.method == 'GET':
        return str(list(message_dict.values()[::-1]))

    if request.method == 'POST':
        mssg_d = request.form.to_dict()
        pair = mssg_d.popitem()
        message_dict[pair[0]] = pair[1]
        return {"statusCode": 200}


if __name__ == '__main__':
    app.run(port=8081)
