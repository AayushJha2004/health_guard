import { useEffect, useState } from "react";
import { useParams, useNavigate, Link } from "react-router-dom";
import Layout from "../components/Layout";
import axios from "../utils/api";

const PatientDetail = () => {
  const { id } = useParams();
  const [patient, setPatient] = useState(null);
  const navigate = useNavigate();

  // ✅ Define sidebarLinks here
  const sidebarLinks = [
    { name: "Personal Info", path: `/patients/${id}` },
    { name: "ECG Data", path: `/patients/${id}/ecg` },
    { name: "Health Metrics", path: `/patients/${id}/metrics` },
  ];

  useEffect(() => {
    const fetchPatientDetail = async () => {
      try {
        const response = await axios.get(`/patients/${id}`);
        setPatient(response.data);
      } catch (error) {
        console.error("Failed to fetch patient details:", error);
      }
    };

    fetchPatientDetail();
  }, [id]);

  if (!patient) return <p className="text-gray-500 text-center mt-8">Loading patient details...</p>;

  return (
    <Layout sidebarLinks={sidebarLinks}>
      <div className="max-w-3xl mx-auto mt-8 bg-white shadow-md rounded-lg p-6 border border-gray-200">
        <h2 className="text-3xl font-bold text-gray-800 mb-4">{patient.name}</h2>
        <div className="space-y-3">
          <div className="flex justify-between border-b pb-2">
            <span className="font-medium text-gray-600">Email:</span>
            <span className="text-gray-800">{patient.email}</span>
          </div>
          <div className="flex justify-between border-b pb-2">
            <span className="font-medium text-gray-600">Phone:</span>
            <span className="text-gray-800">{patient.phone}</span>
          </div>
          <div className="flex justify-between">
            <span className="font-medium text-gray-600">Condition:</span>
            <span
              className={`px-3 py-1 rounded-full text-sm font-medium ${
                patient.condition === "Good"
                  ? "bg-green-100 text-green-600"
                  : patient.condition === "Abnormal"
                  ? "bg-yellow-100 text-yellow-600"
                  : patient.condition === "Critical"
                  ? "bg-red-100 text-red-600"
                  : "bg-gray-100 text-gray-600"
              }`}
            >
              {patient.condition}
            </span>
          </div>
        </div>

        {/* ✅ Add Links */}
        <div className="mt-6 flex justify-center gap-6">
          <Link
            to={`/patients/${patient.id}`}
            className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg shadow transition"
          >
            Personal Info
          </Link>
          <Link
            to={`/patients/${patient.id}/ecg`}
            className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg shadow transition"
          >
            ECG Data
          </Link>
          <Link
            to={`/patients/${patient.id}/metrics`}
            className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg shadow transition"
          >
            Health Metrics
          </Link>
        </div>
      </div>
    </Layout>
  );
};

export default PatientDetail;
