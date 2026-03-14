import os


class LoadTextFromPathList:
    """
    Input:
      text_paths : newline-separated list of txt file paths

    Output:
      combined_text : concatenated text in the format
        "character_name: content"
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text_paths": (
                    "STRING",
                    {
                        "multiline": True,
                        "default": ""
                    }
                )
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("combined_text",)

    FUNCTION = "load"

    CATEGORY = "🐹 HamsterNodes/Loader"

    def load(self, text_paths: str):

        paths = [
            p.strip()
            for p in text_paths.splitlines()
            if p.strip()
        ]

        lines = []

        for path in paths:

            name = os.path.splitext(os.path.basename(path))[0]

            if not os.path.exists(path):
                lines.append(f"{name}：[FILE NOT FOUND]")
                continue

            content = None

            # try multiple encodings (Windows JP friendly)
            for enc in ("utf-8-sig", "utf-8", "cp932"):
                try:
                    with open(path, "r", encoding=enc) as f:
                        content = f.read().strip()
                    break
                except Exception:
                    pass

            if not content:
                lines.append(f"{name}：[READ ERROR]")
            else:
                lines.append(f"{name}：{content}")

        combined_text = "\n".join(lines)

        return (combined_text,)