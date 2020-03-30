from itertools import combinations, permutations
 
if __name__=='__main__':
    a = range(20)
    count = 0
    # for i in range(1,len(a)): #子集
    for each in combinations(a,4):
        count+=1
        print(count)
            