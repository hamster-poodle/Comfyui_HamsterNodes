import os

class LoadTextFromPathList:
    """
    入力:
      text_paths : 改行区切りの txt ファイルパス一覧

    出力:
      combined_text : 全txtを
        「キャラクター名：内容」
        の形式で改行結合した STRING
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
    CATEGORY = "IO/Text"

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

            # 日本語Windows想定
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