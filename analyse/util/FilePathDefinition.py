import os.path

# ../analyse 这个目录
rootDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_FILE = rootDir + "/input"
OUTPUT_FILE = rootDir + "/output"

CF_ROOT = "HWStatistics"
CF_DEBUG_DIR = CF_ROOT + "/debug_record"
CF_INFO_DIR = CF_ROOT + "/info_record"
CF_ACTIVITY_DIR = CF_ROOT + "/active"
CF_CHARGE_DIR = CF_ROOT + "/charge_record"

USER_NAME = INPUT_FILE + "/13266826670"
ACTIVE_ROOT_PATH = USER_NAME + "/" + CF_ACTIVITY_DIR

CF_SESSION_PREFIX = "graph"
CF_OUTPUT_POWER_USAGE = "session_power_usage"
EXCEL_SUFFIX = ".xlsx"

# export
EXPORT_APP_DETAIL_USAGES = "app_detail_usages"
EXPORT_APP_SUMMARY_USAGES = "app_summary_usages"
EXPORT_SESSION_SUMMARY = "session_summary"
EXPORT_UNITS_POWER = "units_power_usage"

# power_params
POWER_PARAMS_MAT = "params_mat.xlsx"
POWER_PARAMS_PATH = USER_NAME + "/" + POWER_PARAMS_MAT
POWER_PARAMS_THETA_IDX = 0
POWER_PARAMS_MU_IDX = 1
POWER_PARAMS_SIGMA_IDX = 2

PP_SCREEN_BRIGHTNESS_IDX = 1
PP_MUSIC_ON_IDX = 2
PP_PHONE_RING_IDX = 3
PP_PHONE_OFF_HOOK_IDX = 4
PP_WIFI_NETWORK_IDX = 5
PP_2G_NETWORK_IDX = 6
PP_3G_NETWORK_IDX = 7
PP_4G_NETWORK_IDX = 8
PP_5G_NETWORK_IDX = 9
PP_OTHER_NETWORK_IDX = 10
PP_IS_WIFI_ENABLE_IDX = 11
PP_NET_WORK_SPEED_IDX = 12
PP_CPU_FREQ0_IDX = 13
PP_CPU_FREQ1_IDX = 14
PP_CPU_FREQ2_IDX = 15
PP_CPU_FREQ3_IDX = 16
PP_CPU_FREQ4_IDX = 17
PP_CPU_FREQ5_IDX = 18
PP_CPU_FREQ6_IDX = 19
PP_CPU_FREQ7_IDX = 20
PP_CPU_BLUETOOTH_IDX = 21
PP_MEM_AVAILABLE_IDX = 22
PP_MEM_ACTIVE_IDX = 23
PP_MEM_DIRTY_IDX = 24
PP_MEM_ANON_PAGE_IDX = 25
PP_MEM_MEM_MAPPED_IDX = 26
PP_HEADERS = ["time_stamp", "screen_brightness", "music_on", "phone_ring", "phone_off_hook", "wifi_network",
              "2g_network", "3g_network", "4g_network", "5g_network", "other_network", "is_wifi_enable",
              "network_speed", "cpu0", "cpu1", "cpu2", "cpu3", "cpu4", "cpu5", "cpu6", "cpu7", "bluetooth",
              "mem_available", "mem_active", "mem_dirty", "mem_anonPages", "mem_mapped", "总功耗"]