"use client";

import { AppLayout } from "@/components/layout/AppLayout";
import { useAuthStore } from "@/store/auth";

export default function SettingsPage() {
  const user = useAuthStore((s) => s.user);

  return (
    <AppLayout>
      <div className="space-y-6">
        <h1 className="text-2xl font-bold">Settings</h1>
        <div className="card max-w-lg">
          <h2 className="text-lg font-semibold mb-4">Profile</h2>
          <dl className="space-y-3 text-sm">
            <div className="flex justify-between">
              <dt className="text-gray-500">Name</dt>
              <dd>{user?.full_name || "-"}</dd>
            </div>
            <div className="flex justify-between">
              <dt className="text-gray-500">Email</dt>
              <dd>{user?.email || "-"}</dd>
            </div>
            <div className="flex justify-between">
              <dt className="text-gray-500">Organization</dt>
              <dd>{user?.organization || "-"}</dd>
            </div>
            <div className="flex justify-between">
              <dt className="text-gray-500">Role</dt>
              <dd className="capitalize">{user?.role || "-"}</dd>
            </div>
          </dl>
        </div>
      </div>
    </AppLayout>
  );
}
