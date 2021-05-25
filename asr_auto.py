import websocket
try:
    import thread
except ImportError:
    import _thread as thread

import json
import pyaudio
import struct
import requests


recoord = False

RATE = 8000
CHUNK = 4096
FORMAT = pyaudio.paInt16
CHANNELS = 1
p = pyaudio.PyAudio()
stream = None
state = None

asrRequestOption = json.dumps({
    'productcode': "DIGITALW",
    'domain': 'default',
    'cmd': "START",
    'transactionid': "0",
    'language': "kor",
    'epd': True,
    'frmt': "0",
    'slu': False,
    'partial': True,
    'cfl': False
})
print('asrRequestOption', asrRequestOption)

# URL = 'http://ip:port/stt'
URL = 'http://127.0.0.1:8000/stt'


def post_res(text):
    res = requests.post(URL, data={'text': text})
    pass


def on_message(ws, message):
    global state
    global recoord
    print("event.data:", message)
    data = json.loads(message)
    if state == 1:
        if data['result'] == 1:
            state = 2
        else:
            recoord = False
            ws.close()
    else:
        if data['rcode'] == 0:
            # epd
            recoord = False
        elif data['rcode'] == 1:
            # final result
            if data['result']:
                print(data['result'])
                post_res(data['result']+'f')
            recoord = False
            ws.close()
        else:
            # partial result
            if data['result']:
                print(data['result'])
                post_res(data['result'])


def on_error(ws, error):
    global recoord
    print(error)
    recoord = False
    stream.stop_stream()
    stream.close()


def on_close(ws):
    global recoord
    print("onclose")
    recoord = False
    stream.stop_stream()
    stream.close()


def on_open(ws):
    global recoord
    global stream
    global state
    state = 1
    recoord = True
    ws.send(asrRequestOption)
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    def run(*args):
        try:
            while recoord:
                frame = stream.read(CHUNK)
                ws.send(struct.pack('b', 0) + frame)
        except:
            pass
    thread.start_new_thread(run, ())


if __name__ == "__main__":
    # websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://asrdemo.llsollu.com/asr/recognition/websocket/",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open

    while True:
        try:
            ws.run_forever()
        except Exception as e:
            # print(e.message())
            pass

