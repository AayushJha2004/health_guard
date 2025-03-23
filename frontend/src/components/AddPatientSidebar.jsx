const AddPatientSidebar = ({ currentSection, onSectionChange }) => {
    const sections = [
      { key: "personal_info", label: "Personal Info" },
      { key: "medical_history", label: "Medical History" },
      { key: "alerts_history", label: "Alerts History" },
      { key: "health_metrics", label: "Health Metrics" },
    ];
  
    return (
      <div className="w-64 h-screen bg-gray-100 border-r fixed top-12 left-0 p-4">
        <nav className="space-y-2">
          {sections.map((section) => (
            <button
              key={section.key}
              onClick={() => onSectionChange(section.key)}
              className={`block px-4 py-2 rounded ${
                currentSection === section.key
                  ? "bg-blue-500 text-white"
                  : "hover:bg-blue-200"
              }`}
            >
              {section.label}
            </button>
          ))}
        </nav>
      </div>
    );
  };
  
  export default AddPatientSidebar;
  