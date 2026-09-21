import json

import streamlit as st
from pyvis.network import Network


st.set_page_config(
    page_title="海洋平台管节点知识图谱",
    page_icon="⚓",
    layout="wide",
)


# 每个知识名称包含：所属概念、名称解释、工程关注点和显示颜色
entities = {
    "海洋平台管节点": {
        "category": "核心对象",
        "concept": "海洋平台导管架结构中的关键连接区域。",
        "explanation": "由多根钢管相互连接形成，负责把不同杆件上的载荷传递到整个平台结构。",
        "focus": "承载能力、应力集中和疲劳寿命",
        "color": "#2563eb",
    },
    "弦管": {
        "category": "结构组成",
        "concept": "管节点中的主要承载钢管。",
        "explanation": "弦管通常直径较大，相当于导管架桁架结构中的主杆件。",
        "focus": "管径、壁厚和局部变形",
        "color": "#0f9f91",
    },
    "支管": {
        "category": "结构组成",
        "concept": "与弦管相连接并向其传递载荷的钢管。",
        "explanation": "支管一般以一定角度连接到弦管上，形成T型、Y型、K型等管节点。",
        "focus": "连接角度、直径比和载荷方向",
        "color": "#0f9f91",
    },
    "焊缝": {
        "category": "连接部位",
        "concept": "将支管与弦管连接为整体的金属连接区域。",
        "explanation": "焊缝保证节点能够传递载荷，但焊趾位置容易出现较大的局部应力。",
        "focus": "焊接质量、焊趾形状和缺陷",
        "color": "#d97706",
    },
    "相贯线": {
        "category": "关键位置",
        "concept": "支管表面与弦管表面相交形成的空间曲线。",
        "explanation": "相贯线环绕支管根部，是管节点几何变化最明显的位置。",
        "focus": "几何突变和周向应力分布",
        "color": "#ea580c",
    },
    "载荷传递": {
        "category": "受力过程",
        "concept": "力和弯矩从支管经过连接区域传向弦管的过程。",
        "explanation": "不同的轴力、弯矩和连接角度会产生不同的节点应力分布。",
        "focus": "轴向载荷、面内弯矩和面外弯矩",
        "color": "#7c3aed",
    },
    "应力集中": {
        "category": "力学现象",
        "concept": "局部应力明显高于结构名义应力的现象。",
        "explanation": "由于管件交汇处发生几何突变，载荷流线改变，从而产生局部高应力。",
        "focus": "最大应力位置和应力集中程度",
        "color": "#dc2626",
    },
    "热点应力": {
        "category": "力学指标",
        "concept": "用于评估焊接结构疲劳问题的局部结构应力。",
        "explanation": "热点应力通常通过焊趾附近若干位置的应力结果外推得到。",
        "focus": "外推位置和热点应力范围",
        "color": "#db2777",
    },
    "应力集中系数": {
        "category": "力学指标",
        "concept": "衡量局部应力放大程度的无量纲系数。",
        "explanation": "应力集中系数通常等于热点应力与名义应力之比，简称SCF。",
        "focus": "SCF数值及其影响参数",
        "color": "#db2777",
    },
    "疲劳裂纹": {
        "category": "失效形式",
        "concept": "结构在反复载荷作用下逐渐产生并扩展的裂纹。",
        "explanation": "海洋波浪会带来长期循环载荷，裂纹往往从焊趾等高应力位置开始。",
        "focus": "裂纹起始位置和疲劳寿命",
        "color": "#9333ea",
    },
    "有限元分析": {
        "category": "研究方法",
        "concept": "将复杂结构离散成有限数量单元进行数值计算的方法。",
        "explanation": "通过建立管节点模型、施加载荷和求解，可以获得完整的应力分布。",
        "focus": "模型尺寸、边界条件和结果验证",
        "color": "#475569",
    },
    "网格划分": {
        "category": "建模步骤",
        "concept": "把有限元模型划分成许多小单元的过程。",
        "explanation": "相贯线和焊缝附近通常需要细化网格，才能更准确地计算局部应力。",
        "focus": "单元尺寸、网格质量和收敛性",
        "color": "#64748b",
    },
}


# 每一条关系的格式是：（起点，终点，关系名称）
relations = [
    ("海洋平台管节点", "弦管", "包含"),
    ("海洋平台管节点", "支管", "包含"),
    ("支管", "焊缝", "通过焊接连接"),
    ("支管", "相贯线", "与弦管相交形成"),
    ("载荷传递", "支管", "经过"),
    ("载荷传递", "应力集中", "可能产生"),
    ("应力集中", "相贯线", "常发生在"),
    ("应力集中", "热点应力", "可表示为"),
    ("热点应力", "应力集中系数", "用于计算"),
    ("应力集中", "疲劳裂纹", "可能导致"),
    ("疲劳裂纹", "焊缝", "常起始于"),
    ("有限元分析", "应力集中", "用于研究"),
    ("有限元分析", "网格划分", "需要进行"),
    ("网格划分", "相贯线", "重点细化"),
]


st.title("⚓ 海洋平台管节点知识图谱")
st.caption("船舶与海洋工程 · Python知识图谱")
st.write("点击图中的知识名称，右侧会显示它的概念、名称解释和工程关注点。")


# 搜索区
keyword = st.text_input("搜索知识名称", placeholder="例如：应力集中、弦管")

if keyword:
    results = [name for name in entities if keyword.lower() in name.lower()]

    if results:
        for name in results:
            information = entities[name]
            with st.container(border=True):
                st.markdown(f"**{name}**　`{information['category']}`")
                st.write(f"概念：{information['concept']}")
                st.write(f"解释：{information['explanation']}")
    else:
        st.warning("没有找到相关知识名称")


