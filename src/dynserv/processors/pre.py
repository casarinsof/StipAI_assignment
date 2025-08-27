class Lowercase:
    def __call__(self, text: str) -> str:
        return text.lower()

class Strip:
    """
    A callable class that strips leading and trailing whitespace from a string.

    Methods
    -------
    __call__(text: str) -> str
        Removes leading and trailing whitespace from the input string.
        Parameters:
            text (str): The string to be stripped.
        Returns:
            str: The stripped string.
    """
    def __call__(self, text: str) -> str:
        return text.strip()

class RemoveEmojis:
    """
    A processor class that removes non-ASCII characters (such as emojis) from a given text string.

    Methods
    -------
    __call__(text: str) -> str
        Returns a new string with all non-ASCII characters removed from the input text.
    """
    def __call__(self, text: str) -> str:
        return ''.join(ch for ch in text if ord(ch) < 128)
