#Check if two arrays are equal or not using Hashmap
import re


def arrEqual(arr1,arr2):
    if len(arr1) !=len(arr2):
        return False
    arr1.sort()
    arr2.sort()
    for i in range(0,len_arr1): # Linear comparision
        if (arr1[i] != arr2[i]):
            return False
    return True

#Using HASHMAP
def arr_Equal(arr1,arr2):
    if len(arr1) !=len(arr2):
        return False
    count={}
    for i in arr1:
        if i in count:
            count[i]+=1
        else:
            count[i]=1
    for i in arr2:
        if i not in count or count[i]==0:
            return False
        else:
            count[i]=-1
    return True
    
# Driver Code
if __name__=="__main__":
    arr1=[2,3,4,5]
    arr2=[3,4,2,5]

    if (arr_Equal(arr1,arr2)):
        print("Yes")
    else:
        print("No")