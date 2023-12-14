import { createApp } from "vue";
import "./style.css";
import App from "./App.vue";
import Home from "./routes/Home.vue";
import Devices from "./routes/Devices.vue";
import Frontdesk from "./routes/Frontdesk.vue";
import { createRouter, createWebHistory } from "vue-router";

// import * as ElementPlusIconsVue from "@element-plus/icons-vue";

const routes = [
    // statiscs and homepage
    { path: "/", component: Home },
    // control devices and manually turn on/off devices
    { path: "/devices", component: Devices },
    { path: "/frontdesk", component: Frontdesk }
];

const router = createRouter({
    history: createWebHistory(),
    //@ts-ignore
    routes
});

const app = createApp(App);

// for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
//     app.component(key, component);
// }
app.use(router);
app.mount("#app");
