import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import axios from "../utils/api";
import Layout from "../components/Layout";

const PatientMetrics = () => {
  const { id } = useParams();
  const [metrics, setMetrics] = useState([]);

  useEffect(() => {
    const fetchMetrics = async () => {
      try {
        const response = await axios.get(`/patients/${id}/metrics`);
        setMetrics(response.data);
      } catch (error) {
        console.error("Failed to fetch metrics:", error);
      }
    };

    fetchMetrics();
  }, [id]);

  return (
    <Layout>
      <div>
        <h2 className="text-2xl font-bold mb-4">Health Metrics</h2>
        {metrics.length === 0 ? (
          <p>No metrics available</p>
        ) : (
          <ul>
            {metrics.map((metric) => (
              <li key={metric.id}>
                {metric.metric_type}: {metric.value}
              </li>
            ))}
          </ul>
        )}
      </div>
    </Layout>
  );
};

export default PatientMetrics;
