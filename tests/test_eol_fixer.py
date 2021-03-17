from newversion.eol_fixer import EOLFixer


class TestEOLFixer:
    def test_is_crlf(self):
        assert EOLFixer.is_crlf("test") is False
        assert EOLFixer.is_crlf("test\ntest") is False
        assert EOLFixer.is_crlf("test\r\ntest") is True

    def test_to_lf(self):
        assert EOLFixer.to_lf("test") == "test"
        assert EOLFixer.to_lf("test\ntest") == "test\ntest"
        assert EOLFixer.to_lf("test\r\ntest") == "test\ntest"

    def test_to_crlf(self):
        assert EOLFixer.to_crlf("test") == "test"
        assert EOLFixer.to_crlf("test\ntest") == "test\r\ntest"
        assert EOLFixer.to_crlf("test\r\ntest") == "test\r\ntest"

    def test_get_line_ending(self):
        assert EOLFixer.get_line_ending("test") == "\n"
        assert EOLFixer.get_line_ending("test\ntest") == "\n"
        assert EOLFixer.get_line_ending("test\r\ntest\n") == "\r\n"

    def test_add_newline(self):
        assert EOLFixer.add_newline("test") == "test\n"
        assert EOLFixer.add_newline("test\ntest") == "test\ntest\n"
        assert EOLFixer.add_newline("test\ntest\n") == "test\ntest\n"
        assert EOLFixer.add_newline("test\ntest\n\n") == "test\ntest\n\n"
        assert EOLFixer.add_newline("test\r\ntest") == "test\r\ntest\r\n"
