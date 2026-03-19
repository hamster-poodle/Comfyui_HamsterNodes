class StringListSlip:

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "strings": ("STRING", {"forceInput": True}),
                "before": ("INT", {"default": 1, "min": 0, "max": 100}),
                "after": ("INT", {"default": 1, "min": 0, "max": 100}),
                "delimiter": ("STRING", {"default": " "}),
                "wrap": ("BOOLEAN", {"default": False}),
            }
        }

    RETURN_TYPES = ("STRING",)
    INPUT_IS_LIST = True
    OUTPUT_IS_LIST = (True,)
    FUNCTION = "slip"
    CATEGORY = "🐹 HamsterNodes/List"

    def slip(self, strings, before, after, delimiter, wrap):

        strings = strings
        before = before[0]
        after = after[0]
        delimiter = delimiter[0]
        wrap = wrap[0]

        result = []
        length = len(strings)

        for i in range(length):

            window = []

            for offset in range(-before, after + 1):

                idx = i + offset

                if wrap:
                    idx = idx % length
                    window.append(strings[idx])
                else:
                    if 0 <= idx < length:
                        window.append(strings[idx])

            result.append(delimiter.join(window))

        return (result,)