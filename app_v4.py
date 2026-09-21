import json

import streamlit as st
import streamlit.components.v1 as components


st.set_page_config(page_title="海洋平台管节点知识图谱", page_icon="⚓", layout="wide")


# 名称：[所属类别, 概念, 名称解释, 工程关注点, 颜色]
entities = {
    "海洋平台管节点": ["核心主题", "海洋平台导管架中的关键连接区域。", "由多根钢管连接形成，承担杆件之间的载荷传递。", "承载能力、应力集中和疲劳寿命", "#d94f64"],
    "结构组成": ["一级分支", "组成管节点的主要钢管构件。", "管节点通常由弦管和支管等基本构件组成。", "构件尺寸和连接形式", "#16a3a5"],
    "连接位置": ["一级分支", "支管与弦管发生连接的关键区域。", "焊缝和相贯线决定了节点局部几何及连接质量。", "局部几何和焊接质量", "#ef6b6b"],
    "受力与疲劳": ["一级分支", "管节点在环境载荷下的受力和疲劳响应。", "载荷传递会造成局部应力集中，并可能引发疲劳损伤。", "应力水平和疲劳寿命", "#e7ad55"],
    "分析方法": ["一级分支", "研究管节点力学性能的数值方法。", "有限元分析通过离散模型计算节点应力分布。", "模型精度和结果验证", "#2f9abb"],
    "弦管": ["结构组成", "管节点中的主要承载钢管。", "弦管直径通常较大，相当于导管架结构中的主杆件。", "管径、壁厚和局部变形", "#16a3a5"],
    "支管": ["结构组成", "与弦管连接并传递载荷的钢管。", "支管以一定角度连接弦管，可形成T型、Y型和K型节点。", "连接角度、直径比和载荷方向", "#16a3a5"],
    "焊缝": ["连接部位", "连接支管与弦管的金属区域。", "焊趾位置容易出现较大的局部应力和疲劳损伤。", "焊接质量、焊趾形状和缺陷", "#ef6b6b"],
    "相贯线": ["关键位置", "支管与弦管表面相交形成的空间曲线。", "相贯线环绕支管根部，是节点几何变化最明显的位置。", "几何突变和周向应力分布", "#ef6b6b"],
    "载荷传递": ["受力过程", "力和弯矩从支管传向弦管的过程。", "轴力和弯矩通过连接区域后形成不同的应力分布。", "轴力、面内弯矩和面外弯矩", "#e7ad55"],
    "应力集中": ["力学现象", "局部应力明显高于名义应力的现象。", "几何突变改变载荷流线，从而产生局部高应力。", "最大应力位置和集中程度", "#e7ad55"],
    "热点应力": ["力学指标", "评估焊接结构疲劳的局部结构应力。", "一般通过焊趾附近若干位置的应力结果外推获得。", "外推位置和热点应力范围", "#e7ad55"],
    "应力集中系数": ["力学指标", "衡量局部应力放大程度的无量纲系数。", "等于热点应力与名义应力之比，简称SCF。", "SCF数值及影响参数", "#e7ad55"],
    "疲劳裂纹": ["失效形式", "反复载荷作用下产生并扩展的裂纹。", "海洋波浪形成循环载荷，裂纹常从焊趾等高应力位置开始。", "裂纹起点和疲劳寿命", "#e7ad55"],
    "有限元分析": ["研究方法", "把复杂结构离散成单元进行数值计算。", "通过建模、施加载荷和求解获得管节点的应力分布。", "模型尺寸、边界条件和验证", "#2f9abb"],
    "网格划分": ["建模步骤", "把有限元模型划分成许多小单元。", "相贯线和焊缝附近需要细化网格以提高计算精度。", "单元尺寸、网格质量和收敛性", "#2f9abb"],
}

