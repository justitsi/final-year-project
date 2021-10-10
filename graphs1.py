import time
start = time.time()

sample = [
    {
        "id": 0,
        "pairsWith": [1]
    },
    {
        "id": 1,
        "pairsWith": [0]
    },
    {
        "id": 2,
        "pairsWith": [0]
    },
    {
        "id": 3,
        "pairsWith": [2]
    },
    {
        "id": 4,
        "pairsWith": [3]
    },
    {
        "id": 5,
        "pairsWith": [8]
    },
    {
        "id": 6,
        "pairsWith": [5]
    },
    {
        "id": 7,
        "pairsWith": [9]
    },
    {
        "id": 8,
        "pairsWith": [7]
    },
    {
        "id": 9,
        "pairsWith": [3]
    }
]


def generateTree(currentElement, elements, totalScore):
    # if there's items in arr call generateTree function
    # print("Startig iteration for", currentElement, elements, totalScore)
    if (len(elements) > 0):
        results = []
        for element in elements:
            elements_copy = elements.copy()
            # print(elements_copy, element)
            result = generateTree(element, removeElementFromArray(
                elements_copy, element), (totalScore+getCompatibilityScore(element, currentElement)))
            # print(result)
            results.append(result)

        highestScoreIndex = 0
        for i in range(0, len(results)):
            if (results[i]['score'] > results[highestScoreIndex]['score']):
                highestScoreIndex = i

        results[highestScoreIndex]["children"].append(currentElement)
        return results[highestScoreIndex]

    # if array has only one item then it's a leaf, return score and element
    else:
        return ({
            "children": [currentElement],
            "score": totalScore
        })


def getCompatibilityScore(el1, el2):
    score = 0
    for potential in el1["pairsWith"]:
        if potential == el2['id']:
            score += 1

    for potential in el2["pairsWith"]:
        if potential == el1['id']:
            score += 1

    return score


def removeElementFromArray(arr, el):
    arr_copy = arr.copy()

    for i in range(0, len(arr)):
        if arr[i]['id'] == el['id']:
            arr_copy.pop(i)
            break

    return arr_copy


result = generateTree(sample[0], removeElementFromArray(sample, sample[0]), 0)
result['children'].reverse()
print(result)


# profiling/ calculate execution time of program
end = time.time()
print(f"Runtime of the program is {end - start}")
