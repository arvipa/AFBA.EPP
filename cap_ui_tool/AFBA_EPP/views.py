import sys
from rest_framework.response import Response
from rest_framework.views import APIView
from collections import OrderedDict
from .models import EppAction, EppProduct, EppGrppymntmd, EppErrormessage, EppGrpmstr, \
    EppGrpprdct, EppBulkreftbl, EppAttribute, EppEnrlmntPrtnrs,EppAgents, EppProductcodes
from .serializers import EppActionSerializer, EppProductSerializer, EppGrppymntmdSerializer, EppErrormessageSerializer, \
    EppGrpmstrSerializer, EppGrpmstrPostSerializers, EppCrtGrpmstrSerializer, EppGrpAgentSerializer
from rest_framework import status, generics
import random as rand
from datetime import datetime, timezone
from AFBA_EPP.config import PRODUCTS, IS_ACTIVE, QUESTIONS, PRODUCT_ACTIVE, PRODUCT_QUESTIONS
from AFBA_EPP.utils import add_product_attr, add_question_attr


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
    inserted =0
    serializer_class = EppCrtGrpmstrSerializer

    def put(self,request):
        f1 = DateRand()
        todayDt = f1.getCurntUtcTime()
        request.data['lstUpdtDt'] = todayDt.strftime('%Y-%m-%d')
        request.data['lstUpdtBy'] = 'Batch'
        if EppGrpmstr.objects.filter(grp_nbr=request.data['grpNbr']).exists():
            pymntput_fk = EppGrppymntmd.objects.get(pk=request.data['grpPymn'])
            #Validates enrlmntPrtnrsId if exists, updats the EppEnrlmntPrtnrs else inserts the data
            request.data['enrlmntPrtnrsId'] = self.validateEnrlmnt(request.data)
            if inserted==0:
                EppEnrlmntPrtnrs.objects.filter(eml_addrss=request.data['emlAddrss']).update\
                    (enrlmnt_prtnrs_id=request.data['enrlmntPrtnrsId'], enrlmnt_prtnrs_nm=request.data['enrlmntPrtnrsNm'],\
                     lst_updt_dt=request.data['lstUpdtDt'], lst_updt_by=request.data['lstUpdtBy'])

            enrollmentput_fk = EppEnrlmntPrtnrs.objects.get(pk=request.data['enrlmntPrtnrsId'])

            EppGrpmstr.objects.filter(grp_nbr=request.data['grpNbr']).update\
                (grp_id=request.data['grpId'], grp_efftv_dt = request.data['grpEfftvDt'],\
                 grp_situs_st = request.data['grpSitusSt'],actv_flg = request.data['actvFlg'],grppymn = pymntput_fk,\
                 enrlmnt_prtnrs = enrollmentput_fk,occ_class = request.data['occClass'],acct_mgr_nm = request.data['acctMgrNm'],\
                 acct_mgr_email_addrs = request.data['acctMgrEmailAddrs'],usr_tkn = request.data['user_token'],\
                 case_tkn = request.data['case_token'],lst_updt_dt = request.data['lstUpdtDt'],lst_updt_by=request.data['lstUpdtBy'])

            i=0
            while (i<len(request.data['grpAgents'])):
                print(request.data['grpAgents'][i])
                if EppAgents.objects.filter(grp=request.data['grpAgents'][i]['grpId']).exists():
                    if EppAgents.objects.filter(agent_id=request.data['grpAgents'][i]['agentId']).exists():

                        EppAgents.objects.filter(agent_id=request.data['grpAgents'][i]['agentId']).update \
                            (agnt_nbr=request.data['grpAgents'][i]['agntNbr'],\
                            agnt_nm=request.data['grpAgents'][i]['agntNm'], \
                            agnt_sub_cnt=request.data['grpAgents'][i]['agntSubCnt'], \
                            agnt_comsn_splt=request.data['grpAgents'][i]['agntComsnSplt'],\
                            lst_updt_dt=request.data['lstUpdtDt'], lst_updt_by=request.data['lstUpdtBy'])
                    else:
                        self.AddAgentDet(request.data,i)
                i=i+1

            return Response("Group No. " + str(request.data['grpNbr']) + " updated sucessfully!",
                        status=status.HTTP_200_OK)


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
        grp_mastr = EppGrpmstr(grppymn=pymnt_fk, enrlmnt_prtnrs=enrollment_fk)
        serializer = EppCrtGrpmstrSerializer(grp_mastr, data=request.data)
        if serializer.is_valid():
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
               i=0
               self.AddAgentDet(request.data,i)
               self.AddBulkData(request.data)
               return Response("Group No. " + str(request.data['grpNbr']) + " updated sucessfully!",
                        status=status.HTTP_200_OK)
            except Exception:
                return Response("Error while inserting into Erpgrpmstr", status=status.HTTP_400_BAD_REQUEST)
        return Response("Error", status=status.HTTP_400_BAD_REQUEST)


    def AddAgentDet(self,data,i):
        try:
            f3 = DateRand()
            todayDt = f3.getCurntUtcTime()
            grpId_fk = EppGrpmstr.objects.get(pk=data['grpId'])
            print('Before Agentmthd')
            Agentmthd = EppAgents(agent_id=data['grpAgents'][i]['agentId'],agnt_nbr =data['grpAgents'][i]['agntNbr'], \
                              agnt_nm=data['grpAgents'][i]['agntNm'], agnt_sub_cnt=data['grpAgents'][i]['agntSubCnt'],\
                              agnt_comsn_splt=data['grpAgents'][i]['agntComsnSplt'],grp=grpId_fk,\
                              crtd_dt=todayDt.strftime('%Y-%m-%d'), crtd_by='Batch')
            Agentmthd.save()

        except Exception:
            return Response("Error while inserting into EppAgents", status=status.HTTP_400_BAD_REQUEST)

    def validateEnrlmnt(self,data):
        global inserted
        try:
            f2 = DateRand()
            todayDt = f2.getCurntUtcTime()
            if EppEnrlmntPrtnrs.objects.filter(eml_addrss=data['emlAddrss']).exists():
                print("Mail Exists")
                enrldict = EppEnrlmntPrtnrs.objects.filter(eml_addrss=data['emlAddrss']).values('enrlmnt_prtnrs_id')
                enrlmntRandom=enrldict[0]['enrlmnt_prtnrs_id']
                inserted=0
            else:
                enrlmntRandom = f2.randgen()
                enrlmntmthd = EppEnrlmntPrtnrs(enrlmnt_prtnrs_id=enrlmntRandom, enrlmnt_prtnrs_nm=data['enrlmntPrtnrsNm'], \
                                       cntct_nm='', eml_addrss=data['emlAddrss'],
                                       phn_nbr='',crtd_dt=todayDt.strftime('%Y-%m-%d'), crtd_by='Batch',
                                       lst_updt_dt=todayDt.strftime('%Y-%m-%d'), \
                                       lst_updt_by='Batch')
                enrlmntmthd.save()
                inserted=1
            return enrlmntRandom
        except Exception:
            print("In exception")
            return Response("Error while inserting into EppEnrlmntPrtnrs", status=status.HTTP_400_BAD_REQUEST)

    def AddBulkData(self, data):
        """
        Add group product, product codes, and bulk data in respective tables.
        :param data: dictionary containing data
        :return: No data.
        """
        prd_cd_keys = ("emp_ProductCode", "sp_ProductCode", "ch_ProductCode")
        is_active_keys = IS_ACTIVE.keys()
        for act_key in is_active_keys:
            check_flag = data.get(act_key, False)
            if check_flag:
                prod_name = IS_ACTIVE[act_key]
                print("Product that should be added is >>> ", prod_name)
                # Using product name get product ID.
                prd_data = EppProduct.objects.filter(product_nm=prod_name.upper())
                prd_dict = list(prd_data.values())[0]
                # Create EPP_GRPPRDCT data.
                grpprdct_id = DateRand().randgen()
                effctv_dt = DateRand().getCurntUtcTime().strftime('%Y-%m-%d')
                try:
                    epp_grp_prd = EppGrpprdct.objects.create(
                        grpprdct_id=grpprdct_id, grp=EppGrpmstr.objects.get(grp_id=data['grpId']),
                        product=EppProduct.objects.get(product_id=prd_dict['product_id']),
                        crtd_dt=data['crtdDt'], crtd_by=data['crtdBy'], lst_updt_dt=data['lstUpdtDt'],
                        lst_updt_by=data['lstUpdtBy'], effctv_dt=effctv_dt)
                except Exception:
                    return Response("Error while inserting into EppGrpprdct", status=status.HTTP_400_BAD_REQUEST)
                prd_detail = data[prod_name]
                # Insert first EPP_ProductCode data.
                for prd_key in prd_cd_keys:
                    if prd_detail.get(prd_key, None):
                        prd_cd = EppProductcodes.objects.create(
                            prodct_cd_id=DateRand().randgen(), product_code=prd_detail[prd_key],
                            product=EppProduct.objects.get(product_id=prd_dict['product_id']),
                            optn=prd_key[:2].upper(), crtd_dt=data['crtdDt'],
                            crtd_by=data['crtdBy'], lst_updt_dt=data['lstUpdtDt'], lst_updt_by=data['lstUpdtBy'])
                # New product attributes in parameters so get its attr and insert its values.
                all_attr = prd_detail.keys()
                for aatr in all_attr:
                    prd_dict = data[IS_ACTIVE[act_key]]
                    prd_attr = EppAttribute.objects.filter(db_attr_nm=aatr, is_qstn_attrbt="N")
                    if prd_attr.exists():
                        bulk_ref = EppBulkreftbl.objects.create(
                            bulk_id=DateRand().randgen(), grpprdct=epp_grp_prd, value=prd_dict[aatr],
                            attr=prd_attr[0], action=EppAction.objects.get(action_id=10001), crtd_dt=data['crtdDt'],
                            crtd_by=data['crtdBy'], lst_updt_dt=data['lstUpdtDt'], lst_updt_by=data['lstUpdtBy'])
                        print("bulk_ref", bulk_ref)
                print("start code of insert")


