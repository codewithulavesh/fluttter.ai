export interface Project {
  id: string;
  name: string;
  description: string;
  template: string;
  createdAt: Date;
  updatedAt: Date;
  thumbnail?: string;
}

export interface FileNode {
  id: string;
  name: string;
  type: 'file' | 'folder';
  children?: FileNode[];
  content?: string;
  language?: string;
}

export interface Variant {
  id: string;
  code: string;
  thumbnail: string;
  confidence: number;
}

export interface StylePreset {
  id: string;
  name: string;
  description: string;
  icon: string;
}

export interface DeviceFrame {
  id: string;
  name: string;
  width: number;
  height: number;
  type: 'phone' | 'tablet';
}

export interface GenerationRequest {
  prompt: string;
  style: string;
  temperature: number;
  variants: number;
}

export interface ConsoleLog {
  id: string;
  type: 'info' | 'warning' | 'error';
  message: string;
  timestamp: Date;
}
