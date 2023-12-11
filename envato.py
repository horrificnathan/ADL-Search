import requests
from bs4 import BeautifulSoup


class EnvatoWeb:
    def __init__(self):
        self.headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Max OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.3'
}
        self.url = 'https://elements.envato.com/sound-effects/'

    def key_words_search_words(self, user_message):
      words = user_message.split()[1:]
      keywords = '%20'.join(words)
      search_words = ' '.join(words)
      return keywords, search_words

    def free_link(self, keywords):
      url = self.url + keywords
      return url
  
    def search(self, keywords):
      response = requests.get(self.url+keywords, headers=self.headers)
      print(f"Request URL: {response.url}")
      content = response.content
      soup = BeautifulSoup(content, 'html.parser')
      result_count = soup.select_one('[data-testid="top-article-visible"] b')
      if result_count:
        first_word = result_count.get_text().split()[0]
        return first_word
      else:
        return None