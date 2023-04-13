# Carter API Python Voice Demo

An example project showing how to use https://www.carterlabs.ai as a voice assistant. This will run on a Raspberry Pi, Macbook, Windows PC and gives you complete voice input and output to your character.

![](https://i.giphy.com/media/26DNc9KWmxRd8nkUU/giphy.webp)
We currently only support a male and female voices and this API is LIKELY TO CHANGE as we move voice out of beta.

We use a combination of PyWebRTC to get the user's voice input, and the Carter API to process the raw audio and generate a high-quality response. It also uses the Carter API to get the agent's voice output.

MORE UPDATES SOON!

## START

First, install the other requirements:
`pip install -r requirements.txt`

Then, run the following command to start the server:

`python app.py --key your-api-key`

To find out more about the API key and configure your agent, visit the [Carter](https://www.carterlabs.ai/) website.
