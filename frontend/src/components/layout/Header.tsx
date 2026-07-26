"use client";

import { useAuthStore } from "@/store/auth";
import { useRouter } from "next/navigation";

export function Header() {
  const { user, logout } = useAuthStore();
  const router = useRouter();

  const handleLogout = () => {
    logout();
    router.push("/auth");
  };

  return (
    <header className="h-16 bg-white border-b border-gray-200 flex items-center justify-between px-6">
      <h2 className="text-lg font-semibold text-gray-800">Due Diligence Platform</h2>
      <div className="flex items-center gap-4">
        <span className="text-sm text-gray-500">{user?.email}</span>
        <button onClick={handleLogout} className="text-sm text-gray-500 hover:text-red-600">
          Logout
        </button>
      </div>
    </header>
  );
}
