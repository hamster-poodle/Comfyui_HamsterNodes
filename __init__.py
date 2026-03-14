from .load_images_from_path_list import LoadImagesFromPathList
from .load_text_from_path_list import LoadTextFromPathList
from .preview_images_nested import PreviewImagesNested

# JavaScriptファイルを読み込むためのディレクトリ指定
# これにより /js/preview_nested.js がフロントエンドで実行されます
WEB_DIRECTORY = "./js"

NODE_CLASS_MAPPINGS = {
    "LoadImagesFromPathList": LoadImagesFromPathList,
    "LoadTextFromPathList": LoadTextFromPathList,
    "PreviewImagesNested": PreviewImagesNested,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LoadImagesFromPathList": "🐹 Load Images From Path List",
    "LoadTextFromPathList": "🐹 Load Text From Path List (Merged)",
    "PreviewImagesNested": "🐹 Preview Images (Nested)",
}

# インポート可能なシンボルを定義
__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]