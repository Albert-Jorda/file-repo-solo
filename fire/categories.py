'''
Add the file extensions and their corresponding categories here
'''
CATEGORIES_MAP = {
    "video": [
        "mp4", "mkv", "webm", "mov"
    ],

    "text": [
        "txt", "py", "js"
    ],

    "image": [
        "jpg", "jpeg", "png"
    ],

    "executable": [
        "exe"
    ],

    "document": [
        "pdf", "docx", "pptx"
    ],
}

DEFAULT_CATEGORY = "others"
CATEGORIES = CATEGORIES_MAP.keys()
