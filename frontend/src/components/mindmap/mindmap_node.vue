<script>
import { LegendClassMap, mmNode } from "./mindmap_func";

export default {
    name : "mindmap_node",
    props : {
        node : {
            type : mmNode,
            required : true,
        },
        scale : {
            type : Number,
            required : true,
        },
        offx : {
            type : Number,
            required : true,
        },
        offy : {
            type : Number,
            required : true,
        },
    },
    data() {
        return {
            LegendClassMap : LegendClassMap,
        };
    },
}
</script>

<template>
    <div :style="node.getStyle(scale,offx,offy)">
        <p>{{ LegendClassMap[node.category.name] }}</p>
        <p>{{ node.content }}</p>
    </div>
</template>