<script>
export default {
    name: "page_connection",
    data() {
        return {
            username: "",
            password: "",
            apiMessage: "",
        };
    },
    methods: {
        async login() {
            try {
                const response = await fetch("http://your-api-url.com/login", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        username: this.username,
                        password: this.password,
                    }),
                });
                const data = await response.json();
                if (response.ok) {
                    this.apiMessage = "Login successful!";
                } else {
                    this.apiMessage = data.message || "Login failed!";
                }
            } catch (error) {
                this.apiMessage = "API unreachable!";
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
            <button type="submit">Login</button>
        </form>
        <p>{{ apiMessage }}</p>
    </div>
</template>