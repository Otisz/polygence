from django.test import TestCase

from matching.models import Mentor, MentorRequest, OutboxMessage, StudentProposal
from matching.services.proposition import StudentPropositionService
from matching.services.student_proposal import StudentProposalService


class StudentProposalServiceTestCase(TestCase):
    def setUp(self):
        self.mentor = Mentor.objects.create(name="Alex", email="alex@example.com")
        self.mentor_request = MentorRequest.objects.create(
            student_name="Jamie",
            student_interests="biology",
        )

    def test_update_response_sets_value(self):
        proposal = StudentProposalService.create(self.mentor_request, self.mentor)
        StudentProposalService.update_response(proposal, StudentProposal.ACCEPT)

        proposal.refresh_from_db()
        self.assertEqual(proposal.response["value"], StudentProposal.ACCEPT)
        self.assertIn("recorded_at", proposal.response)

    def test_propose_writes_outbox_with_links(self):
        proposal = StudentPropositionService.propose_mentor_to_student(self.mentor_request, self.mentor)

        self.assertTrue(proposal.yes_url.endswith(f"/{proposal.uuid}/accept"))
        self.assertTrue(proposal.no_url.endswith(f"/{proposal.uuid}/reject"))

        message = OutboxMessage.objects.get()
        self.assertIn(proposal.yes_url, message.body)
        self.assertIn(proposal.no_url, message.body)
