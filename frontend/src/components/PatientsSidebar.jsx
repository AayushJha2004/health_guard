const PatientsSidebar = ({ filters, setFilters, onApplyFilters }) => {
  const handleChange = (key, value) => {
    setFilters(prev => ({
      ...prev,
      [key]: value || ""
    }));
  };

  return (
    <div className="w-64 h-screen bg-gray-100 border-r fixed top-12 left-0 p-4">
      <h2 className="text-xl font-bold mb-4">Filters</h2>
      
      <input
        type="text"
        placeholder="Search by Name"
        value={filters.name || ""}
        onChange={(e) => handleChange("name", e.target.value)}
        className="border p-2 rounded w-full"
      />
      
      <input
        type="number"
        placeholder="Age"
        value={filters.age || ""}
        onChange={(e) => handleChange("age", e.target.value)}
        className="border p-2 rounded w-full mt-2"
      />
      
      <input
        type="text"
        placeholder="Blood Group"
        value={filters.blood_group || ""}
        onChange={(e) => handleChange("blood_group", e.target.value)}
        className="border p-2 rounded w-full mt-2"
      />

      <button
        onClick={onApplyFilters}
        className="bg-blue-500 text-white px-4 py-2 rounded w-full mt-4"
      >
        Apply Filters
      </button>
    </div>
  );
};

export default PatientsSidebar;
