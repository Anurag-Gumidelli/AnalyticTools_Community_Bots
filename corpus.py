import re
import os
from nltk.stem import WordNetLemmatizer

dir1 = 'corpus/coca-samples-text'
dir2 = 'corpus/webtext'
dir3 = 'corpus/wiki'

dirs = [dir1, dir2, dir3]
corpus = dict()
lemmatizer = WordNetLemmatizer()

for dir in dirs:
    for file in os.listdir(dir):
        current = os.path.join(dir, file)
        with open(current, 'r') as f:
            while (l := f.readline()):
                l = re.sub(r'[^\w\s]', '', l)
                words = l.split()
            
                for word in words:
                    if not word.isnumeric():
                        cur = lemmatizer.lemmatize(word.strip().lower())
                    
                        if cur in corpus:
                            corpus[cur] += 1
                        else:
                            corpus[cur] = 1


with open('corpus.txt', 'w') as c:
    for k,v in corpus.items():
        freq = v/3
        c.write(f'{k}   {freq}\n')
