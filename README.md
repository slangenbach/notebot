# NoteBot

Let's have a chat about your notes!

## About

NoteBot is a simple, ChatGPT-powered chatbot with whom you can converse about your (my) notes.  

## Installation

Install NoteBot

    poetry install

Create a `.env` file in the root of the repo and insert your OpenAI API KEY

    OPENAI_API_KEY="sk-..."

## Usage

Launch NoteBot

    python notebot/main.py

Launch Notebot

    python notebot/main.py --note-repo-url https://github.com/YOUR_USER/YOUR_REPO.git

Get help

    python notebot/main.py -h
