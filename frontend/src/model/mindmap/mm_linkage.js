export class mmLinkage {
    startnode;
    endnode;
    thickness;

    constructor(startnode, endnode, thickness) {
        this.startnode = startnode;
        this.endnode = endnode;
        this.thickness = thickness;
    }

    getStyle(scale, baseOffsetX, baseOffsetY) {
        const scaledStartX = this.startnode.x * scale;
        const scaledStartY = this.startnode.y * scale;
        const scaledEndX = this.endnode.x * scale;
        const scaledEndY = this.endnode.y * scale;

        const length = Math.sqrt(Math.pow(scaledEndX - scaledStartX, 2) + Math.pow(scaledEndY - scaledStartY, 2));
        const angle = Math.atan2(scaledEndY - scaledStartY, scaledEndX - scaledStartX) * 180 / Math.PI;

        return {
            "height": (this.thickness * scale) + "px",
            "width": length + "px",
            "left": (scaledStartX + baseOffsetX) + "px", // 50 * scale to center
            "top": (scaledStartY + baseOffsetY) + "px", // 50 * scale to center
            "transform": `rotate(${angle}deg)`,
            "transform-origin": "0 50%",
        };
    }
}