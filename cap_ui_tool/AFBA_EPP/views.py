# Standard library imports.
import sys
import random as rand
from collections import OrderedDict
from datetime import datetime, timezone

# Related third-party imports.
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, generics

# Local application/library specific imports.
from AFBA_EPP.models import (EppAction, EppProduct, EppGrppymntmd, EppErrormessage,
                             EppGrpmstr, EppGrpprdct, EppBulkreftbl, EppAttribute,
                             EppEnrlmntPrtnrs, EppAgents, EppProductcodes)
from AFBA_EPP.serializers import (EppActionSerializer, EppProductSerializer,
                                  EppGrppymntmdSerializer, EppErrormessageSerializer,
                                  EppGrpmstrSerializer, EppGrpmstrPostSerializers,
                                  EppCrtGrpmstrSerializer, EppGrpAgentSerializer)
from AFBA_EPP.config import (PRODUCTS, IS_ACTIVE, QUESTIONS, PRODUCT_ACTIVE,
                             PRODUCT_QUESTIONS, IS_ACTIVE_REVERSE, IS_ACTIVE_QUESTION)
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
        {"id": "AL", "state": "AL"},
        {"id": "AK", "state": "AK"},
        {"id": "AZ", "state": "AZ"},
        {"id": "AR", "state": "AR"},
        {"id": "CA", "state": "CA"},
        {"id": "CO", "state": "CO"},
        {"id": "CT", "state": "CT"},
        {"id": "DC", "state": "DC"},
        {"id": "DE", "state": "DE"},
        {"id": "FL", "state": "FL"},
        {"id": "GA", "state": "GA"},
        {"id": "HI", "state": "HI"},
        {"id": "ID", "state": "ID"},
        {"id": "IL", "state": "IL"},
        {"id": "IN", "state": "IN"},
        {"id": "IA", "state": "IA"},
        {"id": "KS", "state": "KS"},
        {"id": "KY", "state": "KY"},
        {"id": "LA", "state": "LA"},
        {"id": "ME", "state": "ME"},
        {"id": "MD", "state": "MD"},
        {"id": "MA", "state": "MA"},
        {"id": "MI", "state": "MI"},
        {"id": "MN", "state": "MN"},
        {"id": "MS", "state": "MS"},
        {"id": "MO", "state": "MO"},
        {"id": "MT", "state": "MT"},
        {"id": "NE", "state": "NE"},
        {"id": "NV", "state": "NV"},
        {"id": "NH", "state": "NH"},
        {"id": "NJ", "state": "NJ"},
        {"id": "NM", "state": "NM"},
        {"id": "NY", "state": "NY"},
        {"id": "NC", "state": "NC"},
        {"id": "ND", "state": "ND"},
        {"id": "OH", "state": "OH"},
        {"id": "OK", "state": "OK"},
        {"id": "OR", "state": "OR"},
        {"id": "PA", "state": "PA"},
        {"id": "RI", "state": "RI"},
        {"id": "SC", "state": "SC"},
        {"id": "SD", "state": "SD"},
        {"id": "TN", "state": "TN"},
        {"id": "TX", "state": "TX"},
        {"id": "UT", "state": "UT"},
        {"id": "VT", "state": "VT"},
        {"id": "VA", "state": "VA"},
        {"id": "WA", "state": "WA"},
        {"id": "WV", "state": "WV"},
        {"id": "WI", "state": "WI"},
        {"id": "WY", "state": "WY"},
        {"id": "PR", "state": "PR"},
        {"id": "VI", "state": "VI"}]
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
        if group_nbr == 'undefined':
            return Response("", status=status.HTTP_200_OK)
        group_data = EppGrpmstr.objects.filter(grp_nbr=group_nbr).select_related()
        group_dict = list(group_data.values())[0]
        return_data = EppGrpmstrPostSerializers(group_data[0]).data
        # Using group_id from group data dict get all group products.
        grp_prd_data = EppGrpprdct.objects.filter(grp=group_dict['grp_id']).prefetch_related('eppproduct')
        grp_prod_lst = list(grp_prd_data.values())
        # Use loop to add product and its bulk data and attributes in return data.
        for grprd_data in grp_prod_lst:
            prd_data = EppProduct.objects.filter(product_id=grprd_data['product_id'])
            prd_dict = list(prd_data.values())[0]
            # print("prd_dict >>> ", prd_dict)
            pr_key = prd_dict['product_nm'].lower()
            return_data.setdefault(pr_key, {})
            # Creat active key in return data.
            return_data.setdefault(IS_ACTIVE_REVERSE[pr_key], True)
            # From configuration get all attributes required within the product.
            prd_attr_conf = PRODUCTS.get(pr_key, ())
            add_product_attr(return_data, pr_key, prd_attr_conf)
            bulk_data = EppBulkreftbl.objects.filter(grpprdct=grprd_data['grpprdct_id'])
            bulk_data_lst = list(bulk_data.values())
            for blk_dat in bulk_data_lst:
                prd_attr_data = EppAttribute.objects.filter(attr_id=blk_dat['attr_id'], is_qstn_attrbt="N")
                prd_attr_list = list(prd_attr_data.values())
                if prd_attr_list:
                    db_attr_name = prd_attr_list[0]['db_attr_nm']
                    db_attr_value = blk_dat['value']
                    return_data.setdefault(pr_key, {}).update({db_attr_name: db_attr_value})
                    db_attr_name_action = db_attr_name + "_action"
                    db_attr_value_action = str(blk_dat['action_id'])
                    return_data.setdefault(pr_key, {}).update({db_attr_name_action: db_attr_value_action})
        return Response(return_data)


