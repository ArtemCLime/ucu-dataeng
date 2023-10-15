import requests
import random
from time import sleep


class RandomMessageSender:
    def __init__(self, url):
        self.url = url

    def send_messages(self, messages):
        for message in messages:
            message = {"message": message}
            response = requests.post(self.url, params=message)
            print(response.text)

    def get_messages(self):
        response = requests.get(self.url)
        return response.json()["log"]


if __name__ == "__main__":
    # Generate some random messages
    num_messages = range(10)
    test_messages = [f"Message {i}: {random.randint(0, 100)}" for i in num_messages]

    # Wait a little bit for the server to start
    sleep(3)
    sender = RandomMessageSender("http://app1:8000/log")
    sender.send_messages(test_messages)
    core_msg = sender.get_messages()

    secondary1 = RandomMessageSender("http://app2:8001/log")
    app2_msg = secondary1.get_messages()

    secondary2 = RandomMessageSender("http://app3:8002/log")
    app3_msg = secondary2.get_messages()
    # Check if all messages are the same
    print(test_messages == core_msg == app2_msg == app3_msg)
