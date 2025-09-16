const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000/api';

export interface UploadResponse {
  success: boolean;
  message: string;
  filename: string;
  originalName: string;
  uploadType: string;
}

export interface PreferencesData {
  preferences: string;
}

export interface AttendanceData {
  totalClasses: number;
  attendedClasses: number;
  plannedAbsences: number;
  preferences: any;
}

export const apiService = {
  uploadFile: async (file: File, uploadType: 'calendar' | 'timetable'): Promise<UploadResponse> => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('uploadType', uploadType);

    const response = await fetch(`${API_BASE_URL}/upload`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      throw new Error('Upload failed');
    }

    return response.json();
  },

  savePreferences: async (preferences: string) => {
    const response = await fetch(`${API_BASE_URL}/preferences`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ preferences }),
    });

    if (!response.ok) {
      throw new Error('Failed to save preferences');
    }

    return response.json();
  },

  calculateAttendance: async (data: AttendanceData) => {
    const response = await fetch(`${API_BASE_URL}/calculate-attendance`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      throw new Error('Failed to calculate attendance');
    }

    return response.json();
  },

  // AI Chat functionality
  sendChatMessage: async (message: string, context: any = {}) => {
    const response = await fetch(`${API_BASE_URL}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message,
        context
      }),
    });

    if (!response.ok) {
      throw new Error('Failed to send chat message');
    }

    return response.json();
  },
};