class DateRand:
    def randgen(self):
        today = self.getCurntUtcTime()
        return str(rand.randint(1, 99999)) + today.strftime('%m%d') + '0' + today.strftime('%y') + today.strftime(
            '%H%M%S')

    def getCurntUtcTime(self):
        return datetime.now(timezone.utc)


class EppCreateGrpList(generics.CreateAPIView):
    inserted = 0
    serializer_class = EppCrtGrpmstrSerializer

    def put(self, request):
        f1 = DateRand()
        todayDt = f1.getCurntUtcTime()
        request.data['lstUpdtDt'] = todayDt.strftime('%Y-%m-%d')
        request.data['lstUpdtBy'] = 'Batch'
        if EppGrpmstr.objects.filter(grp_nbr=request.data['grpNbr']).exists():
            pymntput_fk = EppGrppymntmd.objects.get(pk=request.data['grpPymn'])
            # Validates enrlmntPrtnrsId if exists, updats the EppEnrlmntPrtnrs else inserts the data
            request.data['enrlmntPrtnrsId'] = self.validateEnrlmnt(request.data)
            if inserted == 0:
                EppEnrlmntPrtnrs.objects.filter(eml_addrss=request.data['emlAddrss']).update \
                    (enrlmnt_prtnrs_id=request.data['enrlmntPrtnrsId'],
                     enrlmnt_prtnrs_nm=request.data['enrlmntPrtnrsNm'], \
                     lst_updt_dt=request.data['lstUpdtDt'], lst_updt_by=request.data['lstUpdtBy'])

            enrollmentput_fk = EppEnrlmntPrtnrs.objects.get(pk=request.data['enrlmntPrtnrsId'])

            EppGrpmstr.objects.filter(grp_nbr=request.data['grpNbr']).update \
                (grp_id=request.data['grpId'], grp_efftv_dt=request.data['grpEfftvDt'], \
                 grp_situs_st=request.data['grpSitusSt'], actv_flg=request.data['actvFlg'], grppymn=pymntput_fk, \
                 enrlmnt_prtnrs=enrollmentput_fk, occ_class=request.data['occClass'],
                 acct_mgr_nm=request.data['acctMgrNm'], \
                 acct_mgr_email_addrs=request.data['acctMgrEmailAddrs'], usr_tkn=request.data['user_token'], \
                 case_tkn=request.data['case_token'], lst_updt_dt=request.data['lstUpdtDt'],
                 lst_updt_by=request.data['lstUpdtBy'])

            i = 0
            while (i < len(request.data['grpAgents'])):
                print(request.data['grpAgents'][i])

                if EppAgents.objects.filter(grp=request.data['grpId']).exists():
                    if EppAgents.objects.filter(agent_id=request.data['grpAgents'][i]['agentId']).exists():

                        EppAgents.objects.filter(agent_id=request.data['grpAgents'][i]['agentId']).update \
                            (agnt_nbr=request.data['grpAgents'][i]['agntNbr'], \
                             agnt_nm=request.data['grpAgents'][i]['agntNm'], \
                             agnt_sub_cnt=request.data['grpAgents'][i]['agntSubCnt'], \
                             agnt_comsn_splt=request.data['grpAgents'][i]['agntComsnSplt'], \
                             lst_updt_dt=request.data['lstUpdtDt'], lst_updt_by=request.data['lstUpdtBy'])
                    else:
                        self.AddAgentDet(request.data, i)
                i = i + 1
            print("Before grpprdct logic")

            if EppGrpprdct.objects.filter(grp=request.data['grpId']).exists():
                grp_lst = list(EppGrpprdct.objects.filter(grp=request.data['grpId']).values())
                for grpprd_data in grp_lst:
                    prd_cd_keys = ("emp_ProductCode", "sp_ProductCode", "ch_ProductCode")
                    is_active_keys = IS_ACTIVE.keys()
                    for act_key in is_active_keys:
                        check_flag = request.data.get(act_key, False)
                        if check_flag:
                            prod_name = IS_ACTIVE[act_key]
                            print("Product that should be added is >>> ", prod_name)
                            prd_data = EppProduct.objects.filter(product_nm=prod_name.upper())
                            prd_dict = list(prd_data.values())[0]
                            print("prd_dict: ", prd_dict)
                            grpprdct_id = grpprd_data['grpprdct_id']
                            effctv_dt = grpprd_data['effctv_dt']
                            try:
                                epp_grp_prd = EppGrpprdct.objects.filter \
                                    (grpprdct_id=grpprdct_id).update \
                                    (product=prd_dict['product_id'],
                                     grp=EppGrpmstr.objects.get(grp_id=request.data['grpId']),
                                     lst_updt_dt=todayDt.strftime('%Y-%m-%d'),
                                     lst_updt_by='Batch', effctv_dt=effctv_dt)

                            except Exception:
                                print("Error while updating:", sys.exc_info()[0])
                            prd_detail = request.data[prod_name]
                            print("prd_detail: ", prd_detail)
                            for prd_key in prd_cd_keys:
                                prdCd_lst = list(EppProductcodes.objects.filter(product_id=prd_dict['product_id'], \
                                                                                product_code=prd_detail[
                                                                                    prd_key]).values())
                                for prdCd_data in prdCd_lst:
                                    if prd_detail.get(prd_key, None):
                                        prd_cd = EppProductcodes.objects.filter \
                                            (prodct_cd_id=prdCd_data['prodct_cd_id'], \
                                             product_code=prd_detail[prd_key]).update \
                                            (product=EppProduct.objects.get(product_id=prd_dict['product_id']),
                                             optn=prd_key[:2].upper(),
                                             lst_updt_dt=todayDt.strftime('%Y-%m-%d'),
                                             lst_updt_by='Batch')
                            all_attr = prd_detail.keys()
                            for aatr in all_attr:
                                print(aatr)
                                prd_dict = request.data[IS_ACTIVE[act_key]]
                                print('prd_dict: ', prd_dict)
                                prd_attr = EppAttribute.objects.filter(db_attr_nm=aatr, is_qstn_attrbt="N")
                                print('prd_attr: ', prd_attr)
                                if prd_attr.exists():
                                    blkData_lst = list(EppBulkreftbl.objects.filter(grpprdct=grpprd_data['grpprdct_id'], \
                                                                                    attr=prd_attr[0].attr_id).values())
                                    if EppBulkreftbl.objects.filter(grpprdct=grpprd_data['grpprdct_id'], \
                                                                    attr=prd_attr[0].attr_id).exists():
                                        count = 0
                                        for blkData_data in blkData_lst:
                                            count = count + 1
                                            print("In bl ref loop", count)
                                            bulk_ref = EppBulkreftbl.objects.filter \
                                                (bulk_id=blkData_data['bulk_id'], \
                                                 grpprdct=grpprd_data['grpprdct_id'],
                                                 attr=prd_attr[0].attr_id).update \
                                                (value=prd_dict[aatr] if prd_dict[aatr].strip() else None,
                                                 attr=prd_attr[0].attr_id,
                                                 action=EppAction.objects.get(action_id=10001),
                                                 lst_updt_dt=todayDt.strftime('%Y-%m-%d'),
                                                 lst_updt_by='Batch')
                                    else:

                                        bulk_ref = EppBulkreftbl.objects.create(
                                            bulk_id=DateRand().randgen(), grpprdct=EppGrpprdct.objects.get \
                                                (grpprdct_id=grpprd_data['grpprdct_id']),
                                            value=prd_dict[aatr],
                                            attr=prd_attr[0], action=EppAction.objects.get(action_id=10001),
                                            crtd_dt=todayDt.strftime('%Y-%m-%d'),
                                            crtd_by='Batch', lst_updt_dt=todayDt.strftime('%Y-%m-%d'),
                                            lst_updt_by='Batch')
                                    print("bulk_ref", bulk_ref)
            return Response("Group No. " + str(request.data['grpNbr']) + " updated sucessfully!",
                            status=status.HTTP_200_OK)

    def post(self, request):
        f1 = DateRand()
        todayDt = f1.getCurntUtcTime()
        grpNumberRandom = f1.randgen()
        if EppGrppymntmd.objects.filter(pk=request.data['grpPymn']).exists():
            pymnt_fk = EppGrppymntmd.objects.get(pk=request.data['grpPymn'])
        else:
            return Response("grpPymn {} is not present in EppGrppymntmd".format(request.data['grpPymn']),
                            status=status.HTTP_400_BAD_REQUEST)
        request.data['enrlmntPrtnrsId'] = self.validateEnrlmnt(request.data)
        enrollment_fk = EppEnrlmntPrtnrs.objects.get(pk=request.data['enrlmntPrtnrsId'])
        request.data['crtdBy'] = 'Batch'
        request.data['grpId'] = grpNumberRandom
        request.data['crtdDt'] = todayDt.strftime('%Y-%m-%d')
        request.data['lstUpdtDt'] = todayDt.strftime('%Y-%m-%d')
        request.data['lstUpdtBy'] = 'Batch'
        grp_mastr = EppGrpmstr(grppymn=pymnt_fk, enrlmnt_prtnrs=enrollment_fk)
        # serializer = EppCrtGrpmstrSerializer(grp_mastr, data=request.data)
        if True:
            try:
                grpMstrMthd = EppGrpmstr(grp_id=request.data['grpId'], grp_nbr=request.data['grpNbr'], \
                                         grp_nm=request.data['grpNm'], grp_efftv_dt=request.data['grpEfftvDt'], \
                                         grp_situs_st=request.data['grpSitusSt'], actv_flg=request.data['actvFlg'], \
                                         grppymn=pymnt_fk, enrlmnt_prtnrs=enrollment_fk, \
                                         crtd_dt=request.data['crtdDt'], crtd_by=request.data['crtdBy'], \
                                         lst_updt_dt=request.data['lstUpdtDt'], lst_updt_by=request.data['lstUpdtBy'], \
                                         occ_class=request.data['occClass'], acct_mgr_nm=request.data['acctMgrNm'], \
                                         acct_mgr_email_addrs=request.data['acctMgrEmailAddrs'], \
                                         usr_tkn=request.data['acctMgrEmailAddrs'],
                                         case_tkn=request.data['acctMgrEmailAddrs'])
                grpMstrMthd.save()
                i = 0
                self.AddAgentDet(request.data, i)
                self.AddBulkData(request.data)
                return Response("Group No. " + str(request.data['grpNbr']) + " updated sucessfully!",
                                status=status.HTTP_200_OK)
            except Exception:
                return Response("Error while inserting into Erpgrpmstr", status=status.HTTP_400_BAD_REQUEST)
        return Response("Error", status=status.HTTP_400_BAD_REQUEST)

    def AddAgentDet(self, data, i):
        try:
            f3 = DateRand()
            todayDt = f3.getCurntUtcTime()
            grpId_fk = EppGrpmstr.objects.get(pk=data['grpId'])
            print('Before Agentmthd')
            Agentmthd = EppAgents(agent_id=data['grpAgents'][i]['agentId'], agnt_nbr=data['grpAgents'][i]['agntNbr'], \
                                  agnt_nm=data['grpAgents'][i]['agntNm'],
                                  agnt_sub_cnt=data['grpAgents'][i]['agntSubCnt'], \
                                  agnt_comsn_splt=data['grpAgents'][i]['agntComsnSplt'], grp=grpId_fk, \
                                  crtd_dt=todayDt.strftime('%Y-%m-%d'), crtd_by='Batch')
            Agentmthd.save()

        except Exception:
            return Response("Error while inserting into EppAgents", status=status.HTTP_400_BAD_REQUEST)

    def validateEnrlmnt(self, data):
        global inserted
        try:
            f2 = DateRand()
            todayDt = f2.getCurntUtcTime()
            if EppEnrlmntPrtnrs.objects.filter(eml_addrss=data['emlAddrss']).exists():
                print("Mail Exists")
                enrldict = EppEnrlmntPrtnrs.objects.filter(eml_addrss=data['emlAddrss']).values('enrlmnt_prtnrs_id')
                enrlmntRandom = enrldict[0]['enrlmnt_prtnrs_id']
                inserted = 0
            else:
                enrlmntRandom = f2.randgen()
                enrlmntmthd = EppEnrlmntPrtnrs(enrlmnt_prtnrs_id=enrlmntRandom,
                                               enrlmnt_prtnrs_nm=data['enrlmntPrtnrsNm'], \
                                               cntct_nm='', eml_addrss=data['emlAddrss'],
                                               phn_nbr='', crtd_dt=todayDt.strftime('%Y-%m-%d'), crtd_by='Batch',
                                               lst_updt_dt=todayDt.strftime('%Y-%m-%d'), \
                                               lst_updt_by='Batch')
                enrlmntmthd.save()
                inserted = 1
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


