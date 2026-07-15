import uuid

from django.conf import settings
from django.db import models


class Mentor(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()

    def __str__(self):
        return self.name


class MentorRequest(models.Model):
    MATCHING = "matching"
    MATCHED = "matched"
    DECLINED = "declined"

    STATUS_CHOICES = [
        (MATCHING, "Matching"),
        (MATCHED, "Matched"),
        (DECLINED, "Declined"),
    ]

    student_name = models.CharField(max_length=200)
    student_interests = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=MATCHING)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student_name} ({self.status})"

    @property
    def is_closed_for_proposals(self) -> bool:
        return self.status in {self.MATCHED, self.DECLINED}


class StudentProposal(models.Model):
    """Proposal sent to a mentor about a potential student match.

    models.JSONField keys of 'response':
    value -- string [reject, accept] marking response of mentor for proposal
    reason.no_good_fit -- boolean marking lack of fit
    reason.no_bandwidth -- boolean marking lack of time
    reason.timezone_issue -- boolean marking the students timezone as an issue
    reason.unavailable_until -- isodate string if no_bandwidth is True
    reason.other -- string for reason
    match_rating -- number [0-10] marking satisfaction of matching
    recorded_at -- datetime
    """

    ACCEPT = "accept"
    REJECT = "reject"

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)
    mentor_request = models.ForeignKey(MentorRequest, on_delete=models.CASCADE)
    response = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        value = self.response.get("value") or "pending"
        return f"Proposal {self.uuid} → {self.mentor.name} ({value})"

    @property
    def yes_url(self) -> str:
        return f"{settings.FRONTEND_URL}/review-student/{self.uuid}/{self.ACCEPT}"

    @property
    def no_url(self) -> str:
        return f"{settings.FRONTEND_URL}/review-student/{self.uuid}/{self.REJECT}"

    @property
    def accepted(self) -> bool:
        return self.answered() and self.response.get("value") == self.ACCEPT

    @property
    def rejected(self) -> bool:
        return self.answered() and self.response.get("value") == self.REJECT

    def answered(self) -> bool:
        return bool(self.response and self.response.get("value") is not None)


class OutboxMessage(models.Model):
    subject = models.CharField(max_length=255)
    recipient = models.EmailField()
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} → {self.recipient}"
