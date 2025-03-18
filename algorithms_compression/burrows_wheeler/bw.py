def suffix_array(text: str) -> map[int]:
    """Given T return suffix array SA(T).

    We use Python’s sorted
    function here for simplicity, but we can do better.
    """
    # Empty suffix '' plays role of $.
    satups = sorted([(text[i:], i) for i in range(0, len(text) + 1)])
    # Extract and return just the offsets
    return map(lambda x: x[1], satups)


def bwt(text: str) -> str:
    """Given text, returns BWT(text), by way of the suffix array."""
    bw = []
    for si in suffix_array(text):
        if si == 0:
            bw.append("$")
        else:
            bw.append(text[si - 1])
    return "".join(bw)  # return string-ized version of list bw


def rank_bwt(bw: str) -> tuple[list, dict]:
    """Given BWT string bw, returns a parallel list of B-ranks.

    Also returns tots, a mapping from characters to # times the
    character appears in BWT.
    """
    tots = dict()
    ranks = []
    for char_i in bw:
        if char_i not in tots:
            tots[char_i] = 0
        ranks.append(tots[char_i])
        tots[char_i] += 1
    return ranks, tots


def first_col(tots: dict) -> dict:
    """Return a map from characters to the range of cells in the firsta \
    column containing the character."""
    first = {}
    totc = 0
    for char_i, count in dict(sorted(tots.items())).items():
        first[char_i] = (totc, totc + count)
        totc += count
    return first


def reverse_bwt(bw: str) -> str:
    """Make T from BWT(T)."""
    ranks, tots = rank_bwt(bw)
    first = first_col(tots)
    row_i = 0
    ver_bwt = "$"
    while bw[row_i] != "$":
        char_i = bw[row_i]
        ver_bwt = char_i + ver_bwt
        row_i = first[char_i][0] + ranks[row_i]
    return ver_bwt


def rank_all_bwt(bw: str) -> tuple[dict, dict]:
    """Given BWT string bw, returns a map of lists.

    Keys are characters and lists are cumulative # of occurrences up to and
    including the row.
    """
    tots = {}
    rank_all = {}
    for char_i in bw:
        if char_i not in tots:
            tots[char_i] = 0
            rank_all[char_i] = []
    for char_i in bw:
        tots[char_i] += 1
        for char_i in tots:
            rank_all[char_i].append(tots[char_i])
    return rank_all, tots


def count_matches(bw: str, ptr: str) -> int:
    """Given BWT(T) and a pattern string ptr, return the number of times p occurs in T."""
    ranks, tots = rank_bwt(bw)
    first = first_col(tots)
    left_border, right_border = first[ptr[-1]]
    i = len(ptr) - 2
    while i >= 0 and right_border > left_border:
        char_i = ptr[i]
        # scan from left_border, looking for occurrences of char_i
        j = left_border
        while j < right_border:
            if bw[j] == char_i:
                left_border = first[char_i][0] + ranks[j]
                break
        j += 1
        if j == right_border:
            left_border = right_border
            break  # no occurrences -> no match
        right_border -= 1
        while bw[right_border] != char_i:
            right_border -= 1
        right_border = first[char_i][0] + ranks[right_border] + 1
        i -= 1
    return right_border - left_border


def count_matches_2(bw: str, ptr: str) -> int:
    """Given BWT(T) and a pattern string p, return the number of times p occurs in T."""
    rank_all, tots = rank_all_bwt(bw)
    first = first_col(tots)
    if ptr[-1] not in first:
        return 0  # character doesn’t occur in T
    left_border, right_border = first[ptr[-1]]
    i = len(ptr) - 2
    while i >= 0 and right_border > left_border:
        char_i = ptr[i]
        left_border = first[char_i][0] + rank_all[char_i][left_border - 1]
        right_border = first[char_i][0] + rank_all[char_i][right_border - 1]
        i -= 1
    return right_border - left_border  # return size of final range


original_text = "Tomorrow_and_tomorrow_and_tomorrow"
original_text = "abaaba"
search_text = "aba"
bw = bwt(original_text)
print(bw)
count = count_matches_2(bw, search_text)
print(f"count {search_text} in {original_text} = {count}\n")
print()
