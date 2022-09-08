from django.urls import path
from googlesheet.views import GoogleSheetView

urlpatterns = [
    path('', GoogleSheetView.as_view(), name='sheet_url'),
]
