# nodes.py
# Load images from path lists (supports both str and list[str])

import os
from PIL import Image
import torch
import torch.nn.functional as F
import numpy as np


class LoadImagesFromPathList:

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {
                    "multiline": True,
                    "default": ""
                }),
                "generate_dummy_if_empty": ("BOOLEAN", {
                    "default": True
                }),
                "normalize_size": ("BOOLEAN", {
                    "default": True
                }),
            }
        }

    RETURN_TYPES = ("IMAGE", "INT")
    RETURN_NAMES = ("images", "group_sizes")

    OUTPUT_IS_LIST = (False, True)

    FUNCTION = "load_images"

    CATEGORY = "🐹 HamsterNodes/Loader"

    def load_images(self, text, generate_dummy_if_empty, normalize_size):

        if isinstance(text, str):
            text = [text]

        all_images = []
        group_sizes = []

        # -------------------------------
        # 画像ロード
        # -------------------------------
        for block in text:

            if not block or not block.strip():
                group_sizes.append(0)
                continue

            paths = [p.strip() for p in block.splitlines() if p.strip()]
            count = 0

            for path in paths:

                if not os.path.exists(path):
                    continue

                try:
                    img = Image.open(path).convert("RGB")
                except Exception:
                    continue

                img_np = np.array(img).astype(np.float32) / 255.0

                # (H,W,C) → (1,C,H,W)
                img_tensor = torch.from_numpy(img_np).permute(2,0,1).unsqueeze(0)

                all_images.append(img_tensor)
                count += 1

            group_sizes.append(count)

        # --------------------------------
        # サイズ正規化
        # longest edge resize → center edge stretch
        # --------------------------------
        if normalize_size and all_images:

            # 最大長辺
            max_long = max(
                max(img.shape[2], img.shape[3]) for img in all_images
            )

            resized = []

            for img in all_images:

                _, c, h, w = img.shape
                long_edge = max(h, w)

                scale = max_long / long_edge

                new_h = int(round(h * scale))
                new_w = int(round(w * scale))

                img = F.interpolate(
                    img,
                    size=(new_h, new_w),
                    mode="bicubic",
                    align_corners=False
                )

                resized.append(img)

            # 最大H,W
            max_h = max(img.shape[2] for img in resized)
            max_w = max(img.shape[3] for img in resized)

            padded = []

            for img in resized:

                _, _, h, w = img.shape

                pad_h = max_h - h
                pad_w = max_w - w

                pad_top = pad_h // 2
                pad_bottom = pad_h - pad_top

                pad_left = pad_w // 2
                pad_right = pad_w - pad_left

                if pad_h > 0 or pad_w > 0:

                    img = F.pad(
                        img,
                        (pad_left, pad_right, pad_top, pad_bottom),
                        mode="replicate"
                    )

                padded.append(img)

            all_images = padded

        # --------------------------------
        # バッチ生成
        # --------------------------------
        if all_images:

            images = torch.cat(all_images, dim=0)

            # (B,C,H,W) → (B,H,W,C)
            images = images.permute(0,2,3,1)

        else:

            if generate_dummy_if_empty:
                images = torch.zeros((1,64,64,3), dtype=torch.float32)
            else:
                images = torch.zeros((0,64,64,3), dtype=torch.float32)

        return (images, group_sizes)