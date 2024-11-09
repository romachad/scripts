import requests
import json

BASE_URL = "https://api.binance.com"
FILE_PATH = "/home/coret/prices.json"
OUTPUT_FILE_PATH = "/home/coret/price_changes.txt"

# Function to fetch all prices from Binance
def fetch_all_prices():
    endpoint = f"{BASE_URL}/api/v3/ticker/price"
    
    try:
        response = requests.get(endpoint)
        response.raise_for_status()
        return response.json()  # Return all ticker data as JSON
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from Binance: {e}")
        return None

# Function to filter specific symbols and display their prices
def filter_prices(symbols, all_prices):
    if not all_prices:
        print("No data available to filter.")
        return

    for ticker in all_prices:
        if ticker["symbol"] in symbols:
            print(f"The current price of {ticker['symbol']} is: {ticker['price']}")

# Function to read old prices from a file
def read_old_prices():
    try:
        with open(FILE_PATH, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}  # If the file does not exist, return an empty dictionary
    except json.JSONDecodeError:
        print("Error reading JSON from the file.")
        return {}

# Function to store new prices in a file and compare with old prices
def store_prices_in_file(symbols, all_prices):
    if not all_prices:
        print("No data available to store.")
        return

    old_prices = read_old_prices()
    new_prices = {}

    for ticker in all_prices:
        symbol = ticker["symbol"]
        if symbol in symbols:
            new_price = float(ticker["price"])
            new_prices[symbol] = new_price

            # Compare with old price if available
            old_price = old_prices.get(symbol)
            #if old_price:
            #    if new_price > old_price:
            #        print(f"The current price of {symbol} is: {new_price} ↑ (increased)")  # Green arrow upwards
            #    elif new_price < old_price:
            #        print(f"The current price of {symbol} is: {new_price} ↓ (decreased)")  # Red arrow downwards
            #    else:
            #        print(f"The current price of {symbol} is: {new_price} (no change)")
            #else:
            #    print(f"The current price of {symbol} is: {new_price} (new data)")

    # Write the new prices to the file
    with open(FILE_PATH, "w") as file:
        json.dump(new_prices, file)

    return old_prices, new_prices

# Function to display prices in a single line with arrow indications and save to a file
def display_prices_inline(symbols, old_prices, new_prices):
    if not new_prices:
        print("No data available to display.")
        return

    output = []
    custom_display = {
        "BTCUSDT": "BTC: ${}",
        "BTCBRL": "BRL: R${}"
    }

    for symbol in symbols:
        new_price = new_prices.get(symbol)
        old_price = old_prices.get(symbol)

        if new_price is not None:
            if symbol in custom_display:
                display_text = custom_display[symbol].format(new_price)
            else:
                display_text = f"{symbol}: {new_price}"

            if old_price:
                if new_price > old_price:
                    #output.append(display_text + " ⬆  ")  # Upwards arrow emoji
                    output.append(display_text + " UP  ")  # Upwards arrow emoji
                elif new_price < old_price:
                    #output.append(display_text + " ⬇  ")  # Downwards arrow emoji
                    output.append(display_text + " DW  ")  # Downwards arrow emoji
                else:
                    output.append(display_text)
            else:
                output.append(display_text)

    # Write the output to a file
    with open(OUTPUT_FILE_PATH, "w") as file:
        file.write(" ".join(output))

# Example usage
if __name__ == "__main__":
    symbols_to_check = ["BTCUSDT", "BTCBRL"]

    # Fetch all prices
    all_prices = fetch_all_prices()

    # Filter and show desired symbols
    # filter_prices(symbols_to_check, all_prices)

    # Store new prices in a file and compare with old prices
    old_prices, new_prices = store_prices_in_file(symbols_to_check, all_prices)

    # Display prices in a single line with arrow indications and save to a file
    display_prices_inline(symbols_to_check, old_prices, new_prices)
