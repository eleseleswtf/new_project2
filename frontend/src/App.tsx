import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import { TableProvider } from "./contexts/TableContext";
import Parkingplace from "./pages/Parkingplace";
import Parkingavailability from "./pages/Parkingavailability";

function App() {
  return (
    <TableProvider>
      <div className="app-container">
        <main className="app-main">
          <Routes>
            <Route path="/parkingplace" element={<Parkingplace />} />
            <Route path="/parkingavailability" element={<Parkingavailability />} />
            <Route path="/" element={<Navigate to="/parkingplace" replace />} />
            <Route path="*" element={<Navigate to="/parkingplace" replace />} />
          </Routes>
        </main>
      </div>
    </TableProvider>
  );
}
export default App;
