# define a client class

import threading
# import time
import database

_MAX_MISSED = 20

class Client:
    def __init__(self, client_id, user_id):
        self.client_id = client_id
        self.user_id = user_id
        self.classroom_id = None
        self.valid = True
        self.missed_heartbeats = 0
        self.heartbeat_interval = 3  # seconds
        self.heartbeat_timer = threading.Timer(self.heartbeat_interval, self.check_heartbeat)
        self.heartbeat_timer.start()

    def set_classroom(self, classroom_id):
        self.classroom_id = classroom_id

    def check_heartbeat(self):
        # while True:
        #     time.sleep(self.heartbeat_interval)
        #     if self.missed_heartbeats >= _MAX_MISSED:
        #         print(f"Client {self.client_id} disconnected")
        #         # Handle disconnection
        #         self.on_disconnect()
        #         break
        #     else:
        #         self.missed_heartbeats += 1

        if self.missed_heartbeats >= _MAX_MISSED:
            print(f"Client {self.client_id} disconnected")
            # Handle disconnection
            self.on_disconnect()
        else:
            self.missed_heartbeats += 1
            self.heartbeat_timer = threading.Timer(self.heartbeat_interval, self.check_heartbeat)
            self.heartbeat_timer.start()

    def receive_heartbeat(self):
        self.missed_heartbeats = 0

    def on_disconnect(self):
        self.valid = False
        self.heartbeat_timer.cancel()
        if self.classroom_id:
            database.leave_classroom(self.user_id, self.classroom_id)

