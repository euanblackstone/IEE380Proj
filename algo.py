from timeit import default_timer as timer
import math
import random
import csv
import json

# write methods for all 25 of the sorting algorithms
# InsertionSort -------------------------------------------------------------
def InsertionSort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key


# MergeSort -----------------------------------------------------------------
def MergeSort(arr, left, right):
    if left < right:

        middle = math.floor((left + right)/2)

        MergeSort(arr, left, middle)
        MergeSort(arr, middle+ 1, right)
        merge(arr, left, middle, right)

def merge(arr, left, middle, right):
    len1 = middle - left + 1
    len2 = right - middle
    
    leftArr = [0] * (len1)
    rightArr = [0] * (len2)

    for i in range(0, len1):
        leftArr[i] = arr[left + i]

    for j in range(0, len2):
        rightArr[j] = arr[middle + 1 + j]

    i = 0
    j = 0
    k = left

    while i < len1 and j < len2:
        if leftArr[i] <= rightArr[j]:
            arr[k] = leftArr[i]
            i += 1
        else:
            arr[k] = rightArr[j]
            j += 1
        k += 1

    while i < len1:
        arr[k] = leftArr[i]
        i += 1
        k += 1

    while j < len2:
        arr[k] = rightArr[j]
        j += 1
        k += 1


# SelectionSort -------------------------------------------------------
def SelectionSort(arr):

    for i in range(len(arr)):
        min = i
        for j in range(i + 1, len(arr)):
            if arr[j] < arr[min]:
                min = j
        (arr[i], arr[min]) = (arr[min], arr[i])


# QuickSort -----------------------------------------------------------
def QuickSort(arr, start, end):
    if start < end:
        pivot = partition(arr, start, end)
        QuickSort(arr, start, pivot - 1)
        QuickSort(arr, pivot + 1, end)

def partition(arr, start, end):
    pivot = arr[end]
    i = start - 1

    for j in range(start, end):
        if arr[j] <= pivot:
            i = i + 1
            (arr[i], arr[j]) = (arr[j], arr[i])

    (arr[i + 1], arr[end]) = (arr[end], arr[i + 1])
    return i + 1


# GnomeSort ------------------------------------------------------------
def GnomeSort(arr):
    pos = 0
    while pos < (len(arr)):
        if pos == 0:
            pos = pos + 1
        if arr[pos] >= arr[pos - 1]:
            pos = pos + 1
        else:
            temp = arr[pos]
            arr[pos] = arr[pos - 1]
            arr[pos - 1] = temp
            pos = pos - 1


# HeapSort ------------------------------------------------------------
def HeapSort(arr):
    length = len(arr)

    for i in range(math.floor(length/2) - 1, -1, -1):
        heapify(arr, length, i)

    for i in range(length - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0)

def heapify(arr, length, i):
    largest = i 
    left = 2 * i + 1 
    right = 2 * i + 2

    if left < length and arr[largest] < arr[left]:
        largest = left

    if right < length and arr[largest] < arr[right]:
        largest = right

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, length, largest)



# BogoSort ------------------------------------------------------------
#pseudocode from wikipedia page for bogosort
def is_sorted(data) -> bool:
    return all(a <= b for a, b in zip(data, data[1:]))

def BogoSort(data):
    while not is_sorted(data):
        random.shuffle(data)


# ShellSort ----------------------------------------------------------
def ShellSort(arr):
    length = len(arr)

    interval = math.floor(length / 2)
    while interval > 0:
        for i in range(interval, length):
            temp = arr[i]
            j = i
            while j >= interval and arr[j - interval] > temp:
                arr[j] = arr[j - interval]
                j -= interval

            arr[j] = temp
        interval = math.floor(interval / 2)


# BubbleSort ----------------------------------------------------------
def BubbleSort(arr):
    for i in range(len(arr)):
        for j in range(0, len(arr) - i - 1):
            if arr[j] > arr[j + 1]:
                (arr[j], arr[j+1]) = (arr[j+1], arr[j])


# CombSort ----------------------------------------------------------------
def CombSort(arr):
    gap = len(arr)
    swaps = True
    while gap > 1 or swaps:
        gap = max(1, int(gap / 1.25))
        swaps = False
        for i in range(len(arr) - gap):
            j = i + gap
            if arr[i] > arr[j]:
                (arr[i], arr[j]) = (arr[j], arr[i])
                swaps = True


