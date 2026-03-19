import { app } from "../../scripts/app.js";

app.registerExtension({
    name: "Hamster.PreviewNested",
    async beforeRegisterNodeDef(nodeType, nodeData) {
        if (nodeData.name === "PreviewImagesNested") {
            const onExecuted = nodeType.prototype.onExecuted;

            nodeType.prototype.onExecuted = function (message) {
                onExecuted?.apply(this, arguments);

                // ランダムID（キャッシュ対策）
                const run_id = Date.now() + "_" + Math.random();

                // 既存widget削除（安全に）
                if (this.widgets) {
                    const w = this.widgets.find(w => w.name === "nested_preview");
                    if (w) {
                        this.removeWidget?.(w);
                    }
                }

                const mainContainer = document.createElement("div");
                mainContainer.style.width = "100%";
                mainContainer.style.display = "flex";
                mainContainer.style.flexDirection = "column";
                mainContainer.style.gap = "10px";
                mainContainer.style.padding = "5px";
                mainContainer.style.boxSizing = "border-box";
                mainContainer.style.overflowY = "auto";
                mainContainer.style.overflowX = "hidden";

                const headerHeight = 40;
                mainContainer.style.height = `${this.size[1] - headerHeight}px`;

                message.nested_images.forEach((group, gIdx) => {
                    const groupWrapper = document.createElement("div");
                    groupWrapper.style.border = "1px solid #666";
                    groupWrapper.style.borderRadius = "4px";
                    groupWrapper.style.padding = "4px";
                    groupWrapper.style.marginBottom = "5px";
                    groupWrapper.style.backgroundColor = "rgba(0,0,0,0.2)";

                    const label = document.createElement("div");
                    label.textContent = `Group ${gIdx}`;
                    label.style.fontSize = "10px";
                    label.style.color = "#aaa";
                    groupWrapper.appendChild(label);

                    const imgList = document.createElement("div");
                    imgList.style.display = "flex";
                    imgList.style.flexWrap = "wrap";
                    imgList.style.gap = "4px";

                    group.forEach((imgData, i) => {
                        const imgContainer = document.createElement("div");
                        imgContainer.style.flex = "1 1 100px";
                        imgContainer.style.maxWidth = "100%";

                        const img = document.createElement("img");

                        // ★ キャッシュ完全回避
                        img.src = `/view?filename=${imgData.filename}&type=${imgData.type}&t=${run_id}_${i}`;

                        img.style.width = "100%";
                        img.style.height = "auto";
                        img.style.display = "block";

                        imgContainer.appendChild(img);
                        imgList.appendChild(imgContainer);
                    });

                    groupWrapper.appendChild(imgList);
                    mainContainer.appendChild(groupWrapper);
                });

                this.addDOMWidget("nested_preview", "HTML", mainContainer);

                this.setDirtyCanvas(true, true);
            };

            const onResize = nodeType.prototype.onResize;

            nodeType.prototype.onResize = function (size) {
                if (onResize) onResize.apply(this, arguments);

                const widget = this.widgets?.find(w => w.name === "nested_preview");

                if (widget && widget.element) {
                    const headerHeight = 40;

                    widget.element.style.height = `${size[1] - headerHeight}px`;

                    // ★ 修正ポイント
                    widget.element.style.width = `${size[0] - 10}px`;
                }
            };
        }
    }
});