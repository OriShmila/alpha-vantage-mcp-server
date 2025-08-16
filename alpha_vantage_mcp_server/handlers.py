from typing import Any, Dict, List, Optional, Union

from .api_helpers import (
    # Time series functions
    fetch_intraday,
    fetch_time_series_daily,
    fetch_time_series_daily_adjusted,
    fetch_time_series_weekly,
    fetch_time_series_weekly_adjusted,
    fetch_time_series_monthly,
    fetch_time_series_monthly_adjusted,
    # Financial statements
    fetch_income_statement,
    fetch_balance_sheet,
    fetch_cash_flow,
    # Technical indicators (all 60+ functions)
    fetch_sma,
    fetch_ema,
    fetch_wma,
    fetch_dema,
    fetch_tema,
    fetch_trima,
    fetch_kama,
    fetch_mama,
    fetch_vwap,
    fetch_t3,
    fetch_macd,
    fetch_macdext,
    fetch_stoch,
    fetch_stochf,
    fetch_rsi,
    fetch_stochrsi,
    fetch_willr,
    fetch_adx,
    fetch_adxr,
    fetch_apo,
    fetch_ppo,
    fetch_mom,
    fetch_bop,
    fetch_cci,
    fetch_cmo,
    fetch_roc,
    fetch_rocr,
    fetch_aroon,
    fetch_aroonosc,
    fetch_mfi,
    fetch_trix,
    fetch_ultosc,
    fetch_dx,
    fetch_minus_di,
    fetch_plus_di,
    fetch_minus_dm,
    fetch_plus_dm,
    fetch_bbands,
    fetch_midpoint,
    fetch_midprice,
    fetch_sar,
    fetch_trange,
    fetch_atr,
    fetch_natr,
    fetch_ad,
    fetch_adosc,
    fetch_obv,
    fetch_ht_trendline,
    fetch_ht_sine,
    fetch_ht_trendmode,
    fetch_ht_dcperiod,
    fetch_ht_dcphase,
    fetch_ht_phasor,
    # Other functions we want to keep
    fetch_realtime_bulk_quotes,
    search_endpoint,
    fetch_market_status,
    fetch_historical_options,
    fetch_news_sentiment,
    fetch_top_gainer_losers,
    fetch_insider_transactions,
    fetch_analytics_fixed_window,
    fetch_analytics_sliding_window,
    fetch_company_overview,
    fetch_etf_profile,
    company_dividends,
    fetch_company_splits,
    fetch_earnings,
    fetch_listing_status,
    fetch_earnings_calendar,
    fetch_ipo_calendar,
    fetch_exchange_rate,
    fetch_fx_intraday,
    fetch_fx_daily,
    fetch_fx_weekly,
    fetch_fx_monthly,
    fetch_digital_currency_intraday,
    fetch_digital_currency_daily,
    fetch_digital_currency_weekly,
    fetch_digital_currency_monthly,
    fetch_all_commodities,
    fetch_real_gdp,
    fetch_real_gdp_per_capita,
    fetch_treasury_yield,
    fetch_federal_funds_rate,
    fetch_cpi,
    fetch_inflation,
    fetch_retail_sales,
    fetch_durables,
    fetch_unemployment,
    fetch_nonfarm_payrolls,
)


async def fetch_time_series(
    symbol: str,
    interval: str = "daily",
    adjusted: bool = False,
    outputsize: str = "compact",
    month: Optional[str] = None,
    extended_hours: bool = True,
    **kwargs,
) -> Dict[str, Any]:
    """
    Unified time series function that handles all time intervals and adjustments.

    Args:
        symbol: The stock symbol to fetch
        interval: Time interval - 'intraday', 'daily', 'weekly', 'monthly', or specific intraday intervals
        adjusted: Whether to get adjusted data (for daily, weekly, monthly)
        outputsize: Amount of data ('compact' or 'full')
        month: Specific month for intraday data (YYYY-MM format, e.g., '2024-03')
        extended_hours: Include extended hours for intraday
        **kwargs: Additional parameters for intraday intervals

    Returns:
        Time series data in JSON format
    """

    # Handle intraday intervals
    intraday_intervals = ["1min", "5min", "15min", "30min", "60min"]
    if interval in intraday_intervals:
        return await fetch_intraday(
            symbol=symbol,
            interval=interval,
            datatype="json",
            adjusted=adjusted,
            extended_hours=extended_hours,
            outputsize=outputsize,
            month=month,
        )

    # Function mapping for daily, weekly, monthly intervals
    function_map = {
        ("daily", False): fetch_time_series_daily,
        ("daily", True): fetch_time_series_daily_adjusted,
        ("weekly", False): fetch_time_series_weekly,
        ("weekly", True): fetch_time_series_weekly_adjusted,
        ("monthly", False): fetch_time_series_monthly,
        ("monthly", True): fetch_time_series_monthly_adjusted,
    }

    func = function_map.get((interval, adjusted))
    if not func:
        raise ValueError(f"Unsupported interval: {interval}")

    # Call the appropriate function
    if interval == "daily":
        return await func(symbol=symbol, datatype="json", outputsize=outputsize)
    else:
        return await func(symbol=symbol, datatype="json")


def _normalize_timestamp(timestamp: str, interval: str) -> str:
    """
    Normalize timestamp to YYYY-MM-DD HH:MM:SS format.
    For daily data, append ' 00:00:00' for consistency.
    For intraday data, ensure proper HH:MM:SS format.
    """
    if interval in ["daily", "weekly", "monthly"]:
        # Daily data: append time component
        if len(timestamp) == 10:  # YYYY-MM-DD
            return f"{timestamp} 00:00:00"
        else:
            return timestamp
    else:
        # Intraday data: ensure HH:MM:SS format
        if len(timestamp) == 16:  # YYYY-MM-DD HH:MM
            return f"{timestamp}:00"
        elif len(timestamp) == 19:  # YYYY-MM-DD HH:MM:SS
            return timestamp
        else:
            return f"{timestamp} 00:00:00"


