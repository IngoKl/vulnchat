# Vulnchat

Ingo Kleiber (2025) <ingo@kleiber.me>

This is a vulnerable chatbot application that mimicks RAG-like behavior. This can be used to demonstrate basic indirect prompt injections.

## Setup

Set the `OPENAI_API_KEY` environmental variable to your OpenAI key (if using the official API). Be aware that OpenAI sometimes blocks indirect prompt injection. The models have been trained to not show vulnerable looking markdown.

## Usage

Ideally, open it up in the devcontainer. Then run `python vulnchat.py`.
