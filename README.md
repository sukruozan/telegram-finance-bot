# telegram-finance-bot @TR_Finance_Bot
This small nerd project is a finance bot which gives currency exchange rates and  uses 1Forge's API together with Telegram Bot API. For telegram bot requests I used [this repo](https://github.com/sukruozan/python-telegram-tutorial). I also used [this repo](https://github.com/1forge/python-forex-quotes).

Once the bot script is started it listens to the messages sent directly to her or the messages written in the groups the bot were added previuosly.

It simply checks the messages whether they contain currency symbols like EURTRY, USDEUR etc. bundles them and make a 1forge request. Then writes back the response to the corresponding chat.


