from .load_images_from_path_list import LoadImagesFromPathList
from .load_text_from_path_list import LoadTextFromPathList

NODE_CLASS_MAPPINGS = {
    "LoadImagesFromPathList": LoadImagesFromPathList,
    "LoadTextFromPathList": LoadTextFromPathList,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LoadImagesFromPathList": "🐹 Load Images From Path List",
    "LoadTextFromPathList": "🐹 Load Text From Path List (Merged)",
}