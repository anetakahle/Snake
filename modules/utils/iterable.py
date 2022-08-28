def avg(seq):
    return sum(seq) / len(seq)

def indexOf(list : list, value : object):
    return list.index(value) if value in list else None