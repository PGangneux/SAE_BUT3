<script>
import ClientAPI from "../model/clientAPI.js";
import router from "../router.js";
export default {
    name: "page_connection",
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
            // Refaire pour plus beau et intuitif (Messages d'erreurs, etc...)
            this.loading = true;
            await ClientAPI.connectAPI(this.username, this.password);
            this.apiMessage = ClientAPI.current_user ? "login bon" : "login pas bon";
            if (ClientAPI.current_user) {
                if (window.history.length > 1){
                    router.go(-1);
                } else {
                    router.replace('/');
                }
            }
            this.loading = false;
        },
    },
};
</script>

<template>
    <div>
        <h1 class="vert-neon">Bienvenue</h1>
        <form @submit.prevent="login" class="local">
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
            <button>Login</button>
        </form>
        <img v-if="this.loading" src="/imgs/spinner.gif" alt="loading image...">
        <p v-if="apiMessage">{{ apiMessage }}</p>
    </div>
</template>

<style scoped>
.local label {
    color : var(--blanc);
}
</style>