<script>
import comp_headerbar from './components/headerbar.vue';
import comp_footerbar from './components/footerbar.vue';

export default {
    name: "page_router",
    components: {
        comp_headerbar,
        comp_footerbar,
    },
};
</script>

<template>
    <p>
        <strong>DEBUG Current route path:</strong> {{ $route.fullPath }}
    </p>
    <comp_headerbar />
    <main>
        <RouterView />
    </main>
    <comp_footerbar />
</template>