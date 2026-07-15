from django.contrib import admin

from matching.models import Mentor, MentorRequest, OutboxMessage, StudentProposal


@admin.register(Mentor)
class MentorAdmin(admin.ModelAdmin):
    list_display = ("name", "email")


@admin.register(MentorRequest)
class MentorRequestAdmin(admin.ModelAdmin):
    list_display = ("student_name", "status", "created_at")
    list_filter = ("status",)


@admin.register(StudentProposal)
class StudentProposalAdmin(admin.ModelAdmin):
    list_display = ("uuid", "mentor", "student_name", "response_value", "created_at")

    @admin.display(description="Student")
    def student_name(self, obj):
        return obj.mentor_request.student_name

    @admin.display(description="Response value")
    def response_value(self, obj):
        return obj.response.get("value") or "—"


@admin.register(OutboxMessage)
class OutboxMessageAdmin(admin.ModelAdmin):
    list_display = ("subject", "recipient", "created_at")
    readonly_fields = ("subject", "recipient", "body", "created_at")
