from rest_framework import serializers
from .models import EppAction, EppProduct, EppGrppymntmd, EppErrormessage, EppGrpmstr, EppAgents, EppEnrlmntPrtnrs


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
    agntNm = serializers.CharField(source='agnt_nm')
    agntSubCnt = serializers.CharField(source='agnt_sub_cnt')
    agntComsnSplt = serializers.CharField(source='agnt_comsn_splt')
    grpId = serializers.CharField(source='grp.grp_id')

    class Meta:
        model = EppAgents
        fields = ('agentId', 'agntNbr', 'agntNm', 'agntSubCnt', 'agntSubCnt', 'agntComsnSplt', 'grpId')


class EppGrpmstrSerializer(serializers.ModelSerializer):
    grpId = serializers.IntegerField(source='grp_id')
    grpNbr = serializers.CharField(source='grp_nbr')
    grpNm = serializers.CharField(source='grp_nm')

    class Meta:
        model = EppGrpmstr
        fields = ('grpId', 'grpNbr', 'grpNm')


class EppGrpmstrPostSerializers(serializers.ModelSerializer):
    grpId = serializers.CharField(source='grp_id')
    grpNbr = serializers.CharField(source='grp_nbr')
    grpNm = serializers.CharField(source='grp_nm')
    grpEfftvDt = serializers.CharField(source='grp_efftv_dt')
    grpSitusSt = serializers.CharField(source='grp_situs_st')
    actvFlg = serializers.CharField(source='actv_flg')
    occClass = serializers.CharField(source='occ_class')
    enrlmntPrtnrsId = serializers.CharField(source='enrlmnt_prtnrs.enrlmnt_prtnrs_id')
    enrlmntPrtnrsNm = serializers.CharField(source='enrlmnt_prtnrs.enrlmnt_prtnrs_nm')
    emlAddrss = serializers.CharField(source='enrlmnt_prtnrs.eml_addrss')
    acctMgrNm = serializers.CharField(source='acct_mgr_nm')
    acctMgrEmailAddrs = serializers.CharField(source='acct_mgr_email_addrs')
    user_token = serializers.CharField(source='usr_tkn')
    case_token = serializers.CharField(source='case_tkn')
    grpAgents = EppAgentsSerializer(many=True, read_only=True)

    class Meta:
        model = EppGrpmstr
        fields = (
            'grpId', 'grpNbr', 'grpNm', 'grpEfftvDt', 'grpSitusSt', 'actvFlg', 'occClass', 'grppymn', 'enrlmntPrtnrsId',
            'enrlmntPrtnrsNm', 'emlAddrss', 'acctMgrNm', 'acctMgrEmailAddrs', 'user_token', 'case_token', 'grpAgents')

        def to_representation(self, instance):
            self.fields['grppymn'] = EppGrppymntmdSerializer(read_only=True)
            return super(EppGrpmstrPostSerializers, self).to_representation(instance)


class EppGrpAgentSerializer(serializers.ModelSerializer):
    agentId = serializers.IntegerField(source='agent_id')
    agntNbr = serializers.CharField(source='agnt_nbr')
    agntNm = serializers.CharField(source='agnt_nm')
    agntSubCnt = serializers.CharField(source='agnt_sub_cnt')
    agntComsnSplt = serializers.IntegerField(source='agnt_comsn_splt')
    grpId = serializers.PrimaryKeyRelatedField(allow_null=True,queryset=EppGrpmstr.objects.all())

    class Meta:
        model = EppAgents
        fields = ('agentId', 'agntNbr', 'agntNm', 'agntSubCnt', 'agntComsnSplt', 'grpId')
        depth = 1


class EppCrtGrpmstrSerializer(serializers.ModelSerializer):
    grpAgents = EppGrpAgentSerializer(many=True, required=True)
    grpPymn = serializers.PrimaryKeyRelatedField(queryset=EppGrppymntmd.objects.all())
    grpId = serializers.CharField(source='grp_id')
    grpNbr = serializers.CharField(source='grp_nbr')
    grpNm = serializers.CharField(source='grp_nm')
    #  grpNm = serializers.SerializerMethodField()
    grpEfftvDt = serializers.DateTimeField(source='grp_efftv_dt')
    grpSitusSt = serializers.CharField(source='grp_situs_st')
    actvFlg = serializers.CharField(source='actv_flg')
    enrlmntPrtnrsId = serializers.PrimaryKeyRelatedField(queryset=EppEnrlmntPrtnrs.objects.all())
    crtdDt = serializers.DateField(source='crtd_dt',read_only=True)
    crtdBy = serializers.CharField(source='crtd_by', read_only=True)
    lstUpdtDt = serializers.DateField(source='lst_updt_dt', read_only=True)
    lstUpdtBy = serializers.CharField(source='lst_updt_by', read_only=True)
    enrlmntPrtnrsNm = serializers.CharField(source='enrlmnt_prtnrs_nm', read_only=True)
    occClass = serializers.IntegerField(source='occ_class')
    acctMgrNm = serializers.CharField(source='acct_mgr_nm')
    acctMgrEmailAddrs = serializers.CharField(source='acct_mgr_email_addrs')
    user_token = serializers.CharField(source='usr_tkn')
    case_token = serializers.CharField(source='case_tkn')

    class Meta:
        model = EppGrpmstr
        fields = ('grpId', 'grpNbr', 'grpNm', 'grpEfftvDt', 'grpSitusSt', 'actvFlg', 'occClass', 'grpPymn',
                  'enrlmntPrtnrsId', 'crtdDt', 'crtdBy', 'lstUpdtDt', 'lstUpdtBy', 'grpAgents', 'acctMgrNm',
                  'acctMgrEmailAddrs', 'user_token', 'case_token')


