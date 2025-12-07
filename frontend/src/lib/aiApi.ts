/**
 * API Client for Flutter AI Code Generator
 * Connects frontend to the FastAPI backend
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export interface GenerateRequest {
    prompt: string;
    temperature?: number;
    max_tokens?: number;
    num_variants?: number;
    style?: string;
}

export interface CodeVariant {
    id: string;
    code: string;
    description: string;
    score: number;
}

export interface GenerateResponse {
    variants: CodeVariant[];
    prompt: string;
    generated_at: string;
}

export interface HealthResponse {
    status: string;
    model_loaded: boolean;
    device: string;
    timestamp: string;
}

export interface ModelInfo {
    base_model: string;
    fine_tuned: boolean;
    model_path: string | null;
    device: string;
    model_type: string;
}

class AIApiClient {
    private baseUrl: string;

    constructor(baseUrl: string = API_BASE_URL) {
        this.baseUrl = baseUrl;
    }

    /**
     * Check API health status
     */
    async healthCheck(): Promise<HealthResponse> {
        const response = await fetch(`${this.baseUrl}/health`);
        if (!response.ok) {
            throw new Error('Health check failed');
        }
        return response.json();
    }

    /**
     * Generate Flutter code variants from a prompt
     */
    async generateCode(request: GenerateRequest): Promise<GenerateResponse> {
        const response = await fetch(`${this.baseUrl}/api/generate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                prompt: request.prompt,
                temperature: request.temperature ?? 0.7,
                max_tokens: request.max_tokens ?? 512,
                num_variants: request.num_variants ?? 3,
                style: request.style ?? 'lovable',
            }),
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to generate code');
        }

        return response.json();
    }

    /**
     * Refine existing code based on instructions
     */
    async refineCode(code: string, instructions: string): Promise<{ refined_code: string }> {
        const response = await fetch(`${this.baseUrl}/api/refine`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ code, instructions }),
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to refine code');
        }

        return response.json();
    }

    /**
     * Get model information
     */
    async getModelInfo(): Promise<ModelInfo> {
        const response = await fetch(`${this.baseUrl}/api/model/info`);
        if (!response.ok) {
            throw new Error('Failed to get model info');
        }
        return response.json();
    }
}

// Export singleton instance
export const aiApi = new AIApiClient();

// Export class for testing
export { AIApiClient };
