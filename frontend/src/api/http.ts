import axios from "axios";

export const http = axios.create({
  baseURL: "",
  timeout: 10000
});

export async function unwrap<T>(request: Promise<{ data: { data: T } }>): Promise<T> {
  const response = await request;
  return response.data.data;
}