class BulkQuestionsList(generics.ListAPIView):
    def get(self, request, grpNbr):
        return_data = OrderedDict()
        group_nbr = self.kwargs['grpNbr']
        group_data = EppGrpmstr.objects.filter(grp_nbr=group_nbr).select_related()
        group_dict = list(group_data.values())[0]
        # Using group_id from group data dict get all group products.
        grp_prd_data = EppGrpprdct.objects.filter(grp=group_dict['grp_id'])
        grp_prod_lst = list(grp_prd_data.values())
        # Use loop to add product and its bulk data and attributes in return data.
        pr_key_list = []
        return_data.update({'grpNbr': self.kwargs['grpNbr']})
        for grprd_data in grp_prod_lst:
            prd_data = EppProduct.objects.filter(product_id=grprd_data['product_id'])
            prd_dict = list(prd_data.values())[0]
            pr_key = PRODUCT_QUESTIONS.get(prd_dict['product_nm'])
            if pr_key:
                pr_key_list.append(prd_dict['product_nm'])
                bulk_data = EppBulkreftbl.objects.filter(grpprdct=grprd_data['grpprdct_id'])
                bulk_data_lst = list(bulk_data.values())
                prd_attr_list = [(
                    list(EppAttribute.objects.filter(attr_id=blk_dat['attr_id'], is_qstn_attrbt='Y').values()),
                    blk_dat['value'], blk_dat['action_id'])
                    for blk_dat in bulk_data_lst if
                    list(EppAttribute.objects.filter(attr_id=blk_dat['attr_id'], is_qstn_attrbt='Y').values())]

                if prd_attr_list:
                    prd_attr_conf = QUESTIONS.get(pr_key, ())
                    add_question_attr(return_data, pr_key, prd_attr_conf)
                    return_data.update({PRODUCT_ACTIVE[prd_dict['product_nm']]: True})
                    return_data.setdefault(pr_key, {}).update({'grpprdctId': str(grprd_data['grpprdct_id'])})
                    emp_count, sp_count, ch_count = 0, 0, 0
                    action_dict = {}
                    for prd_attr in prd_attr_list:
                        db_attr_name = prd_attr[0][0]['db_attr_nm']
                        db_attr_value = prd_attr[1]
                        if ('emp_' in db_attr_name) and (emp_count == 0):
                            emp_count = 1
                            action_dict.update({'emp_action': prd_attr[2]})
                        if ('sp_' in db_attr_name) and (sp_count == 0):
                            sp_count = 1
                            action_dict.update({'sp_action': prd_attr[2]})
                        if ('ch_' in db_attr_name) and (ch_count == 0):
                            ch_count = 1
                            action_dict.update({'ch_action': prd_attr[2]})
                        return_data.setdefault(pr_key, {}).update({db_attr_name: db_attr_value})
                    return_data.setdefault(pr_key, {}).update(action_dict)
                else:
                    return_data.setdefault(pr_key, None)
                    return_data.update({PRODUCT_ACTIVE.get(prd_dict['product_nm']): False})
        if pr_key_list:
            all_pr_key = [k for k in PRODUCT_QUESTIONS]
            diff_pr = [set(all_pr_key) - set(pr_key_list)][0]
            if diff_pr:
                for pr in diff_pr:
                    return_data.update({PRODUCT_ACTIVE.get(pr): False})
                    return_data.update({PRODUCT_QUESTIONS.get(pr): None})
        return Response(return_data)
