// Modified by Sanrathi, 2026
import { requireAdminSession } from "@/utils/serverAuth";
import AdminPanel from "./AdminPanel";

export const metadata = {
  title: "Admin | Sanrathi Slide Maker",
};

export default async function AdminPage() {
  await requireAdminSession();
  return <AdminPanel />;
}
