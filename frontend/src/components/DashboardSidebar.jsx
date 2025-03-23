import { useEffect, useState } from "react";
import axios from "../utils/api";

const DashboardSidebar = ({ onSelectCondition }) => {
  const [counts, setCounts] = useState({
    Good: 0,
    Normal: 0,
    Abnormal: 0,
    Critical: 0,
    Total: 0,
  });

  useEffect(() => {
    const fetchCounts = async () => {
      try {
        const response = await axios.get("/dashboard/patients/condition-counts");
        setCounts(response.data);
      } catch (error) {
        console.error("Failed to fetch patient counts:", error);
      }
    };

    fetchCounts();
  }, []);

  const items = [
    { label: "Good", value: "Good", count: counts.Good },
    { label: "Normal", value: "Normal", count: counts.Normal },
    { label: "Abnormal", value: "Abnormal", count: counts.Abnormal },
    { label: "Critical", value: "Critical", count: counts.Critical },
  ];

  return (
    <div className="w-64 h-screen bg-gray-100 border-r fixed top-12 left-0 p-4">
      <h2 className="text-xl font-bold mb-4">Patient Conditions</h2>
      <nav className="space-y-2">
        {items.map((item) => (
          <button
            key={item.value}
            onClick={() => onSelectCondition(item.value)}
            className="block w-full px-4 py-2 rounded hover:bg-blue-200 text-left"
          >
            {item.label} ({item.count}/{counts.Total})
          </button>
        ))}
      </nav>
    </div>
  );
};

export default DashboardSidebar;
