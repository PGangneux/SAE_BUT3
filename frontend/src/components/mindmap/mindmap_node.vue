<script>
import { mmNode } from "./mindmap_func";

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
}
</script>

<template>
    <div :style="node.getStyle(scale,offx,offy)">
        {{ node.category.name }}
    </div>
</template>