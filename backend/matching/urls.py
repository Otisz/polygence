from django.urls import path

from matching.views import get_proposal_active, list_outbox, list_proposals, review_student, review_student_v2

urlpatterns = [
    path("review-student/<uuid:current>/v2/", review_student_v2),
    path("review-student/<uuid:current>/", review_student),
    path("proposal-active/<uuid:student_proposal_uuid>/", get_proposal_active),
    path("proposals/", list_proposals),
    path("outbox/", list_outbox),
]
