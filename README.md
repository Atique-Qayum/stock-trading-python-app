```markdown
# Stock Data Extractor 📈

A Python-based data pipeline that extracts real-time stock ticker information from the Polygon.io API. Built as part of Zach Wilson's Data Engineering Beginner Bootcamp.

## 🚀 Features

- **Real-time Data Extraction**: Fetches current stock ticker data from Polygon.io API
- **Pagination Handling**: Automatically handles API pagination through `next_url` responses
- **Rate Limit Management**: Intelligent retry logic with strategic delays to avoid HTTP 429 errors
- **CSV Export**: Structures and saves data to CSV format for easy analysis
- **Error Resilience**: Comprehensive error handling for API requests, JSON parsing, and file operations

## 📊 Results

- **Successful Extraction**: 11,730 stock tickers retrieved
- **Pages Processed**: 12 API pages paginated through seamlessly
- **Error Handling**: Overcame API rate limiting (HTTP 429) with intelligent retry logic

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/stock-data-extractor.git
   cd stock-data-extractor
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   - Create a `.env` file in the root directory
   - Add your Polygon.io API key:
     ```
     POLYGON_API_KEY=your_api_key_here
     ```

## 📋 Requirements

Create a `requirements.txt` file with:
```
requests>=2.28.0
python-dotenv>=0.19.0
```

## 🚦 Usage

Run the extractor:
```bash
python stock_extractor.py
```

The script will:
- Connect to Polygon.io API
- Handle pagination automatically
- Save results to `tickers.csv`
- Display real-time progress in the console

## 📁 Output

The extracted data includes:
- Ticker symbols
- Company names
- Market information
- Exchange data
- CIK numbers
- FIGI identifiers
- Currency information
- Last updated timestamps

Sample output file: `tickers.csv` with 11,730 rows of structured data

## 🏗️ Architecture

```
API Request → Pagination Handling → Rate Limit Management → Data Processing → CSV Export
```

## 🔧 Technical Implementation

### Rate Limit Solution
```python
# Handle Polygon API rate limits (5 requests/minute)
REQUEST_DELAY = 12  # seconds between requests

if response.status_code == 429:
    retry_after = int(response.headers.get('Retry-After', 60))
    print(f"Rate limited. Waiting {retry_after} seconds...")
    time.sleep(retry_after)
    continue
```

### Pagination Handling
```python
while 'next_url' in data:
    print(f'Fetching next page: {data["next_url"]}')
    response = requests.get(data['next_url'] + f"&apiKey={POLYGON_API_KEY}")
    time.sleep(REQUEST_DELAY)  # Respect rate limits
```

## 📈 Challenges Overcome

- **HTTP 429 Errors**: Implemented retry logic with header-based delay parsing
- **Large Dataset Handling**: Managed pagination for 11,000+ records across 12 pages
- **Data Consistency**: Ensured proper field mapping across all API responses
- **Memory Management**: Optimized for efficient processing of large datasets

## 🎯 Learning Outcomes

- Real-world API integration and authentication
- Pagination handling for large datasets
- Rate limit management and error resilience
- Data structuring and CSV export techniques
- Environment variable security best practices

## 🙏 Acknowledgments

Part of Zach Wilson's free Data Engineering Beginner Bootcamp.  
Learn more at: [learn.dataexpert.io](https://learn.dataexpert.io)

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
```
