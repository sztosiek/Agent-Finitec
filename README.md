
# Movie Financial Results Agent

This project provides an intelligent command-line assistant that fetches and extracts **budget** and **box office** data for movies using a combination of tools like **Wikipedia**, **Brave Search**, and a local **knowledge base**.

## What It Does

The agent:
- Receives a movie name as input.
- Searches for budget and box office info from the following sources, in order:
  1. Local `knowledge_base.md`
  2. Wikipedia
  3. Brave Search (fetches and parses full webpage content)
- Extracts and converts financial data into integers.
- Returns structured results directly to the terminal.

## Project Structure

```
.
├── .env                  # API keys
├── requirements.txt      # Python dependencies
├── knowledge_base.md     # Local database of movie financials
└── src/
    ├── agent.py          # Core agent definition and tool logic
    └── cli_agent.py      # Command-line interface to interact with the agent
```

## How to Run

1. **Install dependencies**

```bash
pip install -r requirements.txt
```

2. **Set up your `.env`**

Create a `.env` file (next to `src/`) with the following contents:

```env
OPEN_API_KEY=your_openai_api_key_here
BRAVE_API_KEY=your_brave_search_api_key_here
```

3. **Run the agent**

```bash
python src/cli_agent.py
```

4. **Interact**

You'll be prompted to enter a movie title. Type the name and get its budget and box office performance. Type `exit` to quit.

## Example

```
Agent CLI ready. Type 'exit' to quit.
What movie are you interested in?: Interstellar
Movie Title: Interstellar
Budget: 165000000
Box Office: 677000000
```

## Tech Stack

- [Pydantic AI](https://github.com/pydantic/pydantic-ai)
- OpenAI GPT-4o
- Brave Search API
- Wikipedia Python API
- BeautifulSoup (HTML parsing)

##  Notes

- Make sure your `.env` file is outside of `src/`, and is correctly loaded via `load_dotenv("../.env")`.
- If Brave search fails due to missing or invalid keys, check your `.env` setup.
