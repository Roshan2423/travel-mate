from django.contrib import admin
from .models import QuestionAnswer, UserInteraction, UserLoginData

class QuestionAnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer')

class UserInteractionAdmin(admin.ModelAdmin):
    list_display = ('user_question', 'bot_response', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user_question', 'bot_response')

class UserLoginDataAdmin(admin.ModelAdmin):
    list_display = ('user', 'login_time', 'ip_address')
    list_filter = ('login_time', 'user')
    search_fields = ('user__username', 'ip_address')

admin.site.register(QuestionAnswer, QuestionAnswerAdmin)
admin.site.register(UserInteraction, UserInteractionAdmin)
admin.site.register(UserLoginData, UserLoginDataAdmin)
