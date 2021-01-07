from mitsuku import PandoraBot
import random
bot = PandoraBot(user_id=random.randint(1,1e7))
inputText = "hello"
outputText = bot.query(inputText)
print(outputText)