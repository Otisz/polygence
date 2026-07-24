import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import { listOutbox } from "../api";

function linkify(body) {
  const parts = body.split(/(https?:\/\/\S+)/g);
  return parts.map((part, index) => {
    if (part.startsWith("http")) {
      const path = part.replace(/^https?:\/\/[^/]+/, "");
      return (
        <Link key={index} to={path || "/"}>
          {part}
        </Link>
      );
    }
    return <span key={index}>{part}</span>;
  });
}

export function DevInbox() {
  const [messages, setMessages] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    listOutbox()
      .then(({ data }) => setMessages(data))
      .catch(() => setError("Could not load outbox. Is the API running?"));
  }, []);

  return (
    <div className="panel">
      <h1>Dev inbox</h1>
      <p className="muted">
        Stand-in for the transactional email mentors receive. Use the accept/decline links below.
        Re-seed with <code>python manage.py seed_proposal</code>.
      </p>
      {error && <div className="alert alert-danger">{error}</div>}
      {!error && messages.length === 0 && <p>No messages yet.</p>}
      {messages.map((message) => (
        <article key={message.id} className="email">
          <header>
            <strong>{message.subject}</strong>
            <span className="muted">to {message.recipient}</span>
          </header>
          <pre>{linkify(message.body)}</pre>
        </article>
      ))}
    </div>
  );
}
