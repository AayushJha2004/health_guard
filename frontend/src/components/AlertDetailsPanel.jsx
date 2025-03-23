const AlertDetailsPanel = ({ alert, onUpdateStatus, onNotify }) => {
  if (!alert) {
    return (
      <div className="p-4">
        <p>Select an alert to view details</p>
      </div>
    );
  }

  return (
    <div className="p-6 bg-white shadow-md rounded-md border">
      <h2 className="text-xl font-bold mb-4">Alert Details</h2>

      <div className="space-y-2">
  <div className="flex justify-between border-b py-2">
    <span className="font-semibold">Message:</span>
    <span>{alert.message || "N/A"}</span>
  </div>
  <div className="flex justify-between border-b py-2">
    <span className="font-semibold">Status:</span>
    <span
      className={`${
        alert.status === "active" ? "text-red-500" : "text-green-500"
      }`}
    >
      {alert.status}
    </span>
  </div>
  <div className="flex justify-between border-b py-2">
    <span className="font-semibold">Created At:</span>
    <span>{new Date(alert.created_at).toLocaleString()}</span>
  </div>

  {/*   Add "View Details" link */}
  <div className="mt-4">
    <a
      href={`http://localhost:5173/alerts/${alert.id}`}
      target="_blank"
      rel="noopener noreferrer"
      className="text-blue-500 underline"
    >
      View Details
    </a>
  </div>
</div>


      {/*   Action Buttons */}
      <div className="mt-4 flex gap-4">
        {alert.status !== "resolved" && (
          <button
            onClick={() => onUpdateStatus("resolved")}
            className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600"
          >
            Resolve
          </button>
        )}
        {alert.status !== "active" && (
          <button
            onClick={() => onUpdateStatus("active")}
            className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600"
          >
            Mark Active
          </button>
        )}
        <button
          onClick={onNotify}
          className="bg-yellow-500 text-white px-4 py-2 rounded hover:bg-yellow-600"
        >
          Notify Emergency Contact
        </button>
      </div>
    </div>
  );
};

export default AlertDetailsPanel;
