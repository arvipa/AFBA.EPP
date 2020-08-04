from .views import EppActionList, EppProductList, EppGrppymntmdList, SitusStateSerializerList, EppErrormessageList, \
    EppGrpmstrList, EppGrpmstrPostList, EppCreateGrpList, BulkQuestionsList,CloneTemplt
from django.urls import path

urlpatterns = [
    path("Lookup/EppAction/", EppActionList.as_view(), name="Eppaction_list"),
    path("Lookup/EppProducts/", EppProductList.as_view(), name="EppProduct_list"),
    path("Lookup/GroupPaymentMethod/", EppGrppymntmdList.as_view(), name="EppPayment_list"),
    path("lookup/LookupsData/", SitusStateSerializerList.as_view(), name="SitusState_list"),
    # path("ErorrMessage/GetErrorMessages", EppErrormessageList.as_view(), name="Error_list"),
    path("GroupSetup/GetGroupsData", EppGrpmstrList.as_view(), name="GroupPayment_list"),
    path("GroupSetup/EditEppGrpSetup", EppCreateGrpList.as_view(), name="EdtGrp_list"),
    path("GroupSetup/EppCreateGrpSetup", EppCreateGrpList.as_view(), name="CreateGrp_list"),
    path("GroupSetup/grpNbr/<str:grpNbr>/", EppGrpmstrPostList.as_view(), name="GroupPayment_list"),
    path("Custom/bulkqstn/grpNbr/<str:grpNbr>/", BulkQuestionsList.as_view(), name="Bulkquestion_list"),
    path("Custom/clonetemplate/grpNbr/<str:grpNbr>/", CloneTemplt.as_view(), name="CloneTemplt_lists"),
]
