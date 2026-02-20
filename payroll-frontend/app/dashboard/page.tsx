export default function DashboardHome() {
  return (
    <div>
      <h1 className="text-3xl font-bold mb-8 text-slate-900">
        Company Dashboard
      </h1>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">

        {/* Total Employees */}
        <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
          <h2 className="text-sm text-slate-500">
            Total Employees
          </h2>
          <p className="text-2xl font-bold text-slate-900 mt-2">
            25
          </p>
        </div>

        {/* Payslips Generated */}
        <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
          <h2 className="text-sm text-slate-500">
            Payslips Generated (This Month)
          </h2>
          <p className="text-2xl font-bold text-slate-900 mt-2">
            18
          </p>
        </div>

        {/* Payroll Total */}
        <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
          <h2 className="text-sm text-slate-500">
            Payroll This Month
          </h2>
          <p className="text-2xl font-bold text-slate-900 mt-2">
            ₹ 4,50,000
          </p>
        </div>

      </div>
    </div>
  );
}