import os
import sys
import json
from chatterbot import ChatBot

import requests
from flask import Flask, request
from settings import TWITTER

app = Flask(__name__)
from chatterbot.trainers import ListTrainer


###################### CHAT BOT ###############################
'''
chatbot = ChatBot(
    'Ron Obvious',
    trainer='chatterbot.trainers.ChatterBotCorpusTrainer'
)

# Train based on the english corpus
chatbot.train("chatterbot.corpus.english")
'''

'''
chatbot = ChatBot("TwitterBot",
    logic_adapters=[
        "chatterbot.logic.BestMatch"
    ],
    input_adapter="chatterbot.input.TerminalAdapter",
    output_adapter="chatterbot.output.TerminalAdapter",
    database="./twitter-database.db",
    twitter_consumer_key=TWITTER["CONSUMER_KEY"],
    twitter_consumer_secret=TWITTER["CONSUMER_SECRET"],
    twitter_access_token_key=TWITTER["ACCESS_TOKEN"],
    twitter_access_token_secret=TWITTER["ACCESS_TOKEN_SECRET"],
    trainer="chatterbot.trainers.TwitterTrainer"
)

chatbot.train()

chatbot.logger.info('Trained database generated successfully!')
'''

chatbot = ChatBot("Fruit")
corpus_file = "../corpus.txt"

with open(corpus_file, "a") as corpus:
    corpus.write("<3")
    corpus.write("\n")

lines = ["hello"]
with open(corpus_file) as f:
    lines = f.read().splitlines()
chatbot.set_trainer(ListTrainer)
chatbot.train(lines)


#############################################################


@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == "fruit-token":
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world !", 200


@app.route('/', methods=['POST'])
def webhook():

    # endpoint for processing incoming messaging events

    data = request.get_json()
    log(data)  # you may not want to log every incoming message in production, but it's good for testing

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message

                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    message_text = messaging_event["message"]["text"]  if "text" in messaging_event["message"] else ""# the message's text

                    # Get a response to an input statement
                    message_text_back = chatbot.get_response(message_text)

                    #store message
                    with open(corpus_file, "a") as corpus:
                        corpus.write(message_text)
                        corpus.write("\n")

                    send_message(sender_id, message_text_back.text)


                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass

    return "ok", 200


def send_message(recipient_id, message_text):

    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": "EAAU2Ik0RVwEBABIZA7PfuetvpGZA79r1pCyMPxHpRj5XZAKEXKnDkZCKg93FWNuJLrYWAH3VZAGbBHQaqZCutezvZArh1A9n7Np5JPvLWIevYFfwpbcEhqgLkZABbWZBpfZACUD3u1AQPK4JOfasQUKtjA6Rf6TXlZCHDKZAA3O8wcngFgZDZD"
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def log(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()


if __name__ == '__main__':
    app.run(debug=True)
