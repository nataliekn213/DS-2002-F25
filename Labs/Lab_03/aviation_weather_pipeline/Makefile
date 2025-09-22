.PHONY: all fetch analyze clean

all: analyze

fetch:
	@echo "[fetch] Starting: downloading METAR JSON..."
	@bash ./fetch_metars.sh
	@echo "[fetch] Done. Raw data saved in 'raw_metars'."

analyze: fetch
	@echo "[analyze] Starting: generating 'weather_report.csv'..."
	@bash ./analyze_data.sh
	@echo "[analyze] Done. Pipeline completed successfully. Output: 'weather_report.csv'."

clean:
	@echo "[clean] Starting: removing generated files..."
	@rm -rf raw_metars weather_report.csv
	@echo "[clean] Done. Workspace clean."

