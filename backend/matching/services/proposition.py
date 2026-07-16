from matching.models import Mentor, MentorRequest, OutboxMessage, StudentProposal
from matching.services.student_proposal import StudentProposalService


class StudentPropositionService:
    @staticmethod
    def propose_mentor_to_student(mentor_request: MentorRequest, mentor: Mentor) -> StudentProposal:
        proposal = StudentProposalService.create(mentor_request=mentor_request, mentor=mentor)
        StudentPropositionService._send_proposal_email(proposal)
        return proposal

    @staticmethod
    def _send_proposal_email(proposal: StudentProposal) -> OutboxMessage:
        student_name = proposal.mentor_request.student_name
        body = (
            f"Hi {proposal.mentor.name},\n\n"
            f"We think {student_name} could be a great match for you.\n\n"
            f"Interests: {proposal.mentor_request.student_interests or 'n/a'}\n\n"
            f"Accept: {proposal.yes_url}\n"
            f"Decline: {proposal.no_url}\n\n"
            "Thanks!\nMatching Team"
        )
        return OutboxMessage.objects.create(
            subject=f"Student proposal: {student_name}",
            recipient=proposal.mentor.email,
            body=body,
        )
