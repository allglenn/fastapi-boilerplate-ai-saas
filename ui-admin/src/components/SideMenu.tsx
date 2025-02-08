import React from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import {
  HomeIcon,
  UsersIcon,
  ArrowLeftOnRectangleIcon,
} from "@heroicons/react/24/outline";

const menuItems = [
  {
    name: "Dashboard",
    icon: HomeIcon,
    path: "/dashboard",
  },
  {
    name: "Users",
    icon: UsersIcon,
    path: "/users",
  },
];

export default function SideMenu() {
  const location = useLocation();
  const navigate = useNavigate();

  const handleLogout = () => {
    // Clear the auth token
    localStorage.removeItem("token");
    // Redirect to login page
    navigate("/login");
  };

  return (
    <div className="w-64 bg-white shadow-lg h-screen flex flex-col">
      <div className="p-4">
        <h2 className="text-2xl font-bold text-gray-800">Admin Panel</h2>
      </div>
      <nav className="mt-4 flex-1">
        {menuItems.map((item) => {
          const isActive = location.pathname === item.path;
          return (
            <Link
              key={item.name}
              to={item.path}
              className={`flex items-center px-4 py-3 text-gray-700 hover:bg-gray-100 ${
                isActive ? "bg-blue-50 text-blue-700" : ""
              }`}
            >
              <item.icon className="w-6 h-6 mr-3" />
              <span className="text-sm font-medium">{item.name}</span>
            </Link>
          );
        })}
      </nav>
      <div className="p-4 border-t">
        <button
          onClick={handleLogout}
          className="flex items-center w-full px-4 py-3 text-gray-700 hover:bg-gray-100 hover:text-red-600 rounded-md"
        >
          <ArrowLeftOnRectangleIcon className="w-6 h-6 mr-3" />
          <span className="text-sm font-medium">Logout</span>
        </button>
      </div>
    </div>
  );
}
