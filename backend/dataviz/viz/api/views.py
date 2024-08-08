from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django_filters import rest_framework as filters
from ..models import InsightData
from ..serializers import InsightDataSerializer







@api_view(['GET', 'POST'])
def insight_list(request):
    if request.method == 'GET':
        insights = InsightData.objects.all()
        
        #filters
        end_year = request.query_params.get('end_year')
        topic = request.query_params.get('topic')
        sector = request.query_params.get('sector')
        region = request.query_params.get('region')
        pestle = request.query_params.get('pestle')
        source = request.query_params.get('source')
        swot = request.query_params.get('swot')
        country = request.query_params.get('country')
        
        if end_year:
            insights = insights.filter(end_year=end_year)
        if topic:
            insights = insights.filter(topic__icontains=topic)
        if sector:
            insights = insights.filter(sector__icontains=sector)
        if region:
            insights = insights.filter(region__icontains=region)
        if pestle:
            insights = insights.filter(pestle__icontains=pestle)
        if source:
            insights = insights.filter(source__icontains=source)
        if swot:
            insights = insights.filter(swot__icontains=swot)
        if country:
            insights = insights.filter(country__icontains=country)

        
        serializer = InsightDataSerializer(insights, many=True)
        data = { "length": len(serializer.data), "data": serializer.data}
        return Response(data)
    
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

