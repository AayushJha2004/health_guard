import { useState } from "react";
import { Link } from "react-router-dom";

const Sidebar = ({ links = [], filters = {}, onFilterChange, onApplyFilters }) => {
  const [localFilters, setLocalFilters] = useState(filters);

  const handleChange = (key, value) => {
    setLocalFilters((prev) => ({ ...prev, [key]: value }));
  };

  const handleApplyFilters = () => {
    if (onApplyFilters) onApplyFilters(localFilters);
  };

  return (
    <div className="w-64 h-screen bg-gray-100 border-r fixed top-12 left-0 p-4 overflow-y-auto">
      {/*   Display static sidebar items */}
      {links.length > 0 && (
        <nav className="space-y-2 mb-4">
          {links.map((link) => (
            <Link
              key={link.name}
              to={link.path || "#"}
              onClick={link.onClick}
              className="block px-4 py-2 rounded hover:bg-blue-200"
            >
              {link.name}
            </Link>
          ))}
        </nav>
      )}

      {/*   Dynamic Filters */}
      {onFilterChange && (
        <div>
          <h3 className="font-bold mb-2">Filters</h3>

          {/*   Condition Filter */}
          <select
            value={localFilters.condition || ""}
            onChange={(e) => handleChange("condition", e.target.value)}
            className="border p-2 w-full mb-2"
          >
            <option value="">All Conditions</option>
            <option value="Good">Good</option>
            <option value="Normal">Normal</option>
            <option value="Abnormal">Abnormal</option>
            <option value="Critical">Critical</option>
          </select>

          {/*   Age Filter */}
          <input
            type="number"
            placeholder="Min Age"
            value={localFilters.min_age || ""}
            onChange={(e) => handleChange("min_age", e.target.value)}
            className="border p-2 w-full mb-2"
          />
          <input
            type="number"
            placeholder="Max Age"
            value={localFilters.max_age || ""}
            onChange={(e) => handleChange("max_age", e.target.value)}
            className="border p-2 w-full mb-2"
          />

          {/*   BMI Filter */}
          <input
            type="number"
            placeholder="Min BMI"
            value={localFilters.bmi_min || ""}
            onChange={(e) => handleChange("bmi_min", e.target.value)}
            className="border p-2 w-full mb-2"
          />
          <input
            type="number"
            placeholder="Max BMI"
            value={localFilters.bmi_max || ""}
            onChange={(e) => handleChange("bmi_max", e.target.value)}
            className="border p-2 w-full mb-2"
          />

          {/*   Heart Rate Filter */}
          <input
            type="number"
            placeholder="Min Heart Rate"
            value={localFilters.heart_rate_min || ""}
            onChange={(e) => handleChange("heart_rate_min", e.target.value)}
            className="border p-2 w-full mb-2"
          />
          <input
            type="number"
            placeholder="Max Heart Rate"
            value={localFilters.heart_rate_max || ""}
            onChange={(e) => handleChange("heart_rate_max", e.target.value)}
            className="border p-2 w-full mb-2"
          />

          {/*   Apply Filters Button */}
          <button
            onClick={handleApplyFilters}
            className="bg-blue-500 text-white px-4 py-2 rounded w-full hover:bg-blue-600"
          >
            Apply Filters
          </button>
        </div>
      )}
    </div>
  );
};

export default Sidebar;