class BulkQuestionAddList(generics.CreateAPIView):
    serializer_class = EppCrtGrpmstrSerializer

    def post(self, request):
        try:
            f1 = DateRand()
            todayDt = f1.getCurntUtcTime()
            group_data = EppGrpmstr.objects.filter(grp_nbr=request.data.get('grpNbr'))
            if group_data:
                for question_key, question_val in PRODUCT_QUESTIONS.items():
                    if question_val in request.data and request.data.get(question_val):
                        question_data = request.data[question_val]
                        bulk_data = list(EppBulkreftbl.objects.filter(grpprdct=question_data['grpprdctId']).values())
                        if bulk_data:
                            for blk_dat in bulk_data:
                                prd_attr_list = list(
                                    EppAttribute.objects.filter(attr_id=blk_dat['attr_id'],
                                                                is_qstn_attrbt='Y').values())
                                if prd_attr_list:
                                    bulk_data_del = EppBulkreftbl.objects.filter(grpprdct=question_data['grpprdctId'],
                                                                                 attr_id=prd_attr_list[0]['attr_id'])
                                    bulk_data_del.delete()
                        ch_val, emp_val, sp_val = question_data['ch_action'], question_data['emp_action'], \
                                                  question_data['sp_action']
                        for rec_key, rec_val in question_data.items():
                            if rec_key not in ('ch_action', 'sp_action', 'emp_action', 'grpprdctId'):
                                action_rec = ''
                                prd_attr_insert = EppAttribute.objects.filter(db_attr_nm=rec_key, is_qstn_attrbt='Y')
                                if 'emp_' in rec_key:
                                    action_rec = emp_val
                                elif 'ch_' in rec_key:
                                    action_rec = ch_val
                                else:
                                    action_rec = sp_val
                                if prd_attr_insert.exists():
                                    bulk_ref = EppBulkreftbl.objects.create(
                                        bulk_id=DateRand().randgen(),
                                        grpprdct=EppGrpprdct.objects.get(grpprdct_id=question_data['grpprdctId']),
                                        value=rec_val, attr=prd_attr_insert[0],
                                        action=EppAction.objects.get(action_id=action_rec),
                                        crtd_dt=todayDt.strftime('%Y-%m-%d'), crtd_by='Batch',
                                        lst_updt_dt=todayDt.strftime('%Y-%m-%d'), lst_updt_by='Batch')
                        return Response(
                            "Questions for Group No. " + str(request.data['grpNbr']) + " updated/created sucessfully!",
                            status=status.HTTP_200_OK)
            else:
                return Response("Data not found in EppGrpmstr table for grpNbr :" + str(request.data['grpNbr']),
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response("Error while inserting in BulRef Table", status=status.HTTP_400_BAD_REQUEST)
