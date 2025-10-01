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
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-sRIl4kxILFvY47J16cr9ZwB07vP4J8+LH7qKQnuqkuIAvNWLzeN8tE5YBujZqJLB" crossorigin="anonymous">
    <p>
        <strong>DEBUG Current route path:</strong> {{ $route.fullPath }}
    </p>
    <comp_headerbar />
    <main>
        <RouterView />
    </main>
    <comp_footerbar />
</template>