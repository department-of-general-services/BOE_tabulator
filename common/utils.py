from pathlib import Path
import numpy as np

REPLACEMENTS = [
    ("Œ", "-"),
    ("ﬁ", '"'),
    ("ﬂ", '"'),
    ("™", "'"),
    ("Ł", "•"),
    ("Š", "-"),
    ("€", " "),
    ("¬", "-"),
    ("–", "…"),
    ("‚", "'"),
    ("Ž", "™"),
    ("˚", "fl"),
    ("˜", "fi"),
    ("˛", "ff"),
    ("˝", "ffi"),
    ("š", "—"),
    ("ü", "ti"),
    ("î", "í"),
    ("è", "c"),
    ("ë", "e"),
    ("Ð", "–"),
    ("Ò", '"'),
    ("Ó", '"'),
    ("Õ", "'"),
]


def del_dir_contents(root):
    """Convenience function so we don't have to empy out pdf_dir by hand
    during testing.

    Removes all
    """
    for p in root.iterdir():
        if p.is_dir():
            del_dir_contents(p)
        else:
            p.unlink()
    for p in root.iterdir():
        if p.is_dir():
            p.rmdir()
    return


def is_empty(_dir: Path) -> bool:
    return not bool([_ for _ in _dir.iterdir()])


def levenshtein(token1, token2):
    distances = np.zeros((len(token1) + 1, len(token2) + 1))

    for t1 in range(len(token1) + 1):
        distances[t1][0] = t1

    for t2 in range(len(token2) + 1):
        distances[0][t2] = t2

    a = 0
    b = 0
    c = 0

    for t1 in range(1, len(token1) + 1):
        for t2 in range(1, len(token2) + 1):
            if token1[t1 - 1] == token2[t2 - 1]:
                distances[t1][t2] = distances[t1 - 1][t2 - 1]
            else:
                a = distances[t1][t2 - 1]
                b = distances[t1 - 1][t2]
                c = distances[t1 - 1][t2 - 1]

                if a <= b and a <= c:
                    distances[t1][t2] = a + 1
                elif b <= a and b <= c:
                    distances[t1][t2] = b + 1
                else:
                    distances[t1][t2] = c + 1

    return distances[len(token1)][len(token2)]


def levenshtein_match(text, options):
    """
    Args:
        text (str): the misspelled string
        options (str): the set of options to select a best match from

    Returns:
        best_match (str): the string that best matches the misspelled input
        best_score (int): the Levenshtein distance between text and best_match
    """
    text = text.lower()
    best_match = ""
    best_score = 9999  # lower scores are better
    for option in options:
        # lev dist == num changes to make text into i
        score = levenshtein(text, option)
        if score < best_score:
            best_score = score
            best_match = option

    return best_match, best_score


def replace_chars(text, replacement_list=REPLACEMENTS):
    """Replaces a set of characters specified by a list of replacement keys

    Args:
        text (str): The raw text whose characters will be replaced
        replacement_list (list): List of tuples in which the first item
        is the current character and the second item is its replacement
    Returns:
        text (str): The text with the characters replaced
    """
    for current, new in replacement_list:
        text = text.replace(current, new)
    return text
