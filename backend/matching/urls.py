from django.urls import path

from matching.views import get_proposal_active, list_outbox, list_proposals, review_student

urlpatterns = [
    path("review-student/<uuid:current>/", review_student),
    path("proposal-active/<uuid:student_proposal_uuid>/", get_proposal_active),
    path("proposals/", list_proposals),
    path("outbox/", list_outbox),
]
