'''
Add the file extensions and their corresponding categories here
'''
CATEGORIES_MAP = {
    "video": [
        "mp4", "mkv", "webm", "mov", "mpeg4",
        "MP4", "MKV", "WEBM", "MOV", "MPEG4",
    ],

    "text": [
        "txt", "py", "js", 'html', 'htm',
        "TXT", "PY", "JS", 'HTML', 'htm'
    ],

    "image": [
        "jpg", "jpeg", "png", "gif",
        "JPG", "JPEG", "PNG", "GIF",
    ],

    "executable": [
        "exe",
        "EXE",
    ],

    "document": [
        "pdf", "docx", "pptx", "ppt", "doc", "xls", "xlsx",
        "PDF", "DOCX", "PPTX", "PPT", "DOC", "XLS", "XLSX",
    ],
    "audio": [
        "mp3", "wav", "avi", "m4a", 'wma',
        "MP3", "WAV", "AVI", "M4A", 'WMA',
    ],
    "compressed": [
        "zip", "rar",
        "ZIP", "RAR",
    ],
}

DEFAULT_CATEGORY = "others"
CATEGORIES = CATEGORIES_MAP.keys()