# 节点坐标均为固定值，保证每次打开排版完全相同。
nodes = {
    "海洋平台管节点": (490, 275, 220, 66, "main"),
    "结构组成": (260, 135, 150, 48, "branch"),
    "连接位置": (260, 405, 150, 48, "branch"),
    "受力与疲劳": (790, 155, 170, 48, "branch"),
    "分析方法": (790, 465, 150, 48, "branch"),
    "弦管": (35, 75, 135, 42, "leaf"),
    "支管": (35, 195, 135, 42, "leaf"),
    "焊缝": (35, 355, 135, 42, "leaf"),
    "相贯线": (35, 475, 135, 42, "leaf"),
    "载荷传递": (1040, 35, 150, 42, "leaf"),
    "应力集中": (1040, 125, 150, 42, "leaf"),
    "热点应力": (1040, 215, 150, 42, "leaf"),
    "应力集中系数": (1040, 305, 150, 42, "leaf"),
    "疲劳裂纹": (1040, 395, 150, 42, "leaf"),
    "有限元分析": (1040, 485, 150, 42, "leaf"),
    "网格划分": (1040, 555, 150, 42, "leaf"),
}

# 清晰的树形层级，不绘制交叉关系线。
links = [
    ("海洋平台管节点", "结构组成", "#16a3a5"),
    ("海洋平台管节点", "连接位置", "#ef6b6b"),
    ("海洋平台管节点", "受力与疲劳", "#e7ad55"),
    ("海洋平台管节点", "分析方法", "#2f9abb"),
    ("结构组成", "弦管", "#16a3a5"),
    ("结构组成", "支管", "#16a3a5"),
    ("连接位置", "焊缝", "#ef6b6b"),
    ("连接位置", "相贯线", "#ef6b6b"),
    ("受力与疲劳", "载荷传递", "#e7ad55"),
    ("受力与疲劳", "应力集中", "#e7ad55"),
    ("受力与疲劳", "热点应力", "#e7ad55"),
    ("受力与疲劳", "应力集中系数", "#e7ad55"),
    ("受力与疲劳", "疲劳裂纹", "#e7ad55"),
    ("分析方法", "有限元分析", "#2f9abb"),
    ("分析方法", "网格划分", "#2f9abb"),
]


st.title("⚓ 海洋平台管节点知识图谱")
st.caption("船舶与海洋工程 · Python知识图谱")
st.write("知识点以思维导图形式分层展示。点击任意名称，可在右侧查看详细解释。")

keyword = st.text_input("搜索知识名称", placeholder="例如：应力集中、弦管")
if keyword:
    matches = [name for name in entities if keyword.lower() in name.lower()]
    if matches:
        for name in matches:
            info = entities[name]
            st.success(f"{name}｜{info[0]}：{info[1]}")
    else:
        st.warning("没有找到相关知识名称")


def anchor(name, toward_right):
    x, y, w, h, _ = nodes[name]
    return (x + w, y + h / 2) if toward_right else (x, y + h / 2)


paths = []
for source, target, color in links:
    sx, sy, sw, sh, _ = nodes[source]
    tx, ty, tw, th, _ = nodes[target]
    target_on_right = tx > sx
    x1, y1 = anchor(source, target_on_right)
    x2, y2 = anchor(target, not target_on_right)
    middle_x = (x1 + x2) / 2
    # 直角折线：横向离开父节点，再纵向对齐，最后横向进入子节点。
    paths.append(
        f'<path d="M {x1} {y1} H {middle_x} V {y2} H {x2}" '
        f'stroke="{color}" stroke-width="2.4" fill="none" />'
    )


