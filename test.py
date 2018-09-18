
def combine_list(left, right):

    if left == []:
        return right
    if right == []:
        return
    if left[0] < right[0]:
        return [left[0]] + combine_list(left[1:], right)
    else:
        return [right[0]] + combine_list(left, right[1:])

print(combine_list([1,2,4],[3,5]))