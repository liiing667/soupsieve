"""Test `nth` child selectors."""
from .. import util
from soupsieve import SelectorSyntaxError


class TestNthChild(util.TestCase):
    """Test `nth` child selectors."""

    MARKUP = """
    <p id="0"></p>
    <p id="1"></p>
    <span id="2" class="test"></span>
    <span id="3"></span>
    <span id="4" class="test"></span>
    <span id="5"></span>
    <span id="6" class="test"></span>
    <p id="7"></p>
    <p id="8" class="test"></p>
    <p id="9"></p>
    <p id="10" class="test"></p>
    <span id="11"></span>
    """

    def test_nth_child_of_s_simple(self):
        """Test `nth` child with selector (simple)."""

        self.assert_selector(
            self.MARKUP,
            ":nth-child(-n+3 of p)",
            ['0', '1', '7'],
            flags=util.HTML
        )

    def test_nth_child_of_s_complex(self):
        """Test `nth` child with selector (complex)."""

        self.assert_selector(
            self.MARKUP,
            ":nth-child(2n + 1 of :is(p, span).test)",
            ['2', '6', '10'],
            flags=util.HTML
        )

        self.assert_selector(
            self.MARKUP,
            ":nth-child(2n + 1 OF :is(p, span).test)",
            ['2', '6', '10'],
            flags=util.HTML
        )

    def test_nth_child_of_s_list(self):
        """Test `nth` child `of S` with a selector list."""

        self.assert_selector(
            self.MARKUP,
            ":nth-child(2n of p, span)",
            ['1', '3', '5', '7', '9', '11'],
            flags=util.HTML
        )

    def test_nth_child_of_s_nested_pseudo(self):
        """Test `nth` child `of S` with a nested pseudo class."""

        markup = """
        <div>
        <p id="1"><b></b></p>
        <p id="2"></p>
        </div>
        """

        self.assert_selector(
            markup,
            "p:nth-child(1 of :has(> b))",
            ['1'],
            flags=util.HTML
        )

    def test_nth_child_of_s_no_match(self):
        """Test `nth` child `of S` that is valid, but matches nothing."""

        # Syntax is valid, so no error is raised; the document simply has no matches.
        self.assert_selector(
            self.MARKUP,
            ":nth-child(1 of .missing)",
            [],
            flags=util.HTML
        )

    def test_nth_child_of_s_missing_selector(self):
        """Test `nth` child `of S` with no selector after `of`."""

        self.assert_raises(':nth-child(2n of)', SelectorSyntaxError)

    def test_nth_child_of_s_missing_nth(self):
        """Test `nth` child `of S` with no `nth` component."""

        self.assert_raises(':nth-child(of div)', SelectorSyntaxError)

    def test_nth_child_of_s_no_whitespace(self):
        """Test `nth` child `of S` requires whitespace around `of`."""

        self.assert_raises(':nth-child(2n ofdiv)', SelectorSyntaxError)

    def test_nth_child_of_s_relative_selector(self):
        """Test `nth` child `of S` does not accept a relative selector."""

        self.assert_raises(':nth-child(2n of > div)', SelectorSyntaxError)

    def test_nth_child_of_s_trailing_combinator(self):
        """Test `nth` child `of S` with a trailing combinator."""

        self.assert_raises(':nth-child(2n of div >)', SelectorSyntaxError)

    def test_nth_child_of_s_empty_slot(self):
        """Test `nth` child `of S` with an empty slot in the selector list."""

        self.assert_raises(':nth-child(2n of div,)', SelectorSyntaxError)
        self.assert_raises(':nth-child(2n of , div)', SelectorSyntaxError)

    def test_nth_of_type_rejects_of_s(self):
        """Test `nth` of type does not support `of S`."""

        self.assert_raises(':nth-of-type(2n of div)', SelectorSyntaxError)
        self.assert_raises(':nth-last-of-type(2n of div)', SelectorSyntaxError)
