// "use client";

// import { useEffect, useState } from "react";
// import Link from "next/link";
// import { api } from "@/lib/api";

// interface Employee {
//   id: number;
//   emp_id: string;
//   name: string;
//   email: string;
// }

// export default function EmployeesPage() {
//   const [employees, setEmployees] = useState<Employee[]>([]);
//   const [loading, setLoading] = useState(true);

//   useEffect(() => {
//     fetchEmployees();
//   }, []);

//   const fetchEmployees = async () => {
//     try {
//       const response = await api.get("/employees");
//       setEmployees(response.data);
//     } catch (error) {
//       console.error("Failed to fetch employees");
//     } finally {
//       setLoading(false);
//     }
//   };

//   return (
//     <div className="bg-gray-100 min-h-screen py-12 px-6">

//       <div className="max-w-5xl mx-auto bg-white p-8 rounded-2xl shadow-lg">

//         {/* Header */}
//         <div className="flex justify-between items-center mb-8">
//           <h1 className="text-2xl font-bold text-black">
//             Employees
//           </h1>

//           <Link
//             href="/dashboard/employees/add"
//             className="bg-black text-white px-4 py-2 rounded-md hover:bg-gray-800 transition"
//           >
//             + Add Employee
//           </Link>
//         </div>

//         {/* Table */}
//         {loading ? (
//           <p>Loading...</p>
//         ) : employees.length === 0 ? (
//           <p className="text-gray-500">No employees found.</p>
//         ) : (
//           <div className="overflow-x-auto">
//             <table className="w-full border-collapse">

//               <thead>
//                 <tr className="bg-gray-200 text-left">
//                   <th className="p-3 text-black">Employee ID</th>
//                   <th className="p-3 text-black">Name</th>
//                   <th className="p-3 text-black">Email</th>
//                 </tr>
//               </thead>

//               <tbody>
//                 {employees.map((emp) => (
//                   <tr
//                     key={emp.id}
//                     className="border-t hover:bg-gray-50 transition"
//                   >
//                     <td className="p-3 text-black">{emp.emp_id}</td>
//                     <td className="p-3 text-black">{emp.name}</td>
//                     <td className="p-3 text-black">{emp.email}</td>
//                   </tr>
//                 ))}
//               </tbody>

//             </table>
//           </div>
//         )}

//       </div>
//     </div>
//   );
// }

"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { api } from "@/lib/api";
import { deleteEmployee } from "@/lib/api";

interface Employee {
  id: number;
  emp_id: string;
  name: string;
  email: string;
}

export default function EmployeesPage() {
  const [employees, setEmployees] = useState<Employee[]>([]);
  const [loading, setLoading] = useState(true);

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

  const handleDelete = async (id: string) => {
  const confirmDelete = window.confirm("Are you sure?");
    if (!confirmDelete) return;

      const password = window.prompt("Enter admin password:");
    if (!password) return;

      try {
        await deleteEmployee(id, password);
        alert("Deleted successfully");
        fetchEmployees(); // refresh list
      } catch (error) {
        alert("Unable to delete");
        console.error(error);
      }
    };

  return (
    <div className="bg-gray-100 min-h-screen py-12 px-6">

      <div className="max-w-5xl mx-auto bg-white p-8 rounded-2xl shadow-lg">

        {/* Header */}
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-2xl font-bold text-black">
            Employees
          </h1>

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
                        onClick={() => handleDelete(emp.id.toString())}
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
    </div>
  );
}