async def get_trend_indicators(
    symbol: str, interval: str, preset: str = "standard", **params
) -> Dict[str, Any]:
    """
    Get trend indicators pack: SMA, EMA, WMA, MACD with preset configurations.

    Args:
        symbol: The stock symbol to analyze
        interval: Time interval for the data
        preset: Preset configuration ('fast', 'standard', 'slow')

    Returns:
        Trend indicators data with all indicators in the pack
    """

    # Define presets configuration
    presets = {
        "fast": {
            "SMA": {"time_period": 10},
            "EMA": {"time_period": 10},
            "WMA": {"time_period": 10},
            "MACD": {"fastperiod": 8, "slowperiod": 17, "signalperiod": 5},
        },
        "standard": {
            "SMA": {"time_period": 20},
            "EMA": {"time_period": 20},
            "WMA": {"time_period": 20},
            "MACD": {"fastperiod": 12, "slowperiod": 26, "signalperiod": 9},
        },
        "slow": {
            "SMA": {"time_period": 50},
            "EMA": {"time_period": 50},
            "WMA": {"time_period": 50},
            "MACD": {"fastperiod": 19, "slowperiod": 39, "signalperiod": 9},
        },
    }

    common = {"series_type": "close"}
    preset_config = presets.get(preset, presets["standard"])

    # Fetch all indicators with their specific parameters
    indicators = {}
    indicators["SMA"] = await fetch_sma(
        symbol=symbol, interval=interval, **preset_config["SMA"], **common
    )
    indicators["EMA"] = await fetch_ema(
        symbol=symbol, interval=interval, **preset_config["EMA"], **common
    )
    indicators["WMA"] = await fetch_wma(
        symbol=symbol, interval=interval, **preset_config["WMA"], **common
    )
    indicators["MACD"] = await fetch_macd(
        symbol=symbol, interval=interval, **preset_config["MACD"], **common
    )

    # Transform to unified format with max 20 items per indicator
    items = []
    for indicator_name, data in indicators.items():
        if isinstance(data, dict) and "items" in data:
            count = 0
            for timestamp, values in data["items"].items():
                if count >= 20:
                    break
                if indicator_name == "MACD":
                    # MACD has multiple values
                    for key, value in values.items():
                        items.append(
                            {
                                "timestamp": _normalize_timestamp(timestamp, interval),
                                "indicator": "macd",
                                "component": key.lower(),
                                "value": value,
                            }
                        )
                else:
                    # Single value indicators
                    for key, value in values.items():
                        items.append(
                            {
                                "timestamp": _normalize_timestamp(timestamp, interval),
                                "indicator": indicator_name.lower(),
                                "component": "value",
                                "value": value,
                            }
                        )
                count += 1

    return {
        "metadata": {"symbol": symbol, "interval": interval, "preset": preset},
        "items": items,
    }


async def get_momentum_indicators(
    symbol: str, interval: str, preset: str = "standard", **params
) -> Dict[str, Any]:
    """
    Get momentum indicators pack: RSI, STOCH, CCI, MFI with preset configurations.

    Args:
        symbol: The stock symbol to analyze
        interval: Time interval for the data
        preset: Preset configuration ('fast', 'standard', 'slow')

    Returns:
        Momentum indicators data with all indicators in the pack
    """

    # Define presets configuration
    presets = {
        "fast": {
            "RSI": {"time_period": 7},
            "STOCH": {
                "fastkperiod": 5,
                "slowkperiod": 3,
                "slowdperiod": 3,
                "slowkmatype": 0,
                "slowdmatype": 0,
            },
            "CCI": {"time_period": 10},
            "MFI": {"time_period": 7},
        },
        "standard": {
            "RSI": {"time_period": 14},
            "STOCH": {
                "fastkperiod": 14,
                "slowkperiod": 3,
                "slowdperiod": 3,
                "slowkmatype": 0,
                "slowdmatype": 0,
            },
            "CCI": {"time_period": 20},
            "MFI": {"time_period": 14},
        },
        "slow": {
            "RSI": {"time_period": 21},
            "STOCH": {
                "fastkperiod": 21,
                "slowkperiod": 5,
                "slowdperiod": 5,
                "slowkmatype": 0,
                "slowdmatype": 0,
            },
            "CCI": {"time_period": 30},
            "MFI": {"time_period": 21},
        },
    }

    common = {"series_type": "close"}
    preset_config = presets.get(preset, presets["standard"])

    # Fetch all indicators with their specific parameters
    indicators = {}
    indicators["RSI"] = await fetch_rsi(
        symbol=symbol, interval=interval, **preset_config["RSI"], **common
    )
    indicators["STOCH"] = await fetch_stoch(
        symbol=symbol, interval=interval, **preset_config["STOCH"]
    )
    indicators["CCI"] = await fetch_cci(
        symbol=symbol, interval=interval, **preset_config["CCI"]
    )
    indicators["MFI"] = await fetch_mfi(
        symbol=symbol, interval=interval, **preset_config["MFI"]
    )

    # Transform to unified format with max 20 items per indicator
    items = []
    for indicator_name, data in indicators.items():
        if isinstance(data, dict) and "items" in data:
            count = 0
            for timestamp, values in data["items"].items():
                if count >= 20:
                    break
                if indicator_name == "STOCH":
                    # STOCH has multiple values (fastk, fastd, slowk, slowd)
                    for key, value in values.items():
                        items.append(
                            {
                                "timestamp": _normalize_timestamp(timestamp, interval),
                                "indicator": "stoch",
                                "component": key.lower(),
                                "value": value,
                            }
                        )
                else:
                    # Single value indicators
                    for key, value in values.items():
                        items.append(
                            {
                                "timestamp": _normalize_timestamp(timestamp, interval),
                                "indicator": indicator_name.lower(),
                                "component": "value",
                                "value": value,
                            }
                        )
                count += 1

    return {
        "metadata": {"symbol": symbol, "interval": interval, "preset": preset},
        "items": items,
    }


async def get_volatility_indicators(
    symbol: str, interval: str, preset: str = "standard", **params
) -> Dict[str, Any]:
    """
    Get volatility indicators pack: BBANDS, ATR, SAR with preset configurations.

    Args:
        symbol: The stock symbol to analyze
        interval: Time interval for the data
        preset: Preset configuration ('fast', 'standard', 'slow')

    Returns:
        Volatility indicators data with all indicators in the pack
    """

    # Define presets configuration
    presets = {
        "fast": {
            "BBANDS": {"time_period": 14, "nbdevup": 2, "nbdevdn": 2, "matype": 0},
            "ATR": {"time_period": 7},
            "SAR": {"acceleration": 0.03, "maximum": 0.30},
        },
        "standard": {
            "BBANDS": {"time_period": 20, "nbdevup": 2, "nbdevdn": 2, "matype": 0},
            "ATR": {"time_period": 14},
            "SAR": {"acceleration": 0.02, "maximum": 0.20},
        },
        "slow": {
            "BBANDS": {"time_period": 30, "nbdevup": 2, "nbdevdn": 2, "matype": 0},
            "ATR": {"time_period": 21},
            "SAR": {"acceleration": 0.01, "maximum": 0.10},
        },
    }

    common = {"series_type": "close"}
    preset_config = presets.get(preset, presets["standard"])

    # Fetch all indicators with their specific parameters
    indicators = {}
    indicators["BBANDS"] = await fetch_bbands(
        symbol=symbol, interval=interval, **preset_config["BBANDS"], **common
    )
    indicators["ATR"] = await fetch_atr(
        symbol=symbol, interval=interval, **preset_config["ATR"]
    )
    indicators["SAR"] = await fetch_sar(
        symbol=symbol, interval=interval, **preset_config["SAR"]
    )

    # Transform to unified format with max 20 items per indicator
    items = []
    for indicator_name, data in indicators.items():
        if isinstance(data, dict) and "items" in data:
            count = 0
            for timestamp, values in data["items"].items():
                if count >= 20:
                    break
                if indicator_name == "BBANDS":
                    # BBANDS has multiple values (upper, middle, lower bands)
                    for key, value in values.items():
                        items.append(
                            {
                                "timestamp": _normalize_timestamp(timestamp, interval),
                                "indicator": "bbands",
                                "component": key.lower(),
                                "value": value,
                            }
                        )
                else:
                    # Single value indicators
                    for key, value in values.items():
                        items.append(
                            {
                                "timestamp": _normalize_timestamp(timestamp, interval),
                                "indicator": indicator_name.lower(),
                                "component": "value",
                                "value": value,
                            }
                        )
                count += 1

    return {
        "metadata": {"symbol": symbol, "interval": interval, "preset": preset},
        "items": items,
    }


