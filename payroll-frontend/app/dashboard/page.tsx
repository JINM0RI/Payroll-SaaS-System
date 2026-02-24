"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { useRouter } from "next/navigation";

export default function DashboardPage() {
  const router = useRouter();

  const [totalEmployees, setTotalEmployees] = useState<number>(0);
  const [recentActivity, setRecentActivity] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem("access_token");

    // Protect dashboard
    if (!token) {
      router.push("/");
      return;
    }

    fetchDashboard();
  }, []);

  const fetchDashboard = async () => {
    try {
      const response = await api.get("/dashboard/stats");
      setTotalEmployees(response.data.total_active_employees);
      setRecentActivity(response.data.recent_activity);
    } catch (error) {
      console.error("Failed to load dashboard");
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    router.push("/");
  };

  return (
    <div className="bg-gray-100 min-h-screen relative">

  {/* Logout Button - Top Right */}
  <div className="absolute top-6 right-8">
    <button
      onClick={handleLogout}
      className="bg-red-500 text-white px-4 py-2 rounded-md hover:bg-red-600 transition"
    >
      Logout
    </button>
  </div>

  <div className="py-10 px-6">
    <div className="max-w-6xl mx-auto">

          {/* Logo Section */}
          <div className="flex flex-col items-center justify-center mb-12">
            <img
              src="/logo.png"
              alt="Company Logo"
              className="w-64 md:w-80 object-contain"
            />
          </div>

          {loading ? (
            <p>Loading...</p>
          ) : (
            <>
              {/* KPI Card */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-10">
                <div className="bg-white p-6 rounded-2xl shadow-md">
                  <h2 className="text-gray-500 text-sm mb-2">
                    Total Active Employees
                  </h2>
                  <p className="text-3xl font-bold text-black">
                    {totalEmployees}
                  </p>
                </div>
              </div>

              {/* Recent Activity */}
              <div className="bg-white p-6 rounded-2xl shadow-md">
                <h2 className="text-lg font-semibold mb-4 text-black">
                  Recent Activity
                </h2>

                <ul className="space-y-2 text-gray-700">
                  {recentActivity.map((activity, index) => (
                    <li key={index}>
                      • {activity}
                    </li>
                  ))}
                </ul>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}