# NoteBot

Let's have a chat about your notes!

Check out the hosted app on [HuggingFace spaces][1]

## About

NoteBot is a simple, LLM-powered chatbot with whom you can converse about your (my) notes.  
Please note that it is early days for NoteBot - you may experience rough edges.

## Installation

Install NoteBot

    pip install -r requirements.txt

_Optional_: Create a `.env` file in the root of the repo and insert your OpenAI API KEY

    OPENAI_API_KEY="sk-..."

## Usage

Launch NoteBot

    python notebot/app.py

Launch Notebot with custom notes repository

    python notebot/app.py --note-repo-url https://github.com/YOUR_USER/YOUR_REPO.git

Launch NoteBot with custom OpenAI API key

    python notebot/app.py --openai-api-key YOUR_API_KEY

Get help

    python notebot/app.py -h

## Development

Install poetry as described in the official [documentation][2]

Install project dependencies

    poetry install

Install pre-commit hooks

    pre-commit install


[1]: https://huggingface.co/spaces/slangenbach/notebot
[2]: https://python-poetry.org/docs/#installation
