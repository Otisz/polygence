import { useState } from "react";

const ACCEPT = "accept";
const REJECT = "reject";

export function FeedbackForm({ uuid, response, updateResponse }) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(false);
  const [responseRecorded, setResponseRecorded] = useState(false);
  const [reason, setReason] = useState({});
  const [matchRating, setMatchRating] = useState(undefined);

  const handleReasonChange = (event) => {
    const { name, value, checked, type } = event.target;
    setReason({ ...reason, [name]: type === "checkbox" ? checked : value });
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    setLoading(true);

    const payload = {
      matchRating,
      reason: response === REJECT ? reason : {},
    };

    updateResponse(uuid, undefined, payload)
      .then(() => setResponseRecorded(true))
      .catch(() => setError(true))
      .finally(() => setLoading(false));
  };

  return (
    <>
      {loading && <p>Saving…</p>}
      {error && (
        <div className="alert alert-danger">
          Something went wrong. Please contact us at mentors@example.com.
        </div>
      )}
      {responseRecorded && <p>Thank you!</p>}
      {!loading && !responseRecorded && !error && (
        <form onSubmit={handleSubmit} className="feedback-form">
          {response === ACCEPT && (
            <MatchRatingField matchRating={matchRating} setMatchRating={setMatchRating} />
          )}
          {response === REJECT && (
            <RejectFormFields reason={reason} handleReasonChange={handleReasonChange} />
          )}
          <button type="submit" className="button">
            Submit
          </button>
        </form>
      )}
    </>
  );
}

function RejectFormFields({ reason, handleReasonChange }) {
  return (
    <>
      <p>
        No problem! Can you let us know why you declined working with this student so we can do a
        better job next time? Thank you!
      </p>
      <label className="check">
        <input
          type="checkbox"
          name="no_good_fit"
          checked={Boolean(reason.no_good_fit)}
          onChange={handleReasonChange}
        />
        Student did not seem like a good fit for me
      </label>
      <label className="check">
        <input
          type="checkbox"
          name="no_bandwidth"
          checked={Boolean(reason.no_bandwidth)}
          onChange={handleReasonChange}
        />
        I do not have the bandwidth during that time frame
      </label>
      <label className="check">
        <input
          type="checkbox"
          name="timezone_issue"
          checked={Boolean(reason.timezone_issue)}
          onChange={handleReasonChange}
        />
        The student&apos;s timezone would make scheduling sessions hard
      </label>
      {reason.no_bandwidth && (
        <label className="field">
          When will you have more bandwidth to mentor?
          <input
            type="date"
            name="unavailable_until"
            value={reason.unavailable_until || ""}
            onChange={handleReasonChange}
          />
        </label>
      )}
      <label className="field">
        Any other things we should know?
        <textarea name="other" rows={4} value={reason.other || ""} onChange={handleReasonChange} />
      </label>
    </>
  );
}

function MatchRatingField({ matchRating, setMatchRating }) {
  return (
    <label className="field">
      We are constantly improving how we match students to mentors. On a scale of 0–10, how would you
      rate this match?
      <select
        value={matchRating ?? ""}
        onChange={(event) => {
          const value = event.target.value;
          setMatchRating(value === "" ? undefined : Number(value));
        }}
      >
        <option value="">Select…</option>
        {Array.from({ length: 11 }, (_, index) => (
          <option key={index} value={index}>
            {index}
          </option>
        ))}
      </select>
    </label>
  );
}
