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

<h2>Known Issues:</h2>
- M1 Mac doesn't seem to support PyAudio.

- Speech-to-text Performance is not optimized and could be optimized in conjunction with n-grams. 

- Speed could be improved.

