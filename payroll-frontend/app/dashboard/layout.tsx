"use client";

import { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const [open, setOpen] = useState(false);
  const pathname = usePathname();

  const menuItems = [
    { name: "Home", path: "/dashboard" },
    { name: "Pay Slip Generator", path: "/dashboard/payslip-generator" },
    { name: "Employees", path: "/dashboard/employees" },
  ];

  return (
    <div className="h-screen bg-slate-100 relative">

      {/* Hamburger - FIXED */}
      <button
        onClick={() => setOpen(!open)}
        className="fixed top-6 left-6 z-50 p-2 rounded-md hover:bg-slate-200 transition"
      >
        <div className="space-y-1">
          <div className="w-6 h-0.5 bg-slate-900"></div>
          <div className="w-6 h-0.5 bg-slate-900"></div>
          <div className="w-6 h-0.5 bg-slate-900"></div>
        </div>
      </button>

      {/* Sidebar */}
      <div
        className={`fixed top-0 left-0 h-full w-64 bg-white shadow-xl transition-transform duration-300 ease-in-out z-40
        ${open ? "translate-x-0" : "-translate-x-full"}`}
      >
        <div className="p-6 pt-24">
          <nav className="flex flex-col space-y-3">
            {menuItems.map((item) => (
              <Link
                key={item.name}
                href={item.path}
                onClick={() => setOpen(false)}
                className={`px-4 py-3 rounded-lg transition-all duration-200
                  ${
                    pathname === item.path
                      ? "bg-indigo-600 text-white"
                      : "text-slate-700 hover:bg-slate-200 hover:text-slate-900"
                  }`}
              >
                {item.name}
              </Link>
            ))}
          </nav>
        </div>
      </div>

      {/* Overlay */}
      {open && (
        <div
          onClick={() => setOpen(false)}
          className="fixed inset-0 bg-black/30 z-30"
        />
      )}

      {/* Main Content */}
      <div className="pt-20 px-10 h-full overflow-auto">
        {children}
      </div>

    </div>
  );
}