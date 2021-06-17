from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer

# Create your views here.


@api_view(['GET'])
def get_daily_planner(request):

    return


