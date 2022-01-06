data = []

for file in data:
    with open(file, 'r') as p:
        p.readline()
        while (l:=p.readline()):
# line style : Timestamp, SentBy, Topic, Message, Specificty, Relavance, Clarity, open_ended, Expanded
            data_array = l.split(',')
            ts = l[0].strip()
            sb = l[1].strip()
            topic = l[2].strip()
            msg = l[3].strip()
            specificity = l[4].strip()
            relevance = l[5].strip()
            clarity = l[6].strip()
            op = l[7].strip()
            expand = l[8].strip()



