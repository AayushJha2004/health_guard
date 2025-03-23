import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from "chart.js";
import axios from "../utils/api";

//   Register necessary components from Chart.js
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const PatientECG = () => {
  const { id } = useParams();
  const [ecgData, setEcgData] = useState([]);

  useEffect(() => {
    const fetchECGData = async () => {
      try {
        const response = await axios.get(`/api/static/ecg/${id}`);
        setEcgData(response.data);
      } catch (error) {
        console.error("Failed to fetch ECG data:", error);
      }
    };

    fetchECGData();
  }, [id]);

  if (!ecgData.length) return <p>No ECG data available</p>;

  const data = {
    labels: ecgData.map((entry) => entry.time),
    datasets: [
      {
        label: "ECG Voltage",
        data: ecgData.map((entry) => entry.voltage),
        fill: false,
        borderColor: "rgb(75, 192, 192)",
        tension: 0.1
      },
    ],
  };

  const options = {
    responsive: true,
    scales: {
      x: {
        type: "linear", //   Set to "linear" instead of "category"
        title: {
          display: true,
          text: "Time",
        },
      },
      y: {
        title: {
          display: true,
          text: "Voltage (mV)",
        },
      },
    },
  };

  return (
    <div>
      <h2 className="text-xl font-bold mb-4">ECG Data</h2>
      <Line data={data} options={options} />
    </div>
  );
};

export default PatientECG;