# BucketSort ----------------------------------------------------------------
def BucketSort(arr):
    maximum = max(arr)
    size = maximum / len(arr)

    buckets = []
    for i in range(len(arr)):
        buckets.append([])

    for i in range(len(arr)):
        j = int(arr[i] / size)
        if j != len(arr):
            buckets[j].append(arr[i])
        else:
            buckets[len(arr) - 1].append(arr[i])

    for k in range(len(arr)):
        InsertionSort(buckets[k])

    outputArr = []
    for l in range(len(arr)):
        outputArr = outputArr + buckets[l]


# BitonicSort --------------------------------------------------------------
def BitonicSort(arr, low, count, direction):
    if count > 1:
        k = math.floor(count / 2)
        BitonicSort(arr, low, k, 1)
        BitonicSort(arr, low + k, k, 0)
        bitonicMerge(arr, low, count, direction)

def bitonicMerge(arr, low, count, direction):
    if count > 1:
        k = math.floor(count / 2)
        for i in range(low, low + k):
            compareAndSwap(arr, i, i + k, direction)
        bitonicMerge(arr, low, k, direction)
        bitonicMerge(arr, low + k, k, direction)

def compareAndSwap(arr, i, j, direction):
    if (direction == 1 and arr[i] > arr[j]) or (direction == 0 and arr[i] < arr[j]):
        (arr[i], arr[j]) = (arr[j], arr[i])


# TimSort ------------------------------------------------------------------
def TimSort(arr):
    length = len(arr)
    minRun = calcMinRun(length)

    for start in range(0, length, minRun):
        InsertionSort(arr)

    size = minRun
    while size < length:
        for left in range(0, length, 2 * size):
            middle = min(length - 1, left + size - 1)
            right = min((left + 2 * size - 1), (length - 1))

            if middle < right:
                merge(arr, left, middle, right)

        size = 2 * size

def calcMinRun(length):
    r = 0
    while length >= 32:
        r |= length & 1
        length >>= 1
    return length + r


# CycleSort ----------------------------------------------------
def CycleSort(arr):
    writes = 0

    for cycles in range(0, len(arr) - 1):
        item = arr[cycles]

        pos = cycles
        for i in range(cycles + 1, len(arr)):
            if arr[i] < item:
                pos += 1

        if pos == cycles:
            continue

        while item == arr[pos]:
            pos += 1
        (arr[pos], item) = (item, arr[pos])
        writes += 1

        while pos != cycles:
            pos = cycles
            for i in range(cycles + 1, len(arr)):
                if arr[i] < item:
                    pos += 1

            while item == arr[pos]:
                pos += 1
            (arr[pos], item) = (item, arr[pos])
            writes += 1

#PigeonholeSort -------------------------------------------------------------
def PigeonholeSort(arr):
    minimum = min(arr)
    maximum = max(arr)
    size = maximum - minimum + 1
  
    holes = [0] * size
  
    for i in arr:
        holes[i - minimum] += 1
  
    i = 0
    for count in range(size):
        while holes[count] > 0:
            holes[count] -= 1
            arr[i] = count + minimum
            i += 1

#IntroSort -----------------------------------------------------
def IntroSort(arr, start, end):
    depth = 2 * math.floor(math.log2(end - start))
    recurseIntroSort(arr, start, end, depth)

def recurseIntroSort(arr, start, end, depth):
    size = end - start
    if size < 16:
        InsertionSort(arr)
        return
 
    if depth == 0:
        HeapSort(arr)
        return
 
    pivot = MedianOfThree(arr, start, math.floor((start + size)/ 2), end)
    (arr[pivot], arr[end]) = (arr[end], arr[pivot])
    partitionIndex = partition(arr, start, end)
 
    recurseIntroSort(arr, start, partitionIndex - 1, depth - 1)
    recurseIntroSort(arr, partitionIndex + 1, end, depth - 1)
 

def MedianOfThree(arr, a, b, d):
    A = arr[a]
    B = arr[b]
    C = arr[d]
 
    if A <= B and B <= C:
        return b
    if C <= B and B <= A:
        return b
    if B <= A and A <= C:
        return a
    if C <= A and A <= B:
        return a
    if B <= C and C <= A:
        return d
    if A <= C and C <= B:
        return d
 

#OddevenSort -------------------------------------------------------------
def OddevenSort(arr):
    swapped = True
    passes = 1
    while(swapped):
        swapped = False

        for i in range(0, len(arr) - 1, 2):
            if arr[i] > arr[i + 1]:
                (arr[i], arr[i + 1]) = (arr[i+1], arr[i])
                swapped = True

        for i in range(1, len(arr) - 1, 2):
            if arr[i] > arr[i + 1]:
                (arr[i], arr[i + 1]) = (arr[i+1], arr[i])
                swapped = True

        passes += 1

