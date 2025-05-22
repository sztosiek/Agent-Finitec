import os
from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic.type_adapter import R
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.tools import Tool
import requests
import wikipedia
from bs4 import BeautifulSoup

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
os.environ["OPENAI_API_KEY"] = os.getenv("OPEN_API_KEY")
BRAVE_API_KEY = os.getenv("BRAVE_API_KEY")

# Initialize the model
model = OpenAIModel("gpt-4o-mini")
class BudgetBoxOffice(BaseModel):
    title: str
    budget: int
    box_office: int

# Create and run the agent
financial_results_agent = Agent(
    model=model,
    output_type=BudgetBoxOffice,
    system_prompt=("You are an assistant that analyzes movie financial results. Your task is to extract and return the budget and box office gross for movies in integer form. Follow these steps:\n"
    "1. First use the knowledge_base tool to check if the movie's financial data is available there.\n"
    "2. If not found in knowledge_base, use wikipedia_search to find budget and box office information:\n"
    "   - First search for the movie's main page using the movie name\n"
    "   - If no data about the movie with that name, use brave_search to find the name it has on wikipedia\n"
    "   - Use that name in wikipedia_search'\n"
    "3. If wikipedia_search doesn't provide the information, use brave_search to find it.\n"
    "\n"
    "When extracting information:\n"
    "- Look for phrases like 'budget', 'box office', 'gross', 'earnings', 'revenue'\n"
    "- Convert amounts to integers for example '$100 million' becomes 100000000\n"
    "- If multiple values are found, choose the most recent one\n"
    "- If no values are found, return 0 for that field\n"
    "\n"
    "Return the results in this format: {'budget': <integer>, 'box_office': <integer>}\n"
    "\n"
    "When using brave_search:\n"
    "- Try different search terms if the first one doesn't work\n"
    "- Be specific about what information you're looking for\n"
    "- If searching for financial data, try different queries like:\n"
    "  - '[movie name] budget'\n"
    "  - '[movie name] movie budget'\n"
    "  - '[movie name] box office'\n"
    "  - '[movie name] financial performance'\n"
    "  - '[movie name] production cost'\n"
    "  - '[movie name] revenue'\n"
    ),
)

@financial_results_agent.tool_plain
def brave_search(query: str) -> str:
    """
    Use this tool to get the full content of pages found using Brave search.
    As a query use the film name or topic.
    This function returns the entire parsed text from each search result page.
    """
    brave_url = "https://api.search.brave.com/res/v1/web/search"
    headers = {
        "Accept": "application/json",
        "X-Subscription-Token": BRAVE_API_KEY
    }
    params = {"q": query, "count": 5}
    print(query)
    try:
        response = requests.get(brave_url, headers=headers, params=params)
        response.raise_for_status()
        items = response.json().get("web", {}).get("results", [])

        extracted_info = []

        for item in items:
            page_url = item.get("url")
            title = item.get("title", "Untitled")

            try:
                page_response = requests.get(page_url, timeout=10)
                page_response.raise_for_status()

                soup = BeautifulSoup(page_response.text, "html.parser")
                full_text = soup.get_text(separator="\n", strip=True)

                extracted_info.append(
                    f"### {title}\n🔗 {page_url}\n\n{full_text}\n"
                )

            except Exception as e:
                extracted_info.append(
                    f"### {title}\n🔗 {page_url}\n\n Error fetching page: {str(e)}"
                )

        final_result = extracted_info or "No results found."
        return final_result

    except Exception as e:
        return f"Error performing Brave search: {str(e)}"



@financial_results_agent.tool_plain
def knowledge_base(query: str) -> str:
    """
    Use this tool to get film financial data from knowledge_base.md file.
    Try to find film in knowledge_base.md that matches the query.
    You will need to extract budget and box office data from the knowledge base.
    """
    with open("knowledge_base.md", "r", encoding="utf-8") as f:
        return f.read()


@financial_results_agent.tool_plain
def wikipedia_search(query: str) -> str:
    """
    Use this tool to get film financial data from Wikipedia.
    As a query use film name of the movie.
    Look for words such as budget, box office, gross, earnings, revenue.
    If there is no movie found with that name, use brave_search tool
    """
    try:
        content = wikipedia.page(query).content
    except:
        return "No movie found with that Name"
    return content