node_parts = []
for name, (x, y, width, height, node_type) in nodes.items():
    info = entities[name]
    safe_name = json.dumps(name, ensure_ascii=False)
    if node_type in {"main", "branch"}:
        fill, stroke, text_color = info[4], info[4], "#ffffff"
        radius = 22 if node_type == "main" else 18
    else:
        fill, stroke, text_color = "#ffffff", info[4], "#253247"
        radius = 7
    font_size = 21 if node_type == "main" else 15
    node_parts.append(
        f'<g class="node" onclick=\'showDetail({safe_name})\'>'
        f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="{radius}" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="2.4" />'
        f'<text x="{x + width / 2}" y="{y + height / 2 + 5}" '
        f'font-size="{font_size}" fill="{text_color}">{name}</text>'
        f'</g>'
    )

node_data = {
    name: {"category": v[0], "concept": v[1], "explanation": v[2], "focus": v[3], "color": v[4]}
    for name, v in entities.items()
}

html = f"""
<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">
<style>
* {{ box-sizing:border-box; }}
body {{ margin:0; background:#f8fafc; font-family:Arial,"Microsoft YaHei",sans-serif; }}
.layout {{ display:grid; grid-template-columns:minmax(850px,1fr) 325px; gap:16px; }}
.map {{ height:640px; border:1px solid #e0e6ef; border-radius:12px; background:white; overflow:hidden; }}
svg {{ width:100%; height:100%; }}
.node {{ cursor:pointer; }}
.node text {{ text-anchor:middle; font-family:"Microsoft YaHei",sans-serif; font-weight:700; pointer-events:none; }}
.node rect {{ filter:drop-shadow(0 3px 4px rgba(15,23,42,.08)); transition:.15s; }}
.node:hover rect {{ stroke-width:4; filter:drop-shadow(0 5px 7px rgba(15,23,42,.17)); }}
.panel {{ padding:22px; min-height:300px; height:max-content; background:white; border:1px solid #e0e6ef; border-top:5px solid #d94f64; border-radius:12px; box-shadow:0 10px 28px rgba(15,23,42,.08); }}
.tag {{ display:inline-block; padding:5px 10px; border-radius:999px; background:#f1f5f9; color:#d94f64; font-size:12px; font-weight:700; }}
h2 {{ margin:13px 0 18px; color:#172033; font-size:22px; }}
.block {{ padding:12px 0; border-top:1px solid #edf2f7; }}
.block strong {{ display:block; margin-bottom:6px; color:#475569; font-size:12px; }}
.block p,.tip {{ margin:0; color:#667386; font-size:14px; line-height:1.75; }}
@media(max-width:950px) {{ .layout {{ grid-template-columns:1fr; }} }}
</style></head><body>
<div class="layout">
  <div class="map">
    <svg viewBox="0 0 1220 630" preserveAspectRatio="xMidYMid meet">
      {''.join(paths)}
      {''.join(node_parts)}
    </svg>
  </div>
  <aside class="panel" id="panel">
    <span class="tag" id="category">使用提示</span>
    <h2 id="name">点击一个名称</h2>
    <p class="tip" id="tip">点击左侧思维导图中的任意知识名称，即可查看详细解释。</p>
    <div id="content" style="display:none">
      <div class="block"><strong>概念</strong><p id="concept"></p></div>
      <div class="block"><strong>名称解释</strong><p id="explanation"></p></div>
      <div class="block"><strong>工程关注点</strong><p id="focus"></p></div>
    </div>
  </aside>
</div>
<script>
const data={json.dumps(node_data, ensure_ascii=False)};
function showDetail(name){{
 const v=data[name];
 document.getElementById('tip').style.display='none';
 document.getElementById('content').style.display='block';
 document.getElementById('name').textContent=name;
 document.getElementById('category').textContent=v.category;
 document.getElementById('category').style.color=v.color;
 document.getElementById('panel').style.borderTopColor=v.color;
 document.getElementById('concept').textContent=v.concept;
 document.getElementById('explanation').textContent=v.explanation;
 document.getElementById('focus').textContent=v.focus;
}}
</script></body></html>
"""

components.html(html, height=670, scrolling=False)
st.caption(f"当前共有 {len(entities)} 个知识名称，采用4个一级分支进行分类展示。")