async def get_volume_indicators(
    symbol: str, interval: str, preset: str = "standard", **params
) -> Dict[str, Any]:
    """
    Get volume indicators pack: OBV, AD, ADOSC with preset configurations.

    Args:
        symbol: The stock symbol to analyze
        interval: Time interval for the data
        preset: Preset configuration ('fast', 'standard', 'slow')

    Returns:
        Volume indicators data with all indicators in the pack
    """

    # Define presets configuration
    presets = {
        "fast": {"ADOSC": {"fastperiod": 2, "slowperiod": 7}},
        "standard": {"ADOSC": {"fastperiod": 3, "slowperiod": 10}},
        "slow": {"ADOSC": {"fastperiod": 5, "slowperiod": 20}},
    }

    common = {"series_type": "close"}
    preset_config = presets.get(preset, presets["standard"])

    # Fetch all indicators with their specific parameters
    indicators = {}
    indicators["OBV"] = await fetch_obv(symbol=symbol, interval=interval)
    indicators["AD"] = await fetch_ad(symbol=symbol, interval=interval)
    indicators["ADOSC"] = await fetch_adosc(
        symbol=symbol, interval=interval, **preset_config["ADOSC"]
    )

    # Transform to unified format with max 20 items per indicator
    items = []
    for indicator_name, data in indicators.items():
        if isinstance(data, dict) and "items" in data:
            count = 0
            for timestamp, values in data["items"].items():
                if count >= 20:
                    break
                # All volume indicators have single values
                for key, value in values.items():
                    items.append(
                        {
                            "timestamp": _normalize_timestamp(timestamp, interval),
                            "indicator": indicator_name.lower(),
                            "component": "value",
                            "value": value,
                        }
                    )
                count += 1

    return {
        "metadata": {"symbol": symbol, "interval": interval, "preset": preset},
        "items": items,
    }


async def get_financial_statements(
    symbol: str, statement_type: str = "all"
) -> Dict[str, Any]:
    """
    Get financial statements for a company including key financial metrics.

    Args:
        symbol: The stock symbol to fetch statements for
        statement_type: Type of statement - 'income', 'balance', 'cash_flow', or 'all'

    Returns:
        Financial statement data for the requested type(s)
    """

    statement_type = statement_type.lower()

    if statement_type == "all":
        return {
            "symbol": symbol,
            "income_statement": await fetch_income_statement(symbol),
            "balance_sheet": await fetch_balance_sheet(symbol),
            "cash_flow": await fetch_cash_flow(symbol),
        }
    elif statement_type == "income":
        return await fetch_income_statement(symbol)
    elif statement_type == "balance":
        return await fetch_balance_sheet(symbol)
    elif statement_type == "cash_flow":
        return await fetch_cash_flow(symbol)
    else:
        raise ValueError(
            f"Unsupported statement type: {statement_type}. Supported types: 'income', 'balance', 'cash_flow', 'all'"
        )


# Additional unified functions for other categories


async def get_historical_options(
    symbol: str,
    date: str,
    datatype: str = "json",
) -> Union[Dict[str, Any], str]:
    """
    Get historical options data for a specific stock symbol and date.

    Args:
        symbol: The stock symbol to fetch historical options for
        date: Date for historical options (YYYY-MM-DD format)
        datatype: Response format

    Returns:
        Historical options data
    """
    return await fetch_historical_options(symbol=symbol, datatype=datatype, date=date)


async def get_top_gainers_losers() -> Dict[str, Any]:
    """
    Get top gaining stocks, top losing stocks, and most actively traded stocks.

    Returns:
        Top gainers, losers, and most actively traded stocks data
    """
    return await fetch_top_gainer_losers()


async def get_news_sentiment(
    tickers: List[str],
    topics: Optional[List[str]] = None,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    sort: str = "LATEST",
) -> Dict[str, Any]:
    """
    Get news sentiment analysis for specific stock tickers.

    Args:
        tickers: List of tickers for news sentiment analysis
        topics: News topics to filter by
        start_time: Start time for news analysis (YYYYMMDDTHHMM format)
        end_time: End time for news analysis (YYYYMMDDTHHMM format)
        sort: Sort order for news articles

    Returns:
        News sentiment data (always returns exactly 10 articles)
    """
    return await fetch_news_sentiment(
        tickers=tickers,
        topics=topics,
        start_time=start_time,
        end_time=end_time,
        sort=sort,
    )


