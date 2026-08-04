from utils.translations.en import MESSAGES as EN_MESSAGES
from utils.translations.hi import MESSAGES as HI_MESSAGES


def translate(key, language="en"):
    """
    Returns translated message based on language.
    Defaults to English if language is not supported.
    """

    if language == "hi":
        return HI_MESSAGES.get(key, key)

    return EN_MESSAGES.get(key, key)