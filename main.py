import requests
from flask import Flask, render_template
from googletrans import Translator


app: Flask = Flask(__name__)
translator: Translator = Translator()


@app.route('/', methods=['GET', 'POST'])
def get_quote() -> str:
    quote_url: str = 'https://api.quotable.io/random'
    response: requests = requests.get(url=quote_url, verify=False)

    if response.status_code == 200:
        quote_data: dict[str: str] = response.json()
        quote_text: str = quote_data.get('content', 'No quote found')
        author: str = quote_data.get('author', 'Unknown')

        trans_text: str = translator.translate(quote_text, dest='ru').text
        trans_author: str = translator.translate(author, dest='ru').text

    else:
        trans_text: str = 'Ошибка при извлечении цитаты'
        trans_author: str = ''

    return render_template('index.html', quote=trans_text, author=trans_author)


if __name__ == "__main__":
    app.run(debug=True)