import { useEffect, useState } from "react";
import { useLocation, useParams } from "react-router-dom";

import * as api from "../api";
import { FeedbackForm } from "./MatchingFeedbackForm";

export function ReviewStudent() {
  const { uuid } = useParams();
  const { pathname } = useLocation();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(false);
  const [responseRecorded, setResponseRecorded] = useState(false);
  const [isMatched, setIsMatched] = useState(false);
  const [studentName, setStudentName] = useState("The student");

  const response = pathname.includes("accept") ? "accept" : "reject";

  useEffect(() => {
    setLoading(true);
    Promise.all([
      api.getProposalActive(uuid).then(({ data }) => {
        setIsMatched(data.is_matched);
        setStudentName(data.student_name);
      }),
      api.updateReviewStudent(uuid, { response }),
    ])
      .then(() => {
        setResponseRecorded(true);
      })
      .catch((err) => {
        if (err.response && err.response.data?.error === "Response already recorded") {
          setResponseRecorded(true);
        } else {
          setError(true);
        }
      })
      .finally(() => {
        setLoading(false);
      });
  }, [uuid, response]);

  return (
    <div className="panel">
      {loading && <p>Loading…</p>}
      {error && (
        <div className="alert alert-danger">
          Something went wrong. Please contact us at mentors@example.com.
        </div>
      )}
      {responseRecorded && response === "accept" && !isMatched && (
        <div className="alert alert-success">Your response has been recorded.</div>
      )}
      {responseRecorded && response === "accept" && isMatched && (
        <div className="alert alert-warning">
          Thank you for your interest! {studentName} is no longer looking for a mentor, so we will
          be on the lookout for another stellar student for you!
        </div>
      )}
      {responseRecorded && (
        <FeedbackForm uuid={uuid} response={response} updateResponse={api.partialUpdateReviewStudent} />
      )}
    </div>
  );
}
