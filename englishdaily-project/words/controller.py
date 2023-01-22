from .models import WordList


def get_word_lists(native=True, user_rg_id=None):
    """Get lists of word lists."""
    list = WordList.objects.filter(native=native).all()
    if list.exists():
        return list
    return []
