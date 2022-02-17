from fire.categories import CATEGORIES_MAP, CATEGORIES, DEFAULT_CATEGORY

def determine_category(filename: str) -> str:
    splitted = filename.split('.')
    fileExtension = splitted[len(splitted) - 1]
    result = DEFAULT_CATEGORY

    for category in CATEGORIES:
        if fileExtension.lower() in CATEGORIES_MAP[category]:
            result = category
            break

    return result


def get_category_choices_mapped() -> list[tuple[str, str]]:
    result: list = list(map(lambda str: (str, str.capitalize()), CATEGORIES))
    result.append((DEFAULT_CATEGORY, DEFAULT_CATEGORY.capitalize()))
    return result
