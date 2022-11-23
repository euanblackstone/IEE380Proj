from timeit import default_timer as timer
import math
import random
import csv
import json
import multiprocessing

# Sorting Algorithms --------------------------------------------------------------------------
# InsertionSort -------------------------------------------------------------
def InsertionSort(arr):
    global arrayWrites

    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            arrayWrites += 1
            j -= 1
        arr[j + 1] = key
        arrayWrites += 1


# MergeSort -----------------------------------------------------------------
def MergeSort(arr, left, right):
    if left < right:

        middle = math.floor((left + right)/2)

        MergeSort(arr, left, middle)
        MergeSort(arr, middle+ 1, right)
        merge(arr, left, middle, right)

def merge(arr, left, middle, right):
    global arrayWrites

    len1 = middle - left + 1
    len2 = right - middle
    
    leftArr = [0] * (len1)
    rightArr = [0] * (len2)
    arrayWrites += 2

    for i in range(0, len1):
        leftArr[i] = arr[left + i]
        arrayWrites += 1

    for j in range(0, len2):
        rightArr[j] = arr[middle + 1 + j]
        arrayWrites += 1

    i = 0
    j = 0
    k = left

    while i < len1 and j < len2:
        if leftArr[i] <= rightArr[j]:
            arr[k] = leftArr[i]
            arrayWrites += 1
            i += 1
        else:
            arr[k] = rightArr[j]
            arrayWrites += 1
            j += 1
        k += 1

    while i < len1:
        arr[k] = leftArr[i]
        arrayWrites += 1
        i += 1
        k += 1

    while j < len2:
        arr[k] = rightArr[j]
        arrayWrites += 1
        j += 1
        k += 1


# SelectionSort -------------------------------------------------------
def SelectionSort(arr):
    global arrayWrites

    for i in range(len(arr)):
        min = i
        for j in range(i + 1, len(arr)):
            if arr[j] < arr[min]:
                min = j
        (arr[i], arr[min]) = (arr[min], arr[i])
        arrayWrites += 2


# QuickSort -----------------------------------------------------------
def QuickSort(arr, start, end):
    if start < end:
        pivot = partition(arr, start, end)
        QuickSort(arr, start, pivot - 1)
        QuickSort(arr, pivot + 1, end)

def partition(arr, start, end):
    global arrayWrites

    pivot = arr[end]
    i = start - 1

    for j in range(start, end):
        if arr[j] <= pivot:
            i = i + 1
            (arr[i], arr[j]) = (arr[j], arr[i])
            arrayWrites += 2

    (arr[i + 1], arr[end]) = (arr[end], arr[i + 1])
    arrayWrites += 2
    return i + 1


# GnomeSort ------------------------------------------------------------
def GnomeSort(arr):
    global arrayWrites

    pos = 0
    while pos < (len(arr)):
        if pos == 0:
            pos = pos + 1
        if arr[pos] >= arr[pos - 1]:
            pos = pos + 1
        else:
            (arr[pos], arr[pos-1]) = (arr[pos-1], arr[pos])
            arrayWrites += 2
            pos = pos - 1


