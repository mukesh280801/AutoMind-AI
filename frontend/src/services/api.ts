const BASE_URL = "http://127.0.0.1:8000";

export async function getBackendStatus() {
  const response = await fetch(`${BASE_URL}/api/status`);

  if (!response.ok) {
    throw new Error("Failed to fetch backend status");
  }

  return response.json();
}

export async function uploadPDF(file: File) {
  const formData = new FormData();

  formData.append("file", file);

  const response = await fetch(`${BASE_URL}/api/upload`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error("Upload Failed");
  }

  return response.json();
}