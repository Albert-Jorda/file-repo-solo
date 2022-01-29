from fire.categories import CATEGORIES_MAP, CATEGORIES, DEFAULT_CATEGORY

def determine_category(filename: str) -> str:
    splitted = filename.split('.')
    fileExtension = splitted[len(splitted) - 1]
    result = DEFAULT_CATEGORY

    for category in CATEGORIES:
        if fileExtension in CATEGORIES_MAP[category]:
            result = category
            break

    return result

def mapper(category_name: str) -> tuple:
    return (category_name, category_name.capitalize())

def get_category_choices_mapped()-> list[tuple]:
    result: list = list(map(mapper, CATEGORIES.keys()))
    result.append((DEFAULT_CATEGORY, DEFAULT_CATEGORY.capitalize()))
    return result
