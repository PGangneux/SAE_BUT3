<script>
import user_t from "../model/user.js";
import router from "../router.js";
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
            this.loading = true;
            try {
                const sleep = ms => new Promise(r => setTimeout(r, ms));
                await sleep(500);
                this.user_current.set(new user_t(this.username, this.password));
                /// console.log("current_user");
                /// console.log(this.user_current);
                this.apiMessage = "login bon";
                await sleep(500);
                if (window.history.length > 1){
                    router.go(-1);
                } else {
                    router.replace('/');
                }
            } catch (error) {
                console.error(error);
                this.apiMessage = error.message;
            } finally {
                this.loading = false;
            }
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
.vert-neon { 
    color : var(--vert-neon);
    justify-self: center;
}
</style>