from agent import financial_results_agent

def run_cli():
    print("Agent CLI ready. Type 'exit' to quit.")
    while True:
        user_input = input("What movie are you interested in?: ")
        if user_input.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break
        response = financial_results_agent.run_sync(user_input)
        print(f"Movie Title: {response.output.title}")
        print(f"Budget: {response.output.budget}")
        print(f"Box Office: {response.output.box_office}")

if __name__ == "__main__":
    run_cli()