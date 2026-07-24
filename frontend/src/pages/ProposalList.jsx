import { useEffect, useState } from "react";

import { listProposals } from "../api";

export function ProposalList() {
  const [proposals, setProposals] = useState([]);
  const [error, setError] = useState("");

  const reload = () => {
    listProposals()
      .then(({ data }) => setProposals(data))
      .catch(() => setError("Could not load proposals. Is the API running?"));
  };

  useEffect(() => {
    reload();
  }, []);

  return (
    <div className="panel">
      <div className="row">
        <h1>Proposals</h1>
        <button type="button" className="button secondary" onClick={reload}>
          Refresh
        </button>
      </div>
      <p className="muted">Ops-facing view of proposal records, including the raw response JSON.</p>
      {error && <div className="alert alert-danger">{error}</div>}
      <div className="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Mentor</th>
              <th>Student</th>
              <th>Response</th>
            </tr>
          </thead>
          <tbody>
            {proposals.map((proposal) => (
              <tr key={proposal.uuid}>
                <td>{proposal.mentor_name}</td>
                <td>{proposal.student_name}</td>
                <td>
                  <pre className="json">{JSON.stringify(proposal.response, null, 2)}</pre>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
