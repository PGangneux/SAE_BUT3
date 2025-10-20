<script>
import comp_headerbar from './components/Headerbar.vue';
import comp_footerbar from './components/Footerbar.vue';

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
  <link href="/assets/css/main.css';" rel="stylesheet" >
    <comp_headerbar />
    <main>
        <RouterView />
    </main>
    <comp_footerbar />
</template>