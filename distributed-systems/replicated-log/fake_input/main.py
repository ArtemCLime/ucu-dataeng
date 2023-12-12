import requests
import random
from time import sleep


class RandomMessageSender:
    def __init__(self, url):
        self.url = url

    def send_messages(self, messages, write_concern):
        for message in messages:
            message = {"message": message, "write_concern": write_concern}
            response = requests.post(self.url, params=message)
            print(response.text)

    def get_messages(self):
        response = requests.get(self.url)
        return response.json()["log"]

    def clean(self):
        requests.delete(self.url)


def run_test(write_concern=3):
    print(f"Running test with write concern {write_concern}")
    num_messages = range(10)
    test_messages = [f"Message {i}: {random.randint(0, 100)}" for i in num_messages]

    sender = RandomMessageSender("http://app1:8000/log")
    sender.send_messages(test_messages, write_concern=write_concern)
    core_msg = sender.get_messages()

    secondary1 = RandomMessageSender("http://app2:8001/log")
    app2_msg = secondary1.get_messages()

    secondary2 = RandomMessageSender("http://app3:8002/log")
    app3_msg = secondary2.get_messages()
    # Check if all messages are the same
    if write_concern == 3:
        print(test_messages == core_msg == app2_msg == app3_msg)
    elif write_concern == 2:
        print((test_messages == core_msg == app2_msg) or (test_messages == core_msg == app3_msg))
    else:
        print(test_messages == core_msg)

    # Clean up
    sender.clean()
    secondary1.clean()
    secondary2.clean()
    print("End of test\n")


if __name__ == "__main__":
    # Wait a little bit for the server to start
    sleep(3)
    # Wait for all servers to replicate
    run_test(write_concern=3)
    # # Wait for master and 1 secondary to replicate
    # run_test(write_concern=2)
    # # Wait for master to replicate
    # run_test(write_concern=1)
