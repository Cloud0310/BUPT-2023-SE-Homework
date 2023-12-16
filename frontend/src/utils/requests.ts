import axios, { AxiosResponse } from "axios";

export const API_BASE_URL = "http://localhost:11451/api";

// Instance Initialization --------------------------------------
const protocol = axios.create({
    baseURL: API_BASE_URL,
    timeout: 1000,
    withCredentials: true,
    responseType: "json"
});

protocol.interceptors.response.use(
    response => response.data,
    error => {
        if (error.response) {
            if (error.response.data) return Promise.reject(error.response.data.error_code);
            else return Promise.reject(error.response.status | 0x40000000);
        } else return Promise.reject(0x7fffffff);
    }
);

// API Functions ------------------------------------------------
export function login(
    username: string,
    password: string,
    successCallback: (data: any) => void,
    errorCallback: (errorCode: number) => void
) {
    protocol
        .post("/login", {
            username: username,
            password: password
        })
        .then(
            data => successCallback(data),
            errorCode => errorCallback(errorCode)
        );
}

function createWithCSRFToken(method: any, url: string, csrfToken: string, data: any): Promise<AxiosResponse> {
    return method(url, data, {
        headers: {
            "X-CSRF-Token": csrfToken
        }
    });
}

export function logout(csrfToken: string, successCallback: () => void, errorCallback: (errorCode: number) => void) {
    createWithCSRFToken(protocol.post, "/logout", csrfToken, {}).then(
        () => successCallback(),
        errorCode => errorCallback(errorCode)
    );
}

export function getAvailableDevices(
    csrfToken: string,
    successCallback: (data: any) => void,
    errorCallback: (errorCode: number) => void
) {
    createWithCSRFToken(protocol.get, "/admin/devices", csrfToken, {}).then(
        data => successCallback(data),
        errorCode => errorCallback(errorCode)
    );
}

export function getAvailableDevicesWithOpen(
    csrfToken: string,
    successCallback: (data: any) => void,
    errorCallback: (errorCode: number) => void
) {
    createWithCSRFToken(protocol.get, "/status", csrfToken, {}).then(
        data => successCallback(data),
        errorCode => errorCallback(errorCode)
    );
}

export function checkInRoom(
    csrfToken: string,
    room: string,
    successCallback: (data: any) => void,
    errorCallback: (errorCode: number) => void
) {
    createWithCSRFToken(protocol.post, "/room/check_in", csrfToken, {
        room: room
    }).then(
        data => successCallback(data),
        errorCode => errorCallback(errorCode)
    );
}

export function checkOutRoom(
    csrfToken: string,
    room: string,
    successCallback: (data: {
        room: string;
        report: { total_cost: number; total_duration: number; details: DeviceData[] };
    }) => void,
    errorCallback: (errorCode: number) => void
) {
    createWithCSRFToken(protocol.post, "/room/check_out", csrfToken, {
        room: room
    }).then(
        data =>
            successCallback(
                data as unknown as {
                    room: string;
                    report: { total_cost: number; total_duration: number; details: DeviceData[] };
                }
            ),
        errorCode => errorCallback(errorCode)
    );
}

export function getRoomStatus(
    csrfToken: string,
    room: string,
    successCallback: (data: any) => void,
    errorCallback: (errorCode: number) => void
) {
    createWithCSRFToken(protocol.get, `/status/${room}`, csrfToken, {}).then(
        data => successCallback(data),
        errorCode => errorCallback(errorCode)
    );
}

export function operationDevice(
    csrfToken: string,
    room: string,
    operation: string,
    data: any,
    successCallback: (data: any) => void,
    errorCallback: (errorCode: number) => void
) {
    createWithCSRFToken(protocol.post, `/admin/device/${room}`, csrfToken, {
        operation: operation,
        data: data
    }).then(
        data => successCallback(data),
        errorCode => errorCallback(errorCode)
    );
}

export interface DeviceData {
    start_time: string;
    end_time: string;
    temperature: number;
    wind_speed: number;
    mode: string;
    sweep: boolean;
    duration: number;
    cost: number;
}

export function addDevice(
    csrfToken: string,
    deviceData: any,
    successCallback: (data: any) => void,
    errorCallback: (errorCode: number) => void
) {
    createWithCSRFToken(protocol.put, "/admin/device", csrfToken, deviceData).then(
        data => successCallback(data),
        errorCode => errorCallback(errorCode)
    );
}

export function removeDevice(
    csrfToken: string,
    deviceData: any,
    successCallback: (data: any) => void,
    errorCallback: (errorCode: number) => void
) {
    protocol
        .request({
            url: "/admin/device",
            method: "delete",
            headers: {
                "X-CSRF-Token": csrfToken
            },
            data: deviceData
        })
        .then(
            data => successCallback(data),
            errorCode => errorCallback(errorCode)
        );
}

// Error Codes --------------------------------------------------
export const ERROR_CODE_MAP: { [errorCode: number]: string } = {
    // Fallback Error Codes
    0x7fffffff: "无法连接到服务器，请稍后再试！",
    1073742224: "API 请求格式错误，这可能是因为当前网页内存在问题。", // 0x40000000 + 400
    1073742225: "无法访问此 API 接入点：访问未授权。", // 0x40000000 + 401
    1073742227: "无法访问此 API 接入点：访问被阻止。", // 0x40000000 + 403
    1073742228: "无法访问服务器 API，请稍后再试！", // 0x40000000 + 404
    1073742229: "API 请求方法错误，这可能是因为当前网页内存在问题。", // 0x40000000 + 405
    1073742324: "服务器发生错误，请稍后再试！" // 0x40000000 + 500
    // Custom Error Codes
};

export const UNKNOWN_ERROR = "未知错误！";
