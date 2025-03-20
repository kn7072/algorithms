"""
ftreeenwick Tree (Binary Indexed Tree) for Competitive Programming.

https://www.geeksforgeeks.org/fenwick-tree-for-competitive-programming/?ysclid=m8hedridz867385971
https://neerc.ifmo.ru/wiki/index.php?title=%D0%94%D0%B5%D1%80%D0%B5%D0%B2%D0%BE_%D0%A4%D0%B5%D0%BD%D0%B2%D0%B8%D0%BA%D0%B0

Сравнение дерева Фенвика и дерева отрезков

-  Дерево Фенвика занимает в константное значение раз меньше памяти, чем дерево отрезков.
Это следует из того, что дерево Фенвика хранит только значение операции для каких-то элементов,
а дерево отрезков хранит сами элементы и частичные результаты операции на подотрезках,
поэтому оно занимает как минимум в два раза больше памяти.
-  Дерево Фенвика проще в реализации.
-  Операция на отрезке, для которой строится дерево Фенвика, должна быть обратимой, а это значит,
что минимум (как и максимум) на отрезке это дерево считать не может, в отличие от дерева отрезков.
Но если нам требуется найти минимум на префиксе, то дерево Фенвика справится с этой задачей.
Такое дерево Фенвика поддерживает операцию уменьшения элементов массива.
Пересчёт минимума в дереве происходит быстрее,
чем обновление массива минимумов на префиксе.
"""


def sum(idx: int, ftree: list) -> int:
    """ """
    running_sum = 0
    while idx > 0:
        running_sum += ftree[idx]
        right_most_set_bit = idx & -idx
        idx -= right_most_set_bit
    return running_sum


def add(idx, X, ftree: list):
    while idx < len(ftree):
        ftree[idx] += X
        right_most_set_bit = idx & -idx
        idx += right_most_set_bit


def range_query(left_border: int, right_border: int, ftree: list) -> int:
    return sum(right_border, ftree) - sum(left_border - 1, ftree)


def main():
    n = 5

    # 1-based indexing
    arr = [-1e9, 1, 2, 3, 4, 5]
    # Initially, all the values of ftreeenwick tree are 0
    ftree = [0] * (n + 1)

    # Build the ftreeenwick tree
    for i in range(1, n + 1):
        add(i, arr[i], ftree)

    # Query the sum from index 1 to 3
    print(range_query(1, 3, ftree))
    # Query the sum from index 2 to 5
    print(range_query(2, 5, ftree))

    # Update element at index i to X
    i = 3
    X = 7
    # We have passed X - arr[i] to the add method because
    # the add method simply adds a number at a particular index.
    # If we need to update the element, we need to pass
    # the difference between the ith element and X to the add
    # method.
    add(i, X - arr[i], ftree)

    # Query the sum from index 1 to 3
    print(range_query(1, 3, ftree))
    # Query the sum from 2 to 5
    print(range_query(2, 5, ftree))


if __name__ == "__main__":
    main()
