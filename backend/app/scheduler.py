from collections import deque
import time
import asyncio


class RoomScheduler:
    def __init__(self, room_id, initial_temperature, target_temperature):
        self.room_id = room_id
        self.priority = 0  # Default priority is 0
        self.current_temperature = initial_temperature
        self.initial_temperature = initial_temperature
        self.target_temperature = target_temperature
        self.is_on = False  # Default is off
        self.last_scheduler_time = time.time()  # Last time the room is scheduled
        self.mode = "cool"  # Default is cool
        self.last_update_temperature = time.time()  # Last time the temperature is updated

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
            """Summer Mode"""
            time_increment = int(time_elapsed / 10)
            if self.current_temperature <= self.initial_temperature:
                change_temperature = self.current_temperature + 0.5 * time_increment
                self.current_temperature = min(
                    change_temperature, self.initial_temperature
                )
                self.last_update_temperature += time_increment * 10


class Scheduler:
    def __init__(self):
        self.waiting_queue = deque()
        self.service_queue = deque()

    def add_room_queue(self, room):
        current_time = time.time()
        if len(self.service_queue) < 3 and len(self.waiting_queue) == 0:
            self.service_queue.append(room)
            room.last_scheduled_time = current_time
            return 1  # OK
        else:
            self.waiting_queue.append(room)
            return 0  # Waiting

    def close_air_conditioner(self, room):
        current_time = time.time()
        room.is_on = False
        if room in self.service_queue:
            self.service_queue.remove(room)
            room.last_update_temperature = current_time
        if room in self.waiting_queue:
            self.waiting_queue.remove(room)

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

    def run_scheduler(self):
        while True:
            self.schedule_rooms()
            asyncio.sleep(10)


scheduler = Scheduler()
room_scheduler_map = {}