#CocktailshakerSort ---------------------------------------------------------
def CocktailshakerSort(arr):
    swapped = True
    passes = 1
    while(swapped):
        swapped = False

        for i in range(0, len(arr) - 1):
            if arr[i] > arr[i + 1]:
                (arr[i], arr[i + 1]) = (arr[i+1], arr[i])
                swapped = True

            if arr[len(arr) - i - 2] > arr[len(arr) - i - 1]:
                (arr[len(arr) - i - 2], arr[len(arr) - i - 1]) = (arr[len(arr) - i - 1], arr[len(arr) - i - 2])
                swapped = True

        passes += 1


# CountSort -----------------------------------------------------------
def CountSort(arr, isRadix, exponent):
    if not isRadix:
        maximum = int(max(arr))
        minimum = int(min(arr))

        countArr = [0 for i in range(maximum- minimum + 1)]
        outputArr = [0 for i in range(len(arr))]

        for i in range(0, len(arr)):
            countArr[arr[i] - minimum] += 1

        for i in range(1, len(countArr)):
            countArr[i] += countArr[i - 1]

        for i in range(len(arr) - 1, -1, -1):
            outputArr[countArr[arr[i] - minimum] - 1] = arr[i]
            countArr[arr[i] - minimum] -= 1

        for i in range(0, len(arr)):
            arr[i] = outputArr[i]

    else:
        length = len(arr)
        outputArr = [0] * (length)
        countArr = [0] * (10)
    
        for i in range(0, length):
            index = math.floor(arr[i] / exponent)
            countArr[index % 10] += 1
    
        for i in range(1, 10):
            countArr[i] += countArr[i - 1]
    
        i = length - 1
        while i >= 0:
            index = math.floor(arr[i] / exponent)
            outputArr[countArr[index % 10] - 1] = arr[i]
            countArr[index % 10] -= 1
            i -= 1
    
        i = 0
        for i in range(0, len(arr)):
            arr[i] = outputArr[i]


#RadixSort -----------------------------------------------------------------
def RadixSort(arr):
    maximum = max(arr)
 
    exponent = 1
    while maximum / exponent >= 1:
        CountSort(arr, True, exponent)
        exponent *= 10
 

#StrandSort ------------------------------------------------------------------
def StrandSort(arr):
	out = strand(arr)
	while len(arr):
		out = mergeList(out, strand(arr))

def strand(arr):
    i = 0
    strand = [arr.pop(0)]
    while i < len(arr):
        if arr[i] > strand[-1]:
            strand.append(arr.pop(i))
        else:
            i = i + 1
    return strand

def mergeList(arr1, arr2):
	out = []
	while len(arr1) and len(arr2):
		if arr1[0] < arr2[0]:
			out.append(arr1.pop(0))
		else:
			out.append(arr2.pop(0))
	out += arr1
	out += arr2
	return out


#SlowSort ---------------------------------------------------------------------
def SlowSort(arr, start, end):
    if start >= end:
        return

    middle = math.floor((start + end)/2)
    SlowSort(arr, start, middle)
    SlowSort(arr, middle+1, end)
    if arr[end] < arr[middle]:
        (arr[end], arr[middle]) = (arr[middle], arr[end])

    SlowSort(arr, start, end - 1)

#StupidSort --------------------------------------------------------------------
def StupidSort(arr):
    i = 0
    while(i < len(arr) - 1):
        if arr[i] > arr[i+1]:
            (arr[i], arr[i+1]) = (arr[i+1], arr[i])
            i = 0
        else:
            i = i + 1;

#StoogeSort ---------------------------------------------------------------------
def StoogeSort(arr, start, end):
    if start >= end:
        return
  
    if arr[start] > arr[end]:
        (arr[start], arr[end]) = (arr[end], arr[start])
  
    if (end - start + 1) > 2:
        t = (int)((end - start + 1)/3)
  
        StoogeSort(arr, start, (end - t))
  
        StoogeSort(arr, start + t, end)
  
        StoogeSort(arr, start, (end - t))

