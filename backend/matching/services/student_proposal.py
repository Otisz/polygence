from typing import Literal

from django.utils import timezone

from matching.models import Mentor, MentorRequest, StudentProposal


class StudentProposalService:
    @staticmethod
    def create(mentor_request: MentorRequest, mentor: Mentor) -> StudentProposal:
        return StudentProposal.objects.create(mentor_request=mentor_request, mentor=mentor)

    @staticmethod
    def get_by_uuid(proposal_uuid: str) -> StudentProposal | None:
        return StudentProposal.objects.filter(uuid=proposal_uuid).first()

    @staticmethod
    def update_response(
        student_proposal: StudentProposal,
        response: Literal[StudentProposal.ACCEPT] | Literal[StudentProposal.REJECT],
    ) -> None:
        proposal_response = {
            "recorded_at": timezone.now().isoformat(),
            "value": response,
        }

        student_proposal.response = proposal_response
        student_proposal.save(update_fields=["response", "updated_at"])

    @staticmethod
    def update_reason_and_rating(student_proposal: StudentProposal, reason, rating) -> None:
        if rating is not None:
            student_proposal.response["match_rating"] = rating

        if reason:
            student_proposal.response["reason"] = reason

        student_proposal.save(update_fields=["response", "updated_at"])
