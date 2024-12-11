import json

# Load Buy Signals
with open('buy_signals.json', 'r') as buy_file:
    buy_signals = json.load(buy_file)

# Load Sell Signals
with open('7DECFINALSHORTSELL.json', 'r') as sell_file:
    sell_signals = json.load(sell_file)

# Example: Parse and display all indicators
print("Buy Indicators:")
for indicator in buy_signals['short_term_buy_indicators']:
    print(f"Name: {indicator['name']}")
    print(f"Formula: {indicator['formula']}")
    print(f"Buy Signal: {indicator['buy_signal']}")
    print(f"Notes: {indicator['notes']}\n")

print("\nSell Indicators:")
for indicator in sell_signals:
    print(f"Name: {indicator['name']}")
    print(f"Formula: {indicator['formula']}")
    print(f"Sell Signal: {indicator['sell_signal']}")
    print(f"Notes: {indicator['notes']}\n")

# Add logic for trading decisions
def make_trade_decision(price, indicator_data, signal_type):
    for indicator in indicator_data:
        if signal_type == "buy" and eval(indicator['buy_signal']):
            print(f"Buy Signal Detected: {indicator['name']}")
        elif signal_type == "sell" and eval(indicator['sell_signal']):
            print(f"Sell Signal Detected: {indicator['name']}")

# Example usage (replace with real-time price data)
current_price = 100  # Replace with real-time price feed
make_trade_decision(current_price, buy_signals['short_term_buy_indicators'], "buy")
make_trade_decision(current_price, sell_signals, "sell")
