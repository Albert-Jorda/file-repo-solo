'''
Add the file extensions and their corresponding categories here
'''
CATEGORIES_MAP = {
    "video": [
        "mp4", "mkv", "webm", "mov", "mpeg4"
    ],

    "text": [
        "txt", "py", "js", 'html', 'htm'
    ],

    "image": [
        "jpg", "jpeg", "png", "gif"
    ],

    "executable": [
        "exe"
    ],

    "document": [
        "pdf", "docx", "pptx", "ppt", "doc", "xls", "xlsx"
    ],
    "audio": [
        "mp3", "wav", "avi", "m4a", 'wma'
    ],
    "compressed": [
        "zip", "rar"
    ],
}

DEFAULT_CATEGORY = "others"
CATEGORIES = CATEGORIES_MAP.keys()
