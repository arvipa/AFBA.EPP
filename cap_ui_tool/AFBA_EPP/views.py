from rest_framework.response import Response
from rest_framework.views import APIView
from django.http.response import JsonResponse
from .models import EppAction, EppProduct, EppGrppymntmd, EppErrormessage, EppGrpmstr, \
    EppGrpprdct, EppBulkreftbl, EppAttribute, EppEnrlmntPrtnrs
from .serializers import EppActionSerializer, EppProductSerializer, EppGrppymntmdSerializer, EppErrormessageSerializer, \
    EppGrpmstrSerializer, EppGrpmstrPostSerializers, EppCrtGrpmstrSerializer, EppGrpAgentSerializer
from rest_framework import status, generics
import random as rand
from datetime import datetime, timezone

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


class EppGrpagentList(APIView):
    def get(self, request):
        grouppy_data = EppGrpmstr.objects.all()
        data = EppGrpAgentSerializer(grouppy_data, many=True).data
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
                print("------db_attr_name----", db_attr_name + "_action")
                db_attr_name_action = db_attr_name + "_action"
                db_attr_value = blk_dat['value']
                db_attr_value_action = blk_dat['action_id']
                return_data[0].setdefault(pr_key, {}).update({db_attr_name: db_attr_value})
                return_data[0].setdefault(pr_key, {}).update({db_attr_name_action: db_attr_value_action})
        return Response(return_data)


class DateRand:
    def randgen(self):
        today = self.getCurntUtcTime()
        return str(rand.randint(1, 99999)) + today.strftime('%m%d') + '0' + today.strftime('%y') + today.strftime('%H%M%S')

    def getCurntUtcTime(self):
        return datetime.now(timezone.utc)


class EppCreateGrpList(generics.CreateAPIView):
    serializer_class = EppCrtGrpmstrSerializer
    serializer_agent = EppGrpAgentSerializer

    def post(self, request):
        f1 = DateRand()
        todayDt = f1.getCurntUtcTime()
        grpNumberRandom = f1.randgen()

        if not (EppGrppymntmd.objects.filter(grppymn_id=request.data['grpPymn']).exists()):
            pymntmthd = EppGrppymntmd(grppymn_id=request.data['grpPymn'], grp_pymnt_md_cd='', grp_pymnt_md_nm='',\
                                       crtd_dt=todayDt.strftime('%Y-%m-%d'),crtd_by='Batch',lst_updt_dt=todayDt.strftime('%Y-%m-%d'),\
                                       lst_updt_by='Batch')
            pymntmthd.save()
            print(status)
            pymnt_fk = EppGrppymntmd.objects.get(pk=request.data['grpPymn'])
        else:
            pymnt_fk = EppGrppymntmd.objects.get(pk=request.data['grpPymn'])
        print(pymnt_fk)
        enrollment_fk = EppEnrlmntPrtnrs.objects.get(pk=request.data['enrlmntPrtnrsId'])
        print('Before fk')
        request.data['crtdBy'] = 'Batch'
        request.data['grpId'] = grpNumberRandom
        request.data['crtdDt'] =todayDt.strftime('%Y-%m-%d')
        request.data['lstUpdtDt'] =todayDt.strftime('%Y-%m-%d')
        request.data['lstUpdtBy'] = 'Batch'
        grp_mastr = EppGrpmstr(grppymn=pymnt_fk, enrlmnt_prtnrs=enrollment_fk)
        serializer = EppCrtGrpmstrSerializer(grp_mastr, data=request.data)
        print(request.data['crtdDt'])
        print(request.data)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            return Response("Group No. " + str(request.data['grpNbr']) + " updated sucessfully!", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)