from fire.filetypes import TYPES

def determine_category(filename: str) -> str:
    splitted = filename.split('.')
    fileExtension = splitted[len(splitted) - 1]
    categories = TYPES.keys()
    result = "others"

    for category in categories:
        if fileExtension in TYPES[category]:
            result = category
            break

    return result

def mapper(category_name: str) -> tuple:
    return (category_name, category_name.capitalize())

def get_choices_mapped()-> list[tuple]:
    return map(mapper, TYPES.keys())
