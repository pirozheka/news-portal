from django import template

register = template.Library()


@register.filter()
def censor(value):
    if not isinstance(value, str):
        raise ValueError("Некорректное значение")

    # Список слов для цензуры
    censored_words = ['редиска', 'Редиска', 'идиот', 'Идиот', 'придурок', 'Придурок']

    # Функция для замены слова на звёздочки
    def replace_with_stars(word):
        return word[0] + '*' * (len(word) - 1)

    # Цензура слов
    for word in censored_words:
        value = value.replace(word, replace_with_stars(word))

    return value