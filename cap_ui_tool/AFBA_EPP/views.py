from rest_framework.response import Response
from rest_framework.views import APIView
from django.http.response import JsonResponse
from .models import EppAction, EppProduct, EppGrppymntmd, EppErrormessage, EppGrpmstr, \
    EppGrpprdct, EppBulkreftbl, EppAttribute
from .serializers import EppActionSerializer, EppProductSerializer, EppGrppymntmdSerializer, EppErrormessageSerializer, \
    EppGrpmstrSerializer, EppGrpmstrPostSerializers
from rest_framework import status, generics


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


class EppGrpmstrPostList(generics.ListAPIView):
    # serializer_class = EppGrpmstrPostSerializers
    #
    # def get_queryset(self):
    #     group_nbr = self.kwargs['grpNbr']
    #     return EppGrpmstr.objects.filter(grp_nbr=group_nbr)
    def get(self, request, grpNbr):
        # Get Group data
        group_nbr = self.kwargs['grpNbr']
        group_data = EppGrpmstr.objects.filter(grp_nbr=group_nbr).select_related()
        group_dict = list(group_data.values())[0]
        return_data = EppGrpmstrPostSerializers(group_data, many=True).data
        # Using group_id from group data dict get all group products.
        grp_prd_data = EppGrpprdct.objects.filter(grp=group_dict['grp_id']).prefetch_related('eppproduct')
        grp_prod_lst = list(grp_prd_data.values())
        # Use loop to add product and its bulk data and attributes in return data.
        for grprd_data in grp_prod_lst:
            prd_data = EppProduct.objects.filter(product_id=grprd_data['product_id'])
            prd_dict = list(prd_data.values())[0]
            # print("prd_dict >>> ", prd_dict)
            pr_key = prd_dict['product_nm'].lower()
            return_data[0].setdefault(pr_key, {})
            bulk_data = EppBulkreftbl.objects.filter(grpprdct=grprd_data['grpprdct_id'])
            bulk_data_lst = list(bulk_data.values())
            for blk_dat in bulk_data_lst:
                # print(blk_dat)
                prd_attr_data = EppAttribute.objects.filter(attr_id=blk_dat['attr_id'])
                prd_attr_list = list(prd_attr_data.values())
                db_attr_name = prd_attr_list[0]['db_attr_nm']
                db_attr_value =blk_dat['value']
                return_data[0].setdefault(pr_key, {}).update({db_attr_name: db_attr_value})
        return Response(return_data)
