"use client";

import { useState } from "react";
import { api } from "@/lib/api";
import { useRouter } from "next/navigation";

export default function LoginPage() {
  const router = useRouter();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  // Register modal states
  const [showRegister, setShowRegister] = useState(false);
  const [adminPassword, setAdminPassword] = useState("");
  const [isFirstUser, setIsFirstUser] = useState(false);

  const handleLogin = async () => {
    try {
      const response = await api.post("/auth/login", {
        email,
        password,
      });

      localStorage.setItem("access_token", response.data.access_token);
      router.push("/dashboard");
    } catch (err: any) {
      setError("Invalid credentials");
    }
  };

  const openRegister = async () => {
    try {
      const res = await api.get("/auth/user-count");
      if (res.data.count === 0) {
        setIsFirstUser(true);
      } else {
        setIsFirstUser(false);
      }
    } catch (err) {
      console.error("Failed to check user count");
    }

    setShowRegister(true);
  };

  const handleRegister = async () => {
    try {
      await api.post("/auth/register", {
        email,
        password,
        admin_password: isFirstUser ? null : adminPassword,
      });

      alert("User registered successfully!");
      setShowRegister(false);
      setAdminPassword("");
    } catch (err: any) {
      alert("Registration failed");
    }
  };

  return (
    <div className="flex items-center justify-center h-screen bg-gray-100">
      <div className="bg-white p-8 rounded-xl shadow-md w-96">
        <h2 className="text-2xl font-bold mb-6 text-center text-black">
          Payroll System
        </h2>

        {error && (
          <p className="text-red-500 text-sm mb-4 text-center">
            {error}
          </p>
        )}

        <input
          type="email"
          placeholder="Email"
          className="w-full mb-4 p-2 border rounded-md text-black"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />

        <input
          type="password"
          placeholder="Password"
          className="w-full mb-4 p-2 border rounded-md text-black"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <button
          onClick={handleLogin}
          className="w-full bg-black bg-black p-2 rounded-md hover:bg-gray-800 mb-3"
        >
          Login
        </button>

        <button
          onClick={openRegister}
          className="w-full bg-black bg-black p-2 rounded-md hover:bg-gray-300"
        >
          Register
        </button>
      </div>

      {/* REGISTER MODAL */}
      {showRegister && (
        <div className="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center">
          <div className="bg-white p-6 rounded-xl w-96">
            <h2 className="text-lg font-semibold mb-4 text-black">
              Register User
            </h2>

            {!isFirstUser && (
              <input
                type="password"
                placeholder="Admin Password"
                value={adminPassword}
                onChange={(e) => setAdminPassword(e.target.value)}
                className="w-full border p-2 rounded mb-3 text-black"
              />
            )}

            <div className="flex justify-end gap-2">
              <button
                onClick={() => setShowRegister(false)}
                className="px-4 py-2 bg-red-600 text-white rounded"
              >
                Cancel
              </button>

              <button
                onClick={handleRegister}
                className="px-4 py-2 bg-black text-white rounded"
              >
                Register
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}