def runSortingAlgorithms():

    n = 30000
    arr = [random.randint(0, 100_000) for i in range(0, n)]

    with open("algo.json") as file:
        algorithms = json.load(file)


    #Start Sorting Algorithms --------------------------------------------------------
    array = arr.copy()
    start = timer()
    InsertionSort(array)
    algorithms["InsertionSort"] = timer() - start
    print("Insertion Sort done")

    array = arr.copy()
    start = timer()
    MergeSort(array, 0, len(array) - 1)
    algorithms["MergeSort"] = timer() - start
    print("Merge Sort done")

    array = arr.copy()
    start = timer()
    SelectionSort(array)
    algorithms["SelectionSort"] = timer() - start
    print("Selection Sort done")

    array = arr.copy()
    start = timer()
    QuickSort(array, 0, len(array) - 1)
    algorithms["QuickSort"] = timer() - start
    print("Quick Sort done")

    array = arr.copy()
    start = timer()
    GnomeSort(array)
    algorithms["GnomeSort"] = timer() - start
    print("Gnome Sort done")

    array = arr.copy()
    start = timer()
    HeapSort(array)
    algorithms["HeapSort"] = timer() - start
    print("Heap Sort done")

    # array = arr.copy()
    # start = timer()
    # BogoSort(array)
    # algorithms["BogoSort"] = timer() - start
    # print("Bogo Sort done")

    array = arr.copy()
    start = timer()
    ShellSort(array)
    algorithms["ShellSort"] = timer() - start
    print("Shell Sort done")

    array = arr.copy()
    start = timer()
    BubbleSort(array)
    algorithms["BubbleSort"] = timer() - start
    print("Bubble Sort done")

    array = arr.copy()
    start = timer()
    CombSort(array)
    algorithms["CombSort"] = timer() - start
    print("Comb Sort done")

    array = arr.copy()
    start = timer()
    CountSort(array, False, 0)
    algorithms["CountSort"] = timer() - start
    print("Count Sort done")

    array = arr.copy()
    start = timer()
    BucketSort(array)
    algorithms["BucketSort"] = timer() - start
    print("Bucket Sort done")

    array = arr.copy()
    start = timer()
    BitonicSort(array, 0, len(array), 1)
    algorithms["BitonicSort"] = timer() - start
    print("Bitonic Sort done")

    array = arr.copy()
    start = timer()
    TimSort(array)
    algorithms["TimSort"] = timer() - start
    print("Tim Sort done")

    array = arr.copy()
    start = timer()
    CycleSort(array)
    algorithms["CycleSort"] = timer() - start
    print("Cycle Sort done")

    #pigeonhole sort performs so well on my list because it works well on n elements if the range of values in the list is roughly equal to n
    array = arr.copy()
    start = timer()
    PigeonholeSort(array)
    algorithms["PigeonholeSort"] = timer() - start
    print("Pigeonhole Sort done")

    array = arr.copy()
    start = timer()
    IntroSort(array, 0, len(array) - 1)
    algorithms["IntroSort"] = timer() - start
    print("Intro Sort done")

    array = arr.copy()
    start = timer()
    OddevenSort(array)
    algorithms["OddevenSort"] = timer() - start
    print("Odd Even Sort done")

    array = arr.copy()
    start = timer()
    CocktailshakerSort(array)
    algorithms["CocktailshakerSort"] = timer() - start
    print("Cocktail Shaker Sort done")

    array = arr.copy()
    start = timer()
    RadixSort(array)
    algorithms["RadixSort"] = timer() - start
    print("Radix Sort done")

    array = arr.copy()
    start = timer()
    StrandSort(array)
    algorithms["StrandSort"] = timer() - start
    print("Strand Sort done")

    array = arr.copy()
    start = timer()
    StoogeSort(array, 0, len(array) - 1)
    algorithms["StoogeSort"] = timer() - start
    print("Stooge Sort done")

    array = arr.copy()
    start = timer()
    SlowSort(array, 0, len(array)-1)
    algorithms["SlowSort"] = timer() - start
    print("Slow Sort done")

    array = arr.copy()
    start = timer()
    StupidSort(array)
    algorithms["StupidSort"] = timer() - start
    print("Stupid Sort done")

    array = arr.copy()
    start = timer()
    array.sort()
    algorithms["Python's Sort"] = timer() - start
    print("Python's Built-in Sort done")

    #Sorting ALgorithms done ----------------------------------------------------

    with open("list.csv", "w") as csvFile:
        writer = csv.writer(csvFile, lineterminator=",\n")
        for val in arr:
            writer.writerow([val])

    with open("algo.json", "w") as file:
        json.dump(algorithms, file, indent=2)


runSortingAlgorithms()
