# Carter Voice Assistant Boilerplate(Python)
An example project showing how to use www.carterapi.com as a voice assistant. It uses LOCAL speech recoginition to get the user's voice input, and then uses the Carter API to get the response. It also uses the Carter API to get the agent's voice output.

<h2>A note on speech recognition:</h2>
This demo used the out-of-the-box wave2vec2 without a n-gram model. This is a very simple model, and it is not recommended for use in production due to it's accuracy limitations. Carter API will soon provide a, more accurate, cloud-based speech recognition model.

<h2>Get Started:</h2>
To get started, install the requirements listed in the `requirements.txt` file by running:

```pip install -r requirements.txt```

Then, run the following command to start the server:

```python app.py --key your-api-key --voice True```

To find out more about the API key and configure your agent, visit the [Carter API](https://www.carterapi.com/).

<h3>PyAudio for M1 Macs</h3>

to install PyAudo for M1 Macs, this will require a small workaround, as PortAudio is not automatically detected.

first, we need to install PortAudio

```brew install portaudio```

then, we need to create a new file:

```nano ~/.pydistutils.cfg```

the contents of that file may vary slightly (ie, version number)

```
[build_ext]
include_dirs=/opt/homebrew/Cellar/portaudio/19.7.0/include/
library_dirs=/opt/homebrew/Cellar/portaudio/19.7.0/lib/
```

where 19.7.0 should be replaced with the portaudio version you get installed.

this should be executed BEFORE running the `pip install -r requirements.txt` command

<h2>Known Issues:</h2>
- M1 Mac doesn't seem to support PyAudio (workaround awaiting testing from others)

- Speech-to-text Performance is not optimized and could be optimized in conjunction with n-grams. 

- Speed could be improved.

