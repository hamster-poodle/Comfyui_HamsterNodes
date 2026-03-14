import numpy as np
from PIL import Image
import folder_paths
import os
import random
import torch

class PreviewImagesNested:
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"images": ("IMAGE",)}}

    # 出力は入力と同じ IMAGE 型。リスト構造を維持して渡します。
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "preview"
    OUTPUT_NODE = True
    CATEGORY = "🐹 HamsterNodes/Preview"

    def preview(self, images):
        # 【修正】元の images 変数を書き換えず、内部処理用に別のリストを作成する
        proc_images = images if isinstance(images, list) else [images]

        output_dir = folder_paths.get_temp_directory()
        nested = []

        for group_i, batch in enumerate(proc_images):
            group_data = []
            
            # batch が [H, W, C] の場合に備えて [1, H, W, C] に正規化（念のため）
            if len(batch.shape) == 3:
                batch = batch.unsqueeze(0)

            for img_i, tensor in enumerate(batch):
                # テンソルを画像に変換
                img_np = (tensor.cpu().numpy() * 255).clip(0, 255).astype(np.uint8)
                image = Image.fromarray(img_np)

                # ランダムIDを付けてファイル名の衝突を避ける
                rand_id = random.randint(0, 1000000)
                filename = f"nested_{group_i}_{img_i}_{rand_id}.png"
                image.save(os.path.join(output_dir, filename))

                group_data.append({
                    "filename": filename,
                    "subfolder": "",
                    "type": "temp",
                    "resolution": f"{image.width}x{image.height}"
                })
            nested.append(group_data)

        # 【修正】result には、加工していない元の images をそのまま返します
        return {
            "ui": {"nested_images": nested},
            "result": (images,)
        }