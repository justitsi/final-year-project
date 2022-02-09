# helper function to print paths in readable format
def printTree(tree):
    string1 = ""
    string2 = ""

    for element in tree['nodes']:
        string1 += str(element['id']) + " "
    for element in tree['nodes']:
        string2 += str(element['groupID']) + " "

    print(string1)
    print(string2)
    print(tree['cost'])


# helper function to remove elements from arrays without index
def removeElementFromArray(arr, el):
    arr_copy = arr.copy()

    for i in range(0, len(arr)):
        if arr[i] == el:
            arr_copy.pop(i)
            break

    return arr_copy


# helper function to remove elements from arrays with index
def removeIndexFromArray(arr, index):
    arr_copy = arr.copy()
    arr_copy.pop(index)
    return arr_copy
