"use client";

import { useCallback, useState } from "react";
import { useDropzone } from "react-dropzone";
import { documentsAPI } from "@/lib/api";

interface FileUploadProps {
  dealId: string;
  onUploadComplete?: () => void;
}

const categories = [
  { value: "pitch_deck", label: "Pitch Deck" },
  { value: "financials", label: "Financial Statements" },
  { value: "cap_table", label: "Cap Table" },
  { value: "legal", label: "Legal Documents" },
  { value: "market_report", label: "Market Report" },
  { value: "other", label: "Other" },
];

export function FileUpload({ dealId, onUploadComplete }: FileUploadProps) {
  const [uploading, setUploading] = useState(false);
  const [category, setCategory] = useState("pitch_deck");

  const onDrop = useCallback(
    async (acceptedFiles: File[]) => {
      setUploading(true);
      try {
        for (const file of acceptedFiles) {
          await documentsAPI.upload(dealId, file, category);
        }
        onUploadComplete?.();
      } catch (err) {
        console.error("Upload failed:", err);
      } finally {
        setUploading(false);
      }
    },
    [dealId, category, onUploadComplete]
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      "application/pdf": [".pdf"],
      "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": [".xlsx"],
      "text/csv": [".csv"],
      "application/vnd.openxmlformats-officedocument.wordprocessingml.document": [".docx"],
      "application/vnd.openxmlformats-officedocument.presentationml.presentation": [".pptx"],
    },
  });

  return (
    <div className="space-y-4">
      <select
        value={category}
        onChange={(e) => setCategory(e.target.value)}
        className="input"
      >
        {categories.map((c) => (
          <option key={c.value} value={c.value}>{c.label}</option>
        ))}
      </select>

      <div
        {...getRootProps()}
        className={`border-2 border-dashed rounded-xl p-8 text-center cursor-pointer transition-colors ${
          isDragActive ? "border-brand-500 bg-brand-50" : "border-gray-300 hover:border-gray-400"
        }`}
      >
        <input {...getInputProps()} />
        {uploading ? (
          <p className="text-gray-500">Uploading...</p>
        ) : isDragActive ? (
          <p className="text-brand-600 font-medium">Drop files here</p>
        ) : (
          <div>
            <p className="text-gray-600 font-medium">Drag & drop files here</p>
            <p className="text-gray-400 text-sm mt-1">PDF, XLSX, CSV, DOCX, PPTX</p>
          </div>
        )}
      </div>
    </div>
  );
}
