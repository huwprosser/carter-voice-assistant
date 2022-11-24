<a href="https://www.carterapi.com"><img src="https://151297354-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FciRkFwFdI6llRRifmbqJ%2Fuploads%2FrWJk4wUxapMwAgqOV3Np%2FBUILT-WITH-CARTER.svg?alt=media&token=32f7a446-b9b8-4ded-9263-1c11158c9c2f" style="width: 200px;" /></a>

# Carter Voice Assistant Boilerplate(Python)

An example project showing how to use www.carterapi.com as a voice assistant. It uses a combination of PyWebRTC and LOCAL speech recoginition (now powered by [OpenAI Whisper](https://github.com/openai/whisper)) to get the user's voice input, and then uses the Carter API to get the response. It also uses the Carter API to get the agent's voice output.

MORE UPDATES SOON!

<h2>Get Started:</h2>
To get started, install the requirements listed in the `requirements.txt` file by running:

First, install [OpenAI Whisper](https://github.com/openai/whisper):
`pip install git+https://github.com/openai/whisper.git `

Then, install the other requirements:
`pip install -r requirements.txt`

Then, run the following command to start the server:

`python app.py --key your-api-key --voice True`

To find out more about the API key and configure your agent, visit the [Carter API](https://www.carterapi.com/).
