from flask import Flask
from twilio.twiml.messaging_response import MessagingResponse
from flask import request
import requests
import json

app = Flask(__name__)


def count_beers(query_results):
    data = json.loads(query_results)
    return len(data)


@app.route("/", methods=['GET', 'POST'])
def handle_sms():

    style = request.form['Body']
    query_results = requests.get("http://beerapi/current?style={}".format(style))

    # if requests.get failed for any reason:
    #    reseponse = MessagingReponse()
    #    response.message("Sorry, I cannot hand your request.  Please try again later")
    #    return str(response)

    count = count_beers(query_results.text)

    response = MessagingResponse()
    if count == 0:
        response.message("Sorry, no results for stout")
    elif count == 1:
        response.message("There is 1 beer with the style {}".format(style))
    else:
        response.message("There are {} beers with the style {}.".format(count, style))
    return str(response)


if __name__ == "__main__":
    app.run(debug=True)

