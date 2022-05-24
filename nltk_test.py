import nltk
import random
from nltk import pos_tag, word_tokenize
from text_generator import TextGenerator
from text_generator import BAD_SYM

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
        self.__dict_text_role = {}
        self.__dict_text = {}
        self.add_all_text()

    def add_to_dict(self, sentense:str):

        template = []
        self.__dict_text = super().add_to_dict(sentense)
        for tag in pos_tag(word_tokenize(sentense), lang='rus'):
            words = self.__dict_text_role.get(tag[1], list())
            words.append(tag[0])
            for s in BAD_SYM:
                words[-1] = words[-1].replace(s, '')
            self.__dict_text_role.update({tag[1]:words})
            template.append(tag[1])
        self.template.append(template)

    def add_all_text(self):
        self.text = self.text.replace('.','.\n')
        if '!' in self.text:
            self.text = self.text.replace('!', '!\n')
        if '?' in self.text:
            self.text = self.text.replace('?', '?\n')
        for sentense in self.text.split('\n'):
            if sentense!='':
                self.add_to_dict(sentense)
        print(self.__dict_text)
        print(self.__dict_text_role)
        print(self.template)


    def check_if_template(self, temp):
        if len(temp)>2:
            temp = temp[-3:-1]
        for template in self.template:
            t = tuple(temp)
            t2 =  tuple(template)
            if any(t == t2[i:len(t) + i] for i in range(len(t2) - len(t) + 1)):
                return True
        return False



    def generate_sentense(self):
        words  = []
        word = random.choice(self.__dict_text.get("$START$"))
        words.append(word)
        st_past = word
        i = 0
        #while word not in ['end', '.', '!', '?', 'END']:
            # if self.__dict_text.get(words[-1]) is None:
            #     st_past+='.'
            #     break
            # word = random.choice(self.__dict_text.get(words[-1]))
            # st_past += ' ' + word
            # template = []
            # for _, tag in pos_tag(word_tokenize(st_past), lang='rus'):
            #     template.append(tag)
            # if self.check_if_template(template) == False:
            #     i+=1
            #     if i == 10:
            #         break
            #     pass
            # else:
            #     i = 0
            #     if word!='end' and word!='END':
            #         words.append(word)


        st = ' '.join(words)
        st = st[0].upper() + st[1:].lower()
        print(st)

    def generate_text(self):
        for t in range(len(self.template)):
            self.generate_sentense()

tg = TextGeneratorNltk(path="data/горфэнт.txt")
tg.generate_text()
