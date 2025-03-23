import { useEffect, useState } from "react";

const RightPanel = ({ title, fetchData, columns, actionButton }) => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadData = async () => {
      try {
        const response = await fetchData();
        setData(response?.data || []);
      } catch (error) {
        console.error(`Failed to fetch ${title}:`, error);
        setData([]);
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, [fetchData]);

  if (loading) return <p>Loading {title}...</p>;

  return (
    <div className="overflow-x-auto">
      <h2 className="text-xl font-bold mb-4">{title}</h2>

      {data.length === 0 ? (
        <p>No records found.</p>
      ) : (
        <table className="table-auto w-full border-collapse border border-gray-200">
          <thead>
            <tr className="bg-blue-100">
              {columns.map((col) => (
                <th key={col.key} className="p-2 border">
                  {col.label}
                </th>
              ))}
              {actionButton && <th className="p-2 border">Actions</th>}
            </tr>
          </thead>
          <tbody>
            {data.map((row) => (
              <tr key={row.id} className="hover:bg-gray-100">
                {columns.map((col) => (
                  <td key={col.key} className="p-2 border">
                    {row[col.key] || "N/A"}
                  </td>
                ))}
                {actionButton && (
                  <td className="p-2 border">{actionButton(row)}</td>
                )}
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default RightPanel;
