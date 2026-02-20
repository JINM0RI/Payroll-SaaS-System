// "use client";

// import { useState } from "react";
// import { useRouter } from "next/navigation";
// import { api } from "@/lib/api";

// export default function AddEmployeePage() {
//   const router = useRouter();

//   const [formData, setFormData] = useState({
//     name: "",
//     email: "",
//   });

//   const [password, setPassword] = useState("");
//   const [loading, setLoading] = useState(false);

//   const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
//     setFormData({
//       ...formData,
//       [e.target.name]: e.target.value,
//     });
//   };

//   const handleSubmit = async () => {
//     if (!formData.name) {
//       alert("Name is required");
//       return;
//     }

//     if (!password) {
//       alert("Please enter your password to confirm");
//       return;
//     }

//     try {
//       setLoading(true);

//       await api.post("/employees/", {
//       name: formData.name,
//       email: formData.email || null,
//       password: password,
//     });

//       router.push("/dashboard/employees");

//     } catch (error: any) {
//       if (error.response?.status === 403) {
//         alert("Invalid password");
//       } else {
//         alert("Failed to add employee");
//       }
//     } finally {
//       setLoading(false);
//     }
//   };

//   return (
//     <div className="bg-gray-100 min-h-screen py-12 px-6">
//       <div className="max-w-md mx-auto bg-white p-8 rounded-2xl shadow-lg">

//         <h1 className="text-2xl font-bold mb-8 text-black">
//           Add Employee
//         </h1>

//         <input
//           type="text"
//           name="name"
//           placeholder="Employee Name"
//           value={formData.name}
//           onChange={handleChange}
//           className="w-full mb-4 p-3 border rounded-md"
//         />

//         <input
//           autoComplete="off"
//           type="email"
//           name="email"
//           placeholder="Employee Email (Optional)"
//           value={formData.email}
//           onChange={handleChange}
//           className="w-full mb-4 p-3 border rounded-md"
//         />

//         <input
//           type="password"
//           autoComplete="new-password"
//           placeholder="Enter your password to confirm"
//           value={password}
//           onChange={(e) => setPassword(e.target.value)}
//           className="w-full mb-6 p-3 border rounded-md"
//         />

//         <button
//           onClick={handleSubmit}
//           disabled={loading}
//           className="w-full bg-black text-white py-3 rounded-md hover:bg-gray-800 transition disabled:opacity-50"
//         >
//           {loading ? "Saving..." : "Save Employee"}
//         </button>

//       </div>
//     </div>
//   );
// }

"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { api } from "@/lib/api";

export default function AddEmployeePage() {
  const router = useRouter();

  const [formData, setFormData] = useState({
    name: "",
    email: "",
  });

  const [loading, setLoading] = useState(false);

  // ------------------------
  // Handle input change
  // ------------------------
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  // ------------------------
  // Handle form submission
  // ------------------------
  const handleSubmit = async () => {
    if (!formData.name) {
      alert("Name is required");
      return;
    }

    try {
      setLoading(true);

      // POST new employee (no password required)
      await api.post("/employees/", {
        name: formData.name,
        email: formData.email || null,
      });

      // alert("Employee added successfully!");
      router.push("/dashboard/employees");

    } catch (error: any) {
      console.error(error);
      alert("Failed to add employee");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-gray-100 min-h-screen py-12 px-6">
      <div className="max-w-md mx-auto bg-white p-8 rounded-2xl shadow-lg">

        <h1 className="text-2xl font-bold mb-8 text-black">
          Add Employee
        </h1>

        <input
          type="text"
          name="name"
          placeholder="Employee Name"
          value={formData.name}
          onChange={handleChange}
          className="w-full mb-4 p-3 border rounded-md"
        />

        <input
          autoComplete="off"
          type="email"
          name="email"
          placeholder="Employee Email (Optional)"
          value={formData.email}
          onChange={handleChange}
          className="w-full mb-6 p-3 border rounded-md"
        />

        <button
          onClick={handleSubmit}
          disabled={loading}
          className="w-full bg-black text-white py-3 rounded-md hover:bg-gray-800 transition disabled:opacity-50"
        >
          {loading ? "Saving..." : "Save Employee"}
        </button>

      </div>
    </div>
  );
}