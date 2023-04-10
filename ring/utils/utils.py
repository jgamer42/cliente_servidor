import hashlib
def get_hash(data:bytes):
    hash:str = hashlib.sha512(data).hexdigest()
    return hash

#Taken / generated with chat-GPT
def binary_search_with_position(arr, x):
    low = 0
    high = len(arr) - 1
    last_comparison = -1

    while low <= high:
        mid = (low + high) // 2
        if arr[mid] < x:
            low = mid + 1
            last_comparison = mid
        elif arr[mid] > x:
            high = mid - 1
            last_comparison = mid
        else:
            return mid, mid

    return last_comparison + 1, high + 1
