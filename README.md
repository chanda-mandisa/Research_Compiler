# Research Compiler

This project allows users to search for research papers from Google Scholar using SerpAPI and compile the results into structured CSV files. Ideal for researchers, students, and anyone interested in aggregating scholarly articles.

## Features

- Retrieve research papers from Google Scholar based on a search query.
- Save search results into a structured CSV format.
- Extract metadata including title, authors, and publication links.
- Asynchronous API requests for efficient data retrieval.

## Getting Started

This project enables users to query Google Scholar for research articles and store the results in a CSV file.

### Installation

#### Clone the Repository
```bash
git clone https://github.com/chanda-mandisa/Research_Compiler.git
cd Research_Compiler
```

### System Requirements

- Python 3.x
- Internet connection (for API requests)

### Dependencies

Install required dependencies using:
```bash
pip install aiohttp
```

## Running the Script

To start fetching research papers:
```bash
python research_scraper.py
```

- The script will prompt for a search query.
- The results will be saved as `research_results_<query>_<timestamp>.csv` in the working directory.

## Usage

1. Run the script and enter a keyword related to the research topic.
2. Wait for the search results to be fetched and formatted.
3. Access the generated CSV file containing the research papers.

## Customization

- Modify the `num_results` parameter in `research_scraper.py` to change the number of articles fetched.
- The script can be adjusted to filter by author, publication year, or other metadata.

## Troubleshooting

### API Key Issues
- Ensure you have a valid SerpAPI key set as an environment variable: `SERPAPI_KEY`.
- If you do not have an API key, sign up at [SerpAPI](https://serpapi.com/).

### CSV File Not Created
- Check if there were results for the given query.
- Ensure you have write permissions in the working directory.

## License

This project is licensed under the MIT License. See `LICENSE` for details.

## Contributions

Contributions are welcome! Feel free to submit a pull request or report issues.

## Author

Developed by [chanda-mandisa].


