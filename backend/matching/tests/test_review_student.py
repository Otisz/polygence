from django.test import TestCase
from rest_framework.test import APIClient

from matching.models import Mentor, MentorRequest, StudentProposal
from matching.services.student_proposal import StudentProposalService


class ReviewStudentPostTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.mentor = Mentor.objects.create(name="Alex", email="alex@example.com")
        self.mentor_request = MentorRequest.objects.create(student_name="Jamie")
        self.proposal = StudentProposal.objects.create(mentor=self.mentor, mentor_request=self.mentor_request)

    def test_records_accept_response(self):
        response = self.client.post(
            f"/api/review-student/{self.proposal.uuid}/",
            {"response": StudentProposal.ACCEPT},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.proposal.refresh_from_db()
        self.assertEqual(self.proposal.response["value"], StudentProposal.ACCEPT)

    def test_records_reject_response(self):
        response = self.client.post(
            f"/api/review-student/{self.proposal.uuid}/",
            {"response": StudentProposal.REJECT},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.proposal.refresh_from_db()
        self.assertEqual(self.proposal.response["value"], StudentProposal.REJECT)

    def test_rejects_second_response(self):
        StudentProposalService.update_response(self.proposal, StudentProposal.ACCEPT)

        response = self.client.post(
            f"/api/review-student/{self.proposal.uuid}/",
            {"response": StudentProposal.REJECT},
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["error"], "Response already recorded")


class ReviewStudentPatchTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.mentor = Mentor.objects.create(name="Alex", email="alex@example.com")
        self.mentor_request = MentorRequest.objects.create(student_name="Jamie")
        self.proposal = StudentProposal.objects.create(mentor=self.mentor, mentor_request=self.mentor_request)
        StudentProposalService.update_response(self.proposal, StudentProposal.REJECT)

    def test_records_decline_reason(self):
        response = self.client.patch(
            f"/api/review-student/{self.proposal.uuid}/",
            {"reason": {"no_good_fit": True}, "match_rating": 3},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.proposal.refresh_from_db()
        self.assertEqual(self.proposal.response["reason"], {"no_good_fit": True})
        self.assertEqual(self.proposal.response["match_rating"], 3)

    def test_rejects_second_reason(self):
        self.client.patch(
            f"/api/review-student/{self.proposal.uuid}/",
            {"reason": {"no_bandwidth": True}},
            format="json",
        )

        response = self.client.patch(
            f"/api/review-student/{self.proposal.uuid}/",
            {"reason": {"timezone_issue": True}},
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["error"], "Reason already recorded")


class ProposalActiveTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.mentor = Mentor.objects.create(name="Alex", email="alex@example.com")
        self.mentor_request = MentorRequest.objects.create(student_name="Jamie")
        self.proposal = StudentProposal.objects.create(mentor=self.mentor, mentor_request=self.mentor_request)

    def test_returns_student_and_open_status(self):
        response = self.client.get(f"/api/proposal-active/{self.proposal.uuid}/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["student_name"], "Jamie")
        self.assertFalse(response.data["is_matched"])
        self.assertIsNone(response.data["response_value"])

class ReviewStudentStaleStateTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.mentor = Mentor.objects.create(name="Alex", email="alex@example.com")
        self.mentor_request = MentorRequest.objects.create(student_name="Jamie")
        self.proposal = StudentProposal.objects.create(mentor=self.mentor, mentor_request=self.mentor_request)

    def test_old_route_allows_stale_state(self):
        self.client.post(
            f"/api/review-student/{self.proposal.uuid}/",
            {"response": StudentProposal.ACCEPT},
            format="json",
        )

        self.client.patch(
            f"/api/review-student/{self.proposal.uuid}/",
            {"response": "reject", "reason": {"no_good_fit": True}, "match_rating": 3},
            format="json",
        )

        self.proposal.refresh_from_db()
        self.assertEqual(self.proposal.response["value"], "reject")
        self.assertEqual(self.proposal.response["reason"], {"no_good_fit": True})
        self.assertEqual(self.proposal.response["match_rating"], 3)

    def test_new_route_overrides_stale_state_with_reject(self):
        self.client.post(
            f"/api/review-student/{self.proposal.uuid}/v2/",
            {"response": StudentProposal.ACCEPT},
            format="json",
        )

        self.client.patch(
            f"/api/review-student/{self.proposal.uuid}/v2/",
            {"response": StudentProposal.REJECT, "reason": {"no_good_fit": True}, "match_rating": 1},
            format="json",
        )

        self.proposal.refresh_from_db()
        self.assertEqual(self.proposal.response["value"], StudentProposal.REJECT)

    def test_new_route_overrides_stale_state_with_accept(self):
        self.client.post(
            f"/api/review-student/{self.proposal.uuid}/v2/",
            {"response": StudentProposal.REJECT},
            format="json",
        )

        self.client.patch(
            f"/api/review-student/{self.proposal.uuid}/v2/",
            {"response": StudentProposal.ACCEPT, "reason": {"no_good_fit": True}, "match_rating": 8},
            format="json",
        )

        self.proposal.refresh_from_db()
        self.assertEqual(self.proposal.response["value"], StudentProposal.ACCEPT)
        self.assertNotIn("reason", self.proposal.response)
        self.assertEqual(self.proposal.response["match_rating"], 8)
