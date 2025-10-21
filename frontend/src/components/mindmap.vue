<script>
export default {
    name: "comp_mindmap",
    inject : ["searchterm"],
    watch : {
        searchterm(olds,news){
            console.log("mindmap searchterm change");
            console.log(olds);
            console.log(news);
        }
    }
};
</script>

<template>
    <div>
        <h2>Mindmap Component</h2>
        <h2>{{ searchterm }}</h2>
    </div>
</template>