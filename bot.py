import telebot, logging
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

logging.basicConfig(level=logging.INFO)

bot = telebot.TeleBot('Telegram API Token')

def clean_string(r):
  r = r.lower()
  r = [c for c in r if c in abc]
  return ''.join(r)

abc = ' 1234567890-йцукенгшщзхъфывапролджэячсмитьбюёqwertyuiopasdfghjklzxcvbnm!@#$%^&*()_+-=,./?\'\\|'

def update():
  with open('dialogs.txt', encoding='utf-8') as f:
    content = f.read()
  
  blocks = content.split('\n')
  dataset = []
  
  for block in blocks:
    replicas = block.split('\\')[:2]
    if len(replicas) == 2:
      pair = [clean_string(replicas[0]), clean_string(replicas[1])]
      if pair[0] and pair[1]:
        dataset.append(pair)
  
  x_text = []
  y = []
  
  for question, answer in dataset[:10000]:
    x_text.append(question)
    y += [answer]
  
  global vectorizer
  vectorizer = CountVectorizer()
  x = vectorizer.fit_transform(x_text)
  
  global clf
  clf = LogisticRegression()
  clf.fit(x, y)

update()

def get_generative_replica(text):
  text_vector = vectorizer.transform([text]).toarray()[0]
  question = clf.predict([text_vector])[0]
  return question

@bot.message_handler(commands=['start'])
def start_message(message):
	bot.send_message(message.chat.id, 'приветствую!')

question = ''

@bot.message_handler(content_types=['text'])
def get_message(message):
  command = message.text.lower()
  if command == 'не так':
    bot.send_message(message.from_user.id, 'тогда как?')
    bot.register_next_step_handler(message, wrong)
  else:
    global question
    question = command
    reply = get_generative_replica(command)
    bot.send_message(message.from_user.id, reply)

def wrong(message):
  a = f'{question}\{message.text.lower()} \n'
  with open('dialogs.txt', 'a', encoding='utf-8') as f:
    f.write(a)
  bot.send_message(message.from_user.id, 'готово! спасибо за поправку :)')
  update()

bot.polling(none_stop=True)
