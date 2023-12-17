import { defineStore } from "pinia";
import { login, logout, ERROR_CODE_MAP, UNKNOWN_ERROR } from "./requests";

export const useLoginStore = defineStore("store", () => {
    const isLoggedIn = ref(false);
    const csrfToken = ref("");
    const username = ref("");
    const password = ref("");
    const showLoginDialog = ref(false);
    const role = ref<"admin" | "checkout" | "AC admin" | null>(null);

    function handleLogin() {
        if (username.value === "" || password.value === "") {
            ElMessage({
                type: "warning",
                message: "用户名或密码不能为空"
            });
            return;
        }
        login(
            username.value,
            password.value,
            data => {
                isLoggedIn.value = true;
                csrfToken.value = data.csrfToken;
                role.value = data.role;
                showLoginDialog.value = false;
            },
            err => {
                ElMessage({
                    type: "error",
                    message: `出现错误${ERROR_CODE_MAP[err] ?? UNKNOWN_ERROR}`
                });
            }
        );
    }

    function handleLogout() {
        logout(
            csrfToken.value,
            () => {
                isLoggedIn.value = false;
                csrfToken.value = "";
                username.value = "";
                password.value = "";
                role.value = null;
                ElMessage({
                    type: "success",
                    message: "登出成功"
                });
            },
            err => {
                ElMessage({
                    type: "error",
                    message: `出现错误${ERROR_CODE_MAP[err] ?? UNKNOWN_ERROR}`
                });
            }
        );
    }
    return { isLoggedIn, csrfToken, username, password, role, showLoginDialog, handleLogin, handleLogout };
});
