import { useEffect, useState } from "react";
import { useParams, useNavigate, Link } from "react-router-dom";
import Layout from "../components/Layout";
import axios from "../utils/api";

const PatientDetail = () => {
  const { id } = useParams();
  const [patient, setPatient] = useState(null);
  const navigate = useNavigate();

  //   Define sidebarLinks here
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

  if (!patient) return <p>Loading...</p>;

  return (
    <Layout sidebarLinks={sidebarLinks}>
      <div>
        <h2>{patient.name}</h2>
        <p>Email: {patient.email}</p>
        <p>Phone: {patient.phone}</p>
        <p>Condition: {patient.condition}</p>

        {/*   Add links */}
        <div className="mt-4">
          <Link to={`/patients/${patient.id}`} className="text-blue-500 underline">
            Personal Info
          </Link>
          {" | "}
          <Link to={`/patients/${patient.id}/ecg`} className="text-blue-500 underline">
            ECG Data
          </Link>
          {" | "}
          <Link to={`/patients/${patient.id}/metrics`} className="text-blue-500 underline">
            Health Metrics
          </Link>
        </div>
      </div>
    </Layout>
  );
};

export default PatientDetail;
