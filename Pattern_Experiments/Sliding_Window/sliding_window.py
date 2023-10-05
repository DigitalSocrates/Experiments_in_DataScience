""" 
Experiment with sliding window 

Example 1:
    find the largest sum in arr over K elements
"""
# imports


def find_avg_of_subarrays (arr: [], K: int):
    ''' brute force approach 
    
        time complexity O(N*K) approaching n^2
        space complexity O(N)
    '''
    results = []
    for i in range(len(arr) - K + 1):
        total_sum = sum(arr[i:i + K])
        avg = total_sum / K
        results.append(avg)
    return results

if __name__ == "__main__":
    # Example usage
    input_arr = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    subarray_length = 3
    averages = find_avg_of_subarrays(input_arr, subarray_length)
    print(f'Averages of subarrays: {averages}')
