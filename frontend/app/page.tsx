"use client";

import { useEffect, useState } from "react";
import styles from "./page.module.css";
import PredictForm from "../components/PredictForm";
import { ApiError, OptionsResponse, PredictRequest, PredictResponse, fetchOptions, predictYield } from "../lib/api";

export default function Home() {
  const [options, setOptions] = useState<OptionsResponse | null>(null);
  const [optionsError, setOptionsError] = useState<string | null>(null);
  const [result, setResult] = useState<PredictResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchOptions()
      .then(setOptions)
      .catch(() => setOptionsError("Tidak bisa terhubung ke server prediksi. Pastikan backend berjalan."));
  }, []);

  async function handleSubmit(payload: PredictRequest) {
    setError(null);
    setResult(null);
    setLoading(true);
    try {
      const res = await predictYield(payload);
      setResult(res);
    } catch (e) {
      setError(e instanceof ApiError ? e.message : "Gagal menghitung prediksi.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className={styles.page}>
      <header className={styles.header}>
        <div className={styles.mark} aria-hidden="true" />
        <span className={styles.wordmark}>
          CropYield<span>-AI</span>
        </span>
      </header>

      <section className={styles.hero}>
        <h1 className={styles.headline}>Prediksi hasil panen dari data iklim &amp; lahan</h1>
        <p className={styles.subhead}>
          Masukkan negara, jenis tanaman, curah hujan, suhu, dan penggunaan pestisida — dapatkan estimasi
          hasil panen dalam ton per hektar.
        </p>
        {options && (
          <span className={styles.r2Badge}>R² model: {options.model_r2.toFixed(3)} pada data uji</span>
        )}
      </section>

      {optionsError && <div className={styles.errorBox}>{optionsError}</div>}

      {options && (
        <PredictForm
          countries={options.countries}
          crops={options.crops}
          yearRange={options.year_range}
          loading={loading}
          onSubmit={handleSubmit}
        />
      )}

      {error && <div className={styles.errorBox}>{error}</div>}

      {result && <ResultCard result={result} />}

      <section className={styles.section}>
        <h2 className={styles.sectionTitle}>Cara kerja</h2>
        <div className={styles.stepGrid}>
          <div className={styles.step}>
            <span className={styles.stepNum}>01</span>
            <h3 className={styles.stepTitle}>Masukkan data</h3>
            <p className={styles.stepText}>Negara, jenis tanaman, tahun, curah hujan, suhu, dan pestisida.</p>
          </div>
          <div className={styles.step}>
            <span className={styles.stepNum}>02</span>
            <h3 className={styles.stepTitle}>Model menghitung</h3>
            <p className={styles.stepText}>
              Gradient boosting yang dilatih pada 28.000+ data historis FAO &amp; World Bank dari 101 negara.
            </p>
          </div>
          <div className={styles.step}>
            <span className={styles.stepNum}>03</span>
            <h3 className={styles.stepTitle}>Lihat estimasi</h3>
            <p className={styles.stepText}>Hasil panen dalam ton/hektar beserta rentang estimasinya.</p>
          </div>
        </div>
      </section>

      <footer className={styles.footer}>
        <span>Model dilatih pada data historis FAO &amp; World Bank — hasil aktual dapat berbeda tergantung faktor lapangan.</span>
        <a href="https://github.com/Momoru2002/CropYield-AI" target="_blank" rel="noreferrer">
          Lihat kode sumber
        </a>
      </footer>
    </main>
  );
}

function ResultCard({ result }: { result: PredictResponse }) {
  const { predicted_yield_tons_per_ha, range_low_tons_per_ha, range_high_tons_per_ha } = result;
  const span = range_high_tons_per_ha - range_low_tons_per_ha || 1;
  const markerPct = ((predicted_yield_tons_per_ha - range_low_tons_per_ha) / span) * 100;

  return (
    <div className={styles.resultCard}>
      <p className={styles.resultLabel}>Estimasi hasil panen</p>
      <p className={styles.resultValue}>
        {predicted_yield_tons_per_ha.toFixed(2)}
        <span className={styles.resultUnit}>ton/ha</span>
      </p>

      <div className={styles.rangeTrack}>
        <div className={styles.rangeFill} style={{ left: 0, width: "100%" }} />
        <div className={styles.rangeMarker} style={{ left: `calc(${markerPct}% - 1px)` }} />
      </div>
      <div className={styles.rangeLabels}>
        <span>{range_low_tons_per_ha.toFixed(2)} ton/ha</span>
        <span>{range_high_tons_per_ha.toFixed(2)} ton/ha</span>
      </div>
    </div>
  );
}
