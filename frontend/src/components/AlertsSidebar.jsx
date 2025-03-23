const AlertsSidebar = ({ alerts, onSelectAlert }) => {
    return (
      <div className="w-64 h-screen bg-gray-100 border-r fixed top-12 left-0 p-4">
        <h2 className="text-lg font-bold mb-4">Alerts</h2>
        <ul className="space-y-2">
          {alerts.map((alert) => (
            <li key={alert.id}>
            <button
              onClick={() => onSelectAlert(alert.id)}
              className={`block px-4 py-2 rounded ${
                alert.message.includes("Emergency")
                  ? "bg-red-500 text-white"
                  : "bg-orange-400 text-white"
              }`}
            >
              #{alert.id} - {alert.message.includes("Emergency") ? "Emergency" : "Abnormal"}
            </button>
          </li>          
          ))}
        </ul>
      </div>
    );
  };
  
  export default AlertsSidebar;
  