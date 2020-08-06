"""
Configuration file to store product attributes.
"""


IS_ACTIVE = {
    "isFPPGActive": "fppg",
    "isHIActive": "hi",
    "isACCActive": "acc",
    "isER_CIActive": "er_ci",
    "isVOL_CIActive": "vol_ci",
    "isVGLActive": "vgl",
    "isBGLActive": "bgl",
    "isFPPIActive": "fppi",
}

IS_ACTIVE_REVERSE = {value: key for key, value in IS_ACTIVE.items()}

RESPONSE_KEY = {
    "fppg": "fppg",
    "hi": "hi",
    "acc": "acc",
    "er_ci": "eR_CI",
    "vol_ci": "voL_CI",
    "vgl": "vgl",
    "bgl": "bgl",
    "fppi": "fppi"
}

PRODUCTS = {
    "fppg": ("effctv_dt", "grp_situs_state", "emp_gi_max_amt", "sp_gi_max_amt",
             "emp_ProductCode", "sp_ProductCode", "ch_ProductCode", "emp_waiver_of_prem",
             "sp_waiver_of_prem", "emp_quality_of_life", "sp_quality_of_life",
             "emp_waiver_of_prem_action", "p_waiver_of_prem_action",
             "emp_quality_of_life_action", "sp_quality_of_life_action",
             "sp_plan_cd", "emp_plan_cd", "ch_plan_cd", "emp_plan_cd_action",
             "sp_plan_cd_action", "ch_plan_cd_action", "emp_qi_max_amt",
             "sp_qi_max_amt", "emp_max_amt", "sp_max_amt", "ch_max_amt",
             "effctv_dt_action", "grp_situs_state_action", "emp_gi_max_amt_action",
             "sp_gi_max_amt_action", "emp_qi_max_amt_action", "sp_qi_max_amt_action",
             "emp_max_amt_action", "sp_max_amt_action", "h_max_amt_action",
             ),
    "fppi": ('effctv_dt', 'emp_gi_max_amt', 'sp_gi_max_amt', 'emp_qi_max_amt', 'sp_qi_max_amt',
             'emp_max_amt', 'sp_max_amt', 'ch_max_amt', 'effctv_dt_action', 'agnt_sig_txt_1',
             'agnt_sig_txt_1_action', 'emp_ProductCode', 'sp_ProductCode', 'ch_ProductCode',
             'emp_waiver_of_prem', 'sp_waiver_of_prem', 'emp_quality_of_life', 'sp_quality_of_life',
             'emp_waiver_of_prem_action', 'sp_waiver_of_prem_action', 'emp_quality_of_life_action',
             'sp_quality_of_life_action', 'emp_gi_max_amt_action', 'sp_gi_max_amt_action',
             'emp_qi_max_amt_action', 'sp_qi_max_amt_action', 'emp_max_amt_action', 'sp_max_amt_action',
             'ch_max_amt_action', 'sp_plan_cd', 'emp_plan_cd', 'ch_plan_cd', 'emp_plan_cd_action', 'sp_plan_cd_action',
             'ch_plan_cd_action', 'agnt_cd_1', 'agnt_nm', 'agnt_comm_split_1', 'agntsub_1', 'agnt_cd_2',
             'agnt_comm_split_2', 'agntsub_2', 'agnt_cd_3', 'agnt_comm_split_3', 'agntsub_3', 'agnt_cd_4',
             'agnt_comm_split_4', 'agntsub_4', 'agnt_cd_1_action', 'agnt_nm_action', 'agnt_comm_split_1_action',
             'agntsub_1_action', 'agnt_cd_2_action', 'agnt_comm_split_2_action', 'agntsub_2_action',
             'agnt_cd_3_action', 'agnt_comm_split_3_action', 'agntsub_3_action', 'agnt_cd_4_action',
             'agnt_comm_split_4_action', 'agntsub_4_action')
}

PLAN_PROD_CD_MAP = {
    "emp_ProductCode": "emp_plan_cd", "sp_ProductCode": "sp_plan_cd", "ch_ProductCode": "ch_plan_cd"
}

REVERSE_PLAN_PROD_CD_MAP = {value: key for key, value in PLAN_PROD_CD_MAP.items()}

QUESTIONS = {
    "fppGqstn": ('grpprdctId', 'emp_qstn_1', 'emp_qstn_2', 'emp_qstn_3a', 'emp_qstn_3b', 'emp_qstn_3c', 'emp_qstn_4',
                 'emp_qstn_5', 'sp_qstn_1', 'sp_qstn_2', 'sp_qstn_3a', 'sp_qstn_3b', 'sp_qstn_3c', 'sp_qstn_4',
                 'sp_qstn_5', 'ch_qstn_1_01', 'ch_qstn_2_01', 'ch_qstn_3_01', 'ch_qstn_4_01'),

    "fppIqstn": (
        'grpprdctId', 'emp_qstn_1', 'emp_qstn_2', 'emp_qstn_3', 'emp_qstn_4', 'emp_qstn_5', 'emp_qstn_6', 'emp_qstn_7',
        'emp_qstn_8', 'emp_qstn_9', 'emp_qstn_10', 'sp_qstn_1', 'sp_qstn_2', 'sp_qstn_3', 'sp_qstn_4', 'sp_qstn_5',
        'sp_qstn_6', 'sp_qstn_7', 'sp_qstn_8', 'sp_qstn_9', 'sp_qstn_10', 'ch_qstn_1_01', 'ch_qstn_2_01',
        'ch_qstn_3_01', 'ch_qstn_4_01', 'ch_qstn_5_01', 'ch_qstn_6_01', 'ch_qstn_7_01', 'ch_qstn_8_01', 'ch_qstn_9_01'
        , 'ch_qstn_10_01'),

    "vgLqstn": (
        'grpprdctId', 'emp_qstn_1a', 'emp_qstn_1b', 'emp_qstn_2', 'emp_qstn_3', 'emp_qstn_4', 'sp_qstn_1a',
        'sp_qstn_1b', 'sp_qstn_2', 'sp_qstn_3', 'sp_qstn_4', 'ch_qstn_1a_01', 'ch_qstn_1b_01', 'ch_qstn_2_01',
        'ch_qstn_3_01', 'ch_qstn_4_01'),

    "voL_CIqstn": (
        'grpprdctId', 'emp_qstn_1', 'emp_qstn_2', 'emp_qstn_3a', 'emp_qstn_3b', 'emp_qstn_3c', 'emp_qstn_3d',
        'emp_qstn_3e', 'emp_qstn_4', 'emp_qstn_5', 'sp_qstn_1', 'sp_qstn_2', 'sp_qstn_3a', 'sp_qstn_3b', 'sp_qstn_3c',
        'sp_qstn_3d', 'sp_qstn_3e', 'sp_qstn_4', 'sp_qstn_5', 'ch_qstn_1_01', 'ch_qstn_2_01')
}

PRODUCT_QUESTIONS = {'FPPG': 'fppGqstn', 'FPPI': 'fppIqstn', 'VOL_CI': 'voL_CIqstn', 'VGL': 'vgLqstn'}

PRODUCT_ACTIVE = {'FPPG': 'isFPPGActive', 'FPPI': 'isFPPIActive', 'VOL_CI': 'isVOL_CIActive', 'VGL': 'isVGLActive'}

IS_ACTIVE_QUESTION = {"isFPPGActive": "fppGqstn", "isVOL_CIActive": "voL_CIqstn", "isVGLActive": "vgLqstn", "isFPPIActive": "fppIqstn",}