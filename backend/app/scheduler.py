import time
import asyncio
import base64
import heapq
import json
import threading
import time
import requests
import rsa
from collections import deque
from datetime import datetime
from threading import Thread
from app import db
from app.models import Status

"""
Hint: scheduler.py is a file that contains all the scheduler functions for the app.
"""

class Scheduler:
    def __init__(self):
        self.waiting_queue = deque()
        self.service_queue = deque()

    # Add a room to the scheduler
    def add_room_queue(self, room):
        current_time = time.time()
        if len(self.service_queue) < 3 and len(self.waiting_queue) == 0:
            self.service_queue.append(room)
            room.last_scheduled_time = current_time
            return 1
        else:
            self.waiting_queue.append(room)
            return 0

    # Remove a room from the scheduler
    def close_air_conditioner(self, room):
        current_time = time.time()
        room.is_on = False
        if room in self.service_queue:
            self.service_queue.remove(room)
            room.last_update_temperature = current_time
        if room in self.waiting_queue:
            self.waiting_queue.remove(room)

    # Update the temperature of all the rooms
    def schedule_rooms(self):
        # Priority scheduling
        self.waiting_queue = deque(
            sorted(self.waiting_queue, key=lambda r: r.priority, reverse=True)
        )

        # Time scheduling
        current_time = time.time()
        while (
            self.service_queue
            and (current_time - self.service_queue[0].last_scheduled_time) >= 20
        ):
            room = self.service_queue.popleft()
            room.last_scheduled_time = current_time
            self.waiting_queue.append(room)

        while self.waiting_queue and len(self.service_queue) < 3:
            room = self.waiting_queue.popleft()
            room.last_scheduled_time = current_time
            self.service_queue.append(room)

    # Run the scheduler
    def run_scheduler(self):
        while True:
            self.schedule_rooms()
            asyncio.sleep(10)


class RoomScheduler:
    def __init__(self, room_id, initial_temperature, target_temperature):
        # All of them are default values
        self.room_id = room_id
        self.priority = 0
        self.current_temperature = initial_temperature
        self.initial_temperature = initial_temperature
        self.target_temperature = target_temperature
        self.is_on = False
        self.last_scheduler_time = time.time()
        self.mode = "cool"
        self.last_update_temperature = time.time()

    # Update the temperature of the room
    def update_temperature(self):
        current_time = time.time()
        time_elapsed = current_time - self.last_update_temperature
        if self.is_on:
            time_increment = int(time_elapsed / 10)
            if self.mode == "cool":
                if self.current_temperature >= self.target_temperature:
                    change_temperature = self.current_temperature - 0.5 * time_increment
                    self.current_temperature = max(
                        change_temperature, self.target_temperature
                    )
                    self.last_update_temperature += time_increment * 10
                else:
                    self.current_temperature = self.target_temperature
            else:
                if self.current_temperature <= self.target_temperature:
                    change_temperature = self.current_temperature + 0.5 * time_increment
                    self.current_temperature = min(
                        change_temperature, self.target_temperature
                    )
                    self.last_update_temperature += time_increment * 10
                else:
                    self.current_temperature = self.target_temperature
        else:
            time_increment = int(time_elapsed / 10)
            if self.current_temperature <= self.initial_temperature:
                change_temperature = self.current_temperature + 0.5 * time_increment
                self.current_temperature = min(
                    change_temperature, self.initial_temperature
                )
                self.last_update_temperature += time_increment * 10


# Send control to client
def client_control(room_id, public_key, operation, value):
    response = requests.post(
        client_remote_map[room_id],
        base64.urlsafe_b64encode(
            rsa.encrypt(json.dumps({"operation": operation, "data": value}).encode(), public_key)
        ).decode(),
    )
    print("Send control to ", client_remote_map[room_id], " with operation ", operation, " and value ", value)
    if response.status_code == 204:
        return True
    else:
        return False

# Make a simple room status
def make_simple_room_status(room_id, public_key):
    return RoomStatusEntry(room_id, public_key, 25, 2, "cool", False, False, 0)

# RoomStatusEntry is a class that contains all the information about a room.
class RoomStatusEntry:
    def __init__(
        self,
        room_id,
        public_key,
        temperature,
        wind_speed,
        mode,
        sweep,
        is_on,
        last_update,
    ):
        self.public_key = rsa.PublicKey.load_pkcs1_openssl_pem(('-----BEGIN PUBLIC KEY-----\n' + public_key + '\n-----END PUBLIC KEY-----').encode())
        self.room_id = room_id
        self.temperature = temperature
        self.initial_temperature = temperature
        self.wind_speed = wind_speed
        self.mode = mode
        self.sweep = sweep
        self.is_on = is_on
        self.last_update = last_update
        self.ctx = None

    def put_status(self):
        self.ctx.push()
        status = Status(
            room_id=self.room_id,
            temperature=self.temperature,
            wind_speed=self.wind_speed,
            mode=self.mode,
            sweep=self.sweep,
            is_on=self.is_on,
            last_update=datetime.utcnow(),
        )
        db.session.add(status)
        db.session.commit()
        self.ctx.pop()

    def set_temperature(self, temperature):
        self.temperature = temperature
        self.put_status()
        client_control(self.room_id, self.public_key, "temperature", str(temperature))

    def set_wind_speed(self, wind_speed):
        self.wind_speed = wind_speed
        self.put_status()
        client_control(self.room_id, self.public_key, "wind_speed", str(wind_speed))

    def set_mode(self, mode):
        self.mode = mode
        self.put_status()
        client_control(self.room_id, self.public_key, "mode", mode)

    def set_sweep(self, sweep):
        self.sweep = sweep
        self.put_status()
        client_control(self.room_id, self.public_key, "sweep", str(sweep))

    def set_is_on(self, is_on):
        self.is_on = is_on
        self.put_status()
        client_control(self.room_id, self.public_key, "start" if is_on else "stop", "")

    def updated(self):
        self.last_update = time.time()

    def __gt__(self, other):
        return self.wind_speed > other.wind_speed

    def __lt__(self, other):
        return self.wind_speed < other.wind_speed

