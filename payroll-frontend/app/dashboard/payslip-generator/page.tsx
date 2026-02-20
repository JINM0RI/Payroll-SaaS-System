"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { api } from "@/lib/api";

export default function PaySlipGeneratorPage(){
  const router = useRouter();
  const [file, setFile] = useState<File | null>(null);
  const [message, setMessage] = useState("");
  const [generatedFiles, setGeneratedFiles] = useState<string[]>([]);
  const [previewFile, setPreviewFile] = useState<string | null>(null);

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      router.push("/login");
    }
  }, []);

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a file");
      return;
    }

    try {
      const token = localStorage.getItem("token");

      const formData = new FormData();
      formData.append("file", file);

      const response = await api.post(
        "/payroll/upload-salary",
        formData,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      setMessage(response.data.message);
      setGeneratedFiles(response.data.files); // IMPORTANT

    } catch (error: any) {
      console.error(error);
      setMessage("Upload failed");
    }
  };

  const handleDownloadAll = () => {
    window.open("http://localhost:8000/payroll/download-all", "_blank");
  };

  return (
  <div className="bg-gray-100 min-h-screen py-12 px-6">

    {/* Page Header */}
    <div className="max-w-md mx-auto">
      <h1 className="text-3xl font-bold mb-8 text-black">
        Pay Slip Generator
      </h1>

      {/* Card */}
      <div className="bg-white p-8 rounded-2xl shadow-lg max-w-md mx-auto">
        <h2 className="text-xl font-semibold mb-6 text-black">
          Upload Salary Excel
        </h2>

        <label className="block mb-6">
          <span className="sr-only">Choose file</span>
          <input
            type="file"
            accept=".xlsx,.xls"
            onChange={(e) =>
              setFile(e.target.files ? e.target.files[0] : null)
            }
            className="block w-full text-sm text-gray-900
                      file:mr-4 file:py-2 file:px-4
                      file:rounded-md file:border-0
                      file:text-sm file:font-semibold
                      file:bg-black file:text-white
                      hover:file:bg-gray-800"
          />
        </label>

        <button
          onClick={handleUpload}
          className="w-full bg-black text-white py-2 rounded-md hover:bg-gray-800 transition"
        >
          Upload
        </button>

        {message && (
          <p className="mt-4 text-green-600">
            {message}
          </p>
        )}

        {generatedFiles.length > 0 && (
          <div className="mt-8">
            <h3 className="font-semibold mb-3 text-black">
              Generated Payslips
            </h3>

            <ul className="space-y-2">
              {generatedFiles.map((fileName, index) => (
                <li
                  key={index}
                  className="text-blue-600 cursor-pointer hover:underline"
                  onClick={() => setPreviewFile(fileName)}
                >
                  {fileName}
                </li>
              ))}
            </ul>

            <button
              onClick={handleDownloadAll}
              className="mt-6 w-full bg-green-600 text-white py-2 rounded-md hover:bg-green-700 transition"
            >
              Download All
            </button>
          </div>
        )}
      </div>
    </div>

    {/* Preview Modal (UNCHANGED) */}
    {previewFile && (
      <div className="fixed inset-0 bg-black bg-opacity-60 flex items-center justify-center z-50">
        <div className="bg-white w-4/5 h-4/5 rounded-xl shadow-xl flex flex-col">

          <div className="flex justify-between items-center px-6 py-3 border-b">
            <h3 className="font-semibold text-lg">
              {previewFile}
            </h3>

            <button
              onClick={() => setPreviewFile(null)}
              className="text-gray-400 hover:text-red-600 text-2xl transition duration-200"
            >
              ×
            </button>
          </div>

          <div className="flex-1">
            <iframe
              src={`http://127.0.0.1:8000/payroll/preview/${previewFile}`}
              className="w-full h-full rounded-b-xl"
            />
          </div>

        </div>
      </div>
    )}

  </div>
);
}
