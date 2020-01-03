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
    a, b = equalizeLength(a['genres'].split("|"), b['genres'].split("|"))
    return jaccard_score(a, b, average='micro')

def getNeighbors(data, movieId, K):
    distances = []
    for i in range(len(data)):
        if (i != movieId):
            dist = ComputeDistance(data.iloc[movieId], data.iloc[i])
            distances.append((data.iloc[i], dist))
    distances.sort(key=operator.itemgetter(1))
    neighbors = []
    for x in range(K):
        neighbors.append(distances[x][0])
    return neighbors

# md = pd.read_csv('./movies.csv')
#
# result = getNeighbors(md, 10, 5)