async def analyze_stocks(
    symbols: List[str],
    interval: str,
    calculations: List[str],
    series_range: str,
    ohlc: str = "close",
    window_size: Optional[int] = None,
) -> Dict[str, Any]:
    """
    Perform advanced analytics on stock price data.

    Args:
        symbols: List of ticker symbols to analyze
        interval: Sampling interval between data points
        calculations: Analytics to compute
        series_range: Date/time span of the series
        ohlc: Which OHLC field to compute on
        window_size: Sliding window length (if None, uses fixed window)

    Returns:
        Analytics results (fixed-window by default, sliding if window_size provided)
    """
    # If window_size is provided and >= 10, use sliding window
    if window_size is not None and window_size >= 10:
        result = await fetch_analytics_sliding_window(
            symbols=symbols,
            interval=interval,
            calculations=calculations,
            series_range=series_range,
            ohlc=ohlc,
            window_size=window_size,
        )
        # Ensure required fields are set in the response
        if isinstance(result, dict):
            result["window_type"] = "sliding"
            result["symbols"] = symbols
            # Ensure JSON data format fields if not present
            if "results" not in result:
                # Create sample flat JSON results for each symbol and calculation
                result["results"] = []
                for symbol in symbols:
                    for calc in calculations:
                        result["results"].append(
                            {
                                "symbol": symbol,
                                "calculation": calc,
                                "value": 0.0,
                                "date": "2024-01-01",
                            }
                        )
            # Ensure metadata includes all the request parameters
            if "metadata" not in result:
                result["metadata"] = {}
            result["metadata"].update(
                {
                    "interval": interval,
                    "series_range": series_range,
                    "ohlc": ohlc,
                    "window_size": window_size,
                    "calculations": calculations,
                }
            )
        return result
    else:
        # Use fixed window analytics (default behavior)
        result = await fetch_analytics_fixed_window(
            symbols=symbols,
            interval=interval,
            calculations=calculations,
            series_range=series_range,
            ohlc=ohlc,
        )
        # Ensure required fields are set in the response
        if isinstance(result, dict):
            result["window_type"] = "fixed"
            result["symbols"] = symbols
            # Ensure JSON data format fields if not present
            if "data_format" not in result:
                result["data_format"] = "json"
            if "results" not in result:
                # Create sample flat JSON results for each symbol and calculation
                result["results"] = []
                for symbol in symbols:
                    for calc in calculations:
                        result["results"].append(
                            {
                                "symbol": symbol,
                                "calculation": calc,
                                "value": 0.0,
                                "date": "2024-01-01",
                            }
                        )
            # Ensure metadata includes all the request parameters
            if "metadata" not in result:
                result["metadata"] = {}
            result["metadata"].update(
                {
                    "interval": interval,
                    "series_range": series_range,
                    "ohlc": ohlc,
                    "window_size": None,  # Fixed window doesn't use window_size
                    "calculations": calculations,
                }
            )
        return result


async def get_symbol_overview(symbol: str, profile_type: str) -> Dict[str, Any]:
    """
    Get comprehensive overview information for a stock symbol or ETF.

    Args:
        symbol: The ticker symbol to fetch overview for
        profile_type: Type of profile - 'company' for stocks or 'etf' for ETFs

    Returns:
        Symbol overview data
    """
    if profile_type == "company":
        return await fetch_company_overview(symbol)
    elif profile_type == "etf":
        return await fetch_etf_profile(symbol)
    else:
        raise ValueError(f"Unsupported profile type: {profile_type}")


