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
        const response = await axios.get(`/health-metrics/${id}/metrics`);
        setMetrics(response.data);
      } catch (error) {
        console.error("Failed to fetch metrics:", error);
      }
    };

    fetchMetrics();
  }, [id]);

  const structuredData = metrics.reduce((acc, metric) => {
    const existingRow = acc.find(row => row.created_at === metric.created_at);
    if (existingRow) {
      existingRow[metric.metric_type] = metric.value;
    } else {
      acc.push({
        created_at: metric.created_at,
        heart_rate: metric.metric_type === "heart_rate" ? metric.value : null,
        respiration: metric.metric_type === "respiration" ? metric.value : null,
        body_temperature: metric.metric_type === "body_temperature" ? metric.value : null,
      });
    }
    return acc;
  }, []);

  return (
    <Layout>
      <div className="max-w-4xl mx-auto mt-8">
        <h2 className="text-3xl font-extrabold mb-6 text-gray-800">
          Health Metrics
        </h2>

        {structuredData.length === 0 ? (
          <p className="text-gray-500">No metrics available</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full bg-white shadow-md rounded-lg overflow-hidden border border-gray-200">
              <thead>
                <tr className="bg-blue-500 text-white">
                  <th className="py-3 px-4 text-left">Timestamp</th>
                  <th className="py-3 px-4 text-left">Heart Rate</th>
                  <th className="py-3 px-4 text-left">Respiration</th>
                  <th className="py-3 px-4 text-left">Body Temperature</th>
                </tr>
              </thead>
              <tbody>
                {structuredData.map((row, index) => (
                  <tr
                    key={index}
                    className="border-b hover:bg-gray-100 transition"
                  >
                    <td className="py-3 px-4">{new Date(row.created_at).toLocaleString()}</td>
                    <td className="py-3 px-4">
                      {row.heart_rate !== null
                        ? `${row.heart_rate} bpm`
                        : "-"}
                    </td>
                    <td className="py-3 px-4">
                      {row.respiration !== null
                        ? `${row.respiration} breaths/min`
                        : "-"}
                    </td>
                    <td className="py-3 px-4">
                      {row.body_temperature !== null
                        ? `${row.body_temperature} °C`
                        : "-"}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </Layout>
  );
};

export default PatientMetrics;