# StatusScheduler is a class that contains all the information about the scheduler.
class StatusScheduler:
    def __init__(self):
        self.ctx = None
        self.room_scheduler_map = {}
        self.waiting_queue = []
        self.service_queue = []
        self.cooldown_queue = []
        self.mutex = threading.Lock()
        self.special_initialized = False

    def room_online(self, room_id, public_key):
        self.mutex.acquire()
        if room_id not in self.room_scheduler_map:
            self.room_scheduler_map[room_id] = make_simple_room_status(room_id, public_key)
            self.room_scheduler_map[room_id].ctx = self.ctx
        self.mutex.release()

    def add_room_in_queue(self, room_id):
        self.mutex.acquire()
        heapq.heappush(self.waiting_queue, room_id)
        self.room_scheduler_map[room_id].updated()
        self.mutex.release()

    def update_wind_speed(self, room_id, wind_speed):
        self.mutex.acquire()
        self.room_scheduler_map[room_id].set_wind_speed(wind_speed)
        if room_id in self.waiting_queue:
            self.waiting_queue.remove(room_id)
            heapq.heapify(self.waiting_queue)
            heapq.heappush(self.waiting_queue, room_id)
        if room_id in self.cooldown_queue:
            self.cooldown_queue.remove(room_id)
            heapq.heapify(self.cooldown_queue)
            heapq.heappush(self.cooldown_queue, room_id)
        self.mutex.release()

    def update_temperature(self, room_id, temperature):
        self.mutex.acquire()
        self.room_scheduler_map[room_id].set_temperature(temperature)
        self.mutex.release()

    def update_mode(self, room_id, mode):
        self.mutex.acquire()
        self.room_scheduler_map[room_id].set_mode(mode)
        self.mutex.release()

    def update_sweep(self, room_id, sweep):
        self.mutex.acquire()
        self.room_scheduler_map[room_id].set_sweep(sweep)
        self.mutex.release()

    def remove_room_from_queue(self, room_id):
        self.mutex.acquire()
        if room_id in self.service_queue:
            self.service_queue.remove(room_id)
        if room_id in self.waiting_queue:
            self.waiting_queue.remove(room_id)
            heapq.heapify(self.waiting_queue)
        if room_id in self.cooldown_queue:
            self.cooldown_queue.remove(room_id)
            heapq.heapify(self.cooldown_queue)
        self.room_scheduler_map[room_id].set_is_on(False)
        self.mutex.release()

    def schedule(self):
        self.mutex.acquire()

        service_queue_copy = self.service_queue.copy()

        for room_id in self.service_queue:
            room_status = self.room_scheduler_map[room_id]
            if room_status.last_update > time.time() - 120:
                self.service_queue.remove(room_id)
                heapq.heappush(self.cooldown_queue, room_id)

        cooldown_queue_copy = self.cooldown_queue.copy()
        cooldown_queue_copy.sort(key=lambda x: self.room_scheduler_map[x].last_update)
        for room_id in cooldown_queue_copy:
            room_status = self.room_scheduler_map[room_id]
            if room_status.last_update > time.time() - 120:
                self.cooldown_queue.remove(room_id)
                heapq.heapify(self.cooldown_queue)
                heapq.heappush(self.waiting_queue, room_id)

        while len(self.service_queue) < 3 and len(self.waiting_queue) > 0:
            room_to_schedule = heapq.heappop(self.waiting_queue)
            self.service_queue.append(room_to_schedule)
        while len(self.service_queue) < 3 and len(self.cooldown_queue) > 0:
            room_to_schedule = heapq.heappop(self.cooldown_queue)
            self.service_queue.append(room_to_schedule)

        to_remove = []
        to_add = []

        service_queue_scheduled_copy = self.service_queue.copy()
        for room_id in service_queue_scheduled_copy:
            if room_id not in service_queue_copy:
                to_add.append(room_id)
        for room_id in service_queue_copy:
            if room_id not in service_queue_scheduled_copy:
                to_remove.append(room_id)

        for room_id in to_remove:
            self.room_scheduler_map[room_id].set_is_on(False)
            self.room_scheduler_map[room_id].updated()
        for room_id in to_add:
            self.room_scheduler_map[room_id].set_is_on(True)
            self.room_scheduler_map[room_id].updated()

        for room_id in self.room_scheduler_map:
            room_status = self.room_scheduler_map[room_id]
            if room_status.last_update < time.time() - 120 and not room_status.is_on:
                if room_status.temperature > room_status.initial_temperature:
                    room_status.set_temperature(room_status.temperature - 1)
                elif room_status.temperature < room_status.initial_temperature:
                    room_status.set_temperature(room_status.temperature + 1)
                room_status.updated()

        self.mutex.release()

    def run_scheduler_thread(self):
        while True:
            self.schedule()
            time.sleep(10)

    def run_scheduler(self, ctx):
        self.ctx = ctx
        Thread(target=self.run_scheduler_thread, daemon=True).start()

# Initialize the scheduler
client_remote_map = {}
scheduler = StatusScheduler()