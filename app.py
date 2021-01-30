import slack
import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, request, Response
from slackeventsapi import SlackEventAdapter
import string
from datetime import datetime, timedelta
import time

load_dotenv()

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(
    os.environ['SLACK_SIGNING_SECRET'], '/slack/events', app)

client = slack.WebClient(token=os.environ['SLACK_BOT_TOKEN'])
BOT_ID = client.api_call("auth.test")['user_id']


BAD_WORDS = ['hmm', 'no', 'tim']

def check_if_bad_words(message):
    msg = message.lower()
    msg = msg.translate(str.maketrans('', '', string.punctuation))

    return any(word in msg for word in BAD_WORDS)


@ slack_event_adapter.on('message')
def message(payload):
    event = payload.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')

    if user_id != None and BOT_ID != user_id:
        if user_id in message_counts:
            message_counts[user_id] += 1
        else:
            message_counts[user_id] = 1

        if text.lower() == 'start':
            send_welcome_message(f'@{user_id}', user_id)
        elif check_if_bad_words(text):
            ts = event.get('ts')
            client.chat_postMessage(
                channel=channel_id, thread_ts=ts, text="THAT IS A BAD WORD!")


# @ app.route('/message-count', methods=['POST'])
# def message_count():
#     data = request.form
#     user_id = data.get('user_id')
#     channel_id = data.get('channel_id')
#     message_count = message_counts.get(user_id, 0)

#     client.chat_postMessage(
#         channel=channel_id, text=f"Message: {message_count}")
#     return Response(), 200


if __name__ == "__main__":
    port = int(os.getenv('PORT', 3000))
    app.run(debug=False, port=port, host='0.0.0.0')

# создали ендпоинт
# @app.route('/webhook2')
# def hello_slack():
#     # получили данные из запроса
#     request_json = request.get_json(silent=True, force=True)
#     # тут ваш код возьмет запрос и вернет в ответ любой dict объект ответа, можно даже пустой
#     # примерно так request_json -> response_body_json
#     ...
#     response_body = json.dumps(request_json)
#     # упаковали все в корректный респонс
#     response = make_response((response_body['challenge']),200)
#     response.headers['Content-Type'] = 'text/plain'
#     # и вернули
#     return response

# if __name__ == '__main__':
#     port = int(os.getenv('PORT', 5000))
#     app.run(debug=False, port=port, host='0.0.0.0')
