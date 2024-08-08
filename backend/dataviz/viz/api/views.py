from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import InsightData
from ..serializers import InsightDataSerializer








@api_view(['GET', 'POST'])
def insight_list(request):
    if request.method == 'GET':
        insights = InsightData.objects.all()
        serializer = InsightDataSerializer(insights, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = InsightDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def insight_detail(request, id):
    try:
        insight = InsightData.objects.get(pk=id)
    except InsightData.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = InsightDataSerializer(insight)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = InsightDataSerializer(insight, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        insight.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

