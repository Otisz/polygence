import { Link, Route, Routes } from "react-router-dom";

import { DevInbox } from "./pages/DevInbox";
import { ProposalList } from "./pages/ProposalList";
import { ReviewStudent } from "./pages/ReviewStudent";

export default function App() {
  return (
    <div className="app">
      <header className="topbar">
        <Link to="/" className="brand">
          Matching take-home
        </Link>
        <nav>
          <Link to="/">Dev inbox</Link>
          <Link to="/proposals">Proposals</Link>
        </nav>
      </header>
      <main>
        <Routes>
          <Route path="/" element={<DevInbox />} />
          <Route path="/proposals" element={<ProposalList />} />
          <Route path="/review-student/:uuid/:decision" element={<ReviewStudent />} />
        </Routes>
      </main>
    </div>
  );
}
