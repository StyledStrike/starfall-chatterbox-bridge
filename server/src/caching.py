import os
import torch
import logger
import config

from glob import glob
from hashlib import md5
from os.path import isfile, isdir, join, normpath
from huggingface_hub import hf_hub_download

AUDIO_CACHE_DIR = config.getCacheDirectory("audio")

"""
    Remove all audio files in the cache directory.
"""
def clearAudioCache():
    files = glob(join(AUDIO_CACHE_DIR, "*.wav"))
    files += glob(join(AUDIO_CACHE_DIR, "*.mp3"))

    if len(files) == 0:
        return

    logger.info("Cleaning audio cache dir...")

    for f in files:
        os.remove(f)

"""
    Returns a file name for generated audio.
    The name will always be the same when given the same backend parameters.
"""
def getAudioFileName(backendName: str, backendArgs: list = [], extension: str = ".wav"):
    filteredArgs = []

    for value in backendArgs:
        if value is not None:
            filteredArgs.append(str(value))

    joinedArgs = "".join(filteredArgs)
    fileName = backendName + "-" + md5( joinedArgs.encode("utf-8") ).hexdigest() + extension

    return normpath(join(AUDIO_CACHE_DIR, fileName))

"""
    Download specific model file(s) from a Hugging Face repository.
    If the file(s) already exist, the download will be skipped.
"""
def downloadFilesFromRepo(repoId, targetDir, fileNames):
    for fileName in fileNames:
        filePath = join(targetDir, fileName)

        if isfile(filePath):
            logger.info(f"Model file is already downloaded: {filePath}")
        else:
            logger.info(f"Downloading model file: {fileName}")

            localPath = hf_hub_download(
                repo_id=repoId,
                filename=fileName,
                local_dir=targetDir
            )

            logger.success(f"Downloaded model to {localPath}")

"""
    Download multilingual Chatterbox TTS model files.
"""
def downloadChatterboxMultilangTTSModel():
    repoId = "ResembleAI/chatterbox"
    modelCacheDir = config.getCacheDirectory("models_chatterbox")

    downloadFilesFromRepo(
        repoId=repoId,
        targetDir=modelCacheDir,
        fileNames = [
            "ve.pt",
            "t3_mtl23ls_v2.safetensors",
            "s3gen.pt",
            "grapheme_mtl_merged_expanded_v1.json",
            "conds.pt",
            "Cangjie5_TC.json"
        ]
    )

    return modelCacheDir

"""
    Download non-multilingual Chatterbox TTS model files.
    (Currently, this is not being used on this program)
"""
"""
def downloadChatterboxTTSModel():
    repoId = "ResembleAI/chatterbox"
    modelCacheDir = config.getCacheDirectory("models_chatterbox")

    downloadFilesFromRepo(
        repoId=repoId,
        targetDir=modelCacheDir,
        fileNames = [
            "ve.safetensors",
            "t3_cfg.safetensors",
            "s3gen.safetensors",
            "tokenizer.json",
            "conds.pt"
        ]
    )

    return modelCacheDir
"""
