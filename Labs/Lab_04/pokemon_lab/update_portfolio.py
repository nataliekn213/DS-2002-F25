import os
import sys
import pandas as pd
import json

# funcion 1 - _load_lookup_data(lookup_dir)
def _load_lookup_data(lookup_dir):
    """Load and flatten all lookup JSON files, keeping key market values."""
    all_lookup_df = []

    for filename in os.listdir(lookup_dir):
        if filename.endswith(".json"):
            filepath = os.path.join(lookup_dir, filename)
            with open(filepath, "r") as f:
                data = json.load(f)

            # flatten nested JSON
            df = pd.json_normalize(data["data"])

            # get the right market price
            df["card_market_value"] = (
                df.get("tcgplayer.prices.holofoil.market", 0.0)
                .fillna(df.get("tcgplayer.prices.normal.market", 0.0))
                .fillna(0.0)
            )

            # rename columns
            df = df.rename(
                columns={
                    "id": "card_id",
                    "name": "card_name",
                    "number": "card_number",
                    "set.id": "set_id",
                    "set.name": "set_name",
                }
            )

            required_cols = [
                "card_id",
                "card_name",
                "card_number",
                "set_id",
                "set_name",
                "card_market_value",
            ]
            all_lookup_df.append(df[required_cols].copy())

    if not all_lookup_df:
        return pd.DataFrame(
            columns=[
                "card_id",
                "card_name",
                "card_number",
                "set_id",
                "set_name",
                "card_market_value",
            ]
        )

    lookup_df = pd.concat(all_lookup_df, ignore_index=True)
    lookup_df = lookup_df.sort_values("card_market_value", ascending=False)
    lookup_df = lookup_df.drop_duplicates(subset=["card_id"], keep="first")

    return lookup_df

# function 2 - _load_inventory_data(investory_dir)
def _load_inventory_data(inventory_dir):
    """Extract and transform inventory CSV data."""
    inventory_data = []

    for filename in os.listdir(inventory_dir):
        if filename.endswith(".csv"):
            filepath = os.path.join(inventory_dir, filename)
            df = pd.read_csv(filepath)
            inventory_data.append(df)

    # if no inventory data found, return an empty DataFrame
    if not inventory_data:
        return pd.DataFrame()

    # concat all CSV DataFrames into one
    inventory_df = pd.concat(inventory_data, ignore_index=True)

    # Unified Key: combine set_id and card_number to make card_id
    inventory_df["card_id"] = (
        inventory_df["set_id"].astype(str) + "-" + inventory_df["card_number"].astype(str)
    )

    return inventory_df

# function 3
def update_portfolio(inventory_dir, lookup_dir, output_file):
    """Main ETL/Loading logic: merge inventory with lookup prices and write CSV."""
    lookup_df = _load_lookup_data(lookup_dir)
    inventory_df = _load_inventory_data(inventory_dir)

    if inventory_df.empty:
        # create an empty CSV with req headers
        empty_cols = [
            "index",
            "binder_name",
            "page_number",
            "slot_number",
            "card_id",
            "card_name",
            "set_id",
            "set_name",
            "card_number",
            "card_market_value",
        ]
        pd.DataFrame(columns=empty_cols).to_csv(output_file, index=False)
        print(f"Error: No inventory files found in '{inventory_dir}'. Empty portfolio created at '{output_file}'.", file=sys.stderr)
        return

    needed_lookup_cols = [
        "card_id",
        "card_name",
        "set_id",
        "set_name",
        "card_number",
        "card_market_value",
    ]
    merged = pd.merge(
        inventory_df,
        lookup_df[needed_lookup_cols],
        on="card_id",
        how="left",
        suffixes=("_inv", "")
    )

    merged["card_market_value"] = merged["card_market_value"].fillna(0.0)
    merged["set_name"] = merged["set_name"].fillna("NOT_FOUND")

    merged["index"] = (
        merged["binder_name"].astype(str) + "-"
        + merged["page_number"].astype(str) + "-"
        + merged["slot_number"].astype(str)
    )

    final_cols = [
        "index",
        "binder_name",
        "page_number",
        "slot_number",
        "card_id",
        "card_name",
        "set_id",
        "set_name",
        "card_number",
        "card_market_value",
    ]
    final_df = merged[final_cols].copy()

    final_df.to_csv(output_file, index=False)
    print(f"Portfolio updated and written to '{output_file}'.")

def main():
    """Run ETL with production directories and output file."""
    inventory_dir = "./card_inventory/"
    lookup_dir = "./card_set_lookup/"
    output_file = "card_portfolio.csv"
    update_portfolio(inventory_dir, lookup_dir, output_file)

def test():
    """Run ETL with test directories and test output file."""
    inventory_dir = "./card_inventory_test/"
    lookup_dir = "./card_set_lookup_test/"
    output_file = "test_card_portfolio.csv"
    update_portfolio(inventory_dir, lookup_dir, output_file)

if __name__ == "__main__":
    print("Starting update_portfolio.py in Test Mode...", file=sys.stderr)
    test()