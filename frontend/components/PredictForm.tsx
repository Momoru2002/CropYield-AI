"use client";

import { useState } from "react";
import styles from "../app/page.module.css";
import { CropOption, PredictRequest } from "../lib/api";

interface PredictFormProps {
  countries: string[];
  crops: CropOption[];
  yearRange: [number, number];
  loading: boolean;
  onSubmit: (payload: PredictRequest) => void;
}

export default function PredictForm({ countries, crops, yearRange, loading, onSubmit }: PredictFormProps) {
  const [country, setCountry] = useState(countries.includes("Indonesia") ? "Indonesia" : countries[0]);
  const [crop, setCrop] = useState(crops[0]?.value ?? "");
  const [year, setYear] = useState(yearRange[1]);
  const [rainfall, setRainfall] = useState(2000);
  const [pesticides, setPesticides] = useState(5000);
  const [temp, setTemp] = useState(26);

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    onSubmit({
      country,
      crop,
      year,
      rainfall_mm: rainfall,
      pesticides_tonnes: pesticides,
      avg_temp_c: temp,
    });
  }

  return (
    <form className={styles.form} onSubmit={handleSubmit}>
      <div className={styles.field}>
        <label className={styles.label} htmlFor="country">
          Negara
        </label>
        <select id="country" className={styles.select} value={country} onChange={(e) => setCountry(e.target.value)}>
          {countries.map((c) => (
            <option key={c} value={c}>
              {c}
            </option>
          ))}
        </select>
      </div>

      <div className={styles.field}>
        <label className={styles.label} htmlFor="crop">
          Jenis tanaman
        </label>
        <select id="crop" className={styles.select} value={crop} onChange={(e) => setCrop(e.target.value)}>
          {crops.map((c) => (
            <option key={c.value} value={c.value}>
              {c.label}
            </option>
          ))}
        </select>
      </div>

      <div className={styles.field}>
        <label className={styles.label} htmlFor="year">
          Tahun tanam
        </label>
        <input
          id="year"
          type="number"
          className={styles.input}
          value={year}
          min={yearRange[0]}
          max={yearRange[1] + 5}
          onChange={(e) => setYear(Number(e.target.value))}
        />
      </div>

      <div className={styles.field}>
        <label className={styles.label} htmlFor="rainfall">
          Curah hujan tahunan
        </label>
        <input
          id="rainfall"
          type="number"
          className={styles.input}
          value={rainfall}
          min={0}
          onChange={(e) => setRainfall(Number(e.target.value))}
        />
        <span className={styles.hint}>mm/tahun</span>
      </div>

      <div className={styles.field}>
        <label className={styles.label} htmlFor="pesticides">
          Penggunaan pestisida
        </label>
        <input
          id="pesticides"
          type="number"
          className={styles.input}
          value={pesticides}
          min={0}
          onChange={(e) => setPesticides(Number(e.target.value))}
        />
        <span className={styles.hint}>ton (skala nasional/regional)</span>
      </div>

      <div className={styles.field}>
        <label className={styles.label} htmlFor="temp">
          Suhu rata-rata
        </label>
        <input
          id="temp"
          type="number"
          step="0.1"
          className={styles.input}
          value={temp}
          onChange={(e) => setTemp(Number(e.target.value))}
        />
        <span className={styles.hint}>°C</span>
      </div>

      <div className={styles.submitRow}>
        <button type="submit" className={styles.submitBtn} disabled={loading || !crop}>
          {loading ? "Menghitung..." : "Prediksi hasil panen"}
        </button>
      </div>
    </form>
  );
}
