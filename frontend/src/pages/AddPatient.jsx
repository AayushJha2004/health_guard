import { useState } from "react";
import { useNavigate } from "react-router-dom"; //   FIXED IMPORT
import axios from "../utils/api";
import AddPatientSidebar from "../components/AddPatientSidebar";
import Layout from "../components/Layout";

const AddPatient = () => {
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    name: "",
    age: "",
    condition: "",
    email: "",
    phone: "",
    emergency_contact: "",
    blood_group: "",
    height: "",
    weight: "",
    address: "",
  });

  const [currentSection, setCurrentSection] = useState("personal_info");

  //   Handle form data changes
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value === "" ? undefined : value, //   Handle controlled component values correctly
    }));
  };  

  //   Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();

    console.log("Submitting data:", formData);

    try {
      const response = await axios.post("/patients/add", formData);
      console.log("Patient added:", response.data);
      alert("Patient added successfully!");
      navigate("/patients");
    } catch (error) {
      console.error("Failed to add patient:", error);
      alert(`Failed to add patient: ${error.response?.data?.detail || error.message}`);
    }
  };

  return (
    <Layout
      sidebar={
        <AddPatientSidebar
          currentSection={currentSection}
          onSectionChange={setCurrentSection}
        />
      }
    >
      <div className="max-w-md mx-auto mt-10 p-6 bg-white shadow-lg rounded-lg">
        <h2 className="text-xl font-bold mb-4">
          {currentSection === "personal_info" && "Add Personal Information"}
          {currentSection === "medical_history" && "Add Medical History"}
          {currentSection === "alerts_history" && "Add Alerts History"}
          {currentSection === "health_metrics" && "Add Health Metrics"}
        </h2>

        {/*   Render form dynamically based on selected section */}
        {currentSection === "personal_info" && (
          <form onSubmit={handleSubmit} className="space-y-4">
            <input
              type="text"
              name="name"
              placeholder="Name"
              value={formData.name || ""}
              onChange={handleChange}
              required
              className="border p-2 w-full rounded"
            />
            <input
              type="number"
              name="age"
              placeholder="Age"
              value={formData.age || ""}
              onChange={handleChange}
              required
              className="border p-2 w-full rounded"
            />
            <select
              name="condition"
              value={formData.condition || ""}
              onChange={handleChange}
              required
              className="border p-2 w-full rounded"
            >
              <option value="">Select Condition</option>
              <option value="Good">Good</option>
              <option value="Normal">Normal</option>
              <option value="Abnormal">Abnormal</option>
              <option value="Critical">Critical</option>
            </select>
            <input
              type="email"
              name="email"
              placeholder="Email"
              value={formData.email || ""}
              onChange={handleChange}
              required
              className="border p-2 w-full rounded"
            />
            <input
              type="text"
              name="phone"
              placeholder="Phone"
              value={formData.phone || ""}
              onChange={handleChange}
              required
              className="border p-2 w-full rounded"
            />
            <input
              type="text"
              name="emergency_contact"
              placeholder="Emergency Contact"
              value={formData.emergency_contact || ""}
              onChange={handleChange}
              required
              className="border p-2 w-full rounded"
            />
            <input
              type="text"
              name="blood_group"
              placeholder="Blood Group"
              value={formData.blood_group || ""}
              onChange={handleChange}
              required
              className="border p-2 w-full rounded"
            />
            <input
              type="number"
              name="height"
              placeholder="Height (cm)"
              value={formData.height || ""}
              onChange={handleChange}
              className="border p-2 w-full rounded"
            />
            <input
              type="number"
              name="weight"
              placeholder="Weight (kg)"
              value={formData.weight || ""}
              onChange={handleChange}
              className="border p-2 w-full rounded"
            />
            <input
              type="text"
              name="address"
              placeholder="Address"
              value={formData.address || ""}
              onChange={handleChange}
              className="border p-2 w-full rounded"
            />
            <button
              type="submit"
              className="bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600"
            >
              Add Patient
            </button>
          </form>
        )}
      </div>
    </Layout>
  );
};

export default AddPatient;
