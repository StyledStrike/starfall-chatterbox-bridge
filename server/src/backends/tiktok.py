import os
import json
import base64
import requests
import logger

from hashlib import md5
from os.path import isfile, join, normpath
from caching import getAudioFileName
from wss import getStringFromDict, getFloatFromDict

"""
    A TTS Backend to generate audio using TikTok's HTTP API.
"""
class TikTokBackend:
    def __init__(self) -> None:
        self.apiURL = "https://tiktok-tts.weilnet.workers.dev/api/generation"

    def shutdown(self):
        pass

    def generate(self, text: str, voice: str):
        logger.debug("[tiktok] Generating...")

        filePath = getAudioFileName("tiktok", [text, voice], ".mp3")

        if isfile(filePath):
            return filePath

        requestBody = {
            "voice": voice,
            "text": text
        }

        response = requests.post(self.apiURL, json=requestBody)
        code = response.status_code

        if code == 200 or code == 400:
            body = json.loads(response.content)

            if body["success"] is False:
                raise Exception(body["error"])

            data = base64.b64decode(body["data"])

            with open(filePath, "wb") as f:
                f.write(data)

            logger.success("[tiktok] Saved to:", logger.highlight(filePath))

            return filePath
        else:
            raise Exception(f"API request failed with status code {code}")

    def generateFromDict(self, text: str, params: dict, settings: dict):
        return self.generate(
            text=text,
            voice=getStringFromDict(params, "voice", "en_us_001"),
        )
