def countTransmitters(arr, n, k):
    if n <= 0 or k <= 0:
        raise Exception ("Incorrect source data")
    arr.sort()

    if arr[0] <= 0:
        raise Exception ("Incorrect source data")

    count = 0
    i = 0
    while(i < n):
        count += 1
        coverage = arr[i] + k
        while (i < n and arr[i] <= coverage):
            i += 1
        coverage = arr[i-1] + k
        while (i < n and arr[i] <= coverage):
            i += 1
    return count