# 创建交互式知识图谱
graph = Network(
    height="620px",
    width="100%",
    directed=True,
    bgcolor="#f8fafc",
    font_color="#172033",
    cdn_resources="in_line",
)


for name, information in entities.items():
    graph.add_node(
        name,
        label=name,
        title=f"点击查看：{name}",
        color={
            "background": information["color"],
            "border": "#ffffff",
            "highlight": {
                "background": information["color"],
                "border": "#facc15",
            },
        },
        size=34 if name == "海洋平台管节点" else 25,
        shape="dot",
    )


for source, target, relation in relations:
    graph.add_edge(
        source,
        target,
        label=relation,
        title=f"{source} —{relation}→ {target}",
        color="#9aa6ba",
    )


graph.set_options(
    """
    {
      "nodes": {
        "borderWidth": 3,
        "font": {
          "size": 16,
          "face": "Microsoft YaHei",
          "color": "#172033",
          "strokeWidth": 4,
          "strokeColor": "#f8fafc"
        }
      },
      "edges": {
        "width": 1.5,
        "arrows": {"to": {"enabled": true, "scaleFactor": 0.7}},
        "font": {
          "size": 11,
          "face": "Microsoft YaHei",
          "color": "#64748b",
          "strokeWidth": 4,
          "strokeColor": "#f8fafc"
        },
        "smooth": {"enabled": true, "type": "dynamic"}
      },
      "interaction": {
        "hover": true,
        "navigationButtons": true,
        "keyboard": true
      },
      "physics": {
        "barnesHut": {
          "gravitationalConstant": -4200,
          "centralGravity": 0.25,
          "springLength": 155,
          "springConstant": 0.04
        },
        "stabilization": {"iterations": 180}
      }
    }
    """
)


graph_html = graph.generate_html()
node_information = json.dumps(entities, ensure_ascii=False)


# 在图谱右侧增加详情面板，并监听节点点击事件
extra_style = """
<style>
  body {
    margin: 0;
    background: #f8fafc;
    font-family: Arial, "Microsoft YaHei", sans-serif;
  }

  #mynetwork {
    width: calc(100% - 365px) !important;
    height: 615px !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 14px;
    background: #ffffff;
  }

  #detail-panel {
    position: fixed;
    right: 12px;
    top: 0;
    width: 325px;
    min-height: 250px;
    padding: 22px;
    box-sizing: border-box;
    border: 1px solid #e2e8f0;
    border-top: 5px solid #2563eb;
    border-radius: 14px;
    background: #ffffff;
    box-shadow: 0 12px 35px rgba(15, 23, 42, 0.08);
  }

  #detail-panel h2 {
    margin: 12px 0 18px;
    color: #172033;
    font-size: 22px;
  }

  #detail-type {
    display: inline-block;
    padding: 5px 10px;
    border-radius: 999px;
    color: #2563eb;
    background: #eff6ff;
    font-size: 12px;
    font-weight: bold;
  }

  .detail-block {
    padding: 13px 0;
    border-top: 1px solid #eef2f7;
  }

  .detail-block strong {
    display: block;
    margin-bottom: 6px;
    color: #475569;
    font-size: 12px;
  }

  .detail-block p {
    margin: 0;
    color: #5f6b7d;
    font-size: 14px;
    line-height: 1.75;
  }

  .empty-tip {
    color: #94a3b8;
    font-size: 14px;
    line-height: 1.8;
  }
</style>
"""


detail_panel = """
<aside id="detail-panel">
  <span id="detail-type">使用提示</span>
  <h2 id="detail-name">点击一个名称</h2>

  <div id="empty-tip" class="empty-tip">
    点击左侧网络图中的任意节点，即可查看该名称的详细解释。
  </div>

  <div id="detail-content" style="display: none;">
    <div class="detail-block">
      <strong>概念</strong>
      <p id="detail-concept"></p>
    </div>

    <div class="detail-block">
      <strong>名称解释</strong>
      <p id="detail-explanation"></p>
    </div>

    <div class="detail-block">
      <strong>工程关注点</strong>
      <p id="detail-focus"></p>
    </div>
  </div>
</aside>

<script>
  const nodeInformation = __NODE_INFORMATION__;

  network.on("click", function (event) {
    if (event.nodes.length === 0) return;

    const name = event.nodes[0];
    const information = nodeInformation[name];
    const panel = document.getElementById("detail-panel");
    const typeLabel = document.getElementById("detail-type");

    document.getElementById("empty-tip").style.display = "none";
    document.getElementById("detail-content").style.display = "block";
    document.getElementById("detail-name").textContent = name;
    document.getElementById("detail-concept").textContent = information.concept;
    document.getElementById("detail-explanation").textContent = information.explanation;
    document.getElementById("detail-focus").textContent = information.focus;

    typeLabel.textContent = information.category;
    typeLabel.style.color = information.color;
    panel.style.borderTopColor = information.color;

    network.focus(name, {
      scale: 1.12,
      animation: {duration: 450, easingFunction: "easeInOutQuad"}
    });
  });
</script>
""".replace("__NODE_INFORMATION__", node_information)


graph_html = graph_html.replace("</head>", extra_style + "</head>")
graph_html = graph_html.replace("</body>", detail_panel + "</body>")

st.iframe(graph_html, height=650)


st.caption(
    f"当前共有 {len(entities)} 个知识名称、{len(relations)} 条知识关系。"
)
