import axios from "axios";
export const http = axios.create({
    baseURL: "",
    timeout: 10000
});
export async function unwrap(request) {
    const response = await request;
    return response.data.data;
}
//# sourceMappingURL=http.js.map