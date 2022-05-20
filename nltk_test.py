import nltk
import random
from nltk import pos_tag, word_tokenize
from text_generator import TextGenerator


path_file = "data/Кафка.txt"
# with open(path_file, mode='r', encoding='utf-8') as fl:
#     text = fl.read()
#
# for sentense in text.split('.'):
#     print(pos_tag(word_tokenize(sentense),lang='rus'))

class TextGeneratorNltk(TextGenerator):

    def __init__(self, path=None, text="Sample Text"):
        super().__init__(path,text)
        self.template = []
        self.__dict_text = {}
        self.add_all_text()
        #

    def add_to_dict(self, sentense:str):

        template = []
        for tag in pos_tag(word_tokenize(sentense), lang='rus'):
            words = self.__dict_text.get(tag[1], list())
            words.append(tag[0])
            self.__dict_text.update({tag[1]:words})
            template.append(tag[1])
        self.template.append(template)


    def generate_sentense(self):
        template = random.choice(self.template)
        st = ""
        for temp in template:
            word = random.choice(self.__dict_text.get(temp))
            st += word + ' '
        st += '.'
        st = st[0].upper() + st[1:].lower()
        print(st)

    def generate_text(self):
        for t in range(len(self.template)):
            self.generate_sentense()

tg = TextGeneratorNltk(path=path_file)
tg.generate_text()
