from rest_framework import serializers
from .models import EppAction, EppProduct, EppGrppymntmd, EppErrormessage, EppGrpmstr


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

    class Meta:
        model = EppGrpmstr
        fields = ('grpId', 'grpNbr', 'grpNm')