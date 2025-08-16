# Alpha Vantage MCP Server

A comprehensive Model Context Protocol (MCP) server that provides access to Alpha Vantage's financial data APIs, including stocks, forex, crypto, commodities, and economic indicators.

## 🚀 Features

### Core Stock APIs
- **Real-time Quotes**: Get current stock prices and metrics
- **Time Series Data**: Daily, weekly, monthly, and intraday data
- **Symbol Search**: Find stocks by company name or ticker

### Fundamental Data
- **Company Overview**: Complete company information and financials
- **Financial Statements**: Income statement, balance sheet, cash flow
- **Earnings Data**: Historical earnings and earnings call transcripts

### Technical Indicators
- **Moving Averages**: SMA, EMA, DEMA, TEMA, TRIMA, KAMA, MAMA, VWAP, T3
- **Momentum Indicators**: RSI, MACD, Stochastic, Williams %R, ROC, MOM
- **Volatility Indicators**: Bollinger Bands, ATR, NATR
- **Volume Indicators**: OBV, A/D Line, A/D Oscillator, MFI

### Market Intelligence
- **News Sentiment**: AI-powered news analysis with sentiment scores
- **Market Movers**: Top gainers, losers, and most active stocks
- **Market Status**: Global exchange status and trading hours

### Forex & Currencies
- **Real-time Exchange Rates**: Currency conversion rates
- **FX Time Series**: Historical forex data with multiple timeframes

### Economic Indicators
- **GDP Data**: Real GDP and GDP per capita
- **Federal Reserve**: Interest rates, money supply
- **Labor Statistics**: Unemployment, nonfarm payrolls
- **Inflation Data**: CPI and inflation rates

### Commodities
- **Energy**: WTI crude oil, Brent crude, natural gas
- **Metals**: Copper, aluminum
- **Agriculture**: Wheat, corn, cotton, sugar, coffee

## 📦 Installation

