from matplotlib.colors import LinearSegmentedColormap
from met_brewer import met_brew


def discrete_met_colors(name: str, num: int) -> list:
    return met_brew(name=name, n=num)


def continues_met_colors(name: str, num: int) -> list:
    return met_brew(name=name, n=num, brew_type="continuous")


custom_colors = [
    "#3A0D60", "#5E93C3", "#FF69B4", "#6B509B", "#E2DA34", "#FDD196", "#F0F0F0", "#F000F0", "#BAFC46", "#FFD6FE",
    "#FE8D00", "#00CC00", "#0000CC", "#A39D24", "#00CCCC", "#E54444", "#BB6008", "#7F3B08", "#000003", "#D0D2FF",
    "#00688C", "#FB8282", "#FFFF11", "#111FFF", "#7E84FF", "#1FFF00", "#D2721C", "#FF001F", "#6FFF0F", "#F6F60F",
    "#880000", "#008800", "#000088", "#888000", "#008888", "#880080", "#808080", "#FF1493", "#008080", "#FF6347",
    "#7FFF00", "#0000FF", "#00C0C0", "#FFF000", "#8B008B", "#00EA6A", "#FF4500", "#48D1CC",
]

custom_colors_2 = [
    "#3A0D60", "#5E93C3", "#FF69B4", "#6B509B", "#E2DA34", "#FDD196", "#F0F0F0", "#A59CC8", "#BAFC46", "#FFD6FE",
    "#FE8D00", "#00CC00", "#0000CC", "#A39D24", "#00CCCC", "#E54444", "#BB6008", "#7F3B08", "#D0D2FF",
    "#00688C", "#FB8282", "#FFFF11", "#111FFF", "#7E84FF", "#D2721C", "#FF001F", "#F6F60F",
    "#880000", "#008800", "#000088", "#888000", "#008888", "#880080", "#808080", "#FF1493", "#008080", "#FF6347",
    "#7FFF00", "#0000FF", "#00C0C0", "#FFF000", "#8B008B", "#00EA6A", "#FF4500", "#48D1CC",
]

short_colors = ["#FCFEA4", "#F8CB34", "#F98D09", "#E35932", "#BB3755", "#892269", "#570F6D", "#200C4A", "#000003"]

keli_colors = ["#4D1E17", "#862718", "#B43A24", "#D89F8A", "#F6E1C6"]

C_9_1 = ["#384C9F", "#5E93C3", "#9DCEE2", "#DEF2F7", "#FEF9B6", "#FDCC7D", "#F7874E", "#DC3B2C", "#A50026"]
C_9_2 = ["#3A0D60", "#6B509B", "#A59CC8", "#D6D8EA", "#F8F3ED", "#FDD196", "#EB9833", "#BB6008", "#7F3B08"]
C_9_3 = ["#FBFCBF", "#FEC488", "#FB8760", "#FB8760", "#B63679", "#822581", "#50127B", "#1C1046", "#000003"]

C_10_2 = ["#252B80", "#3752A4", "#3C6DB4", "#48C687", "#81C998", "#BDD638", "#FBCD11", "#EF5E21", "#EB1D22", "#7D1315"]
C_10_3 = ["#001886", "#0034F5", "#0966FF", "#11D6FF", "#4AFFB9", "#BAFC46", "#FED707", "#FE6504", "#F60101", "#850402"]
C_11_1 = ["#001886", "#0034F5", "#0966FF", "#11D6FF", "#4AFFB9", "#BAFC46", "#FED707", "#FE6504", "#F60101",
          "#850402", "#3C6DB4", "#48C687"]
C_11_2 = ["#3A0D60", "#6B509B", "#A59CC8", "#D6D8EA", "#F8F3ED", "#FDD196", "#EB9833", "#BB6008", "#7F3B08",
          "#DEF2F7", "#FEF9B6"]
C_11_3 = ["#384C9F", "#5E93C3", "#9DCEE2", "#DEF2F7", "#FEF9B6", "#FDCC7D", "#F7874E", "#DC3B2C", "#D6D8EA",
         "#F8F3ED", "#EB9833", ]
C_11_4 = ["#384C9F", "#5E93C3", "#9DCEE2", "#DEF2F7", "#FEF9B6", "#FDCC7D", "#F7874E", "#DC3B2C", "#B63679",
          "#822581", "#1C1046", ]

C_20_1 = C_9_3 + C_11_2
C_20_2 = C_9_2 + C_11_3
C_20_3 = C_9_2 + C_11_4
C_20_4 = C_9_3[1:] + C_11_1

# 创建自定义颜色映射
cmap = LinearSegmentedColormap.from_list('custom_cmap', C_9_1)

C_7_1 = ["#440154", "#433983", "#30678D", "#20908C", "#36B877", "#90D643", "#FDE724"]