from rest_framework.response import Response
from rest_framework.views import APIView
from django.http.response import JsonResponse
from .models import EppAction, EppProduct, EppGrppymntmd, EppErrormessage, EppGrpmstr
from .serializers import EppActionSerializer, EppProductSerializer, EppGrppymntmdSerializer, EppErrormessageSerializer, \
    EppGrpmstrSerializer


class EppActionList(APIView):
    def get(self, request):
        actions = EppAction.objects.all()
        data = EppActionSerializer(actions, many=True).data
        return Response(data)


class EppProductList(APIView):
    def get(self, request):
        products = EppProduct.objects.all()
        data = EppProductSerializer(products, many=True).data
        return Response(data)


class EppGrppymntmdList(APIView):
    def get(self, request):
        payments = EppGrppymntmd.objects.all()
        data = EppGrppymntmdSerializer(payments, many=True).data
        return Response(data)


class SitusStateSerializerList(APIView):
    state_data = {"situsState": [
        {"id": 0, "state": '''---Select---'''},
        {"Id": "AL", "State": "AL"},
        {"Id": "AK", "State": "AK"},
        {"Id": "AZ", "State": "AZ"},
        {"Id": "AR", "State": "AR"},
        {"Id": "CA", "State": "CA"},
        {"Id": "CO", "State": "CO"},
        {"Id": "CT", "State": "CT"},
        {"Id": "DC", "State": "DC"},
        {"Id": "DE", "State": "DE"},
        {"Id": "FL", "State": "FL"},
        {"Id": "GA", "State": "GA"},
        {"Id": "HI", "State": "HI"},
        {"Id": "ID", "State": "ID"},
        {"Id": "IL", "State": "IL"},
        {"Id": "IN", "State": "IN"},
        {"Id": "IA", "State": "IA"},
        {"Id": "KS", "State": "KS"},
        {"Id": "KY", "State": "KY"},
        {"Id": "LA", "State": "LA"},
        {"Id": "ME", "State": "ME"},
        {"Id": "MD", "State": "MD"},
        {"Id": "MA", "State": "MA"},
        {"Id": "MI", "State": "MI"},
        {"Id": "MN", "State": "MN"},
        {"Id": "MS", "State": "MS"},
        {"Id": "MO", "State": "MO"},
        {"Id": "MT", "State": "MT"},
        {"Id": "NE", "State": "NE"},
        {"Id": "NV", "State": "NV"},
        {"Id": "NH", "State": "NH"},
        {"Id": "NJ", "State": "NJ"},
        {"Id": "NM", "State": "NM"},
        {"Id": "NY", "State": "NY"},
        {"Id": "NC", "State": "NC"},
        {"Id": "ND", "State": "ND"},
        {"Id": "OH", "State": "OH"},
        {"Id": "OK", "State": "OK"},
        {"Id": "OR", "State": "OR"},
        {"Id": "PA", "State": "PA"},
        {"Id": "RI", "State": "RI"},
        {"Id": "SC", "State": "SC"},
        {"Id": "SD", "State": "SD"},
        {"Id": "TN", "State": "TN"},
        {"Id": "TX", "State": "TX"},
        {"Id": "UT", "State": "UT"},
        {"Id": "VT", "State": "VT"},
        {"Id": "VA", "State": "VA"},
        {"Id": "WA", "State": "WA"},
        {"Id": "WV", "State": "WV"},
        {"Id": "WI", "State": "WI"},
        {"Id": "WY", "State": "WY"},
        {"Id": "PR", "State": "PR"},
        {"Id": "VI", "State": "VI"}]
    }

    def get(self, request):
        return Response(self.state_data)


class EppErrormessageList(APIView):
    def get(self, request):
        error_data = EppErrormessage.objects.all()
        data = EppErrormessageSerializer(error_data, many=True).data
        return Response(data)


class EppGrpmstrList(APIView):
    def get(self, request):
        grouppy_data = EppGrpmstr.objects.all()
        data = EppGrpmstrSerializer(grouppy_data, many=True).data
        return Response(data)

