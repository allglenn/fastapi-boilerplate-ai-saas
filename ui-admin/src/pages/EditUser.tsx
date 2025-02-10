import React, { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import axios from "axios";
import SideMenu from "../components/SideMenu";

interface User {
  id: number;
  email: string;
  full_name: string;
  role: string;
  is_active: boolean;
}

interface UpdateUserForm {
  email: string;
  full_name: string;
}

export default function EditUser() {
  const navigate = useNavigate();
  const { id } = useParams<{ id: string }>();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [user, setUser] = useState<User | null>(null);
  const [formData, setFormData] = useState<UpdateUserForm>({
    email: "",
    full_name: "",
  });

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const token = localStorage.getItem("token");
        if (!token || !id) {
          navigate("/users");
          return;
        }

        const response = await axios.get(
          `${import.meta.env.VITE_API_URL}/users/${id}`,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        setUser(response.data);
        setFormData({
          email: response.data.email,
          full_name: response.data.full_name,
        });
      } catch (error) {
        console.error("Failed to fetch user:", error);
        setError("Failed to fetch user data");
        if (axios.isAxiosError(error) && error.response?.status === 401) {
          navigate("/login");
        } else {
          navigate("/users");
        }
      }
    };

    fetchUser();
  }, [id, navigate]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      const token = localStorage.getItem("token");
      await axios.put(`${import.meta.env.VITE_API_URL}/users/${id}`, formData, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      navigate("/users");
    } catch (error) {
      console.error("Failed to update user:", error);
      setError("Failed to update user. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  if (!user) {
    return (
      <div className="flex h-screen bg-gray-100">
        <SideMenu />
        <main className="flex-1 p-8">
          <div className="max-w-2xl mx-auto">
            {error ? (
              <div className="bg-red-50 border-l-4 border-red-400 p-4 rounded-md">
                <p className="text-sm text-red-700">{error}</p>
              </div>
            ) : (
              <p>Loading...</p>
            )}
          </div>
        </main>
      </div>
    );
  }

  return (
    <div className="flex h-screen bg-gray-100">
      <SideMenu />
      <main className="flex-1 p-8">
        <div className="max-w-2xl mx-auto">
          <h1 className="text-2xl font-bold text-gray-800 mb-6">Edit User</h1>

          {error && (
            <div className="bg-red-50 border-l-4 border-red-400 p-4 mb-6 rounded-md">
              <p className="text-sm text-red-700">{error}</p>
            </div>
          )}

          <form
            onSubmit={handleSubmit}
            className="bg-white shadow-md rounded-lg p-6 space-y-6"
          >
            <div>
              <label
                htmlFor="full_name"
                className="block text-sm font-medium text-gray-700"
              >
                Full Name
              </label>
              <input
                type="text"
                id="full_name"
                name="full_name"
                value={formData.full_name}
                onChange={handleChange}
                required
                className="input-field mt-1"
              />
            </div>

            <div>
              <label
                htmlFor="email"
                className="block text-sm font-medium text-gray-700"
              >
                Email
              </label>
              <input
                type="email"
                id="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                required
                className="input-field mt-1"
              />
            </div>

            <div>
              <label
                htmlFor="role"
                className="block text-sm font-medium text-gray-700"
              >
                Role
              </label>
              <input
                type="text"
                id="role"
                value={user.role}
                disabled
                className="input-field mt-1 bg-gray-50"
              />
            </div>

            <div className="flex justify-end space-x-4">
              <button
                type="button"
                onClick={() => navigate("/users")}
                className="px-4 py-2 text-gray-700 bg-gray-100 rounded-md hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-gray-500"
              >
                Cancel
              </button>
              <button type="submit" disabled={loading} className="btn-primary">
                {loading ? "Saving..." : "Save Changes"}
              </button>
            </div>
          </form>
        </div>
      </main>
    </div>
  );
}
