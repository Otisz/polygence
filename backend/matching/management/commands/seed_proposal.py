from django.core.management.base import BaseCommand

from matching.models import Mentor, MentorRequest, OutboxMessage, StudentProposal
from matching.services.proposition import StudentPropositionService


class Command(BaseCommand):
    help = "Reset demo data and create one student proposal with accept/decline email links"

    def handle(self, *args, **options):
        OutboxMessage.objects.all().delete()
        StudentProposal.objects.all().delete()
        MentorRequest.objects.all().delete()
        Mentor.objects.all().delete()

        mentor = Mentor.objects.create(name="Alex Mentor", email="alex.mentor@example.com")
        mentor_request = MentorRequest.objects.create(
            student_name="Jamie Student",
            student_interests="machine learning, computational biology",
            status=MentorRequest.MATCHING,
        )
        proposal = StudentPropositionService.propose_mentor_to_student(mentor_request, mentor)

        self.stdout.write(self.style.SUCCESS("Seeded proposal"))
        self.stdout.write(f"  uuid:    {proposal.uuid}")
        self.stdout.write(f"  accept:  {proposal.yes_url}")
        self.stdout.write(f"  decline: {proposal.no_url}")
        self.stdout.write("  outbox:  http://localhost:5173/  (Dev inbox)")
        self.stdout.write("  admin:   http://localhost:8000/admin/")