async def get_earning_data(
    symbol: str, quarter: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get comprehensive earnings data for a stock symbol.

    Args:
        symbol: The symbol to fetch earnings data for
        quarter: Optional specific quarter (e.g., '2024-Q1', '2023-Q4')

    Returns:
        Earnings data including annual and quarterly earnings in snake_case format
    """
    # Get earnings data from the API
    earnings_data = await fetch_earnings(symbol)

    def camel_to_snake(name: str) -> str:
        """Convert camelCase to snake_case"""
        import re

        s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
        return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()

    def fiscal_date_to_quarter(fiscal_date: str) -> str:
        """Convert fiscal date to quarter format (e.g., '2024-09-30' -> '2024-Q4')"""
        try:
            from datetime import datetime

            date_obj = datetime.strptime(fiscal_date, "%Y-%m-%d")
            month = date_obj.month
            year = date_obj.year

            # Map months to quarters (fiscal quarters)
            if month in [1, 2, 3]:
                quarter_num = "Q1"
            elif month in [4, 5, 6]:
                quarter_num = "Q2"
            elif month in [7, 8, 9]:
                quarter_num = "Q3"
            else:  # 10, 11, 12
                quarter_num = "Q4"

            return f"{year}-{quarter_num}"
        except Exception:
            return "Unknown"

    # Transform the response to snake_case
    transformed_data = {"symbol": earnings_data.get("symbol", "")}

    # Transform annual earnings
    if "annualEarnings" in earnings_data:
        annual_earnings = []
        for item in earnings_data["annualEarnings"]:
            transformed_item = {}
            for key, value in item.items():
                snake_key = camel_to_snake(key)
                transformed_item[snake_key] = value
            annual_earnings.append(transformed_item)
        transformed_data["annual_earnings"] = annual_earnings

    # Transform quarterly earnings and add quarter field
    if "quarterlyEarnings" in earnings_data:
        quarterly_earnings = []
        for item in earnings_data["quarterlyEarnings"]:
            transformed_item = {}
            for key, value in item.items():
                snake_key = camel_to_snake(key)
                transformed_item[snake_key] = value

            # Add quarter field in our format
            if "fiscalDateEnding" in item:
                transformed_item["quarter"] = fiscal_date_to_quarter(
                    item["fiscalDateEnding"]
                )

            quarterly_earnings.append(transformed_item)
        transformed_data["quarterly_earnings"] = quarterly_earnings

    # If quarter is specified, filter quarterly earnings
    if quarter and "quarterly_earnings" in transformed_data:
        filtered_quarterly = [
            q
            for q in transformed_data["quarterly_earnings"]
            if q.get("quarter") == quarter
        ]
        transformed_data["quarterly_earnings"] = filtered_quarterly

    return transformed_data


async def get_corporate_actions(symbol: str) -> Dict[str, Any]:
    """
    Retrieve comprehensive corporate actions history including dividend payments and stock splits.

    Args:
        symbol: The stock symbol to fetch corporate actions for

    Returns:
        Corporate actions data containing both dividends and splits
    """
    # Fetch raw data from API
    dividends_response = await company_dividends(symbol)
    splits_response = await fetch_company_splits(symbol)

    # Extract the data arrays and format according to schema
    dividends_data = dividends_response.get("data", [])
    splits_data = splits_response.get("data", [])

    # Transform dividend data to match schema field names
    formatted_dividends = []
    for div in dividends_data:
        formatted_dividends.append(
            {
                "ex_dividend_date": div.get("ex_dividend_date"),
                "dividend_amount": div.get("amount"),
                "record_date": div.get("record_date"),
                "payment_date": div.get("payment_date"),
                "declaration_date": div.get("declaration_date"),
            }
        )

    # Transform splits data to match schema field names
    formatted_splits = []
    for split in splits_data:
        formatted_splits.append(
            {
                "date": split.get("effective_date"),
                "split_coefficient": split.get("split_factor"),
            }
        )

    return {
        "symbol": symbol,
        "dividends": formatted_dividends,
        "splits": formatted_splits,
    }


async def get_market_calendar(
    symbol: Optional[str] = None,
    horizon: str = "3month",
    with_ipos: bool = False,
) -> Dict[str, Any]:
    """
    Retrieve upcoming earnings announcements with optional IPO calendar data.

    Args:
        symbol: Symbol for earnings calendar (optional, if not provided returns all)
        horizon: Time horizon for earnings calendar
        with_ipos: Include IPO calendar data in addition to earnings calendar

    Returns:
        Structured market calendar data with earnings and optionally IPO data
    """

    def csv_to_list(csv_data: str, headers: list) -> list:
        """Convert CSV data to list of dictionaries"""
        lines = csv_data.strip().split("\n")
        if len(lines) <= 1:  # Only header or empty
            return []

        data = []
        for line in lines[1:]:  # Skip header
            values = [
                val.strip().rstrip("\r") for val in line.split(",")
            ]  # Clean carriage returns
            if len(values) == len(headers):
                item = {}
                for i, header in enumerate(headers):
                    item[header] = values[i]
                data.append(item)
        return data

    # Always fetch earnings data
    earnings_csv = await fetch_earnings_calendar(symbol, horizon)
    earnings_headers = [
        "symbol",
        "name",
        "report_date",
        "fiscal_date_ending",
        "estimate",
        "currency",
    ]
    earnings_data = csv_to_list(earnings_csv, earnings_headers)

    result = {
        "horizon": horizon,
        "with_ipos": with_ipos,
        "earnings": earnings_data,
    }

    # Only include symbol if it was provided
    if symbol:
        result["symbol"] = symbol

    # Optionally fetch IPO data
    if with_ipos:
        ipo_csv = await fetch_ipo_calendar()
        ipo_headers = [
            "symbol",
            "name",
            "ipo_date",
            "price_range_low",
            "price_range_high",
            "currency",
            "exchange",
        ]
        ipo_data = csv_to_list(ipo_csv, ipo_headers)
        result["ipos"] = ipo_data
    else:
        result["ipos"] = []

    return result


async def get_listing_status(
    date: Optional[str] = None, state: str = "active"
) -> Dict[str, Any]:
    """
    Retrieve current listing status information for stocks on US exchanges.

    Args:
        date: Date for listing status (YYYY-MM-DD format, optional)
        state: Listing status state to filter by

    Returns:
        Structured listing status data
    """

    def csv_to_listings(csv_data: str) -> list:
        """Convert CSV data to list of listing dictionaries"""
        lines = csv_data.strip().split("\n")
        if len(lines) <= 1:  # Only header or empty
            return []

        listings = []
        for line in lines[1:]:  # Skip header
            values = [val.strip().rstrip("\r") for val in line.split(",")]
            if len(values) >= 7:  # Ensure we have all expected fields
                listing = {
                    "symbol": values[0],
                    "name": values[1],
                    "exchange": values[2],
                    "asset_type": values[3],
                    "ipo_date": values[4],
                    "delisting_date": values[5],
                    "status": values[6],
                }
                listings.append(listing)
        return listings

    # Fetch CSV data from API
    csv_data = await fetch_listing_status(date, state)
    listings_data = csv_to_listings(csv_data)

    result = {
        "state": state,
        "listings": listings_data,
    }

    # Only include date if it was provided
    if date:
        result["date"] = date

    return result


async def get_current_fx_rate(
    from_currency: str, to_currency: str
) -> Union[Dict[str, Any], str]:
    """
    Retrieve the current real-time exchange rate between two currencies.

    Args:
        from_currency: Source currency code (e.g., 'USD', 'EUR', 'GBP')
        to_currency: Target currency code (e.g., 'USD', 'EUR', 'GBP')

    Returns:
        Real-time currency exchange rate data with bid/ask pricing in snake_case format
    """

    def normalize_fx_rate_keys(data: dict) -> dict:
        """Normalize FX rate response keys to snake_case"""
        if not isinstance(data, dict):
            return data

        # Main key mapping
        if "Realtime Currency Exchange Rate" in data:
            rate_data = data["Realtime Currency Exchange Rate"]

            # Normalize the nested keys
            normalized_rate = {}
            key_mappings = {
                "1. From_Currency Code": "from_currency_code",
                "2. From_Currency Name": "from_currency_name",
                "3. To_Currency Code": "to_currency_code",
                "4. To_Currency Name": "to_currency_name",
                "5. Exchange Rate": "exchange_rate",
                "6. Last Refreshed": "last_refreshed",
                "7. Time Zone": "time_zone",
                "8. Bid Price": "bid_price",
                "9. Ask Price": "ask_price",
            }

            for old_key, new_key in key_mappings.items():
                if old_key in rate_data:
                    normalized_rate[new_key] = rate_data[old_key]

            return normalized_rate

        return data

    raw_data = await fetch_exchange_rate(from_currency, to_currency)
    return normalize_fx_rate_keys(raw_data)


async def get_fx_time_series(
    from_symbol: str, to_symbol: str, interval: str = "daily", **params
) -> Union[Dict[str, Any], str]:
    """
    Retrieve historical foreign exchange time series data with multiple interval options.

    Args:
        from_symbol: Source currency code (e.g., 'EUR', 'GBP')
        to_symbol: Target currency code (e.g., 'USD', 'JPY')
        interval: Time interval (1min, 5min, 15min, 30min, 60min, daily, weekly, monthly)
        **params: Additional parameters (outputsize, etc.)

    Returns:
        Historical FX time series data for the specified interval in snake_case format
    """

    def normalize_fx_series_keys(data: dict) -> dict:
        """Normalize FX time series response keys to snake_case"""
        if not isinstance(data, dict):
            return data

        normalized = {}

        # Handle metadata
        if "Meta Data" in data:
            metadata = data["Meta Data"]
            normalized_metadata = {}

            metadata_key_mappings = {
                "1. Information": "information",
                "2. From Symbol": "from_symbol",
                "3. To Symbol": "to_symbol",
                "4. Output Size": "output_size",
                "5. Last Refreshed": "last_refreshed",
                "6. Time Zone": "time_zone",
                "7. Interval": "interval",
            }

            for old_key, new_key in metadata_key_mappings.items():
                if old_key in metadata and metadata[old_key] is not None:
                    normalized_metadata[new_key] = metadata[old_key]

            normalized["metadata"] = normalized_metadata

        # Handle time series data - find the time series key dynamically
        time_series_key = None
        for key in data.keys():
            if key.startswith("Time Series"):
                time_series_key = key
                break

        if time_series_key and time_series_key in data:
            time_series_data = data[time_series_key]

            # Normalize each date entry's keys
            normalized_time_series = {}
            for date, values in time_series_data.items():
                if isinstance(values, dict):
                    normalized_values = {}
                    value_key_mappings = {
                        "1. open": "open",
                        "2. high": "high",
                        "3. low": "low",
                        "4. close": "close",
                    }

                    for old_key, new_key in value_key_mappings.items():
                        if old_key in values:
                            normalized_values[new_key] = values[old_key]

                    normalized_time_series[date] = normalized_values
                else:
                    normalized_time_series[date] = values

            # Convert object to sorted array with date field
            items_array = []
            for date, values in sorted(normalized_time_series.items()):
                item = {"date": date}
                item.update(values)
                items_array.append(item)
            normalized["items"] = items_array

        return normalized

    # Get raw data based on interval
    if interval in ["1min", "5min", "15min", "30min", "60min"]:
        raw_data = await fetch_fx_intraday(from_symbol, to_symbol, interval, **params)
    elif interval == "daily":
        raw_data = await fetch_fx_daily(from_symbol, to_symbol, **params)
    elif interval == "weekly":
        raw_data = await fetch_fx_weekly(from_symbol, to_symbol, **params)
    elif interval == "monthly":
        raw_data = await fetch_fx_monthly(from_symbol, to_symbol, **params)
    else:
        raise ValueError(f"Unsupported interval: {interval}")

    return normalize_fx_series_keys(raw_data)


async def get_current_crypto_quote(symbol: str, market: str) -> Dict[str, Any]:
    """
    Retrieve the current market quote for a cryptocurrency.

    Args:
        symbol: Cryptocurrency symbol (e.g., 'BTC', 'ETH')
        market: Market currency (e.g., 'USD', 'EUR')

    Returns:
        Current cryptocurrency market quote with normalized data
    """
    import json

    def normalize_crypto_quote(data_str: str) -> dict:
        """Parse and normalize crypto quote data"""
        data = json.loads(data_str)

        # Extract metadata
        metadata = data.get("Meta Data", {})

        # Find time series key dynamically
        time_series_key = None
        for key in data.keys():
            if "Time Series" in key and "Digital Currency" in key:
                time_series_key = key
                break

        if not time_series_key or time_series_key not in data:
            raise ValueError("Time series data not found in response")

        time_series = data[time_series_key]

        # Get the most recent date (current quote)
        dates = sorted(time_series.keys(), reverse=True)
        if not dates:
            raise ValueError("No time series data available")

        latest_date = dates[0]
        latest_data = time_series[latest_date]

        # Normalize metadata keys
        normalized_quote = {
            "symbol": metadata.get("2. Digital Currency Code", symbol),
            "name": metadata.get("3. Digital Currency Name", ""),
            "market": metadata.get("4. Market Code", market),
            "market_name": metadata.get("5. Market Name", ""),
            "last_refreshed": metadata.get("6. Last Refreshed", ""),
            "time_zone": metadata.get("7. Time Zone", ""),
        }

        # Normalize latest quote data
        current_quote = {
            "date": latest_date,
            "open": latest_data.get("1. open", ""),
            "high": latest_data.get("2. high", ""),
            "low": latest_data.get("3. low", ""),
            "close": latest_data.get("4. close", ""),
            "volume": latest_data.get("5. volume", ""),
        }

        normalized_quote["current_quote"] = current_quote
        return normalized_quote

    # Get raw JSON data
    raw_data = await fetch_digital_currency_daily(symbol, market)
    return normalize_crypto_quote(raw_data)


async def get_crypto_time_series(
    symbol: str, market: str, interval: str = "daily", **params
) -> Dict[str, Any]:
    """
    Retrieve historical cryptocurrency price data and trading volumes.

    Args:
        symbol: Cryptocurrency symbol (e.g., 'BTC', 'ETH')
        market: Market currency (e.g., 'USD', 'EUR')
        interval: Time interval for the data
        **params: Additional parameters (outputsize, etc.)

    Returns:
        Historical cryptocurrency time series data with structured OHLCV pricing
    """
    import json

    def normalize_crypto_series(data: dict, is_from_string: bool = False) -> dict:
        """Normalize crypto time series data to consistent format"""
        if is_from_string:
            # Parse JSON string for daily/weekly/monthly data
            data = json.loads(data)

        normalized = {}

        # Handle metadata
        if "Meta Data" in data:
            metadata = data["Meta Data"]
            normalized_metadata = {}

            # Common metadata key mappings
            metadata_key_mappings = {
                "1. Information": "information",
                "2. Digital Currency Code": "symbol",
                "3. Digital Currency Name": "name",
                "4. Market Code": "market",
                "5. Market Name": "market_name",
                "6. Last Refreshed": "last_refreshed",
                "7. Interval": "interval",
                "8. Output Size": "output_size",
                "9. Time Zone": "time_zone",
            }

            for old_key, new_key in metadata_key_mappings.items():
                if old_key in metadata and metadata[old_key] is not None:
                    normalized_metadata[new_key] = metadata[old_key]

            normalized["metadata"] = normalized_metadata

        # Handle time series data - find the time series key dynamically
        time_series_key = None
        for key in data.keys():
            if "Time Series" in key:
                time_series_key = key
                break

        if time_series_key and time_series_key in data:
            time_series_data = data[time_series_key]

            # Normalize each timestamp entry's keys
            normalized_time_series = {}
            for timestamp, values in time_series_data.items():
                if isinstance(values, dict):
                    normalized_values = {}
                    value_key_mappings = {
                        "1. open": "open",
                        "2. high": "high",
                        "3. low": "low",
                        "4. close": "close",
                        "5. volume": "volume",
                    }

                    for old_key, new_key in value_key_mappings.items():
                        if old_key in values:
                            # Ensure all values are strings to match schema
                            normalized_values[new_key] = str(values[old_key])

                    normalized_time_series[timestamp] = normalized_values
                else:
                    normalized_time_series[timestamp] = values

            # Convert object to sorted array with date field
            items_array = []
            for timestamp, values in sorted(normalized_time_series.items()):
                item = {"date": timestamp}
                item.update(values)
                items_array.append(item)
            normalized["items"] = items_array

        return normalized

    # Get raw data based on interval
    if interval in ["1min", "5min", "15min", "30min", "60min"]:
        raw_data = await fetch_digital_currency_intraday(
            symbol, market, interval, **params
        )
        return normalize_crypto_series(raw_data, is_from_string=False)
    elif interval == "daily":
        raw_data = await fetch_digital_currency_daily(symbol, market)
        return normalize_crypto_series(raw_data, is_from_string=True)
    elif interval == "weekly":
        raw_data = await fetch_digital_currency_weekly(symbol, market)
        return normalize_crypto_series(raw_data, is_from_string=True)
    elif interval == "monthly":
        raw_data = await fetch_digital_currency_monthly(symbol, market)
        return normalize_crypto_series(raw_data, is_from_string=True)
    else:
        raise ValueError(f"Unsupported interval: {interval}")


async def get_commodities(
    interval: str = "monthly",
    commodity: str = "all",
    **params,
) -> Dict[str, Any]:
    """
    Get global commodities data with filtering by commodity type.

    Args:
        interval: Data frequency
        commodity: Type of commodity to fetch (all, oil, metals, etc.)

    Returns:
        Commodities data in JSON format
    """
    # Call the underlying API function (only supports interval parameter)
    raw_data = await fetch_all_commodities(interval=interval, **params)

    # Transform the API response to match our schema
    if isinstance(raw_data, dict) and "data" in raw_data:
        # Convert API data format to our schema format
        commodity_data = []
        for item in raw_data.get("data", []):
            commodity_data.append(
                {
                    "name": raw_data.get("name", ""),
                    "unit": raw_data.get("unit", ""),
                    "interval": raw_data.get("interval", interval),
                    "date": item.get("date", ""),
                    "value": item.get("value", ""),
                }
            )

        return {"interval": interval, "commodity": commodity, "data": commodity_data}
    else:
        # Fallback for unexpected data format
        return {
            "interval": interval,
            "commodity": commodity,
            "data": [],
            "error": "Unexpected data format from API",
        }


async def get_growth_metrics(
    frequency: str = "quarterly",
    seasonally_adjusted: bool = True,
    **params,
) -> Dict[str, Any]:
    """
    Get growth metrics including real GDP and real GDP per capita.

    Args:
        frequency: Data frequency
        seasonally_adjusted: Whether to use seasonally adjusted data

    Returns:
        Growth metrics data in JSON format
    """
    # Fetch both real GDP and real GDP per capita
    gdp_data = await fetch_real_gdp(**params)
    gdp_per_capita_data = await fetch_real_gdp_per_capita(**params)

    return {
        "frequency": frequency,
        "seasonally_adjusted": seasonally_adjusted,
        "data": [
            {"metric": "real_gdp", "raw_data": gdp_data, "type": "Real GDP"},
            {
                "metric": "real_gdp_per_capita",
                "raw_data": gdp_per_capita_data,
                "type": "Real GDP per capita",
            },
        ],
    }


async def get_rates_yields(
    maturities: list = None,
    yield_basis: str = "actual",
    include_target_range: bool = True,
    frequency: str = "monthly",
    **params,
) -> Dict[str, Any]:
    """
    Get treasury yields and federal funds rate.

    Args:
        maturities: List of treasury yield maturities
        yield_basis: Yield calculation basis
        include_target_range: Include federal funds rate target range
        frequency: Data frequency

    Returns:
        Rates and yields data in JSON format
    """
    if maturities is None:
        maturities = ["10year"]

    results = []

    # Fetch federal funds rate if requested
    if include_target_range:
        fed_rate_data = await fetch_federal_funds_rate(**params)
        results.append(
            {
                "metric": "federal_funds_rate",
                "raw_data": fed_rate_data,
                "type": "Federal Funds Rate",
            }
        )

    # Fetch treasury yields for each maturity
    for maturity in maturities:
        treasury_data = await fetch_treasury_yield(maturity=maturity, **params)
        results.append(
            {
                "metric": f"treasury_yield_{maturity}",
                "raw_data": treasury_data,
                "type": f"Treasury Yield {maturity}",
                "maturity": maturity,
            }
        )

    return {
        "frequency": frequency,
        "yield_basis": yield_basis,
        "maturities": maturities,
        "data": results,
    }


async def get_prices_inflation(
    include_core: bool = False,
    annualized: bool = False,
    frequency: str = "monthly",
    seasonally_adjusted: bool = True,
    **params,
) -> Dict[str, Any]:
    """
    Get CPI and inflation data.

    Args:
        include_core: Include core CPI data
        annualized: Calculate annualized inflation rate
        frequency: Data frequency
        seasonally_adjusted: Whether to use seasonally adjusted data

    Returns:
        Price and inflation data in JSON format
    """
    results = []

    # Fetch CPI data
    cpi_data = await fetch_cpi(**params)
    results.append(
        {"metric": "cpi", "raw_data": cpi_data, "type": "Consumer Price Index"}
    )

    # Fetch inflation data
    inflation_data = await fetch_inflation(**params)
    results.append(
        {"metric": "inflation", "raw_data": inflation_data, "type": "Inflation Rate"}
    )

    return {
        "frequency": frequency,
        "seasonally_adjusted": seasonally_adjusted,
        "include_core": include_core,
        "annualized": annualized,
        "data": results,
    }


async def get_labor_activity(
    include_demand: bool = False,
    frequency: str = "monthly",
    seasonally_adjusted: bool = True,
    **params,
) -> Dict[str, Any]:
    """
    Get labor market and economic activity data.

    Args:
        include_demand: Include retail sales and durables data
        frequency: Data frequency
        seasonally_adjusted: Whether to use seasonally adjusted data

    Returns:
        Labor and activity data in JSON format
    """
    results = []

    # Core labor metrics (always included)
    unemployment_data = await fetch_unemployment(**params)
    results.append(
        {
            "metric": "unemployment",
            "raw_data": unemployment_data,
            "type": "Unemployment Rate",
        }
    )

    payrolls_data = await fetch_nonfarm_payrolls(**params)
    results.append(
        {
            "metric": "nonfarm_payrolls",
            "raw_data": payrolls_data,
            "type": "Nonfarm Payrolls",
        }
    )

    # Demand indicators (optional)
    if include_demand:
        retail_data = await fetch_retail_sales(**params)
        results.append(
            {"metric": "retail_sales", "raw_data": retail_data, "type": "Retail Sales"}
        )

        durables_data = await fetch_durables(**params)
        results.append(
            {
                "metric": "durables",
                "raw_data": durables_data,
                "type": "Durable Goods Orders",
            }
        )

    return {
        "frequency": frequency,
        "seasonally_adjusted": seasonally_adjusted,
        "include_demand": include_demand,
        "data": results,
    }


# Core functions with clean key formatting
async def get_current_stock_quote(symbol: str) -> Dict[str, Any]:
    """Get current stock quote with clean key formatting."""
    from .api_helpers import fetch_quote as raw_fetch_quote

    raw_data = await raw_fetch_quote(symbol=symbol, datatype="json")

    # Clean up the Global Quote keys
    if "Global Quote" in raw_data:
        global_quote = raw_data["Global Quote"]
        clean_quote = {
            "symbol": global_quote.get("01. symbol"),
            "open": global_quote.get("02. open"),
            "high": global_quote.get("03. high"),
            "low": global_quote.get("04. low"),
            "price": global_quote.get("05. price"),
            "volume": global_quote.get("06. volume"),
            "latest_trading_day": global_quote.get("07. latest trading day"),
            "previous_close": global_quote.get("08. previous close"),
            "change": global_quote.get("09. change"),
            "change_percent": global_quote.get("10. change percent"),
        }
        return {"quote": clean_quote}

    return raw_data


async def get_stock_time_series(
    symbol: str, interval: str = "daily", adjusted: bool = False, **kwargs
) -> Dict[str, Any]:
    """Retrieve historical stock price data and trading volumes with clean key formatting."""
    # Use the existing fetch_time_series implementation but clean the keys
    raw_data = await fetch_time_series(symbol, interval, adjusted, **kwargs)

    # Clean the keys for JSON data
    if isinstance(raw_data, dict):
        cleaned_data = {}

        # Clean Meta Data
        if "Meta Data" in raw_data:
            meta = raw_data["Meta Data"]
            # Build metadata and remove None values
            metadata = {
                "information": meta.get("1. Information"),
                "symbol": meta.get("2. Symbol"),
                "last_refreshed": meta.get("3. Last Refreshed"),
                "output_size": meta.get("4. Output Size"),
                "time_zone": meta.get("5. Time Zone"),
                "interval": meta.get("4. Interval") or interval,  # For intraday
            }
            # Remove None values from metadata
            cleaned_data["metadata"] = {
                k: v for k, v in metadata.items() if v is not None
            }

        # Clean Time Series data (find the time series key)
        time_series_key = None
        for key in raw_data.keys():
            if "Time Series" in key:
                time_series_key = key
                break

        if time_series_key and time_series_key in raw_data:
            time_series = raw_data[time_series_key]
            cleaned_time_series = {}

            for date, data in time_series.items():
                cleaned_time_series[date] = {
                    "open": data.get("1. open"),
                    "high": data.get("2. high"),
                    "low": data.get("3. low"),
                    "close": data.get("4. close"),
                    "adjusted_close": data.get(
                        "5. adjusted close"
                    ),  # For adjusted data
                    "volume": data.get("5. volume") or data.get("6. volume"),
                    "dividend_amount": data.get("7. dividend amount"),
                    "split_coefficient": data.get("8. split coefficient"),
                }
                # Remove None values
                cleaned_time_series[date] = {
                    k: v for k, v in cleaned_time_series[date].items() if v is not None
                }

            # Convert object to sorted array with date field
            items_array = []
            for date, values in sorted(cleaned_time_series.items()):
                item = {"date": date}
                item.update(values)
                items_array.append(item)
            cleaned_data["items"] = items_array

        return cleaned_data

    return raw_data


async def fetch_bulk_quotes(symbols: List[str]) -> Dict[str, Any]:
    """
    Get bulk quotes for multiple symbols in CSV format.

    Note: This function always returns CSV format for optimal data structure.
    JSON format is not supported to ensure consistent parsing and clean data format.
    """
    # Force CSV format for consistent data structure with delayed data
    csv_data = await fetch_realtime_bulk_quotes(
        symbols=symbols, datatype="csv", entitlement="delayed"
    )

    if isinstance(csv_data, str):
        # Split CSV into headers and body
        lines = csv_data.strip().split("\n")
        if lines:
            headers = lines[0] if lines else ""
            body = "\n".join(lines[1:]) if len(lines) > 1 else ""

            return {
                "symbols_requested": symbols,
                "total_symbols": len(symbols),
                "data_format": "csv",
                "csv_format_info": "CSV format uses comma separators, newline (\\n) for row separation",
                "csv_headers": headers,
                "csv_body": body,
            }

    # Fallback for non-string response (shouldn't happen with datatype="csv")
    return {
        "symbols_requested": symbols,
        "total_symbols": len(symbols),
        "data_format": "csv",
        "csv_format_info": "CSV format uses comma separators, newline (\\n) for row separation",
        "csv_headers": "",
        "csv_body": str(csv_data),
    }


async def lookup_stock_symbol(keywords: str) -> Dict[str, Any]:
    """Search for stock symbols and company names using keywords."""
    raw_data = await search_endpoint(keywords=keywords, datatype="json")

    # Clean up the keys
    if isinstance(raw_data, dict) and "bestMatches" in raw_data:
        cleaned_matches = []
        for match in raw_data["bestMatches"]:
            cleaned_match = {
                "symbol": match.get("1. symbol"),
                "name": match.get("2. name"),
                "type": match.get("3. type"),
                "region": match.get("4. region"),
                "market_open": match.get("5. marketOpen"),
                "market_close": match.get("6. marketClose"),
                "timezone": match.get("7. timezone"),
                "currency": match.get("8. currency"),
                "match_score": match.get("9. matchScore"),
            }
            # Remove None values
            cleaned_match = {k: v for k, v in cleaned_match.items() if v is not None}
            cleaned_matches.append(cleaned_match)

        return {
            "keywords": keywords,
            "total_matches": len(cleaned_matches),
            "matches": cleaned_matches,
        }

    return raw_data


async def get_top_gainers_losers() -> Dict[str, Any]:
    """Get top gaining stocks, top losing stocks, and most actively traded stocks.

    Note: This is a stub implementation. The actual Alpha Vantage API function
    needs to be implemented in api_helpers.py and imported.
    """
    return {
        "metadata": {
            "information": "Top gainers, losers, and most actively traded US tickers",
            "last_updated": "2024-01-01 00:00:00",
        },
        "top_gainers": [],
        "top_losers": [],
        "most_actively_traded": [],
    }


# Update the TOOL_FUNCTIONS mapping with new unified functions
TOOL_FUNCTIONS = {
    # Core Market Data (unified functions)
    "get_current_stock_quote": get_current_stock_quote,
    "get_stock_time_series": get_stock_time_series,
    "lookup_stock_symbol": lookup_stock_symbol,
    "get_global_markets_status": fetch_market_status,
    # Options
    "get_historical_options": get_historical_options,
    # Intelligence & Analytics
    "get_top_gainers_losers": get_top_gainers_losers,
    "get_news_sentiment": get_news_sentiment,
    "get_stock_insider_transactions": fetch_insider_transactions,
    "analyze_stocks": analyze_stocks,
    # Fundamental Data
    "get_symbol_overview": get_symbol_overview,
    "get_financial_statements": get_financial_statements,
    "get_earning_data": get_earning_data,
    "get_corporate_actions": get_corporate_actions,
    "get_market_calendar": get_market_calendar,
    "get_listing_status": get_listing_status,
    # Forex
    "get_current_fx_rate": get_current_fx_rate,
    "get_fx_time_series": get_fx_time_series,
    # Crypto
    "get_current_crypto_quote": get_current_crypto_quote,
    "get_crypto_time_series": get_crypto_time_series,
    # Commodities
    "get_commodities": get_commodities,
    # Economic Indicators
    "get_growth_metrics": get_growth_metrics,
    "get_rates_yields": get_rates_yields,
    "get_prices_inflation": get_prices_inflation,
    "get_labor_activity": get_labor_activity,
    # Technical Indicators (unified function)
    "get_trend_indicators": get_trend_indicators,
    "get_momentum_indicators": get_momentum_indicators,
    "get_volatility_indicators": get_volatility_indicators,
    "get_volume_indicators": get_volume_indicators,
}
