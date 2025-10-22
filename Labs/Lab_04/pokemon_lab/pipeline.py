import sys
import update_portfolio
import generate_summary

def run_production_pipeline():
    print("Starting production pipeline...", file=sys.stderr)

    print("ETL Step: Updating portfolio...", file=sys.stderr)
    update_portfolio.main()

    print("Reporting Step: Generating summary...", file=sys.stderr)
    generate_summary.main()

    print("Pipeline complete.", file=sys.stderr)

if __name__ == "__main__":
    run_production_pipeline()