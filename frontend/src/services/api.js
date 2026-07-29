import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:8000",
});

export async function createJob(formData) {
  const response = await api.post("/generate", formData);
  return response.data;
}

export async function getJob(jobId) {
  const response = await api.get(`/jobs/${jobId}`);
  return response.data;
}

export function getGeneratedImageUrl(imagePath) {
  if (!imagePath) {
    return null;
  }

  if (imagePath.startsWith("http://") || imagePath.startsWith("https://")) {
    return imagePath;
  }

  const normalizedPath = imagePath.replace(/^generated\//, "/generated/");
  return `${api.defaults.baseURL}${normalizedPath}`;
}
