import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "../utils/api";
import Layout from "../components/Layout";
import PatientsSidebar from "../components/PatientsSidebar";
import RightPanel from "../components/RightPanel";

const Patients = () => {
  const navigate = useNavigate();
  const [filters, setFilters] = useState({
    name: "",
    age: "",
    blood_group: ""
  });
  const [patients, setPatients] = useState([]);

  //   Fetch all patients by default + filters
  const fetchPatients = async () => {
    try {
      const params = Object.fromEntries(
        Object.entries(filters).filter(([_, value]) => value)
      );
      const response = await axios.get("/patients", { params });
      setPatients(response.data);
    } catch (error) {
      console.error("Failed to fetch patients:", error);
    }
  };

  useEffect(() => {
    fetchPatients();
  }, []);

  const columns = [
    { key: "id", label: "Patient ID" },
    { key: "name", label: "Name" },
    { key: "age", label: "Age" },
    { key: "condition", label: "Condition" },
    { key: "blood_group", label: "Blood Group" }
  ];

  return (
    <Layout
      sidebar={
        <PatientsSidebar
          filters={filters}
          setFilters={setFilters}
          onApplyFilters={fetchPatients}
        />
      }
    >
      <RightPanel
        title="Patients"
        fetchData={() => Promise.resolve({ data: patients })}
        columns={columns}
        actionButton={(row) => (
          <button
            onClick={() => navigate(`/patients/${row.id}`)}
            className="bg-blue-500 text-white px-4 py-2 rounded"
          >
            View
          </button>
        )}
      />
    </Layout>
  );
};

export default Patients;
