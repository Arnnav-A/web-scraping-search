# Web Browser Query Agent

This project is a CLI prototype for an intelligent web scraping agent that can understand and respond to your queries.

## Workflow

 - User inputs a query.
 - Check whether the query is a valid searchable query, through an LLM.
 - Web-search and extract the text from the first 5 results.
 - Ask an LLM to summarize and respond to the user's original request.

## Architectural Decisions
 - Using groq cloud for free API access to multiple models with generous limits and native integration with LangChain.
 - Using gemma2 as my LLM for quick and inexpensive inference.
 - Creating a local FAISS cache to respond to similar queries through huggingface embeddings.
 - Currently running playwright without headless mode as it is more reliable for catching URLs.
 - Implemented LangChain for LLM calls to create a modular solution that can be expanded later.

## Steps to run locally
 - Download the repository.
 - Install all packages with `pip install requirements.txt`
 - Run `playwright install` before your first query.
 - Run `python main.py "your query"`

Note: The first run would require downloading the local huggingface embedding model, so it will take extra time.
