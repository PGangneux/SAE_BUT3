<script>
import BASE_URL from '../config.js';
export default {
    name: "page_connection",
    inject : ["user_current"],
    data() {
        return {
            loading : false,
            username: "",
            password: "",
            apiMessage: "",
        };
    },
    methods: {
        async login() {
            try {
                this.loading = true;
                const sleep = ms => new Promise(r => setTimeout(r, ms));
                await sleep(1000);
                const response = await fetch(BASE_URL + "API/utilisateurs/", {
                    method: "GET",
                    /// headers: { "Content-Type": "application/json" },
                    /// body: JSON.stringify({
                    ///     username: this.username,
                    ///     password: this.password, // warning change to hash
                    /// }),
                });
                const data = await response.json();
                console.log("connection data return");
                console.log(data);
                if (response.ok) {
                    this.apiMessage = "Login successful!";
                } else {
                    this.apiMessage = data.message || "Login failed!";
                }
                this.user_current.set(...data);
            } catch (error) {
                console.error(error);
                this.apiMessage = "API unreachable!";
            } finally {
                this.loading = false;
            }
        },
    },
};
</script>

<template>
    <div>
        <p>page_connection</p>
        <form @submit.prevent="login">
            <label>
                Username:
                <input v-model="username" type="text" required />
            </label>
            <br />
            <label>
                Password:
                <input v-model="password" type="password" required />
            </label>
            <br />
            <button @click="login">Login</button>
        </form>
        <img v-if="this.loading" src="/imgs/spinner.gif" alt="loading image...">
        <p>{{ apiMessage }}</p>
    </div>
</template>