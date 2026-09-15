const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface CropOption {
  value: string;
  label: string;
}

export interface OptionsResponse {
  countries: string[];
  crops: CropOption[];
  year_range: [number, number];
  model_r2: number;
}

export interface PredictRequest {
  country: string;
  crop: string;
  year: number;
  rainfall_mm: number;
  pesticides_tonnes: number;
  avg_temp_c: number;
}

export interface PredictResponse {
  predicted_yield_hg_per_ha: number;
  predicted_yield_tons_per_ha: number;
  range_low_tons_per_ha: number;
  range_high_tons_per_ha: number;
}

export class ApiError extends Error {
  status: number;
  constructor(message: string, status: number) {
    super(message);
    this.status = status;
  }
}

async function handle<T>(res: Response): Promise<T> {
  if (!res.ok) {
    const body = await res.json().catch(() => ({ detail: "Terjadi kesalahan tak terduga." }));
    const detail =
      typeof body.detail === "string" ? body.detail : "Input tidak valid, periksa kembali nilainya.";
    throw new ApiError(detail, res.status);
  }
  return res.json();
}

export async function fetchOptions(): Promise<OptionsResponse> {
  const res = await fetch(`${API_BASE}/yield/options`);
  return handle<OptionsResponse>(res);
}

export async function predictYield(payload: PredictRequest): Promise<PredictResponse> {
  const res = await fetch(`${API_BASE}/yield/predict`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  return handle<PredictResponse>(res);
}
