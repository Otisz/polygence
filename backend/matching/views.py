from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response

from matching.models import OutboxMessage, StudentProposal
from matching.services.student_proposal import StudentProposalService


@api_view(["POST", "PATCH"])
@authentication_classes([])
@permission_classes([])
def review_student(request, current):
    student_proposal: StudentProposal | None = StudentProposalService.get_by_uuid(current)

    if not student_proposal:
        return Response({"error": "Student proposal not found"}, 400)

    if request.method == "POST":
        response = request.data.get("response")

        if not response:
            return Response({"error": "Missing response"}, 400)

        if response not in {StudentProposal.ACCEPT, StudentProposal.REJECT}:
            return Response({"error": "Unsupported response"}, 400)

        if "value" in student_proposal.response:
            return Response({"error": "Response already recorded"}, 400)

        StudentProposalService.update_response(student_proposal, response)
        return Response({"message": "Response recorded", "success": True})

    if request.method == "PATCH":
        reason = request.data.get("reason")
        match_rating = request.data.get("match_rating")

        if "reason" in student_proposal.response:
            return Response({"error": "Reason already recorded"}, 400)

        StudentProposalService.update_reason_and_rating(student_proposal, reason, match_rating)
        return Response({"message": "Reason recorded", "success": True})

    return Response(data={"message": "Method Not Allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(["POST", "PATCH"])
@authentication_classes([])
@permission_classes([])
def review_student_v2(request, current):
    student_proposal: StudentProposal | None = StudentProposalService.get_by_uuid(current)

    if not student_proposal:
        return Response({"error": "Student proposal not found"}, 400)

    response = request.data.get("response")

    if request.method == "POST":

        if not response:
            return Response({"error": "Missing response"}, 400)

        if response not in {StudentProposal.ACCEPT, StudentProposal.REJECT}:
            return Response({"error": "Unsupported response"}, 400)

        if "value" in student_proposal.response:
            return Response({"error": "Response already recorded"}, 400)

        StudentProposalService.update_response(student_proposal, response)
        return Response({"message": "Response recorded", "success": True})

    if request.method == "PATCH":
        reason = request.data.get("reason")
        match_rating = request.data.get("match_rating")

        if "reason" in student_proposal.response:
            return Response({"error": "Reason already recorded"}, 400)

        StudentProposalService.update_response(student_proposal, response)

        if response == StudentProposal.ACCEPT:
            StudentProposalService.update_reason_and_rating(student_proposal, None, match_rating)
        else:
            StudentProposalService.update_reason_and_rating(student_proposal, reason, None)
        return Response({"message": "Reason recorded", "success": True})

    return Response(data={"message": "Method Not Allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(["GET"])
@authentication_classes([])
@permission_classes([])
def get_proposal_active(request, student_proposal_uuid):
    student_proposal = StudentProposalService.get_by_uuid(student_proposal_uuid)

    if not student_proposal:
        return Response({"error": "Student proposal not found"}, status=status.HTTP_404_NOT_FOUND)

    mentor_request = student_proposal.mentor_request

    return Response(
        {
            "is_matched": mentor_request.is_closed_for_proposals,
            "student_name": mentor_request.student_name,
            "response_value": student_proposal.response.get("value"),
        }
    )


@api_view(["GET"])
@authentication_classes([])
@permission_classes([])
def list_proposals(request):
    proposals = StudentProposal.objects.select_related("mentor", "mentor_request").order_by("-created_at")
    return Response(
        [
            {
                "uuid": str(proposal.uuid),
                "mentor_name": proposal.mentor.name,
                "student_name": proposal.mentor_request.student_name,
                "response": proposal.response,
                "yes_url": proposal.yes_url,
                "no_url": proposal.no_url,
            }
            for proposal in proposals
        ]
    )


@api_view(["GET"])
@authentication_classes([])
@permission_classes([])
def list_outbox(request):
    messages = OutboxMessage.objects.order_by("-created_at")
    return Response(
        [
            {
                "id": message.id,
                "subject": message.subject,
                "recipient": message.recipient,
                "body": message.body,
                "created_at": message.created_at.isoformat(),
            }
            for message in messages
        ]
    )
