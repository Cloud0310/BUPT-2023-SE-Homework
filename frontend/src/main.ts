import { createApp } from "vue";
import "./style.css";
import App from "./App.vue";
import Admin from "./routes/Admin.vue";
import Devices from "./routes/Devices.vue";
import Frontdesk from "./routes/Frontdesk.vue";
import { createRouter, createWebHistory } from "vue-router";

const routes = [
    // statiscs and homepage
    { path: "/admin", component: Admin },
    // control devices and manually turn on/off devices
    { path: "/devices", component: Devices },
    { path: "/frontdesk", component: Frontdesk }
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

const app = createApp(App);

app.use(router);
app.mount("#app");
