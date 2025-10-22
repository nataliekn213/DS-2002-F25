import os
import sys
import pandas as pd

# function 1 - generate_summary(portfolio_file)
def generate_summary(portfolio_file):
    if not os.path.exists(portfolio_file):
        print(f"Error: '{portfolio_file}' does not exist.", file=sys.stderr)
        sys.exit(1)

    df = pd.read_csv(portfolio_file)

    if df.empty:
        print("The portfolio file is empty. No data to summarize.")
        return

    total_portfolio_value = df["card_market_value"].sum()

    # Most Valauble Card
    max_idx = df["card_market_value"].idxmax()
    most_valuable_card = df.loc[max_idx]

    print(f"Total Portfolio Value: ${total_portfolio_value:,.2f}")
    print(
        "Most Valuable Card: "
        f"{most_valuable_card['card_name']} "
        f"(ID: {most_valuable_card['card_id']}) — "
        f"${most_valuable_card['card_market_value']:,.2f}"
    )

def main():
    generate_summary("card_portfolio.csv")

def test():
    generate_summary("test_card_portfolio.csv")

if __name__ == "__main__":
    test()