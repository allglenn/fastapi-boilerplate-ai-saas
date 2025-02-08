import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import SideMenu from "../components/SideMenu";

interface User {
  email: string;
  full_name: string;
}

export default function Dashboard() {
  const [user, setUser] = useState<User | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const token = localStorage.getItem("token");
        if (!token) {
          navigate("/login");
          return;
        }

        const response = await axios.get(
          `${import.meta.env.VITE_API_URL}/users/me`,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        setUser(response.data);
      } catch (error) {
        console.error("Failed to fetch user data:", error);
        // If unauthorized, redirect to login
        if (axios.isAxiosError(error) && error.response?.status === 401) {
          navigate("/login");
        }
      }
    };

    fetchUserData();
  }, [navigate]);

  return (
    <div className="flex h-screen bg-gray-100">
      <SideMenu />
      <main className="flex-1 p-8">
        <h1 className="text-4xl font-bold text-gray-800">
          {user ? `Welcome back, ${user.full_name}!` : "Loading..."}
        </h1>

      </main>
    </div>
  );
}
