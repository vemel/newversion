"""
Converter between Unix and WIndows line endings.
"""


class EOLFixer:
    """
    Converter between Unix and WIndows line endings.
    """

    CRLF = "\r\n"
    LF = "\n"

    @classmethod
    def is_crlf(cls, text: str) -> bool:
        """
        Check whether text has `\r\n` characters.

        Arguments:
            text -- Text to check.
        """
        return cls.CRLF in text

    @classmethod
    def to_lf(cls, text: str) -> str:
        """
        Convert `\r\n` to `\n`.

        Arguments:
            text -- Text to convert.

        Returns:
            Converted text.
        """
        if not cls.is_crlf(text):
            return text

        return text.replace(cls.CRLF, cls.LF)

    @classmethod
    def to_crlf(cls, text: str) -> str:
        """
        Convert `\n` to `\r\n`.

        Arguments:
            text -- Text to convert.

        Returns:
            Converted text.
        """
        if cls.is_crlf(text):
            return text

        return text.replace(cls.LF, cls.CRLF)

    @classmethod
    def get_line_ending(cls, text: str) -> str:
        """
        Get line ending character.
        """
        return cls.CRLF if cls.is_crlf(text) else cls.LF

    @classmethod
    def add_newline(cls, text: str) -> str:
        """
        Add newline character to the end if it is missing.
        """
        line_ending = cls.get_line_ending(text)
        if text.endswith(line_ending):
            return text

        return f"{text}{line_ending}"
