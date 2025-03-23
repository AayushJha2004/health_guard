import { useAuth } from "../context/AuthContext";
import { Link } from "react-router-dom";
import { BellIcon, UserCircleIcon } from "@heroicons/react/24/solid";

const Header = () => {
  const { user, logout } = useAuth();

  return (
    <header className="flex justify-between items-center bg-blue-600 text-white px-6 py-3 shadow-md fixed top-0 left-0 right-0 z-10">
      {/* Logo */}
      <Link to="/" className="text-xl font-bold">
        HealthGuard
      </Link>

      {/* Navigation Links */}
      <nav className="flex gap-6 ml-auto">
        {user ? (
          <>
            <Link to="/dashboard" className="hover:underline">
              Dashboard
            </Link>
            <Link to="/patients" className="hover:underline">
              Patients
            </Link>
            <Link
              to="/patients/add"
              className="hover:underline bg-green-500 px-3 py-1 rounded"
            >
              + Add Patient
            </Link>
          </>
        ) : (
          <>
            <Link to="/login" className="hover:underline">
              Login
            </Link>
            <Link to="/signup" className="hover:underline">
              Signup
            </Link>
          </>
        )}
      </nav>

      {/* Notifications and Profile */}
      {user && (
        <div className="flex items-center gap-4 ml-4">
          <Link to="/alerts">
            <BellIcon className="h-6 w-6 cursor-pointer hover:text-gray-200" />
          </Link>

          {/* Profile Dropdown */}
          <div className="relative group">
            <UserCircleIcon className="h-6 w-6 cursor-pointer" />
            <div className="absolute right-0 top-8 w-32 bg-white shadow-md rounded hidden group-hover:block">
              <Link
                to="/profile"
                className="block px-4 py-2 hover:bg-gray-100 text-black"
              >
                Profile
              </Link>
              <button
                onClick={logout}
                className="block px-4 py-2 w-full text-left hover:bg-gray-100 text-black"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      )}
    </header>
  );
};

export default Header;
