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
      <div className="max-w-4xl mx-auto mt-8">
        <h2 className="text-3xl font-extrabold mb-6 text-gray-800">
          Health Metrics
        </h2>
        {metrics.length === 0 ? (
          <p className="text-gray-500">No metrics available</p>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {metrics.map((metric) => (
              <div
                key={metric.id}
                className="bg-white shadow-md rounded-lg p-6 border border-gray-200 hover:shadow-lg transition-shadow"
              >
                <h3 className="text-lg font-semibold text-gray-700 capitalize">
                  {metric.metric_type}
                </h3>
                <p className="text-2xl font-bold text-blue-500 mt-2">
                  {metric.value}
                </p>
              </div>
            ))}
          </div>
        )}
      </div>
    </Layout>
  );
};

export default PatientMetrics;
