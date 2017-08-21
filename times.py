def subset_sum(numbers, target, partial=[]):
    s = sum(partial)

    # check if the partial sum is equals to target
    if s >= target-1 and s<= target-1: 
        print "sum(%s)=%s" % (partial, target)
    if s > target+1:
        return  # if we reach the number why bother to continue

    for i in range(len(numbers)):
        n = numbers[i]
        remaining = numbers[i+1:]
        subset_sum(remaining, target, partial + [n]) 


if __name__ == "__main__":
    arr = [1.2, 0.5, 2.4,3.54,9.12,8.34,4.12,5.72,7.25,10.67, 3.12, 6.66, 8.13, 10.25, 12.234, 11.61, 2.66, 4.14, 3.3, 5.0]
    subset_sum(arr+arr, 26)
