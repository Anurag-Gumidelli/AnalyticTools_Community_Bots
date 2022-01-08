import re
import os
from nltk.stem import WordNetLemmatizer
import math
from datetime import datetime
import datetime as dt

# each file has an Analytics object
class Analytics:
    def __init__(self, corpus, lemmatizer):

        self.informativeness = 0    #info measure
        self.relevance = 0          #relevance measure
        self.specific = 0           #specific measure
        self.clarity = 0            #clarity measure 
        self.open_ended_len = 0     #
        self.num_open = 0
        self.exp_closed = 0
        self.response_lens = []
        self.start_t = 0
        self.end_t = 0
        self.q_open = False
        self.corpus = corpus
        self.num_q = 0
        self.num_skip = 0
        self.lemmatizer = lemmatizer
        self.end_msg = 'Thank you for taking the time to complete this survey. Please click on \'END CHAT\' button to start the post-study questionnaire.'
    
    
    def info(self, words):
        for word in words:
            cur = self.lemmatizer.lemmatize(word.strip())
            if cur in self.corpus:
                hr = self.corpus[cur]
                self.informativeness += math.log((1/hr), 2)
    
    
    def process(self,time, sent, msg, spec, rel, clar, op, exp ):
        if sent == 'user':
            if msg.lower().find('skip this topic') != -1:
                self.num_skip += 1
                return

            if spec == '1':
                    self.specific +=1

            if rel == '1':
                self.relevance += 1

            if clar == '1':
                self.clarity +=1 


            if op == '1':
                words = re.sub(r'[^\w\s]', '', msg).lower().split()
                if self.q_open:
                    ans_time = datetime.strptime(time.split('+')[0], "%Y-%m-%d %H:%M:%S.%f")
                    self.response_lens.append( ( len(words), (ans_time - self.start_t)) )
                    self.q_open = False
                else:
                    ch = self.response_lens.pop()
                    self.response_lens.append( ((ch[0] + len(words)), ch[1] ) )

                self.info(words)

            if op == '0':
                if exp == '1':
                    self.exp_closed += 1
        
        else:
            if msg[-1] == '?':
                self.num_q += 1
                self.q_open = True

            elif msg.find('Hello and thank you for connecting!') != -1:
                self.start_t = datetime.strptime(time.split('+')[0], "%Y-%m-%d %H:%M:%S.%f")
            elif msg == self.end_msg:
                self.end_t = datetime.strptime(time.split('+')[0], "%Y-%m-%d %H:%M:%S.%f")
    

    def results(self, fileName) -> str:
        dif = self.end_t - self.start_t
        time = dif.total_seconds()
        res = f'{fileName}\n'
        res += f'Specificity = {self.specific}\nRelavance = {self.relevance}\nClarity = {self.clarity}\n'
        res += f'Questions Asked = {self.num_q}\nQuestions Skipped = {self.num_skip}\nExpanded_closed = {self.exp_closed}\n'
        res += f'Informativeness = {self.informativeness}\nTotal Time = {time}'

        return res



if __name__ == '__main__':
    corpus = dict()

    with open('corpus.txt','r') as f:
        while (entry := f.readline()):
            data = entry.split()
            word = data[0]
            hit_rate = float(data[1])
            corpus[word] = hit_rate



    data = ['data/P1_chat.csv']
    lemmatizer = WordNetLemmatizer()
    for file in data:
        with open(file, 'r') as p:
            file_analytics = Analytics(corpus, lemmatizer)
            while (l:=p.readline()):
    # line style : Timestamp, SentBy, Topic, Message, Specificty, Relavance, Clarity, open_ended, Expanded
                data_array = l.split(',')
                # if len(data_array) != 8:
                #     print('ERROR')
                #     break
                ts = data_array[0].strip()
                sb = data_array[1].strip()
                topic = data_array[2].strip()
                msg = ''.join(data_array[3:-5]).strip()
                spec = data_array[-5].strip()
                rel = data_array[-4].strip()
                clar = data_array[-3].strip()
                op = data_array[-2].strip()
                exp = data_array[-1].strip()
                file_analytics.process(ts, sb, msg, spec, rel, clar, op, exp )

            res = file_analytics.results( (names :=file.split('/')) [1])
            o_file = names[0] + '/res/' + names[1]
            with open(o_file,'w') as o_f:
                o_f.write(res)



