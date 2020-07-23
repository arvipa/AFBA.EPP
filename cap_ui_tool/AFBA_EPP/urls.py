from .views import EppActionList, EppProductList, EppGrppymntmdList, SitusStateSerializerList, EppErrormessageList, \
    EppGrpmstrList
from django.urls import path

urlpatterns = [
    path("Lookup/EppAction/", EppActionList.as_view(), name="Eppaction_list"),
    path("Lookup/EppProducts/", EppProductList.as_view(), name="EppProduct_list"),
    path("Lookup/GroupPaymentMethod/", EppGrppymntmdList.as_view(), name="EppPayment_list"),
    path("Lookup/LookupsData/", SitusStateSerializerList.as_view(), name="SitusState_list"),
    # path("ErorrMessage/GetErrorMessages", EppErrormessageList.as_view(), name="Error_list"),
    path("GroupSetup/GetGroupsData", EppGrpmstrList.as_view(), name="GroupPayment_list")
]
