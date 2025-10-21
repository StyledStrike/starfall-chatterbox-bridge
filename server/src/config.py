import os
import logger
import torch
import platform

from pathlib import Path
from os.path import isfile, isdir, join, normpath

def getWebsocketHost():
    return "127.0.0.1"

def getWebsocketPort():
    return 8001

def getBestTorchDevice():
    if torch.cuda.is_available():
        return "cuda"

    elif torch.xpu.is_available():
        return "xpu"

    elif torch.backends.mps.is_available():
        return "mps"

    return "cpu"

def getSOXDeviceType():
    return "waveaudio" if platform.system() == "Windows" else "pulseaudio"

def getSOXDeviceName():
    # On Linux, change this to match the PulseAudio device used for the virtual mic.
    linuxAudioDeviceName = "alsa_output.pci-0000_30_00.6.analog-stereo"

    return "CABLE Input" if platform.system() == "Windows" else linuxAudioDeviceName

"""
    Get the location of the cache directory.

    If you provide `dirName`, this function will also
    create a directory with that name inside of the
    cache directory, and include it in the return value.
"""
def getCacheDirectory(dirName: str = "."):
    dirPath = normpath(join(os.getcwd(), "..", ".cache", dirName))

    if not isdir(dirPath):
        os.makedirs(dirPath, exist_ok=True)

    return dirPath
