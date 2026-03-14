import { app } from "../../scripts/app.js";

app.registerExtension({
    name: "Hamster.PreviewNested",
    async beforeRegisterNodeDef(nodeType, nodeData) {
        if (nodeData.name === "PreviewImagesNested") {
            const onExecuted = nodeType.prototype.onExecuted;

            nodeType.prototype.onExecuted = function (message) {
                onExecuted?.apply(this, arguments);

                // 既存のウィジェットをクリア
                if (this.widgets) {
                    this.widgets = this.widgets.filter(w => w.name !== "nested_preview");
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

                // 【重要】ノードの現在のサイズに合わせて初期の高さを設定
                const headerHeight = 40; // ノードのタイトルバー等の概算高さ
                mainContainer.style.height = `${this.size[1] - headerHeight}px`;

                message.nested_images.forEach((group, gIdx) => {
                    const groupWrapper = document.createElement("div");
                    groupWrapper.style.border = "1px solid #666";
                    groupWrapper.style.borderRadius = "4px";
                    groupWrapper.style.padding = "4px";
                    groupWrapper.style.marginBottom = "5px";
                    groupWrapper.style.backgroundColor = "rgba(0,0,0,0.2)";
                    groupWrapper.innerHTML = `<div style="font-size:10px; color:#aaa;">Group ${gIdx}</div>`;

                    const imgList = document.createElement("div");
                    imgList.style.display = "flex";
                    imgList.style.flexWrap = "wrap";
                    imgList.style.gap = "4px";

                    group.forEach(imgData => {
                        const imgContainer = document.createElement("div");
                        imgContainer.style.flex = "1 1 100px";
                        imgContainer.style.maxWidth = "100%";

                        const img = document.createElement("img");
                        img.src = `/view?filename=${imgData.filename}&type=${imgData.type}`;
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

            // 【修正の肝】ノードがリサイズされたときに呼ばれる関数
            const onResize = nodeType.prototype.onResize;
            nodeType.prototype.onResize = function (size) {
                if (onResize) onResize.apply(this, arguments);

                // ノード内にある作成したDOMウィジェットを探す
                const widget = this.widgets?.find(w => w.name === "nested_preview");
                if (widget && widget.element) {
                    const headerHeight = 40;
                    // ノードの新しいサイズ(size[1])に合わせて、中のHTMLの高さを書き換える
                    widget.element.style.height = `${size[1] - headerHeight}px`;
                    // 横幅も必要に応じて調整（基本は100%でOK）
                    widget.element.style.width = `${size - 10}px`;
                }
            };
        }
    }
});