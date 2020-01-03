import operator
from sklearn.metrics import jaccard_score


def equalizeLength(list1, list2):
    len1 = len(list1)
    len2 = len(list2)

    while len1 != len2:
        if len1 > len2:
            list2.append("")
        else:
            list1.append("")

        len1 = len(list1)
        len2 = len(list2)

    return list1, list2

def ComputeDistance(a, b):
    a, b = equalizeLength(str(a['genres']).split("|"), str(b['genres']).split("|"))
    return jaccard_score(a, b, average='micro')

def getNeighbors(data, movieId, K):
    distances = []
    for i in data['movieId']:
        if (i != str(movieId)):
            dist = ComputeDistance(data.loc[data['movieId'] == str(movieId)], data.loc[data['movieId'] == str(i)])
            distances.append((data.loc[data['movieId'] == str(i)], dist))
    distances.sort(key=operator.itemgetter(1))
    neighbors = []
    for x in range(K):
        neighbors.append(distances[x][0])
    return neighbors