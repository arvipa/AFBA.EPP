from rest_framework.response import Response
from rest_framework.views import APIView
from django.http.response import JsonResponse
from .models import EppAction, EppProduct, EppGrppymntmd, EppErrormessage, EppGrpmstr, \
    EppGrpprdct, EppBulkreftbl, EppAttribute, EppEnrlmntPrtnrs,EppAgents
from .serializers import EppActionSerializer, EppProductSerializer, EppGrppymntmdSerializer, EppErrormessageSerializer, \
    EppGrpmstrSerializer, EppGrpmstrPostSerializers, EppCrtGrpmstrSerializer, EppGrpAgentSerializer
from rest_framework import status, generics
import random as rand
from datetime import datetime, timezone
from AFBA_EPP.config import PRODUCTS
from AFBA_EPP.utils import add_product_attr

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
        return_data = EppGrpmstrcdPostSerializers(group_data, many=True).data
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
            # From configuration get all attributes required within the product.
            prd_attr_conf = PRODUCTS.get(pr_key, ())
            add_product_attr(return_data, pr_key, prd_attr_conf)
            bulk_data = EppBulkreftbl.objects.filter(grpprdct=grprd_data['grpprdct_id'])
            bulk_data_lst = list(bulk_data.values())
            for blk_dat in bulk_data_lst:
                # print(blk_dat)
                prd_attr_data = EppAttribute.objects.filter(attr_id=blk_dat['attr_id'])
                prd_attr_list = list(prd_attr_data.values())
                db_attr_name = prd_attr_list[0]['db_attr_nm']
                db_attr_value = blk_dat['value']
                return_data[0].setdefault(pr_key, {}).update({db_attr_name: db_attr_value})
                db_attr_value_action = blk_dat['action_id']
                if db_attr_name.find("_action") > 1:
                    return_data[0].setdefault(pr_key, {}).update({db_attr_name: db_attr_value_action})
        return Response(return_data)


class DateRand:
    def randgen(self):
        today = self.getCurntUtcTime()
        return str(rand.randint(1, 99999)) + today.strftime('%m%d') + '0' + today.strftime('%y') + today.strftime('%H%M%S')

    def getCurntUtcTime(self):
        return datetime.now(timezone.utc)


class EppCreateGrpList(generics.CreateAPIView):
    serializer_class = EppCrtGrpmstrSerializer

    def post(self, request):
        f1 = DateRand()
        todayDt = f1.getCurntUtcTime()
        grpNumberRandom = f1.randgen()
        if EppGrppymntmd.objects.filter(pk=request.data['grpPymn']).exists():
            pymnt_fk = EppGrppymntmd.objects.get(pk=request.data['grpPymn'])
        else:
            return Response("grpPymn {} is not present in EppGrppymntmd".format(request.data['grpPymn']), status=status.HTTP_400_BAD_REQUEST)
        request.data['enrlmntPrtnrsId'] = self.validateEnrlmnt(request.data)
        enrollment_fk = EppEnrlmntPrtnrs.objects.get(pk=request.data['enrlmntPrtnrsId'])
        request.data['crtdBy'] = 'Batch'
        request.data['grpId'] = grpNumberRandom
        request.data['crtdDt'] =todayDt.strftime('%Y-%m-%d')
        request.data['lstUpdtDt'] =todayDt.strftime('%Y-%m-%d')
        request.data['lstUpdtBy'] = 'Batch'
        print(request.data['grpEfftvDt'])
        grp_mastr = EppGrpmstr(grppymn=pymnt_fk, enrlmnt_prtnrs=enrollment_fk)
        serializer = EppCrtGrpmstrSerializer(grp_mastr, data=request.data)
        if serializer.is_valid():
            print("serializer valid")
            try:
               grpMstrMthd = EppGrpmstr(grp_id=request.data['grpId'], grp_nbr=request.data['grpNbr'],\
                                        grp_nm=request.data['grpNm'],grp_efftv_dt=request.data['grpEfftvDt'], \
                                        grp_situs_st=request.data['grpSitusSt'], actv_flg=request.data['actvFlg'], \
                                        grppymn=pymnt_fk, enrlmnt_prtnrs=enrollment_fk,\
                                        crtd_dt= request.data['crtdDt'],crtd_by= request.data['crtdBy'],\
                                        lst_updt_dt=request.data['lstUpdtDt'],lst_updt_by=request.data['lstUpdtBy'],\
                                        occ_class=request.data['occClass'],acct_mgr_nm=request.data['acctMgrNm'],\
                                        acct_mgr_email_addrs=request.data['acctMgrEmailAddrs'],\
                                        usr_tkn=request.data['acctMgrEmailAddrs'],case_tkn=request.data['acctMgrEmailAddrs'])
               grpMstrMthd.save()
               print("Before Agent Creation")
               self.AddAgentDet(request.data)
               return Response("Group No. " + str(request.data['grpNbr']) + " updated sucessfully!",
                        status=status.HTTP_200_OK)
            except Exception:
                return Response("Error while inserting into Erpgrpmstr", status=status.HTTP_400_BAD_REQUEST)
        return Response("Error", status=status.HTTP_400_BAD_REQUEST)


    def AddAgentDet(self,data):
        try:
            grpId_fk = EppGrpmstr.objects.get(pk=data['grpId'])
            Agentmthd = EppAgents(agent_id=data['grpAgents'][0]['agentId'],agnt_nbr =data['grpAgents'][0]['agntNbr'], \
                              agnt_nm=data['grpAgents'][0]['agntNm'], agnt_sub_cnt=data['grpAgents'][0]['agntSubCnt'],\
                              agnt_comsn_splt=data['grpAgents'][0]['agntComsnSplt'],grp=grpId_fk,\
                              crtd_dt=data['crtdDt'], crtd_by=data['crtdBy'])
            Agentmthd.save()

        except Exception:
            return Response("Error while inserting into EppAgents", status=status.HTTP_400_BAD_REQUEST)

    def validateEnrlmnt(self,data):
        try:
            f2 = DateRand()
            if EppEnrlmntPrtnrs.objects.filter(eml_addrss=data['emlAddrss']).exists():
                enrldict = EppEnrlmntPrtnrs.objects.filter(eml_addrss=data['emlAddrss']).values('enrlmnt_prtnrs_id')
                enrlmntRandom=enrldict[0]['enrlmnt_prtnrs_id']
            else:
                enrlmntRandom = f2.randgen()
                enrlmntmthd = EppEnrlmntPrtnrs(enrlmnt_prtnrs_id=enrlmntRandom, enrlmnt_prtnrs_nm=data['enrlmntPrtnrsNm'], \
                                       cntct_nm='', eml_addrss=data['emlAddrss'],
                                       phn_nbr='',crtd_dt=data['crtdDt'], crtd_by=data['crtdBy'],
                                       lst_updt_dt=data['lstUpdtDt'], \
                                       lst_updt_by=data['lstUpdtBy'])
                enrlmntmthd.save()
            return enrlmntRandom

        except Exception:
            return Response("Error while inserting into EppEnrlmntPrtnrs", status=status.HTTP_400_BAD_REQUEST)