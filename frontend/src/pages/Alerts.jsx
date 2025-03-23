import { useState, useEffect } from "react";
import axios from "../utils/api";
import AlertsSidebar from "../components/AlertsSidebar";
import AlertDetailsPanel from "../components/AlertDetailsPanel";
import Layout from "../components/Layout";

const Alerts = () => {
  const [alerts, setAlerts] = useState([]);
  const [selectedAlert, setSelectedAlert] = useState(null);

  //   Fetch alerts from backend
  useEffect(() => {
    const fetchAlerts = async () => {
      try {
        const response = await axios.get("/alerts");
        setAlerts(response.data);
      } catch (error) {
        console.error("Failed to fetch alerts:", error);
      }
    };

    fetchAlerts();
  }, []);

  //   Fetch single alert when selected
  const fetchAlertDetails = async (alertId) => {
    try {
      const response = await axios.get(`/alerts/${alertId}`);
      setSelectedAlert(response.data);
    } catch (error) {
      console.error("Failed to fetch alert details:", error);
    }
  };
  

  //   Update alert status
  const handleUpdateStatus = async (status) => {
    if (!selectedAlert) return;

    try {
      await axios.put(`/alerts/${selectedAlert.id}`, { status });
      alert(`Alert status updated to "${status}"`);
      fetchAlertDetails(selectedAlert.id);
    } catch (error) {
      console.error("Failed to update alert status:", error);
    }
  };

  //   Notify Emergency Contact
  const handleNotify = async () => {
    if (!selectedAlert) return;

    try {
      const response = await axios.post(`/alerts/${selectedAlert.id}/notify`);
      alert(response.data.message);
    } catch (error) {
      console.error("Failed to notify:", error);
    }
  };

  return (
    <Layout
      sidebar={<AlertsSidebar alerts={alerts} onSelectAlert={fetchAlertDetails} />}
    >
      <AlertDetailsPanel
        alert={selectedAlert}
        onUpdateStatus={handleUpdateStatus}
        onNotify={handleNotify}
      />
    </Layout>
  );
};

export default Alerts;
