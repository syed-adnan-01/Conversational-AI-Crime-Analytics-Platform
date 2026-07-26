import api from "@/lib/api";

export interface UploadRecord {
  file_id: string;
  filename: string;
  category: string;
  content_type: string;
  size_bytes: number;
  storage_provider: string;
  case_id?: string;
  uploaded_at: string;
}

export interface UploadHealth {
  status: string;
  active_provider: string;
}

export const uploadService = {
  uploadFile: (file: File, category: string, caseId?: string): Promise<UploadRecord> => {
    const formData = new FormData();
    formData.append("file", file);
    formData.append("category", category);
    if (caseId) {
      formData.append("case_id", caseId);
    }
    return api.post<UploadRecord>("/uploads", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    }).then((res) => res.data);
  },

  listUploads: (category?: string, caseId?: string): Promise<UploadRecord[]> => {
    const params = new URLSearchParams();
    if (category) params.append("category", category);
    if (caseId) params.append("case_id", caseId);
    return api.get<UploadRecord[]>(`/uploads?${params.toString()}`).then((res) => res.data);
  },

  getUploadMetadata: (fileId: string): Promise<UploadRecord> =>
    api.get<UploadRecord>(`/uploads/${fileId}`).then((res) => res.data),

  getHealth: (): Promise<UploadHealth> =>
    api.get<UploadHealth>("/uploads/health").then((res) => res.data),

  deleteUpload: (fileId: string): Promise<void> =>
    api.delete<void>(`/uploads/${fileId}`).then((res) => res.data),
};
