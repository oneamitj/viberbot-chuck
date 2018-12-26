from flask import Flask, request, Response
from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.messages.text_message import TextMessage
from viberbot.api.viber_requests import ViberConversationStartedRequest
from viberbot.api.viber_requests import ViberFailedRequest
from viberbot.api.viber_requests import ViberMessageRequest
from viberbot.api.viber_requests import ViberSubscribedRequest
from viberbot.api.viber_requests import ViberUnsubscribedRequest
from viberbot.api.event_type import EventType

import time
import logging
import sched
import threading
import os
import datetime as dt
import json

from bs4 import BeautifulSoup
import urllib.request, urllib.error, urllib.parse

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

app = Flask(__name__)
viber = Api(BotConfiguration(
    name='MY_BOT_NAME',
    avatar='MY_IMAGE_URL',
    auth_token='MY_APP_TOKEN'
))


@app.route('/', methods=['GET'])
def HOME():
    # print("--------------------------------HOME--------------------------------")
    return "<html><h1>Viber bot that gives Chuck Norris joke as reply of each message.</h1></html>"


@app.route('/', methods=['POST'])
def incoming():
    # logger.debug("received request. post data: {0}".format(request.get_data()))
    # print("--------------------------------{}--------------------------------".format(request.get_data()))

    try:
        # print("--------------------------------INSIDE TRY--------------------------------")
        viber_request = viber.parse_request(request.get_data())

        if isinstance(viber_request, ViberMessageRequest):
            message = retrieve_chuck_joke()
            viber.send_messages(viber_request.sender.id, [
                TextMessage(text=message)
            ])
        elif isinstance(viber_request, ViberConversationStartedRequest) \
                or isinstance(viber_request, ViberSubscribedRequest) \
                or isinstance(viber_request, ViberUnsubscribedRequest):
            viber.send_messages(viber_request.sender.id, [
                TextMessage(None, None, viber_request.get_event_type())
            ])
        elif isinstance(viber_request, ViberFailedRequest):
            logger.warning("client failed receiving message. failure: {0}".format(viber_request))

        # elif isinstance(viber_request, EventType.WEBHOOK):
            # logger.debug("WEBHOOKEVENTS: {0}".format(request.get_data()))
            # print("--------------------------------WEBHOOKEVENTS--------------------------------")
    except Exception as e:
        return "--------------------------------ERRRRRRRRRRRRRRRRRRRR--------------------------------" + str(e)

    return Response(status=200)

def set_webhook(viber):
    # print("--------------------------------SET WEBHOOK--------------------------------")
    # I used heroku as it is easier and serves over https
    viber.set_webhook('HEROKU_APP_URL', [EventType.WEBHOOK, EventType.CONVERSATION_STARTED, EventType.DELIVERED, EventType.MESSAGE, EventType.SUBSCRIBED, EventType.UNSUBSCRIBED, EventType.FAILED, EventType.SEEN])

@app.route('/chuckjoke', methods=['GET'])
def retrieve_chuck_joke(url="https://chucknorrisfacts.net/random-fact.php"):
    user_agent = 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.63 Safari/534.3'
    headers = {'User-Agent': user_agent}
    joke_txt = ""

    try:
        req = urllib.request.Request(url, None, headers)
        response = urllib.request.urlopen(req)
        html_page = response.read()
        response.close()
        soup_page = BeautifulSoup(html_page, "html.parser")
        joke_p = soup_page.find_all('p')
        joke_txt = joke_p[0].get_text()
    except Exception as e:
        logger.debug('Error fetching data from ' + url, e)

    return joke_txt

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1>"

if __name__ == "__main__":
    scheduler = sched.scheduler(time.time, time.sleep)
    scheduler.enter(13, 1, set_webhook, (viber,))
    t = threading.Thread(target=scheduler.run)
    t.start()

    app.run(host='0.0.0.0', port=int(os.getenv("PORT", "8443")), debug=True)

