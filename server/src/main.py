import os
import logger
import config
import caching
import traceback

from os.path import join
from wss import WSSManager
from sox import SoXAudioPlayer
from terman import TerminalManager

from wss import getStringFromDict
from backends import chatterbox, tiktok
from textify import textify

class App():
    def __init__(self, host=config.getWebsocketHost(), port=config.getWebsocketPort()):
        caching.clearAudioCache()

        self.settings = {
            "failedAudio": join(os.getcwd(), "error.wav"),

            "soxDeviceType": config.getSOXDeviceType(),
            "soxDeviceName": config.getSOXDeviceName(),

            # Default Chatterbox generation params when using the terminal
            "chatterboxLanguage": "en",
            "chatterboxExaggeration": 0.5,
            "chatterboxTemperature": 0.8,
            "chatterboxCFG": 0.5,
            "chatterboxInputAudioPath": None,
        }

        self.terman = TerminalManager()
        self.terman.addCommand("device", "Set the audio device name that SoX will use", self.deviceNameCallback)
        self.terman.addCommand("exaggeration", "Set exaggeration value for use on Chatterbox", self.chatterboxExaggerationCallback)
        self.terman.addCommand("temperature", "Set temperature value for use on Chatterbox", self.chatterboxTemperatureCallback)
        self.terman.addCommand("inputaudio", "Set inputAudioPath value for use on Chatterbox", self.chatterboxInputAudioCallback)
        self.terman.addCommand("csay", "Turns text into speech using Chatterbox", self.chatterboxSayCallback)
        self.terman.addCommand("tsay", "Turns text into speech using the TikTok API", self.tiktokSayCallback)
        self.terman.addCommand("stop", "Stops all audio clips being played", self.stopAllCallback)

        self.wss = WSSManager(host=host,port=port)
        self.wss.onMessageCallback = self.onMessageCallback

        self.sox = SoXAudioPlayer()

        torchDevice = config.getBestTorchDevice()

        self.backends = {
            "chatterbox": chatterbox.ChatterboxBackend(device=torchDevice),
            "tiktok": tiktok.TikTokBackend()
        }

    def run(self):
        self.terman.runForever()
        self.sox.stopAll()
        self.wss.shutdown()

        for instance in self.backends.values():
            instance.shutdown()

    def generate(self, backendName: str, text: str, params: dict):
        backend = self.backends.get(backendName, None)

        if backend is None:
            raise ValueError(f"Unknown backend: {backendName}")

        text = textify(text, symbolsToWords=False, numbersToWords=False)    
        logger.debug(logger.highlight(backendName + ">"), text)

        return backend.generateFromDict(text, params, self.settings)

    def onMessageCallback(self, data):
        command = getStringFromDict(data, "command")

        if command is not None:
            if command == "stopall":
                self.sox.stopAll()
            else:
                self.wss.broadcastError(f"Unknown command: {command}")
            return

        backendName = getStringFromDict(data, "backend")
        text = getStringFromDict(data, "text")
        effects = getStringFromDict(data, "effects")

        if backendName is None:
            self.wss.broadcastError("Missing backend parameter")
            return

        if text is None:
            self.wss.broadcastError("Missing text parameter")
            return

        audioPath = None
        errorMessage = "Failed to generate audio"

        try:
            audioPath = self.generate(backendName, text, data)
        except Exception as e:
            logger.error(traceback.format_exc())
            errorMessage = str(e)

        if audioPath is None:
            self.wss.broadcastError(errorMessage)
            self.sox.play(self.settings["failedAudio"])
            return

        try:
            self.sox.play(
                filePath=audioPath,
                deviceType=self.settings["soxDeviceType"],
                deviceName=self.settings["soxDeviceName"],
                effects=effects
            )

        except Exception as e:
            logger.error("Failed to play audio:", e)
            self.wss.broadcastError("Failed to play audio")

    def onSettingCommand(self, name: str, valueType: str, value: str):
        value = value.strip()

        if len(value) == 0:
            print(f"{valueType} = {self.settings[name]}")
            return

        if valueType == "string":
            self.settings[name] = value
            print(f"{valueType} = {self.settings[name]}")
            return

        try:
            value = float(value)
            self.settings[name] = value
            print(f"{valueType} = {self.settings[name]}")

        except ValueError as e:
            logger.error("Invalid value!")

    def deviceNameCallback(self, args, rawargs):
        self.onSettingCommand("soxDeviceName", "string", rawargs)

    def chatterboxExaggerationCallback(self, args, rawargs):
        self.onSettingCommand("chatterboxExaggeration", "float", rawargs)

    def chatterboxTemperatureCallback(self, args, rawargs):
        self.onSettingCommand("chatterboxTemperature", "float", rawargs)

    def chatterboxInputAudioCallback(self, args, rawargs):
        self.onSettingCommand("chatterboxInputAudioPath", "string", rawargs)

    def soxEffectsCallback(self, args, rawargs):
        self.onSettingCommand("soxEffects", "string", rawargs)
    
    def stopAllCallback(self, args, rawargs):
        self.sox.stopAll()

    def chatterboxSayCallback(self, args, rawargs):
        self.onMessageCallback({
            "backend": "chatterbox",
            "text": rawargs
        })

    def tiktokSayCallback(self, args, rawargs):
        self.onMessageCallback({
            "backend": "tiktok",
            "text": rawargs
        })    

if __name__ == "__main__":
    app = App()
    app.run()
