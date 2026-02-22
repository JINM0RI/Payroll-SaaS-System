"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { api, deleteEmployee } from "@/lib/api";

interface Employee {
  id: number;
  emp_id: string;
  name: string;
  email: string;
}

export default function EmployeesPage() {
  const [employees, setEmployees] = useState<Employee[]>([]);
  const [loading, setLoading] = useState(true);

  // Modal state
  const [showModal, setShowModal] = useState(false);
  const [selectedEmployee, setSelectedEmployee] = useState<string | null>(null);
  const [adminPassword, setAdminPassword] = useState("");
  const [deleteLoading, setDeleteLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  useEffect(() => {
    fetchEmployees();
  }, []);

  const fetchEmployees = async () => {
    try {
      const response = await api.get("/employees");
      setEmployees(response.data);
    } catch (error) {
      console.error("Failed to fetch employees");
    } finally {
      setLoading(false);
    }
  };

  const openDeleteModal = (id: string) => {
    setSelectedEmployee(id);
    setAdminPassword("");
    setErrorMessage("");
    setShowModal(true);
  };

  const confirmDelete = async () => {
    if (!selectedEmployee) return;

    setDeleteLoading(true);
    setErrorMessage("");

    try {
      await deleteEmployee(selectedEmployee, adminPassword);
      setShowModal(false);
      fetchEmployees();
    } catch (error) {
      setErrorMessage("Incorrect password or unable to delete.");
    } finally {
      setDeleteLoading(false);
    }
  };

  return (
    <div className="bg-gray-100 min-h-screen py-12 px-6">
      <div className="max-w-5xl mx-auto bg-white p-8 rounded-2xl shadow-lg">

        {/* Header */}
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-2xl font-bold text-black">Employees</h1>

          <Link
            href="/dashboard/employees/add"
            className="bg-black text-white px-4 py-2 rounded-md hover:bg-gray-800 transition"
          >
            + Add Employee
          </Link>
        </div>

        {/* Table */}
        {loading ? (
          <p>Loading...</p>
        ) : employees.length === 0 ? (
          <p className="text-gray-500">No employees found.</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full border-collapse">
              <thead>
                <tr className="bg-gray-200 text-left">
                  <th className="p-3 text-black">Employee ID</th>
                  <th className="p-3 text-black">Name</th>
                  <th className="p-3 text-black">Email</th>
                  <th className="p-3 text-black">Actions</th>
                </tr>
              </thead>

              <tbody>
                {employees.map((emp) => (
                  <tr
                    key={emp.id}
                    className="border-t hover:bg-gray-50 transition"
                  >
                    <td className="p-3 text-black">{emp.emp_id}</td>
                    <td className="p-3 text-black">{emp.name}</td>
                    <td className="p-3 text-black">{emp.email}</td>
                    <td className="p-3">
                      <button
                        className="bg-red-500 text-white px-3 py-1 rounded hover:bg-red-600 transition"
                        onClick={() => openDeleteModal(emp.id.toString())}
                      >
                        Delete
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* DELETE MODAL */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50">
          <div className="bg-white p-6 rounded-xl w-96 shadow-lg">

            <h2 className="text-lg font-semibold mb-4 text-black">
              Confirm Delete
            </h2>

            <p className="text-sm text-gray-600 mb-4">
              Enter password to delete this employee.
            </p>

            <input
              type="password"
              placeholder="Admin Password"
              value={adminPassword}
              onChange={(e) => setAdminPassword(e.target.value)}
              className="w-full border p-2 rounded mb-3 text-black placeholder:text-black"
            />

            {errorMessage && (
              <p className="text-red-500 text-sm mb-3">{errorMessage}</p>
            )}

            <div className="flex justify-end gap-2">
              <button
                onClick={() => setShowModal(false)}
                className="px-4 py-2 bg-black text-white rounded"
                disabled={deleteLoading}
              >
                Cancel
              </button>

              <button
                onClick={confirmDelete}
                className="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700 transition"
                disabled={deleteLoading}
              >
                {deleteLoading ? "Deleting..." : "Confirm Delete"}
              </button>
            </div>

          </div>
        </div>
      )}
    </div>
  );
}