import pandas as pd
import argparse
import time
import threading
import requests
import hashlib
import base64
import rsa
from rsa import common
from rsa import transform
from rsa import core
from typing import List

FILENAME = 'test_case.xlsx'

url = None
port = None

room_map = {
    '房间1': 101,
    '房间2': 102,
    '房间3': 103,
    '房间4': 104,
    '房间5': 105,
}

def generate_signature(message, public_key):
    # Hash the message
    hash_obj = hashlib.sha256(message.encode('utf-8'))
    hash = hash_obj.digest()
    # Decode the public key
    public_key = base64.b64decode(public_key)
    # Convert the public key to an RSA key
    key = rsa.PublicKey.load_pkcs1_openssl_pem(public_key)
    # Encrypt the hash with the RSA key
    signature = rsa.encrypt(hash, key)
    # Encode the encrypted hash in base64
    signature = base64.b64encode(signature)
    # Convert the encrypted hash from bytes to string
    signature = signature.decode('utf-8')

    return signature

def read_excel_case(filename):
    df = pd.read_excel(filename, sheet_name='测试用例')
    return df.iloc[2:28, 0:6]

class Action:
    def __init__(self, room_id: str, input: str):
        self.room_id = room_id
        self.input = input
        self.url = "http://localhost"
        self.port = 11451
        self.unique_id = "unique_id"
        self.public_key = "public_key"

    def post(self):
        current_time = int(time.time())
        if self.input == '开机' or self.input == '关机':
            operation = 'start' if self.input == '开机' else 'stop'
            data = None
        elif self.input in ['高', '中', '低']:
            operation = 'wind_speed'
            speed_map = {
                '高': 3,
                '中': 2,
                '低': 1
            }
            data = speed_map[self.input]
        else:
            operation = 'temperature'
            data = int(self.input)

        signature = generate_signature(operation + self.unique_id + str(data) + str(current_time), self.public_key)

        params = {
            'operation': operation,
            'data': data,
            'time': current_time,
            'unique_id': self.unique_id,
            'signature': signature
        }

        try:
            res = requests.post(f"{self.url}:{self.port}/api/device/client/{self.room_id}", json=params, timeout=5)
            res.raise_for_status()  # This will raise an HTTPError if the HTTP request returned an unsuccessful status code
        except requests.Timeout:
            print("请求超时请重新发送")
            res = requests.post(f"{self.url}:{self.port}/api/device/client/{self.room_id}", json=params)
        except requests.HTTPError as err:
            print(f"请求失败，状态码：{err.response.status_code}")
        else:
            if res.status_code == 204:
                print("操作成功")
            else:
                print(f"操作失败，响应内容：{res.json()}")

time_lock = [False] * 26
condition = threading.Condition()


def thread_request(actions: List[List[Action]]):
    global time_lock, condition
    try:
        # Send request
        for idx, action_list in enumerate(actions):
            for action in action_list:
                print('第%d分钟，%d，%s' % (idx, action.room_id, action.input))
                try:
                    action.post()
                except Exception as e:
                    print(f"请求失败: {e}")
                    exit(0)
                time.sleep(0.4)
        
            with condition:
                time_lock[idx] = True
                time.sleep(1.5)
                condition.notify_all()
            time.sleep(10)
    except KeyboardInterrupt:
        print("线程请求被中断")
        return

roomInfo = None
scheduleInfo = None

def thread_query(actions):
    global time_lock, condition
    try:
        api_room_info = '/api/device/client'
        api_schedule = '/api/device/client'
        df_rooms = pd.DataFrame()
        df_schedule = pd.DataFrame()
        for idx, _ in enumerate(actions):
            with condition:
                condition.wait_for(lambda: time_lock[idx])
            print('第%d分钟' % idx)
            tmp_df = pd.DataFrame()
            for room_id in room_map.values():
                params = {
                    'room_number': room_id
                }
                try:
                    res = requests.get(url + ':' + str(port) + api_room_info, params=params, timeout=5)
                except requests.Timeout:
                    print("请求超时,重新发送")
                    res = requests.get(url + ':' + str(port) + api_room_info, params=params)
                data_dict = res.json()
                # Convert to a dataframe
                data = [data_dict]
                columns_order = ['cur_temperature', 'set_temperature', 'speed', 'bill']
                this_df = pd.DataFrame(data, columns=columns_order)
                tmp_df = pd.concat([tmp_df, this_df], axis=1)
                time.sleep(0.5)
            try:
                res2 = requests.get(url + ':' + str(port) + api_schedule, timeout=5)
            except requests.Timeout:
                print("请求超时,重新发送")
                res2 = requests.get(url + ':' + str(port) + api_schedule)
                    
            df_rooms = pd.concat([df_rooms, tmp_df], axis=0)
            print(df_rooms)
            
            data_schedule = res2.json()
            serving_queue = ['', '', '']
            waiting_queue = ['', '']
            for idx, value in enumerate(data_schedule['serving_queue']):
                serving_queue[idx] = str(value)
            for idx, value in enumerate(data_schedule['waiting_queue']):
                waiting_queue[idx] = str(value)
            
            df1 = pd.DataFrame([serving_queue])
            df2 = pd.DataFrame([waiting_queue])
            df_cat = pd.concat([df1, df2], axis=1)
            df_schedule = pd.concat([df_schedule, df_cat], axis=0)
            print(df_schedule)
            
    except KeyboardInterrupt:
        print("线程查询被中断")
        return
    
    global roomInfo, scheduleInfo
    roomInfo = df_rooms
    scheduleInfo = df_schedule

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-u',
                        '--url', 
                        type=str, 
                        default='127.0.0.1')
    parser.add_argument('-p',
                        '--port', 
                        type=int, 
                        default=11451)
    args = parser.parse_args()

    url = args.url
    port = args.port
    
    url = 'http://' + url
    
    # Read excel case
    case_df = read_excel_case(FILENAME)
    
    # To string
    actions = []
    for index, row in case_df.iterrows():
        time_ = row['时间(min)']
        action_once = []
        for room in case_df.columns[1:]:
            operation = row[room]
            if not pd.isna(operation):
                # If operation is not nan, then add to the action list
                tmp_op = str(operation)
                room_id = room_map[room]
                op = []
                if '，' in tmp_op:
                    op = tmp_op.split('，')
                else:
                    op.append(tmp_op)
                for item in op:
                    action_once.append(Action(room_id, item))
                    
        actions.append(action_once)

    thread1 = threading.Thread(target=thread_request, args=(actions,), daemon=True)
    thread2 = threading.Thread(target=thread_query, args=(actions,), daemon=True)
    thread1.start()
    time.sleep(1)
    thread2.start()
    
    try:
        # Wait for the thread to finish
        thread1.join()
        thread2.join()
    except KeyboardInterrupt:
        print("主程序中断")
    df = pd.read_excel(FILENAME, sheet_name='测试用例')
    target1 = df.iloc[2:28, 6:26]
    target2 = df.iloc[2:28, 27:32]
    assert target1.size == roomInfo.size
    assert target2.size == scheduleInfo.size
    
    # Create a file to store the result
    writer = pd.ExcelWriter('test_result.xlsx')
    df.to_excel(writer, sheet_name='测试用例', index=False)
    roomInfo.to_excel(writer, sheet_name='房间信息', index=False)
    scheduleInfo.to_excel(writer, sheet_name='调度信息', index=False)
    writer.save()