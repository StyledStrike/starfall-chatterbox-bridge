# starfall-chatterbox-bridge

A Python websocket server that handles text-to-speech generation and playback with [Chatterbox TTS](https://github.com/resemble-ai/chatterbox), by receiving text from the chat box within Garry's Mod.

# Requirements

- Garry's Mod with [StarfallEx](https://github.com/thegrb93/StarfallEx) installed
- A dedicated GPU, with a minimum recommended VRAM amount of 6 GB (or more if you're playing on a "big" server)

# Installation

## Prepare files

Clone this repository to a directory of your choosing:

```sh
git clone https://github.com/StyledStrike/starfall-chatterbox-bridge.git
```

For the rest of this guide, I'll refer to the directory where you've cloned this repository as `starfall-chatterbox-bridge`.

## Install UV

Install the [uv package manager](https://docs.astral.sh/uv/#installation). It's much easier and faster to handle Python versions and install packages with it, but if you prefer to do it manually, nothing is stopping you from installing Python 3.12.11 and using `pip` instead.

> Note: If you want to install `uv` manually, you can download the latest binaries for your OS/architecture from [here](https://github.com/astral-sh/uv/releases), extract it to a directory, and then add that directory to your `PATH` environment variable.

## Install dependencies

Open a terminal on `starfall-chatterbox-bridge/`, then type these commands:

```sh
cd server
uv venv --python 3.12.11

# For Windows:
call .venv/Scripts/activate.bat

# For Linux:
source .venv/bin/activate
```

### Installing PyTorch

Pick one of these PyTorch commands depending on your hardware.

> Note: I only have access to a NVIDIA GPU, instructions for others are untested.

#### NVIDIA GPUs

```sh
uv pip install torch==2.6.0 torchaudio==2.6.0 --index-url https://download.pytorch.org/whl/cu126
```

#### AMD ROCM (Linux only)

```sh
uv pip install torch==2.6.0 torchaudio==2.6.0 --index-url https://download.pytorch.org/whl/rocm6.2.4
```

#### Intel Arc GPUs

```sh
uv pip install torch==2.6.0 torchaudio==2.6.0 --index-url https://download.pytorch.org/whl/xpu
uv pip install intel-extension-for-pytorch==2.6.10+xpu --extra-index-url https://pytorch-extension.intel.com/release-whl/stable/xpu/us/
```

#### Other dependencies

After installing PyTorch, run this command:

```sh
uv pip install -r requirements.txt
```

## SoX (Sound eXchange)

To support playing audio with effects, [SoX](https://sourceforge.net/projects/sox/) must be installed.

### Manual download on Windows

- Download the [zipped binaries from here](https://sourceforge.net/projects/sox/files/sox/14.4.2/sox-14.4.2-win32.zip/download)
- Extract it to `starfall-chatterbox-bridge/sox-14.4.2/`.
- Make sure the SoX executable is located at `starfall-chatterbox-bridge/sox-14.4.2/sox.exe`

### Installation on Linux

For Linux users, I can only advise to search and install a `sox` package (name may vary) for your distribution.

# Prepare Garry's Mod

If you haven't done it already, install the Chromium Beta for Garry's Mod:

- Make sure the game is closed
- Right-click Garry's Mod on your Steam library, click on `Properties...`, and then `Betas`
- Select the `x86-64 - Chromium + 64 bit binaries` beta
- Wait for Steam to download the necessary files

> Note for Linux users: make sure to also run [GModPatchTool](https://github.com/solsticegamestudios/GModPatchTool) afterwards.

Next, you should either copy `starfall-chatterbox-bridge/starfall-tts-v3.txt` to your `GarrysMod/garrysmod/data/starfall/` folder, or copy the contents from that file and paste them on the Starfall Editor.

# Setup a virtual audio cable

## Windows

Download and install Vincent Burel's [VB-CABLE](https://vb-audio.com/Cable/). Voicemeeter can work too, as long as you know the "input" device name, and make the server use it by typing this command after starting:

```
device CABLE Input
```

## Linux

> TODO: Add tips for setting up a virtual microphone on Linux, and how to change it on `server/src/config.py`

# Running the TTS

- Run the server by double-clicking `run.bat` (on Windows) or executing `chmod +x run.sh; ./run.sh` (on Linux)
- On first run, you'll have to wait for the server to download the required Chatterbox models
- Once the server says `Ready!`, you can open the Starfall script and spawn the chip in-game
- Say something in the chat!

## Commands

You can type `help` while the server is running to see a list of commands.

You can also type `csay <message>` to use the Chatterbox TTS directly from the terminal.

# Known issues

- First generation with Chatterbox can be slower, as it "warms up"
- SoX might show `sox WARN wav: wave header missing extended part of fmt chunk` warnings, they can be ignored
- The provided SoX binaries for Windows do not support *.mp3* files, so you cannot use the TikTok TTS backend for now
- Sometimes when exiting, the WebSocket server might throw an error. It can be ignored
- Chatterbox's `exageration` parameter is not having a pronounced effect at this time. It did with the english-only models, but not after the multilingual update
