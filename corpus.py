import re

file1 = 'corpus/a.txt'
file2 = 'corpus/b.txt'
file3 = 'corpus/c.txt'
file4 = 'corpus/d.txt'

files = [file1, file2, file3, file4]
corpus = dict()

for file in files:

    with open(file, 'r') as f:
        while (l := f.readline()):
            l = re.sub(r'[^\w\s]', '', l)
            words = l.split()
        
            for word in words:
            
                cur = word.strip().lower()
            
                if cur in corpus:
                    corpus[cur] += 1
                else:
                    corpus[cur] = 1


with open('corpus.txt', 'w') as c:
    for k,v in corpus.items():
        freq = v/len(files)
        c.write(f'{k}   {freq}\n')
