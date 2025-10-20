<script setup>
import { ref } from 'vue'


</script>

<template>
    <nav> 
        <ul>
            <li>
                <button type="button" @click="count++">count is {{ count }}</button>
            </li>
            <li>
                <label for="site-search">Search the site:</label>
                <input type="search" id="site-search" name="q" />
                <button>Search</button>
            </li>
            <li>
                <button type="button" @click="count++">count is {{ count }}</button>
            </li>
            <li>
                <button type="button" @click="count++">count is {{ count }}</button>
            </li>
        </ul>
    </nav>

  <h1>{{ msg }}</h1>


</template>

<style scoped>
.read-the-docs {
  color: #888;
}
</style>
