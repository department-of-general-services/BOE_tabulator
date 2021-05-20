import pytest

from common.scrape_utils import MONTHS
from common.utils import replace_chars, levenshtein_match, levenshtein

alphabet = "abcdefghijklmnopqrstuvwxyz"


@pytest.mark.parametrize(
    "text,expected", [("March 17, 2010", "March 17, 2010"), ("ﬁquotesﬂ", '"quotes"')]
)
def test_replace_chars(text, expected):
    output = replace_chars(text)
    print("OUTPUT")
    print(output)
    print("EXPECTED")
    print(expected)
    assert output == expected


@pytest.mark.parametrize(
    "word_a,word_b,expected_distance",
    [
        ("possible", "impossible", 2),
        ("possible", "sorry", 7),
        ("January", "Jaunary", 2),
        ("June", "une", 1),
    ],
)
def test_levenshtein_distance(word_a, word_b, expected_distance):
    """Tests the Levenshtein distance algorithm created as a helper
    function for parse_long_date"""

    distance = levenshtein(word_a, word_b)
    assert distance == expected_distance


class TestLevenshteinMatch:
    """Tests the month misspelling detection.
    This test also specifically *excludes* the misspellings of:
      'juny'
      'jule'
    because both of these misspellings have Levenshtein distances
    of 1 to both "june" and "july" and it's not possible to determine
    the correct month without a lot of extra work. If we run into these
    misspellings it will probably be easier to catch that specific error
    than rework the function(s) to make the right call."""

    def test_single_deletions(self):
        """Test for correct detection of months with single-letter deletions."""
        deletions = dict()
        for month in MONTHS:
            deletions[month] = list()
            for j in range(len(month)):
                deletions[month].append(month[:j] + month[j + 1 :])

        for month, month_dels in deletions.items():
            for deletion in month_dels:
                match, score = levenshtein_match(deletion, MONTHS)
                assert (
                    match == month
                ), f"month={month}, match={match}, score={score}, del={deletion}"

    def test_single_misspell(self):
        """Test for correct detection of months with single-letter changes.
        Specifically exempts "jule" and "juny" as they are special cases that
        hopefully never come up. (And if they do, it'll probably be easier
        to specifically handle those errors than rework the spellchecking
        to accomodate them)"""
        misspellings = dict()
        for month in MONTHS:
            misspellings[month] = list()
            for j in range(len(month)):
                for char in alphabet:  # all possible single-letter changes
                    misspell = month[:j] + char + month[j + 1 :]
                    misspellings[month].append(misspell)

        for month, month_misspells in misspellings.items():
            for misspelling in month_misspells:
                if misspelling in [
                    "juny",
                    "jule",
                ]:  # specific exception for special case we hope to never see
                    assert 1
                else:
                    match, score = levenshtein_match(misspelling, MONTHS)
                    assert match == month, (
                        f"month={month}, match={match}, score={score},"
                        f"misspell={misspelling}"
                    )
