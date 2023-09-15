import pyecharts.options as opts
from pyecharts.charts import Pie

inner_x_data = ["type1", "type2", "type3"]
inner_y_data = [335, 679, 1548]
inner_data_pair = [list(z) for z in zip(inner_x_data, inner_y_data)]
outer_x_data = ["ad1", "ad2", "ad3", "ad4", "ad5", "ad6", "ad7", "ad8", "da9", "ad10"]
outer_y_data = [335, 310, 234, 135, 1048, 251, 147, 102]
outer_data_pair = [list(z) for z in zip(outer_x_data, outer_y_data)]
c=(
    Pie(init_opts=opts.InitOpts(width="900px", height="600px"))
    .add(
        series_name="from",
        data_pair=inner_data_pair,
        radius=[0, "30%"],
        label_opts=opts.LabelOpts(position="inner"),
    )
    .add(
        series_name="from",
        radius=["40%", "55%"],
        data_pair=outer_data_pair,
        label_opts=opts.LabelOpts(
            position="outside",
            formatter="{a|{a}}{abg|}\n{hr|}\n {b|{b}: }{c} {per|{d}%} ",
            background_color="#eee",
            border_color="#aaa",
            border_width=1,
            border_radius=4,
            rich={
                "a": {"color": "#999", "lineHeight": 22, "align": "center"},
                "abg": {
                    "backgroundColor": "#e3e3e3",
                    "width": "100%",
                    "align": "right",
                    "height": 22,
                    "borderRadius": [4, 4, 0, 0],
                },
                "hr": {
                    "borderColor": "#aaa",
                    "width": "100%",
                    "borderWidth": 0.5,
                    "height": 0,
                },
                "b": {"fontSize": 16, "lineHeight": 33},
                "per": {
                    "color": "#eee",
                    "backgroundColor": "#334455",
                    "padding": [2, 4],
                    "borderRadius": 2,
                },
            },
        ),
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="巢状富⽂本饼图"),
        legend_opts=opts.LegendOpts(
            pos_left="right", # 标签位置
            orient="vertical", # 表现⽔平⽅式
            type_="scroll", # 是否可以滚动，
        )
    )
    .set_series_opts(
        tooltip_opts=opts.TooltipOpts(
                trigger="item", formatter="{a} <br/>{b}: {c} ({d}%)"
            )
        )
    # .render("巢状富⽂本饼图.html")
)

c.render_notebook()
