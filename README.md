# LLM powered voice assistant in Python

[![Discord](https://img.shields.io/badge/Discord-%235865F2.svg?style=for-the-badge&logo=discord&logoColor=white)](https://discord.gg/EBfr3vHd8M)

An example project showing how to use PyWebRTCVad and [Carter](https://www.carterlabs.ai) with your voice in Python. This will run on a Raspberry Pi, Macbook, Windows PC and gives you complete voice input and output to your character. It also uses the Carter API to get the agent's voice output (subject to improvement soon!)

## Steve Jobs demo:

https://user-images.githubusercontent.com/16668357/235618782-0a96bc5b-8c66-4ee8-90d5-cec540da72fa.mp4

## 🚀 START

First, install the other requirements:

`pip install -r requirements.txt`

Then, run the following command to start the server:

`python app.py --key your-api-key --user=UNIQUE_STRING`

To find out more about the API key and configure your agent, visit the [Carter](https://www.carterlabs.ai/) website.

<h3>PyAudio for M1 Macs</h3>
to install PyAudo for M1 Macs, this will require a small workaround, as PortAudio is not automatically detected.
first, we need to install PortAudio

```
brew install portaudio
```

If the command 'brew' is not found, run this command and then try the previous step again.

```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

then, we need to create a new file:

```
nano ~/.pydistutils.cfg
```

the contents of that file may vary slightly (ie, version number)

```
[build_ext]
include_dirs=/opt/homebrew/Cellar/portaudio/19.7.0/include/
library_dirs=/opt/homebrew/Cellar/portaudio/19.7.0/lib/
```

where 19.7.0 should be replaced with the portaudio version you get installed.
this should be executed BEFORE running the `pip install -r requirements.txt` command
