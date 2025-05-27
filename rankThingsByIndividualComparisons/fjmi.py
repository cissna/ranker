"""
imported from
https://github.com/PunkChameleon/ford-johnson-merge-insertion-sort/blob/master/fjmi.py

MODIFIED:
1. All element‑vs‑element comparisons now use the **opposite** operator
   ("<" where the original used ">"/">=").
2. Final list is returned in **descending** order by a single in‑place
   `reverse()`.
3. **Duplicate‑element bug fixed** — the `create_s` routine had a 0‑based /
   1‑based indexing mix‑up that re‑inserted one `pend` element twice.  The
   iterator now starts at 2 (because `pend[0]` is already inserted) and the
   loop guards ensure we never address `pend[-1]` or run one step past the
   end.  Edge‑case of input length ≤ 2 is also handled.
"""

import bisect

# ---------------------------------------------------------------------------
#  Helpers
# ---------------------------------------------------------------------------

# Split into pairs
def create_pairs(a):
    split_array = []
    temp_array = []

    for _, value in enumerate(a, start=1):
        if len(temp_array) == 1:
            temp_array.append(value)
            split_array.append(temp_array)
            temp_array = []
        elif len(split_array) * 2 == len(a) - 1:
            split_array.append(value)
        else:
            temp_array.append(value)
    return split_array


# Sort each pair into ascending order (so pair[1] is the larger element)
def sort_each_pair(split_array):
    for pair in split_array:
        if len(pair) == 2 and pair[1] < pair[0]:
            pair[0], pair[1] = pair[1], pair[0]
    return split_array


# ---------------------------------------------------------------------------
#  Recursive pair‑list insertion‑sort (by the **larger** value in each pair)
# ---------------------------------------------------------------------------

def insert(element, A, n):
    if n < 0:
        A[0] = element
    elif not (element[1] < A[n][1]):          # element[1] >= A[n][1]
        if n == len(A) - 1:
            A.append(element)
        else:
            A[n + 1] = element
    else:
        if n == len(A) - 1:
            A.append(A[n])
        else:
            A[n + 1] = A[n]
            insert(element, A, n - 1)


def insertion_sort_pairs(A, n):
    if n < 1:
        return A
    insertion_sort_pairs(A, n - 1)
    insert(A[n], A, n - 1)


# Jacobsthal utilities
def jacobsthal(n):
    if n == 0:
        return 0
    if n == 1:
        return 1
    return jacobsthal(n - 1) + 2 * jacobsthal(n - 2)


def build_jacob_insertion_sequence(array):
    array_len = len(array)
    sequence = []
    j = 3  # first index that matters
    while jacobsthal(j) < array_len - 1:
        sequence.append(jacobsthal(j))
        j += 1
    return sequence


# ---------------------------------------------------------------------------
#  Core sequence builder (FIXED)
# ---------------------------------------------------------------------------

def create_s(sorted_split_array, straggler, print_comparision_estimation=False):
    """Builds the main sequence *S* and inserts the pend elements following the
    Ford–Johnson schedule.  Duplicate‑insertion bug fixed (May 2025)."""

    S, pend = [], []
    comparisons_made = 0

    # Split the sorted pairs into their two working lists
    for pair in sorted_split_array:
        S.append(pair[1])     # larger element of the pair
        pend.append(pair[0])  # smaller element

    # Edge case: fewer than two pairs – nothing to pend‑insert
    if not pend:
        if straggler is not False:
            S.insert(bisect.bisect(S, straggler), straggler)
        return S

    # Insert the very first pend element (index 1 in the 1‑based paper spec)
    S.insert(0, pend[0])

    # ---------------------------------------------------------------------
    # Iterator starts at **2** because pend[1] is already in S.
    # ---------------------------------------------------------------------
    iterator = 2
    index_sequence = {1}
    last = None
    jacob_sequence = build_jacob_insertion_sequence(pend)

    while iterator <= len(pend):
        # Prefer the next Jacobsthal index when allowed
        if jacob_sequence and last != "jacob":
            idx = jacob_sequence.pop(0)
            if idx in index_sequence:
                continue  # should not happen but be safe
            item = pend[idx - 1]
            index_sequence.add(idx)
            last = "jacob"
        else:
            if iterator in index_sequence:
                iterator += 1
                continue
            item = pend[iterator - 1]
            index_sequence.add(iterator)
            last = "not‑jacob"
            iterator += 1

        insertion_point = bisect.bisect(S, item, 0, len(S))
        S.insert(insertion_point, item)
        comparisons_made += 2

    # Straggler (odd‑length input) – binary‑insert into the whole list
    if straggler is not False:
        insertion_point = bisect.bisect(S, straggler, 0, len(S))
        S.insert(insertion_point, straggler)
        comparisons_made += 2

    if print_comparision_estimation:
        print("Approximate Comparisons Made:")
        print(comparisons_made)

    return S


# ---------------------------------------------------------------------------
#  Public API – merge‑insertion sort (descending)
# ---------------------------------------------------------------------------

def merge_insertion_sort(A):
    # print("Starting Array:")
    # print(A)

    # Handle odd length by detaching the final element (straggler)
    has_straggler = len(A) % 2 != 0
    straggler = A.pop() if has_straggler else False

    # Phase 1 – pair splitting & per‑pair ordering
    split_array = create_pairs(A)
    sorted_split_array = sort_each_pair(split_array)

    # Phase 2 – recursively sort the pairs by their larger element
    insertion_sort_pairs(sorted_split_array, len(sorted_split_array) - 1)

    # Phase 3 – build the main sequence and pend‑insert the rest
    S = create_s(sorted_split_array, straggler, print_comparision_estimation=True)

    # Phase 4 – produce descending order as requested
    S.reverse()

    # print("Sorted Array (descending):")
    # print(S)
    return S
