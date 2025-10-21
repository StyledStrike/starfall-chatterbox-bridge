import os
import logger
import config
import torch
import torchaudio

from os.path import join, isfile
from typing import Optional, Tuple, Any
from caching import getAudioFileName, downloadChatterboxMultilangTTSModel
from wss import getStringFromDict, getFloatFromDict

from chatterbox.mtl_tts import ChatterboxMultilingualTTS

class ChatterboxBackend:
    def __init__(self, device="cpu") -> None:
        logger.info(f"[Chatterbox] Using device: {device}")
        modelDir = downloadChatterboxMultilangTTSModel()

        self.model = ChatterboxMultilingualTTS.from_local(
            ckpt_dir=modelDir,
            device=device
        )

        # We'll manually cache audio conditioning to speedup
        # generation while constantly switching audio inputs.
        self.audioCondCache = {}

    def shutdown(self):
        #self.model.shutdown()
        self.model = None

    def getAudioConditionals(self, exaggeration: float, audioPath: Optional[str] = None):
        if audioPath is None:
            return self.model.conds

        entry = self.audioCondCache.get(audioPath, None)

        if entry is None:
            logger.debug(f"Caching conditionals for audio: {audioPath}")

            self.model.prepare_conditionals(audioPath, exaggeration=exaggeration)
            self.audioCondCache[audioPath] = self.model.conds
        
        return self.model.conds

    def generate(self, text: str, language: str, exaggeration: float, temperature: float, cfg: float, inputAudioPath: str | None = None):
        logger.debug({
            "exaggeration": exaggeration,
            "temperature": temperature,
            "inputAudioPath": inputAudioPath
        })

        if inputAudioPath is not None:
            inputAudioPath = config.getInputAudioFilePath(inputAudioPath)

            if not isfile(inputAudioPath):
                raise ValueError(f"Invalid input audio file: {inputAudioPath}")

        filePath = getAudioFileName("chatterbox", [text, language, exaggeration, temperature, cfg, inputAudioPath])
    
        if isfile(filePath):
            return filePath

        logger.debug(f"[Chatterbox] Generating {language} text... ({exaggeration} exaggeration)")

        # Reuse cached conditionals
        self.model.conds = self.getAudioConditionals(exaggeration, inputAudioPath)

        wav = self.model.generate(
            text,
            language_id=language,
            audio_prompt_path=inputAudioPath,
            exaggeration=exaggeration,
            cfg_weight=cfg,
            temperature=temperature,
            max_new_tokens=300,
            max_cache_len=500,
            repetition_penalty=1.5,
            #min_p=0.05,
            #top_p=1.0,
        )

        torchaudio.save(filePath, wav, self.model.sr)
        logger.success("[Chatterbox] Saved to:", logger.highlight(filePath))

        return filePath

    def generateFromDict(self, text: str, params: dict, settings: dict):
        return self.generate(
            text=text,
            language=getStringFromDict(params, "language", settings["chatterboxLanguage"]),
            exaggeration=getFloatFromDict(params, "exaggeration", settings["chatterboxExaggeration"]),
            temperature=getFloatFromDict(params, "temperature", settings["chatterboxTemperature"]),
            cfg=getFloatFromDict(params, "cfg", settings["chatterboxCFG"]),
            inputAudioPath=getStringFromDict(params, "inputAudioPath", settings["chatterboxInputAudioPath"]),
        )
