from xmlrpc.client import ResponseError
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from .serializers import IncomeSerializer, SourceSerializer
from .models import Income,  Source


@api_view(http_method_names=['GET', 'POST'])
@permission_classes([IsAuthenticated])
def sources(request: Request) -> Response:

    if request.method == 'GET':
        sources = Source.objects.filter(user=request.user)
        source_serializer = SourceSerializer(sources, many=True)
        return Response(source_serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        data = request.data
        data['user'] = request.user.pk
        source_serializer = SourceSerializer(data=data)
        if source_serializer.is_valid():
            source_serializer.save()
            return Response(source_serializer.data, status=status.HTTP_201_CREATED)
        return Response(source_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(http_method_names=['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def update_sources(request: Request, pk: int) -> Response:
    user = request.user.pk

    if request.method == 'PUT':
        data = request.data
        data['user'] = user
        source_exists = Source.objects.get(pk=pk)

        if source_exists:
            source_serializer = SourceSerializer(source_exists, data=data)

            if source_serializer.is_valid():
                source_serializer.save()
                return Response(source_serializer.data, status=status.HTTP_205_RESET_CONTENT)

            return Response(source_serializer.errors, status=status.HTTP_424_FAILED_DEPENDENCY)

        else:
            return Response({'data': 'source don\'t exists'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        source_exists = Source.objects.filter(user=user, pk=pk)
        if source_exists:
            source_exists.delete()
            return Response({'message': 'the source has been deleted '}, status=status.HTTP_204_NO_CONTENT)
        return Response({'message': 'source dont\'t exists'}, status=status.HTTP_404_NOT_FOUND)


@api_view(http_method_names=['GET', 'POST'])
@permission_classes([IsAuthenticated])
def income(request: Request) -> Response:

    if request.method == 'GET':
        incomes = Income.objects.filter(user=request.user)
        serialized_incomes = IncomeSerializer(incomes, many=True)
        return Response(serialized_incomes.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        list_sources = []
        data = request.data.copy()
        data['user'] = request.user.pk

        sources = request.data.pop('source')
        if sources:
            for source in sources:
                check_source = Source.objects.filter(pk=source['id']).first()
                if check_source:
                    s_serializer = SourceSerializer(check_source, many=False)
                    list_sources.append(
                        {'user': request.user.pk, **s_serializer.data})

        data['source'] = list_sources

        serialized_income = IncomeSerializer(data=data)

        if serialized_income.is_valid():
            serialized_income.save()
            return Response(serialized_income.data, status=status.HTTP_201_CREATED)
        return Response(serialized_income.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(http_method_names=['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def income_details(request: Request, pk: int) -> Response:
    user = request.user.pk

    if request.method == "PUT":
        data = request.data.copy()
        data['user'] = user
        income = Income.objects.filter(user=user, pk=pk).first()

        if income:
            serialized_income = IncomeSerializer(income, data=data)

            if serialized_income.is_valid():
                serialized_income.save()
                return Response(serialized_income.data, status=status.HTTP_202_ACCEPTED)

            return Response(serialized_income.errors, status=status.HTTP_424_FAILED_DEPENDENCY)
        else:
            return Response({'message': "Income of this credentials don't exits"}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "DELETE":
        income_existis = Income.objects.filter(user=user, pk=pk).first()
        if income_existis:
            income_existis.delete()
            return Response({'data': 'removed'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'data': 'error could not edit the source'}, status=status.HTTP_404_NOT_FOUND)
