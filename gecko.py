import requests

def fetch_crypto_prices(ids, vs_currencies):
    """
    Fetch cryptocurrency prices from the CoinGecko API.

    :param ids: List of cryptocurrency IDs (e.g., ["bitcoin", "ethereum"]).
    :param vs_currencies: List of fiat/crypto currencies (e.g., ["usd", "eur"]).
    :return: JSON response with the prices.
    """
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": ",".join(ids),  # Combine IDs into a comma-separated string
        "vs_currencies": ",".join(vs_currencies)  # Combine vs_currencies into a comma-separated string
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

if __name__ == "__main__":
    # Example input: Cryptocurrency IDs and vs_currencies
    crypto_ids = ["bitcoin", "monero", "usd"]
    vs_currencies = ["usd", "btc", "brl"]
    
    # Fetch and print the prices
    prices = fetch_crypto_prices(crypto_ids, vs_currencies)
    if prices:
        print("Cryptocurrency Prices:")
        for crypto, data in prices.items():
            print(f"{crypto.capitalize()}:")
            for currency, price in data.items():
                print(f"  {currency.upper()}: {price}")

