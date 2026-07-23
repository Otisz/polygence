const API_BASE = "/api";

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
    ...options,
  });

  let data = null;
  try {
    data = await response.json();
  } catch {
    data = null;
  }

  if (!response.ok) {
    const error = new Error("Request failed");
    error.response = { data, status: response.status };
    throw error;
  }

  return { data };
}

export const getProposalActive = (uuid) => request(`/proposal-active/${uuid}/`);

export const updateReviewStudent = (uuid, payload) =>
  request(`/review-student/${uuid}/`, {
    method: "POST",
    body: JSON.stringify(payload),
  });

export const partialUpdateReviewStudent = (uuid, _response, payload) =>
  request(`/review-student/${uuid}/`, {
    method: "PATCH",
    body: JSON.stringify({
      reason: payload?.reason,
      match_rating: payload?.matchRating,
    }),
  });

export const listOutbox = () => request("/outbox/");

export const listProposals = () => request("/proposals/");
