from .models import WordList


def get_word_lists(native=True, user_rg_id=None):
    """Get lists of word lists."""

    return WordList.objects.filter(native=native).all()
