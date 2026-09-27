"""Test has selectors."""
from .. import util
from soupsieve import SelectorSyntaxError


class TestHas(util.TestCase):
    """Test has selectors."""

    MARKUP = """
    <div id="0" class="aaaa">
        <p id="1" class="bbbb"></p>
        <p id="2" class="cccc"></p>
        <p id="3" class="dddd"></p>
        <div id="4" class="eeee">
        <div id="5" class="ffff">
        <div id="6" class="gggg">
            <p id="7" class="hhhh"></p>
            <p id="8" class="iiii zzzz"></p>
            <p id="9" class="jjjj"></p>
            <div id="10" class="kkkk">
                <p id="11" class="llll zzzz"></p>
            </div>
        </div>
        </div>
        </div>
    </div>
    """

    MARKUP2 = """
    <div id="0" class="aaaa">
        <p id="1" class="bbbb"></p>
    </div>
    <div id="2" class="cccc">
        <p id="3" class="dddd"></p>
    </div>
    <div id="4" class="eeee">
        <p id="5" class="ffff"></p>
    </div>
    <div id="6" class="gggg">
        <p id="7" class="hhhh"></p>
    </div>
    <div id="8" class="iiii">
        <p id="9" class="jjjj"></p>
        <span id="10"></span>
    </div>
    """

    def test_has_descendant(self):
        """Test has descendant."""

        self.assert_selector(
            self.MARKUP,
            'div:not(.aaaa):has(.kkkk > p.llll)',
            ['4', '5', '6'],
            flags=util.HTML | util.NOCACHE
        )

    def test_has_next_sibling(self):
        """Test has next sibling."""

        self.assert_selector(
            self.MARKUP,
            'p:has(+ .dddd:has(+ div .jjjj))',
            ['2'],
            flags=util.HTML | util.NOCACHE
        )

    def test_has_subsequent_sibling(self):
        """Test has subsequent sibling."""

        self.assert_selector(
            self.MARKUP,
            'p:has(~ .jjjj)',
            ['7', '8'],
            flags=util.HTML | util.NOCACHE
        )

    def test_has_child(self):
        """Test has2."""

        self.assert_selector(
            self.MARKUP2,
            'div:has(> .bbbb)',
            ['0'],
            flags=util.HTML | util.NOCACHE
        )

    def test_has_case(self):
        """Test has case insensitive."""

        self.assert_selector(
            self.MARKUP,
            'div:NOT(.aaaa):HAS(.kkkk > p.llll)',
            ['4', '5', '6'],
            flags=util.HTML | util.NOCACHE
        )

    def test_has_mixed(self):
        """Test has mixed."""

        self.assert_selector(
            self.MARKUP2,
            'div:has(> .bbbb, .ffff, .jjjj)',
            ['0', '4', '8'],
            flags=util.HTML | util.NOCACHE
        )

        self.assert_selector(
            self.MARKUP2,
            'div:has(.ffff, > .bbbb, .jjjj)',
            ['0', '4', '8'],
            flags=util.HTML | util.NOCACHE
        )

    def test_has_nested_pseudo(self):
        """Test has with nested pseudo."""

        self.assert_selector(
            self.MARKUP2,
            'div:has(> :not(.bbbb, .ffff, .jjjj))',
            ['2', '6', '8'],
            flags=util.HTML | util.NOCACHE
        )

        self.assert_selector(
            self.MARKUP2,
            'div:not(:has(> .bbbb, .ffff, .jjjj))',
            ['2', '6'],
            flags=util.HTML | util.NOCACHE
        )

    def test_has_no_match(self):
        """Test has with a non-matching selector."""

        self.assert_selector(
            self.MARKUP2,
            'div:has(:paused)',
            [],
            flags=util.HTML | util.NOCACHE
        )

    def test_many_siblings(self):
        """Test many siblings case."""

        import soupsieve as sv
        from bs4 import BeautifulSoup

        selector = "div:has(a ~ b)"
        for n in (1000, 2000, 4000, 8000):
            html = "<div>" + ("<a></a>" * n) + "</div>"
            soup = BeautifulSoup(html, "html.parser")
            self.assertEqual(len(sv.select(selector, soup)), 0)

    def test_has_empty(self):
        """Test has with empty slot due to no selectors."""

        self.assert_raises('div:has()', SelectorSyntaxError)
        self.assert_raises('div:has(,a)', SelectorSyntaxError)
        self.assert_raises('div:has(a,)', SelectorSyntaxError)
        self.assert_raises('div:has(a,,a)', SelectorSyntaxError)

    def test_invalid_incomplete_has(self):
        """Test `:has()` fails with just a combinator."""

        self.assert_raises(':has(>)', SelectorSyntaxError)

    def test_invalid_has_double_combinator(self):
        """Test `:has()` fails with consecutive combinators."""

        self.assert_raises(':has(>> has a)', SelectorSyntaxError)
        self.assert_raises(':has(> has, >> a)', SelectorSyntaxError)
        self.assert_raises(':has(> has >> a)', SelectorSyntaxError)

    def test_invalid_has_trailing_combinator(self):
        """Test `:has()` fails with trailing combinator."""

        self.assert_raises(':has(> has >)', SelectorSyntaxError)

    def test_has_nested_has(self):
        """Test `:has()` nested within `:has()`."""

        markup = """
        <div id="1"><span><a></a></span></div>
        <div id="2"><span></span></div>
        """

        self.assert_selector(
            markup,
            'div:has(:has(a))',
            ['1'],
            flags=util.HTML
        )

        self.assert_selector(
            markup,
            'div:has(span:has(a))',
            ['1'],
            flags=util.HTML
        )

    def test_has_nested_has_in_not(self):
        """Test nested `:has()` within `:not()`."""

        markup = """
        <div id="1"><span><a></a></span></div>
        <div id="2"><span></span></div>
        """

        self.assert_selector(
            markup,
            'div:has(:not(:has(a)))',
            ['1', '2'],
            flags=util.HTML
        )

    def test_has_nested_empty_inner(self):
        """Test that an empty inner `:has()` fails at parse time."""

        self.assert_raises(':has(:has())', SelectorSyntaxError)

    def test_has_valid_but_empty_match(self):
        """Test `:has()` that is valid, but matches nothing."""

        # Syntax is valid, so no error is raised; the document simply has no matches.
        self.assert_selector(
            self.MARKUP2,
            'div:has(> .missing)',
            [],
            flags=util.HTML
        )

    def test_has_scope_pinned(self):
        """
        Test `:scope` inside `:has()`.

        PINNED BEHAVIOR: `:scope` currently resolves to the scope of the `select`
        call (the document here), not the element that `:has()` is anchored to,
        so this matches nothing. Browsers resolve `:scope` inside `:has()` to the
        anchor element. Pinned as the actual behavior; revisit if the
        implementation changes.
        """

        markup = """
        <div id="1"><span></span></div>
        """

        self.assert_selector(
            markup,
            'div:has(:scope > span)',
            [],
            flags=util.HTML
        )
