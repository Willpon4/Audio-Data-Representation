import subprocess
import threading
import mido
from mido import Message

MIDI_MIN = 0
MIDI_MAX = 127

class MidiStreamInterpreter:
    def __init__(self, c_executable_path):
        self.c_executable_path = c_executable_path
        self.process = None
        self.running = False

    def start(self):
        if self.running:
            return
        self.running = True
        self.process = subprocess.Popen(
            [self.c_executable_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        threading.Thread(target=self._read_stdout, daemon=True).start()

    def stop(self):
        if self.process:
            self.process.terminate()
        self.running = False

    def _read_stdout(self):
        with mido.open_output() as outport:
            for line in self.process.stdout:
                print(f"[C Output] {line.strip()}")
                try:
                    numbers = list(map(int, line.strip().split()))
                    for val in numbers:
                        if MIDI_MIN <= val <= MIDI_MAX:
                            msg = Message('note_on', note=val, velocity=64, time=0)
                            outport.send(msg)
                except ValueError:
                    print("Invalid MIDI data received")
