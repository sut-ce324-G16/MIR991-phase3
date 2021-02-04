import json
from collections import Counter

import numpy as np
from fast_pagerank import pagerank
from scipy import sparse


def rank():
    file1 = open('Crawler/result.txt', 'r')
    lines = file1.readlines()
    list_r = []
    dict_id = {}
    num_id = 0
    for line in lines:
        json_data = json.loads(line)
        if int(json_data['id']) not in dict_id:
            dict_id[int(json_data['id'])] = num_id
            num_id += 1
        for r in json_data['references']:
            r = r.replace("https://academic.microsoft.com/paper/", "")
            if int(r) not in dict_id:
                dict_id[int(r)] = num_id
                num_id += 1
            list_r.append([dict_id[int(json_data['id'])], dict_id[int(r)]])

    weights = np.array([1 for _ in range(len(list_r))])
    list_r = np.array(list_r)
    G = sparse.csr_matrix((weights, (list_r[:, 0], list_r[:, 1])), shape=(num_id, num_id))
    alpha = float(input("Enter alpha for page rank:"))
    pr = pagerank(G, p=alpha)
    for i, id in enumerate(dict_id.keys()):
        dict_id[id] = pr[i]

    k = Counter(dict_id)
    high = k.most_common(10)
    print("Ids with 10 highest pageranks:")
    for i in high:
        print(i[0], " :", i[1], " ")
