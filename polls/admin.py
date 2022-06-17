from django.contrib import admin
from .models import Question, Choice

class ChoiceInline(admin.TabularInline):
  model = Choice
  extra = 3

class QuestionAdmin(admin.ModelAdmin):
  list_display = ('question_test', 'pub_date', 'was_published_recently')

  fieldsets = [
    (None,               {'fields': ['question_test']}),
    ('Date information', {'fields': ['pub_date']}),
  ]
  inlines = [ChoiceInline]

  list_filter = ['pub_date']
  search_fields = ['question_test']

admin.site.register(Question, QuestionAdmin)