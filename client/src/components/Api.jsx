export const API = import.meta.env.VITE_API_URL;

export function apiUrl(path) {
  return `${API}${path.startsWith("/") ? "" : "/"}${path}`;
}