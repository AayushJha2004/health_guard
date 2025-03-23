import { useState, useEffect } from "react";
import Layout from "../components/Layout";
import RightPanel from "../components/RightPanel";
import DashboardSidebar from "../components/DashboardSidebar";
import axios from "../utils/api";

const Dashboard = () => {
  const [selectedCondition, setSelectedCondition] = useState("Good");
  const [patients, setPatients] = useState([]);

  useEffect(() => {
    const fetchPatients = async () => {
      try {
        const response = await axios.get("/dashboard/patients/by-condition", {
          params: { condition: selectedCondition },
        });
        setPatients(response.data);
      } catch (error) {
        console.error("Failed to fetch patients:", error);
      }
    };

    fetchPatients();
  }, [selectedCondition]);

  const columns = [
    { key: "id", label: "Patient ID" },
    { key: "name", label: "Name" },
    { key: "age", label: "Age" },
    { key: "condition", label: "Condition" },
    { key: "blood_group", label: "Blood Group" },
  ];

  return (
    <Layout sidebar={<DashboardSidebar onSelectCondition={setSelectedCondition} />}>
      <RightPanel
        title={`Patients in ${selectedCondition} Condition`}
        fetchData={() => Promise.resolve({ data: patients })}
        columns={columns}
        actionButton={(row) => (
          <button
            className="bg-blue-500 text-white px-4 py-2 rounded"
            onClick={() => console.log("View Details", row)}
          >
            View
          </button>
        )}
      />
    </Layout>
  );
};

export default Dashboard;
