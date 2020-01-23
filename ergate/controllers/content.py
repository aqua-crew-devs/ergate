import os
from threading import Thread
import uuid
from datetime import datetime

import requests
from streamlink import Streamlink

import ergate.utils.upload import upload_file


def _init_record(stream_url, callback_url):
    filename = str(uuid.uuid4())
    requests.post(
        callback_url,
        json={
            "event": "record_initialized",
            "id": filename,
            "timestamp": datetime().strftime("%Y-%m-%d %H:%m:%s"),
        },
    )
    try:
        session = Streamlink()
        streams = session.streams(stream_url)
        source_stream = streams["source"]
        stream_fd = source_stream.open()
        os.makedirs("records", exist_ok=True)

        total_byte_accepted = 0
        SIZE_OF_THUNK = 1024
        # report to callback when 1M data is accepted
        bytes_for_next_callback = 1024 * 1024
        with open("./records/{}".format(filename), "wb") as record_fd:
            while True:
                data = stream_fd.read(SIZE_OF_THUNK)
                record_fd.write(data)
                total_byte_accepted += SIZE_OF_THUNK
                bytes_for_next_callback -= SIZE_OF_THUNK

                if bytes_for_next_callback <= 0:
                    request.post(
                        callback_url,
                        json={
                            "event": "downloading",
                            "id": filename,
                            "timestamp": datetime().strftime("%Y-%m-%d %H:%m:%s"),
                            "total_bytes": total_byte_accepted,
                        },
                    )
                    bytes_for_next_callback = 1024 * 1024

                if data == "":
                    break

        requests.post(
            callback_url,
            json={
                "event": "downloaded",
                "id": filename,
                "timestamp": datetime().strftime("%Y-%m-%d %H:%m:%s"),
                "total_bytes": total_byte_accepted,
            },
        )

        upload_file("./records/{}".format(filename), filename, "blackbox-statics")

        requests.post(
            callback_url,
            json={
                "event": "uploaded",
                "id": filename,
                "timestamp": datetime().strftime("%Y-%m-%d %H:%m:%s"),
                "total_bytes": total_byte_accepted,
            },
        )
    except Error as err:
        requests.post(
            callback_url,
            json={
                "event": "error",
                "id": filename,
                "timestamp": datetime().strftime("%Y-%m-%d %H:%m:%s"),
                "error": str(err),
            },
        )


class Content:
    def __init__(self, stream_url, callback_url):
        self._stream_url = stream_url
        self._callback_url = callback_url

    def record(self):
        thread = Thread(
            target=_init_record, args=(self._stream_url, self._callback_url)
        )
        thread.start()
