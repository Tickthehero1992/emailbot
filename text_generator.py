import random

path_to_file = "data/горфэнт.txt"

BAD_SYM = ['\n', '\r', '\t', '\ufeff', '(', ')' ]
class TextGenerator:

    def __init__(self, path=None, text="Sample text"):
        if path is not None:
            with open(path, mode='r', encoding='utf-8') as fl:
                self.__text = fl.read()
        else:
            self.__text = text
        self.__dict_text = dict()

    def __call__(self, *args, **kwargs):
        return self.__text

    def __str__(self):
        return self.__text

    def add_to_dict(self, sentense:str):
        for sym in BAD_SYM:
            sentense = sentense.replace(sym, '')
        if ',' in sentense:
            sentense = sentense.replace(',',' , ')
        if sentense.split(' ') != []:
            word_list = ["$START$"]+sentense.split(' ') + ["END"]

        for word in word_list:
            if word == '':
                word_list.remove(word)

        for i in range(len(word_list)-1):
            list_next = self.__dict_text.get(word_list[i], list())
            list_next.append(word_list[i+1])
            self.__dict_text.update({word_list[i]:list_next})


    def add_all_text(self):
        sentense_list = self.__text.split('.')
        for sentense in sentense_list:
            self.add_to_dict(sentense)

    def generate_sentense(self):
        st = ""
        word = random.choice(list(self.__dict_text.get("$START$")))
        while word == "END":
            word = random.choice(list(self.__dict_text.get("$START$")))
        if len(word) >1:
            st = word[0].upper() + word[1:]
        else:
            st = word.upper()
        while word not in ["end", "END"]:
            word = random.choice(self.__dict_text.get(word))
            if word in ["end", "END"]:
                st += '. '
            else:
                st += ' ' + word

        return st

    def generate_text(self):
        text = ""
        j = 0
        for i in range(len(self.__dict_text["$START$"])):
            text += self.generate_sentense()
            j += 1
            if j % 5 == 0 :
                text += '\n'
        return text

tg = TextGenerator(path="data/Кафка.txt")
tg.add_all_text()
text = tg.generate_text()
print(text)

#
# with open("data/file.txt", mode='w', encoding='utf-8') as fl:
#     fl.write(text)