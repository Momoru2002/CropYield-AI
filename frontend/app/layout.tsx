import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "CropYield-AI — Prediksi hasil panen dari data iklim & lahan",
  description:
    "Prediksi hasil panen (ton/hektar) berdasarkan curah hujan, suhu, pestisida, negara, dan jenis tanaman.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="id">
      <body>{children}</body>
    </html>
  );
}
