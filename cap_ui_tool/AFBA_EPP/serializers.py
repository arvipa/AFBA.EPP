from rest_framework import serializers
from .models import EppAction, EppProduct, EppGrppymntmd, EppErrormessage, EppGrpmstr, EppAgents


class EppActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EppAction
        fields = ('action_id', 'name')


class EppProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = EppProduct
        fields = ('product_id', 'product_nm')


class EppGrppymntmdSerializer(serializers.ModelSerializer):
    grpPymn = serializers.CharField(source='grppymn_id')
    grpPymntMdCd = serializers.CharField(source='grp_pymnt_md_cd')
    grpPymntMdNm = serializers.SerializerMethodField()

    def get_grpPymntMdNm(self, obj):
        return obj.grp_pymnt_md_cd + ' - ' + obj.grp_pymnt_md_nm

    class Meta:
        model = EppGrppymntmd
        fields = ('grpPymn', 'grpPymntMdCd', 'grpPymntMdNm')


class SitusStateSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    State = serializers.ReadOnlyField()

    class Meta:
        model = EppGrppymntmd
        fields = ('id', 'State')


class EppErrormessageSerializer(serializers.ModelSerializer):
    errmsgId = serializers.IntegerField(source='errmsg_id')
    errmsgDesc = serializers.CharField(source='errmsg_desc')

    class Meta:
        model = EppErrormessage
        fields = ('errmsgId', 'errmsgDesc')


class EppAgentsSerializer(serializers.ModelSerializer):
    agentId = serializers.IntegerField(source='agent_id')
    agntNbr = serializers.CharField(source='agnt_nbr')
    agntNbr = serializers.CharField(source='agnt_nm')
    agntSubCnt = serializers.CharField(source='agnt_sub_cnt')
    agntComsnSplt = serializers.CharField(source='agnt_comsn_splt')
    grpId = serializers.CharField(source='grp')

    class Meta:
        model = EppAgents
        fields = ('agentId', 'agntNbr', 'agntNbr', 'agntSubCnt', 'agntSubCnt', 'agntComsnSplt', 'grpId')


class EppGrpmstrSerializer(serializers.ModelSerializer):
    grpId = serializers.IntegerField(source='grp_id')
    grpNbr = serializers.CharField(source='grp_nbr')
    grpNm = serializers.CharField(source='grp_nm')

    class Meta:
        model = EppGrpmstr
        fields = ('grpId', 'grpNbr', 'grpNm')


class EppGrpmstrPostSerializers(serializers.ModelSerializer):
    grpId = serializers.IntegerField(source='grp_id')
    grpNbr = serializers.CharField(source='grp_nbr')
    grpNm = serializers.CharField(source='grp_nm')
    grpEfftvDt = serializers.CharField(source='grp_efftv_dt')
    grpSitusSt = serializers.CharField(source='grp_situs_st')
    actvFlg = serializers.CharField(source='actv_flg')
    occClass = serializers.CharField(source='occ_class')
    grpPymn = serializers.CharField(source='grppymn')
    enrlmntPrtnrsId = serializers.SerializerMethodField('get_enrolment_partnerid')
    enrlmntPrtnrsNm = serializers.SerializerMethodField('get_enrolment_partnername')
    emlAddrss = serializers.SerializerMethodField('get_enrolment_partneremlAddrss')
    acctMgrNm = serializers.CharField(source='acct_mgr_nm')
    acctMgrEmailAddrs = serializers.CharField(source='acct_mgr_email_addrs')
    user_token = serializers.CharField(source='usr_tkn')
    case_token = serializers.CharField(source='case_tkn')
    # agents = serializers.RelatedField(source='EppAgents', read_only=True)
    # agents = EppAgentsSerializer(many=False, read_only=True)

    def get_enrolment_partnerid(self, obj):
        return obj.enrlmnt_prtnrs.enrlmnt_prtnrs_id

    def get_enrolment_partnername(self, obj):
        return obj.enrlmnt_prtnrs.enrlmnt_prtnrs_nm

    def get_enrolment_partneremlAddrss(self, obj):
        return obj.enrlmnt_prtnrs.eml_addrss

    # def get_agent

    class Meta:
        model = EppGrpmstr
        fields = (
            'grpId', 'grpNbr', 'grpNm', 'grpEfftvDt', 'grpSitusSt', 'actvFlg', 'occClass', 'grpPymn', 'enrlmntPrtnrsId',
            'enrlmntPrtnrsNm', 'emlAddrss', 'acctMgrNm', 'acctMgrEmailAddrs', 'user_token', 'case_token')
