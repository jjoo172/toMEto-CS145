import utils
import json
import tqdm
from collections import defaultdict
 
def distance(a, b):
    m = len(a) + 1
    n = len(b) + 1
    d = [[0 for i in xrange(n)] for j in xrange(m)]
    for i in range(1, m):
    	d[i][0] = i
    for j in range(1, n):
    	d[0][j] = j


    for j in range(1, n):
    	for i in range(1, m):
    		cost = 0
    		if a[i - 1] != b[j - 1]:
    			cost = 1
    		d[i][j] = min(min(d[i-1][j] + 1, d[i][j-1] + 1), d[i-1][j-1] + cost)
    return d[m-1][n-1]




if __name__ == '__main__':
	top = utils.gettop()
	mat = defaultdict(lambda: defaultdict(int))
	for a in tqdm.tqdm(top):
		for b in top:
			mat[a][b] = distance(a, b)

	with open('edit_dist.txt', 'w') as outfile:
		json.dump(mat, outfile)



