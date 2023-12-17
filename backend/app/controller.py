import base64
import heapq
import json
import threading
import time
from datetime import datetime
from threading import Thread

import requests
import rsa

from app import db
from app.datamodel import Status

client_remote_map = {}

TIME_SCHEDULE = 20


def client_control(room_id, public_key, operation, value):
    # 发送控制命令到客户端
    response = requests.post(
        client_remote_map[room_id],
        base64.urlsafe_b64encode(
            rsa.encrypt(
                json.dumps({"operation": operation, "data": value}).encode(), public_key
            )
        ).decode(),
    )
    print(
        "发送控制命令至",
        client_remote_map[room_id],
        "，操作为",
        operation,
        "，值为",
        value,
    )
    if response.status_code == 204:
        return True
    else:
        return False


def make_simple_room_status(room_id, public_key):
    # 创建简单的房间状态对象
    return RoomStatusEntry(room_id, public_key, 25, 2, "cool", False, False, 0)



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
        # 初始化房间状态对象
        self.public_key = rsa.PublicKey.load_pkcs1_openssl_pem(
            (
                "-----BEGIN PUBLIC KEY-----\n"
                + public_key
                + "\n-----END PUBLIC KEY-----"
            ).encode()
        )
        self.room_id = room_id
        self.temperature = temperature
        self.initial_temperature = temperature
        self.wind_speed = wind_speed
        self.mode = mode
        self.sweep = sweep
        self.is_on = is_on
        self.last_update = last_update
        self.last_temperature_update = last_update
        self.last_start = last_update
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
        if is_on:
            self.last_start = time.time()
        self.put_status()
        client_control(self.room_id, self.public_key, "start" if is_on else "stop", "")

    def updated(self):
        self.last_update = time.time()

    def updated_temperature(self):
        self.last_temperature_update = time.time()

    def __gt__(self, other):
        return self.wind_speed > other.wind_speed

    def __lt__(self, other):
        return self.wind_speed < other.wind_speed


class StatusScheduler:
    def __init__(self):
        # 初始化调度器
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
            self.room_scheduler_map[room_id] = make_simple_room_status(
                room_id, public_key
            )
            self.room_scheduler_map[room_id].ctx = self.ctx
        self.mutex.release()

    def add_room_in_queue(self, room_id):
        self.mutex.acquire()
        room_status = self.room_scheduler_map[room_id]
        if (
            room_status not in self.service_queue
            and room_status not in self.waiting_queue
            and room_status not in self.cooldown_queue
        ):
            heapq.heappush(self.waiting_queue, room_status)
            room_status.set_is_on(False)
            room_status.updated()
        self.mutex.release()

    def update_wind_speed(self, room_id, wind_speed):
        self.mutex.acquire()
        room_status = self.room_scheduler_map[room_id]
        room_status.set_wind_speed(wind_speed)
        if room_status in self.waiting_queue:
            self.waiting_queue.remove(room_status)
            heapq.heapify(self.waiting_queue)
            heapq.heappush(self.waiting_queue, room_status)
        if room_status in self.cooldown_queue:
            self.cooldown_queue.remove(room_status)
            heapq.heapify(self.cooldown_queue)
            heapq.heappush(self.cooldown_queue, room_status)
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
        room_status = self.room_scheduler_map[room_id]
        if room_status in self.service_queue:
            self.service_queue.remove(room_status)
        if room_status in self.waiting_queue:
            self.waiting_queue.remove(room_status)
            heapq.heapify(self.waiting_queue)
        if room_status in self.cooldown_queue:
            self.cooldown_queue.remove(room_status)
            heapq.heapify(self.cooldown_queue)
        room_status.set_is_on(False)
        self.mutex.release()

    def schedule(self):
        self.mutex.acquire()

        # initialize
        self.service_queue.sort(key=lambda x: x.last_start)
        service_queue_copy = self.service_queue.copy()

        # timeout cooldown for RR
        for room_status in self.service_queue:
            if room_status.last_update <= time.time() - TIME_SCHEDULE:
                self.service_queue.remove(room_status)
                room_status.updated()
                heapq.heappush(self.cooldown_queue, room_status)

        # timeout waiting for RR
        cooldown_queue_copy = self.cooldown_queue.copy()
        cooldown_queue_copy.sort(key=lambda x: x.last_update)
        for room_status in cooldown_queue_copy:
            if room_status.last_update <= time.time() - TIME_SCHEDULE:
                self.cooldown_queue.remove(room_status)
                heapq.heapify(self.cooldown_queue)
                heapq.heappush(self.waiting_queue, room_status)

        heapq.heapify(self.waiting_queue)
        heapq.heapify(self.cooldown_queue)

        # schedule
        while len(self.service_queue) < 3 and len(self.waiting_queue) > 0:
            room_to_schedule = heapq.heappop(self.waiting_queue)
            self.service_queue.append(room_to_schedule)
        while len(self.service_queue) < 3 and len(self.cooldown_queue) > 0:
            room_to_schedule = heapq.heappop(self.cooldown_queue)
            self.service_queue.append(room_to_schedule)

        # update status
        to_remove = []
        to_add = []

        service_queue_scheduled_copy = self.service_queue.copy()
        for room_status in service_queue_scheduled_copy:
            if room_status not in service_queue_copy:
                to_add.append(room_status)
        for room_status in service_queue_copy:
            if room_status not in service_queue_scheduled_copy:
                to_remove.append(room_status)

        for room_status in to_remove:
            room_status.set_is_on(False)
            room_status.updated()
        for room_status in to_add:
            room_status.set_is_on(True)
            room_status.updated()

        # update temperature for not running rooms
        for id in self.room_scheduler_map:
            room_status = self.room_scheduler_map[id]
            if (
                room_status.last_temperature_update <= time.time() - TIME_SCHEDULE
                and not room_status.is_on
            ):
                if room_status.temperature > room_status.initial_temperature:
                    room_status.set_temperature(room_status.temperature - 1)
                elif room_status.temperature < room_status.initial_temperature:
                    room_status.set_temperature(room_status.temperature + 1)
                room_status.updated_temperature()

        self.mutex.release()

    def run_scheduler_thread(self):
        while True:
            self.schedule()
            print(
                "Current service queue: ",
                [i.room_id for i in self.service_queue],
                " Waiting queue: ",
                [i.room_id for i in self.waiting_queue],
                " Cooldown queue: ",
                [i.room_id for i in self.cooldown_queue],
            )
            time.sleep(1)

    def run_scheduler(self, ctx):
        self.ctx = ctx
        Thread(target=self.run_scheduler_thread, daemon=True).start()


def main():
    # 实例化调度器
    scheduler = StatusScheduler()

if __name__ == "__main__":
    main()
