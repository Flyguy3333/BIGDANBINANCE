import json

# Load buy signals
with open('buy_signals.json', 'r') as f:
    buy_signals = json.load(f)

# Load sell signals
with open('7DECFINALSHORTSELL.json', 'r') as f:
    sell_signals = json.load(f)

# Print buy signals
print("Buy Signals:")
print(json.dumps(buy_signals, indent=4))

# Print sell signals
print("\nSell Signals:")
print(json.dumps(sell_signals, indent=4))
