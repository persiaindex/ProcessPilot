import { Navigate, Route, Routes } from "react-router-dom";

import AppLayout from "../layouts/AppLayout";
import CreateRequestPage from "../pages/CreateRequestPage";
import DashboardPage from "../pages/DashboardPage";
import LoginPage from "../pages/LoginPage";
import RequestDetailPage from "../pages/RequestDetailPage";
import RequestsPage from "../pages/RequestsPage";

function AppRouter() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />

      <Route path="/" element={<AppLayout />}>
        <Route index element={<Navigate to="/dashboard" replace />} />
        <Route path="dashboard" element={<DashboardPage />} />
        <Route path="requests" element={<RequestsPage />} />
        <Route path="requests/new" element={<CreateRequestPage />} />
        <Route path="requests/:requestId" element={<RequestDetailPage />} />
      </Route>
    </Routes>
  );
}

export default AppRouter;