import os
from threading import Thread

from streamlink import Streamlink


def _init_record(stream_url, callback_url):
    session = Streamlink()
    streams = session.streams(stream_url)
    source_stream = streams['source']
    stream_fd = source_stream.open()
    filename = 'new_file.ts'
    os.makedirs('records', exist_ok=True)

    
    with open('./records/{}'.format(filename), 'wb') as record_fd:
        while True:
            data = stream_fd.read(1024)
            record_fd.write(data)

            if data == '':
                break

class Content:
    def __init__(self, stream_url, callback_url):
        self._stream_url = stream_url
        self._callback_url = callback_url

    def record(self):
        thread = Thread(target=_init_record, args=(self._stream_url, self._callback_url))
        thread.start()

        while True:
            print(thread.is_alive())