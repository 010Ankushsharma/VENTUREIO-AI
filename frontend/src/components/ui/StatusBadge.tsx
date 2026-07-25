import { cn } from "@/lib/utils";

const statusStyles: Record<string, string> = {
  pending: "bg-gray-100 text-gray-700",
  in_progress: "bg-blue-100 text-blue-700",
  completed: "bg-green-100 text-green-700",
  archived: "bg-yellow-100 text-yellow-700",
  failed: "bg-red-100 text-red-700",
};

export function StatusBadge({ status }: { status: string }) {
  return (
    <span className={cn("badge", statusStyles[status] || "bg-gray-100 text-gray-700")}>
      {status.replace("_", " ")}
    </span>
  );
}