### Prerequisites
- Python 3.11 or higher
- [uv](https://github.com/astral-sh/uv) package manager
- Alpha Vantage API key (free at [alphavantage.co](https://www.alphavantage.co/support/#api-key))

### Setup

1. **Clone and install**:
   ```bash
   git clone https://github.com/yourusername/alpha-vantage-mcp-server
   cd alpha-vantage-mcp-server
   uv sync
   ```

2. **Configure API key**:
   ```bash
   cp .env.example .env
   # Edit .env and add your Alpha Vantage API key
   ```

3. **Test the installation**:
   ```bash
   uv run python test_server.py
   ```

## 🔧 Configuration

### Environment Variables

Create a `.env` file with your Alpha Vantage API key:

```bash
# Required: Your Alpha Vantage API key
ALPHA_VANTAGE_KEY=your_api_key_here

# Optional: Debug mode
DEBUG=false
```

### Rate Limits

- **Free Tier**: 25 requests per day, 5 requests per minute
- **Premium Plans**: Start at $49.99/month with higher limits
- Visit [Alpha Vantage Premium](https://www.alphavantage.co/premium/) for details

## 🎯 Usage with MCP Clients

### Claude Desktop Configuration

Add to your Claude Desktop configuration:

```json
{
  "mcpServers": {
    "alpha-vantage": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/yourusername/alpha-vantage-mcp-server",
        "alpha-vantage-mcp-server"
      ],
      "env": {
        "ALPHA_VANTAGE_KEY": "your_api_key_here"
      }
    }
  }
}
```

### Available Tools

The server provides 25+ comprehensive tools covering all major financial data categories:

#### Core Market Data
- **get_current_stock_quote** - Real-time stock quotes with clean formatting
- **get_stock_time_series** - Historical price data (daily, weekly, monthly, intraday)
- **lookup_stock_symbol** - Search stocks by company name or symbol
- **get_global_markets_status** - Worldwide exchange status and trading hours

#### Technical Analysis
- **get_trend_indicators** - SMA, EMA, WMA, MACD with preset configurations
- **get_momentum_indicators** - RSI, Stochastic, CCI, MFI indicators
- **get_volatility_indicators** - Bollinger Bands, ATR, SAR indicators
- **get_volume_indicators** - OBV, A/D Line, A/D Oscillator

#### Fundamental Data
- **get_symbol_overview** - Company profiles and key metrics
- **get_financial_statements** - Income statements, balance sheets, cash flow
- **get_earning_data** - Historical earnings with quarterly breakdowns
- **get_corporate_actions** - Dividend history and stock splits

#### Market Intelligence
- **get_news_sentiment** - AI-powered news analysis with sentiment scores
- **get_top_gainers_losers** - Market movers and most active stocks
- **get_stock_insider_transactions** - Insider trading activity
- **analyze_stocks** - Advanced analytics and statistical calculations

#### Forex & Crypto
- **get_current_fx_rate** - Real-time currency exchange rates
- **get_fx_time_series** - Historical forex data with multiple intervals
- **get_current_crypto_quote** - Current cryptocurrency market quotes
- **get_crypto_time_series** - Historical crypto price data

#### Economic Indicators
- **get_growth_metrics** - GDP and economic growth data
- **get_rates_yields** - Treasury yields and federal funds rates
- **get_prices_inflation** - CPI and inflation metrics
- **get_labor_activity** - Employment and labor market data
- **get_commodities** - Global commodities pricing data

#### Market Calendar
- **get_market_calendar** - Earnings announcements and IPO calendar
- **get_listing_status** - Stock listing and delisting information
- **get_historical_options** - Options trading data

## 🧪 Testing

Run the comprehensive test suite:

```bash
uv run python test_server.py
```

The test suite includes:
- ✅ Schema validation for all tools
- ✅ Input parameter validation  
- ✅ Output format verification
- ✅ Error handling tests
- ✅ Rate limit awareness

## 📊 Example Usage

### Get Stock Quote
```python
# Through MCP client:
await get_current_stock_quote(symbol="AAPL")
```

### Technical Analysis
```python
# Get momentum indicators for Apple stock
await get_momentum_indicators(
    symbol="AAPL",
    interval="daily", 
    preset="standard"
)
```

### Market Intelligence
```python
# Get news sentiment for multiple stocks
await get_news_sentiment(
    tickers=["AAPL", "MSFT", "GOOGL"]
)
```

### Economic Data
```python
# Get latest GDP data
await get_growth_metrics(
    frequency="quarterly",
    seasonally_adjusted=true
)
```

### Advanced Analytics
```python
# Perform statistical analysis on stock data
await analyze_stocks(
    symbols=["AAPL", "MSFT"],
    interval="DAILY",
    calculations=["MEAN", "STDDEV", "CORRELATION"],
    series_range="6month"
)
```

## 🔍 API Coverage

This MCP server implements **25+ comprehensive tools** that leverage Alpha Vantage's extensive API coverage:

- **Core Market Data** (4 unified tools covering 10+ endpoints)
- **Technical Analysis** (4 indicator packs covering 15+ indicators)  
- **Fundamental Data** (4 tools covering company financials)
- **Market Intelligence** (4 tools for news, movers, and insider data)
- **Forex & Crypto** (4 tools for currency and crypto data)
- **Economic Indicators** (4 tools covering GDP, inflation, employment)
- **Commodities & Calendar** (3 tools for commodities and market events)

Each tool is designed for optimal usability with preset configurations and clean, structured outputs.

## ⚠️ Important Notes

### Rate Limiting
- Free tier has strict limits (25 requests/day)
- Production usage requires premium subscription
- Server handles rate limiting gracefully

### Data Format
- All responses follow Alpha Vantage's JSON structure
- CSV format supported for select endpoints
- Comprehensive error handling included

### Best Practices
- Cache responses when possible
- Respect rate limits
- Use appropriate intervals for your use case
- Monitor API usage

## 🛠️ Development

### Project Structure
```
alpha-vantage-mcp-server/
├── alpha_vantage_mcp_server/
│   ├── __init__.py
│   ├── __main__.py
│   ├── server.py          # MCP server implementation
│   ├── handlers.py        # Unified tool function implementations
│   ├── api_helpers.py     # Alpha Vantage API client functions
│   └── tools.json         # Complete tool schema definitions
├── test_cases.json        # Test scenarios
├── test_server.py         # Test runner
├── pyproject.toml         # Project configuration
└── README.md
```

### Adding New Tools
1. Add function implementation to `handlers.py`
2. Add tool schema definition to `tools.json`
3. Update `TOOL_FUNCTIONS` mapping in `handlers.py`
4. Add comprehensive test cases to `test_cases.json`
5. Run tests to ensure schema validation passes

## 📈 Roadmap

- [ ] Add more economic indicator tools
- [ ] Implement intelligent caching layer  
- [ ] Add data export utilities
- [ ] Expand error handling and retry logic
- [ ] Add request batching optimization
- [ ] Create preset collections for common analysis workflows

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## 📄 License

[Add your license here]

## 🙏 Acknowledgments

- [Alpha Vantage](https://www.alphavantage.co/) for providing the financial data API
- [MCP](https://github.com/modelcontextprotocol) for the protocol specification
- Claude and Anthropic for MCP client support

---

**Ready to analyze financial markets with AI? Get your free Alpha Vantage API key and start exploring!** 🚀📈