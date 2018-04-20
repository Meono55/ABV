from flask import Flask
from twilio.twiml.messaging_response import MessagingResponse
from flask import request

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def handle_sms():


    #get sms msg from HTTP params

    inbound_message = request.form['Body']

    #get query from sms Msg




    response = MessagingResponse()

    print(inbound_message)

    response.message("HELLO THERE DUDE")

    return str(response)



if __name__ == "__main__":
    app.run(debug=True)

