# Project Setup

## Setting up the virtual environment
This time we are just using the built-in venv environments with Python. 

```
python3.12 -m venv .venv
source .venv/bin/activate
```

Installing libraries...
```
pip install "ag2[openai]"
pip install pyverilog
```

## API Key setup
Lastly you'll want to set up your API key in a file. The code is written to pull an OpenAI API Key from an environment variable. I recommend having a file in the top level directory of this project called `.env.sh` to source with the API key setup in it. 

```
touch .env.sh
echo "export OPENAI_API_KEY={API KEY HERE!!! NO BRACKETS}" > .env.sh
```

After that if you do `python3 main.py` *right now* you should see the code run but it will likely throw an error about Pydantic not being able to serialize a custom type we are using. 