# HeapSort ------------------------------------------------------------
def HeapSort(arr):
    global arrayWrites

    length = len(arr)

    for i in range(math.floor(length/2) - 1, -1, -1):
        heapify(arr, length, i)

    for i in range(length - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        arrayWrites += 2
        heapify(arr, i, 0)

def heapify(arr, length, i):
    global arrayWrites

    largest = i 
    left = 2 * i + 1 
    right = 2 * i + 2

    if left < length and arr[largest] < arr[left]:
        largest = left

    if right < length and arr[largest] < arr[right]:
        largest = right

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        arrayWrites += 2
        heapify(arr, length, largest)



# BogoSort ------------------------------------------------------------
#pseudocode from wikipedia page for bogosort
def is_sorted(data) -> bool:
    return all(a <= b for a, b in zip(data, data[1:]))

def BogoSort(data):
    global arrayWrites

    while not is_sorted(data):
        random.shuffle(data)
        arrayWrites += 1


# ShellSort ----------------------------------------------------------
def ShellSort(arr):
    global arrayWrites

    length = len(arr)

    interval = math.floor(length / 2)
    while interval > 0:
        for i in range(interval, length):
            temp = arr[i]
            j = i
            while j >= interval and arr[j - interval] > temp:
                arr[j] = arr[j - interval]
                arrayWrites += 1
                j -= interval

            arr[j] = temp
            arrayWrites += 1
        interval = math.floor(interval / 2)


# BubbleSort ----------------------------------------------------------
def BubbleSort(arr):
    global arrayWrites

    for i in range(len(arr)):
        for j in range(0, len(arr) - i - 1):
            if arr[j] > arr[j + 1]:
                (arr[j], arr[j+1]) = (arr[j+1], arr[j])
                arrayWrites += 2


# CombSort ----------------------------------------------------------------
def CombSort(arr):
    global arrayWrites

    gap = len(arr)
    swaps = True
    while gap > 1 or swaps:
        gap = max(1, int(gap / 1.25))
        swaps = False
        for i in range(len(arr) - gap):
            j = i + gap
            if arr[i] > arr[j]:
                (arr[i], arr[j]) = (arr[j], arr[i])
                arrayWrites += 2
                swaps = True


# BucketSort ----------------------------------------------------------------
def BucketSort(arr):
    global arrayWrites

    maximum = max(arr)
    size = maximum / len(arr)

    buckets = []
    for i in range(len(arr)):
        buckets.append([])
        arrayWrites += 1

    for i in range(len(arr)):
        j = int(arr[i] / size)
        if j != len(arr):
            buckets[j].append(arr[i])
            arrayWrites += 1
        else:
            buckets[len(arr) - 1].append(arr[i])
            arrayWrites += 1

    for k in range(len(arr)):
        InsertionSort(buckets[k])

    outputArr = []
    for l in range(len(arr)):
        outputArr = outputArr + buckets[l]
        arrayWrites += 1


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
    global arrayWrites

    if (direction == 1 and arr[i] > arr[j]) or (direction == 0 and arr[i] < arr[j]):
        (arr[i], arr[j]) = (arr[j], arr[i])
        arrayWrites += 2


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
    global arrayWrites
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
        arrayWrites += 2
        writes += 1

        while pos != cycles:
            pos = cycles
            for i in range(cycles + 1, len(arr)):
                if arr[i] < item:
                    pos += 1

            while item == arr[pos]:
                pos += 1
            (arr[pos], item) = (item, arr[pos])
            arrayWrites += 2
            writes += 1

#PigeonholeSort -------------------------------------------------------------
def PigeonholeSort(arr):
    global arrayWrites

    minimum = min(arr)
    maximum = max(arr)
    size = maximum - minimum + 1
  
    holes = [0] * size
    arrayWrites += 1
  
    for i in arr:
        holes[i - minimum] += 1
        arrayWrites += 1
  
    i = 0
    for count in range(size):
        while holes[count] > 0:
            holes[count] -= 1
            arr[i] = count + minimum
            arrayWrites += 1
            i += 1

#IntroSort -----------------------------------------------------
def IntroSort(arr, start, end):
    depth = 2 * math.floor(math.log2(end - start))
    recurseIntroSort(arr, start, end, depth)

def recurseIntroSort(arr, start, end, depth):
    global arrayWrites

    size = end - start
    if size < 16:
        InsertionSort(arr)
        return
 
    if depth == 0:
        HeapSort(arr)
        return
 
    pivot = MedianOfThree(arr, start, math.floor((start + size)/ 2), end)
    (arr[pivot], arr[end]) = (arr[end], arr[pivot])
    arrayWrites += 2
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
    global arrayWrites

    swapped = True
    passes = 1
    while(swapped):
        swapped = False

        for i in range(0, len(arr) - 1, 2):
            if arr[i] > arr[i + 1]:
                (arr[i], arr[i + 1]) = (arr[i+1], arr[i])
                arrayWrites += 2
                swapped = True

        for i in range(1, len(arr) - 1, 2):
            if arr[i] > arr[i + 1]:
                (arr[i], arr[i + 1]) = (arr[i+1], arr[i])
                arrayWrites += 2
                swapped = True

        passes += 1

#CocktailshakerSort ---------------------------------------------------------
def CocktailshakerSort(arr):
    global arrayWrites

    swapped = True
    passes = 1
    while(swapped):
        swapped = False

        for i in range(0, len(arr) - 1):
            if arr[i] > arr[i + 1]:
                (arr[i], arr[i + 1]) = (arr[i+1], arr[i])
                arrayWrites += 2
                swapped = True

            if arr[len(arr) - i - 2] > arr[len(arr) - i - 1]:
                (arr[len(arr) - i - 2], arr[len(arr) - i - 1]) = (arr[len(arr) - i - 1], arr[len(arr) - i - 2])
                arrayWrites += 2
                swapped = True

        passes += 1


# CountSort -----------------------------------------------------------
def CountSort(arr, isRadix, exponent):
    global arrayWrites

    if not isRadix:
        maximum = int(max(arr))
        minimum = int(min(arr))

        countArr = [0 for i in range(maximum- minimum + 1)]
        outputArr = [0 for i in range(len(arr))]
        arrayWrites += 2

        for i in range(0, len(arr)):
            countArr[arr[i] - minimum] += 1
            arrayWrites += 1

        for i in range(1, len(countArr)):
            countArr[i] += countArr[i - 1]
            arrayWrites += 1

        for i in range(len(arr) - 1, -1, -1):
            outputArr[countArr[arr[i] - minimum] - 1] = arr[i]
            countArr[arr[i] - minimum] -= 1
            arrayWrites += 2

        for i in range(0, len(arr)):
            arr[i] = outputArr[i]
            arrayWrites += 1

    else:
        length = len(arr)
        outputArr = [0] * (length)
        countArr = [0] * (10)
        arrayWrites += 2
    
        for i in range(0, length):
            index = math.floor(arr[i] / exponent)
            countArr[index % 10] += 1
            arrayWrites += 1
    
        for i in range(1, 10):
            countArr[i] += countArr[i - 1]
            arrayWrites += 1
    
        i = length - 1
        while i >= 0:
            index = math.floor(arr[i] / exponent)
            outputArr[countArr[index % 10] - 1] = arr[i]
            countArr[index % 10] -= 1
            arrayWrites += 2
            i -= 1
    
        i = 0
        for i in range(0, len(arr)):
            arr[i] = outputArr[i]
            arrayWrites += 1


#RadixSort -----------------------------------------------------------------
def RadixSort(arr):
    maximum = max(arr)
 
    exponent = 1
    while maximum / exponent >= 1:
        CountSort(arr, True, exponent)
        exponent *= 10
 

#StrandSort ------------------------------------------------------------------
def StrandSort(arr):
    global arrayWrites

    out = strand(arr)
    arrayWrites += 1

    while len(arr):
        out = mergeList(out, strand(arr))
        arrayWrites += 1


def strand(arr):
    global arrayWrites

    i = 0
    strand = [arr.pop(0)]
    arrayWrites += 1
    while i < len(arr):
        if arr[i] > strand[-1]:
            strand.append(arr.pop(i))
            arrayWrites += 1
        else:
            i = i + 1
    return strand

def mergeList(arr1, arr2):
    global arrayWrites

    out = []
    while len(arr1) and len(arr2):
        if arr1[0] < arr2[0]:
            out.append(arr1.pop(0))
            arrayWrites += 1
        else:
            out.append(arr2.pop(0))
            arrayWrites += 1
    out += arr1
    out += arr2
    arrayWrites += 2
    return out



#SlowSort ---------------------------------------------------------------------
def SlowSort(arr, start, end):
    global arrayWrites

    if start >= end:
        return

    middle = math.floor((start + end)/2)
    SlowSort(arr, start, middle)
    SlowSort(arr, middle+1, end)
    if arr[end] < arr[middle]:
        (arr[end], arr[middle]) = (arr[middle], arr[end])
        arrayWrites += 2

    SlowSort(arr, start, end - 1)

#StupidSort --------------------------------------------------------------------
def StupidSort(arr):
    global arrayWrites

    i = 0
    while(i < len(arr) - 1):
        if arr[i] > arr[i+1]:
            (arr[i], arr[i+1]) = (arr[i+1], arr[i])
            arrayWrites += 2
            i = 0
        else:
            i = i + 1;

#StoogeSort ---------------------------------------------------------------------
def StoogeSort(arr, start, end):
    global arrayWrites

    if start >= end:
        return
  
    if arr[start] > arr[end]:
        (arr[start], arr[end]) = (arr[end], arr[start])
        arrayWrites += 2
  
    if (end - start + 1) > 2:
        t = (int)((end - start + 1)/3)
  
        StoogeSort(arr, start, (end - t))
  
        StoogeSort(arr, start + t, end)
  
        StoogeSort(arr, start, (end - t))

# End of Sorting Algorithms ----------------------------------------------------------------------------

def countSortedNumsInArr(arr):
    count = 0
    for i in range(len(arr)):
        if i == 0:
            if arr[i] <= arr[i+1]:
                count += 1
        elif i == len(arr) - 1:
            if arr[i] >= arr[i-1]:
                count += 1
        else:
            if arr[i] <= arr[i+1] and arr[i] >= arr[i-1]:
                count += 1

    return count

def sortElementsInTime(n):
    arr = [random.randint(0, 100_000) for i in range(0, n)]

    p = multiprocessing.Process(target=InsertionSort(arr))
    p.start()

    p.join(10)

    if p.is_alive():
        print("kill sort")
        p.terminate()
        p.join()


def timeSortingAlgorithms(n):
    global arrayWrites

    arr = [random.randint(0, 100_000) for i in range(0, n)]
    arrayWritesList = {}

    with open("algo.json") as file:
        algorithms = json.load(file)

    with open("list.csv", "w") as csvFile:
        writer = csv.writer(csvFile, lineterminator=",\n")
        for val in arr:
            writer.writerow([val])


    #Start Sorting Algorithms --------------------------------------------------------
    array = arr.copy()
    start = timer()
    InsertionSort(array)
    algorithms["InsertionSort"] = timer() - start
    arrayWritesList["InsertionSort"] = arrayWrites
    print("Insertion Sort done. %s array writes occurred." % (arrayWrites))

    array = arr.copy()
    arrayWrites = 0
    start = timer()
    MergeSort(array, 0, len(array) - 1)
    algorithms["MergeSort"] = timer() - start
    arrayWritesList["MergeSort"] = arrayWrites
    print("Merge Sort done. %s array writes occurred." % (arrayWrites))

    array = arr.copy()
    arrayWrites = 0
    start = timer()
    SelectionSort(array)
    algorithms["SelectionSort"] = timer() - start
    arrayWritesList["SelectionSort"] = arrayWrites
    print("Selection Sort done. %s array writes occurred." % (arrayWrites))

    array = arr.copy()
    arrayWrites = 0
    start = timer()
    QuickSort(array, 0, len(array) - 1)
    algorithms["QuickSort"] = timer() - start
    arrayWritesList["QuickSort"] = arrayWrites
    arrayWritesList["QuickSort"] = arrayWrites
    print("Quick Sort done. %s array writes occurred." % (arrayWrites))

    array = arr.copy()
    arrayWrites = 0
    start = timer()
    GnomeSort(array)
    algorithms["GnomeSort"] = timer() - start
    arrayWritesList["GnomeSort"] = arrayWrites
    print("Gnome Sort done. %s array writes occurred." % (arrayWrites))

    array = arr.copy()
    arrayWrites = 0
    start = timer()
    HeapSort(array)
    algorithms["HeapSort"] = timer() - start
    arrayWritesList["HeapSort"] = arrayWrites
    print("Heap Sort done. %s array writes occurred." % (arrayWrites))

    # array = arr.copy()
    arrayWrites = 0
    # start = timer()
    # BogoSort(array)
    # algorithms["BogoSort"] = timer() - start
    arrayWritesList["BogoSort"] = arrayWrites
    print("Bogo Sort done. %s array writes occurred." % (arrayWrites))

    array = arr.copy()
    arrayWrites = 0
    start = timer()
    ShellSort(array)
    algorithms["ShellSort"] = timer() - start
    arrayWritesList["ShellSort"] = arrayWrites
    print("Shell Sort done. %s array writes occurred." % (arrayWrites))

    array = arr.copy()
    arrayWrites = 0
    start = timer()
    BubbleSort(array)
    algorithms["BubbleSort"] = timer() - start
    arrayWritesList["BubbleSort"] = arrayWrites
    print("Bubble Sort done. %s array writes occurred." % (arrayWrites))

    array = arr.copy()
    arrayWrites = 0
    start = timer()
    CombSort(array)
    algorithms["CombSort"] = timer() - start
    arrayWritesList["CombSort"] = arrayWrites
    print("Comb Sort done. %s array writes occurred." % (arrayWrites))

    array = arr.copy()
    arrayWrites = 0
    start = timer()
    CountSort(array, False, 0)
    algorithms["CountSort"] = timer() - start
    arrayWritesList["CountSort"] = arrayWrites
    print("Count Sort done. %s array writes occurred." % (arrayWrites))

    array = arr.copy()
    arrayWrites = 0
    start = timer()
    BucketSort(array)
    algorithms["BucketSort"] = timer() - start
    arrayWritesList["BucketSort"] = arrayWrites
    print("Bucket Sort done. %s array writes occurred." % (arrayWrites))

    array = arr.copy()
    arrayWrites = 0
    start = timer()
    BitonicSort(array, 0, len(array), 1)
    algorithms["BitonicSort"] = timer() - start
    arrayWritesList["BitonicSort"] = arrayWrites
    print("Bitonic Sort done. %s array writes occurred." % (arrayWrites))

    array = arr.copy()
    arrayWrites = 0
    start = timer()
    CycleSort(array)
    algorithms["CycleSort"] = timer() - start
    arrayWritesList["CycleSort"] = arrayWrites
    print("Cycle Sort done. %s array writes occurred." % (arrayWrites))

    array = arr.copy()
    arrayWrites = 0
    start = timer()
    PigeonholeSort(array)
    algorithms["PigeonholeSort"] = timer() - start
    arrayWritesList["PigeonholeSort"] = arrayWrites
    print("Pigeonhole Sort done. %s array writes occurred." % (arrayWrites))

    array = arr.copy()
    arrayWrites = 0
    start = timer()
    IntroSort(array, 0, len(array) - 1)
    algorithms["IntroSort"] = timer() - start
    arrayWritesList["IntroSort"] = arrayWrites
    print("Intro Sort done. %s array writes occurred." % (arrayWrites))

    array = arr.copy()
    arrayWrites = 0
    start = timer()
    OddevenSort(array)
    algorithms["OddevenSort"] = timer() - start
    arrayWritesList["OddevenSort"] = arrayWrites
    print("Odd Even Sort done. %s array writes occurred." % (arrayWrites))

    array = arr.copy()
    arrayWrites = 0
    start = timer()
    CocktailshakerSort(array)
    algorithms["CocktailshakerSort"] = timer() - start
    arrayWritesList["CocktailshakerSort"] = arrayWrites
    print("Cocktail Shaker Sort done. %s array writes occurred." % (arrayWrites))

    array = arr.copy()
    arrayWrites = 0
    start = timer()
    RadixSort(array)
    algorithms["RadixSort"] = timer() - start
    arrayWritesList["RadixSort"] = arrayWrites
    print("Radix Sort done. %s array writes occurred." % (arrayWrites))

    array = arr.copy()
    arrayWrites = 0
    start = timer()
    StrandSort(array)
    algorithms["StrandSort"] = timer() - start
    arrayWritesList["StrandSort"] = arrayWrites
    print("Strand Sort done. %s array writes occurred." % (arrayWrites))

    array = arr.copy()
    arrayWrites = 0
    start = timer()
    StoogeSort(array, 0, len(array) - 1)
    algorithms["StoogeSort"] = timer() - start
    arrayWritesList["StoogeSort"] = arrayWrites
    print("Stooge Sort done. %s array writes occurred." % (arrayWrites))

    # array = arr.copy()
    arrayWrites = 0
    # start = timer()
    # SlowSort(array, 0, len(array)-1)
    # algorithms["SlowSort"] = timer() - start
    arrayWritesList["SlowSort"] = arrayWrites
    print("Slow Sort done. %s array writes occurred." % (arrayWrites))

    array = arr.copy()
    arrayWrites = 0
    start = timer()
    StupidSort(array)
    algorithms["StupidSort"] = timer() - start
    arrayWritesList["StupidSort"] = arrayWrites
    print("Stupid Sort done. %s array writes occurred." % (arrayWrites))

    array = arr.copy()
    arrayWrites = 0
    start = timer()
    TimSort(array)
    algorithms["TimSort"] = timer() - start
    arrayWritesList["TimSort"] = arrayWrites
    print("Tim Sort done. %s array writes occurred." % (arrayWrites))

    #Note
    #Python's built in sort uses tim sort, so im gonna use tim sort's array writes as python's
    #I cant go into the sort function and count the arraywrites since python's sort is in c
    #I think this is a fine compromise
    array = arr.copy()
    start = timer()
    array.sort()
    algorithms["Python's Sort"] = timer() - start
    arrayWritesList["Python's Sort"] = arrayWrites
    print("Python's Built-in Sort done. %s array writes occurred." % (arrayWrites))

    #Sorting ALgorithms done ----------------------------------------------------


    with open("algo.json", "w") as file:
        json.dump(algorithms, file, indent=2)

    with open("accesses.json", "w") as file:
        json.dump(arrayWritesList, file, indent=2)


#sortElementsInTime(100_000)

if __name__ == '__main__':

    # arr = [random.randint(0, 100_000) for i in range(0, 10000)]

    # p = multiprocessing.Process(target=InsertionSort, args=(arr,))
    # p.start()

    # p.join(10)

    # if p.is_alive():
    #     print("kill sort")
    #     p.terminate()
    #     p.join()

    # with open("test.csv", "w") as csvFile:
    #     writer = csv.writer(csvFile, lineterminator=",\n")
    #     for val in arr:
    #         writer.writerow([val])

    # print(countSortedNumsInArr(arr))
    arrayWrites = 0

    timeSortingAlgorithms(1000)
