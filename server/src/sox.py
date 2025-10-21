import os
import logger
import subprocess

from threading import Thread

"""
    A utility class to play audio files using SoX subprocesses.
"""
class SoXAudioPlayer():
    def __init__(self):
        self.bufferSize = "4096"
        self.lastIndex = 0
        self.processes = {}

    def play(self, filePath: str, deviceType: str, deviceName: str, effects=None):
        args = [
            "sox",
            "--no-show-progress",
            "--buffer",
            self.bufferSize,
            filePath,
            "--type",
            deviceType,
            deviceName,
            "pad",
            "0",
            "1"
        ]

        if effects is not None:
            effects = effects.split()

            for i in effects:
                args.append(i)

        self.lastIndex += 1
        index = str(self.lastIndex)

        def play_thread_function():
            with subprocess.Popen(args) as proc:
                self.processes[index] = proc
                logger.info(f"[SoX] Audio #{index} is playing")

            del( self.processes[index] )

        play_thread = Thread(target=play_thread_function)
        play_thread.start()

    def stopAll(self):
        logger.warn("[SoX] Stopping all sounds")

        for index in self.processes:
            self.processes[index].kill()
