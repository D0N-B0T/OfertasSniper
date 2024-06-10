##  Solotodo Price Bot

This script is a Telegram bot that monitors product prices on Solotodo.cl and sends notifications when a price drops. 

**Features:**

* **Price Monitoring:** Continuously checks the prices of products specified in `libs/listaProductos.py` for price drops.
* **Telegram Notifications:** Sends notifications to a designated Telegram chat when a price drops.
* **Database Management:** Stores product names and prices in a SQLite database (`items.db`) for comparison.
* **Price History:**  Keeps track of past prices for each product, allowing for the calculation of price discounts.
* **Automatic Restart:**  Restarts the bot in case of unexpected errors or interruptions.

**Dependencies:**

* `telebot`
* `beautifulsoup4`
* `sqlite3`
* `requests`
* `time`
* `os`
* `sys`
* `retrying`
* `pyshorteners`

**Installation:**

1. Create a new Telegram bot using the BotFather (@BotFather).
2. Obtain the bot token and save it in `libs/secret.py`.
3. Install the required Python libraries: `pip install telebot beautifulsoup4 requests retrying pyshorteners`
4. Create a new Telegram group and add the bot to the group.
5. Add the group ID to `libs/secret.py`.
6. Run the script.

**Configuration:**

* **`libs/listaProductos.py`:**  Contains a list of product URLs to monitor.
* **`libs/secret.py`:** Contains the Telegram bot token and group ID.

**How to Use:**

1. Add the desired product URLs to `libs/listaProductos.py`.
2. Run the script.
3. The bot will start monitoring the prices of the products.
4. When a price drops, the bot will send a notification to the Telegram group.

**Important:**

* The `publicAPI` function is used to fetch product information from Solotodo's public API. 
* The `getItems` function scrapes product prices from the Solotodo website.
* The `comparaDB` function compares current prices with previous prices stored in the database and sends notifications accordingly.

**Disclaimer:**

This script is provided for educational purposes only. It is recommended to consult with Solotodo's Terms of Service before using this script. The author is not responsible for any misuse or damage caused by this script. 
