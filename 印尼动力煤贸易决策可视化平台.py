"""
印尼动力煤贸易决策可视化平台
基于 2026 年 3-4 月市场数据的实战分析
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# 页面配置
st.set_page_config(
    page_title="印尼动力煤贸易决策平台",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义 CSS 样式
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .alert-box {
        background-color: #ffebee;
        border-left: 4px solid #f44336;
        padding: 15px;
        margin: 10px 0;
        border-radius: 4px;
    }
    .success-box {
        background-color: #e8f5e9;
        border-left: 4px solid #4caf50;
        padding: 15px;
        margin: 10px 0;
        border-radius: 4px;
    }
    .warning-box {
        background-color: #fff3e0;
        border-left: 4px solid #ff9800;
        padding: 15px;
        margin: 10px 0;
        border-radius: 4px;
    }
    h1, h2, h3 {
        color: #1f2937;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding-left: 20px;
        padding-right: 20px;
    }
</style>
""", unsafe_allow_html=True)

# 标题
st.title("📊 印尼动力煤贸易决策可视化平台")
st.markdown("**基于 2026 年 3-4 月市场数据的实战分析** | 数据更新日期：2026 年 4 月 14 日")
st.markdown("---")

# 侧边栏 - 核心指标概览
with st.sidebar:
    st.header("🔍 核心指标速览")
    
    # 决策级指标
    st.subheader("决策级指标")
    st.metric("CCI3800 FOB", "58.7 美元/吨", "+0.5 美元")
    st.metric("CCI4700 FOB", "76.7 美元/吨", "+0.2 美元")
    st.metric("海运费 (印尼 - 华南)", "9.5-10.5 美元/吨", "+0.5 美元")
    st.metric("内外贸价差", "倒挂 10 元/吨", "修复中")
    
    st.divider()
    
    # 预警级指标
    st.subheader("预警级指标")
    st.metric("RKAB 已批额度", "5.8 亿吨", "接近 6 亿吨目标")
    st.metric("中国电厂库存可用天数", "17-18 天", "正常水平")
    st.metric("印度电厂库存可用天数", "19.2 天", "安全水平")
    
    st.divider()
    
    # 风险预警
    st.subheader("⚠️ 风险预警")
    st.warning("出口税政策落地概率：40%")
    st.info("中东局势缓和概率：50%")
    st.warning("中国需求不及预期概率：30%")

# 主内容区域 - 标签页
tabs = st.tabs([
    "📈 核心指标监控",
    "💰 贸易利润测算",
    "📊 价格预测与走势",
    "🎯 贸易策略建议",
    "⚠️ 风险预警",
    "✅ 决策检查清单"
])

# ==================== 标签页 1: 核心指标监控 ====================
with tabs[0]:
    st.header("📈 核心指标监控")
    
    # 第一行：四个关键指标卡片
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h4>🔥 CCI3800 FOB</h4>
            <h2 style="color: #1f77b4;">58.7</h2>
            <p>美元/吨 | 较昨日 +0.2</p>
            <p style="color: #666; font-size: 12px;">采购成本基准</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h4>🚢 海运费</h4>
            <h2 style="color: #ff7f0e;">9.5-10.5</h2>
            <p>美元/吨 | 高位运行</p>
            <p style="color: #666; font-size: 12px;">印尼至华南港</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h4>📊 内外贸价差</h4>
            <h2 style="color: #d62728;">-10</h2>
            <p>元/吨 | 倒挂收窄</p>
            <p style="color: #666; font-size: 12px;">3800 大卡</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h4>⚡ 电企招标价</h4>
            <h2 style="color: #2ca02c;">540</h2>
            <p>元/吨 | 舱底含税</p>
            <p style="color: #666; font-size: 12px;">3800 大卡</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 第二行：价差走势和成本测算
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 内外贸价差历史走势")
        
        # 价差历史数据
        价差数据 = pd.DataFrame({
            '日期': ['3/13', '3/16', '3/20', '3/25', '3/30', '4/2', '4/9', '当前'],
            '倒挂幅度': [-45, -35, -25, -20, -15, -10, -8, -10],
        })
        
        fig_价差 = go.Figure()
        fig_价差.add_trace(go.Scatter(
            x=价差数据['日期'],
            y=价差数据['倒挂幅度'],
            mode='lines+markers',
            name='倒挂幅度',
            line=dict(color='#d62728', width=3),
            marker=dict(size=10),
            fill='tozeroy',
            fillcolor='rgba(214, 39, 40, 0.1)'
        ))
        
        # 添加阈值线
        fig_价差.add_hline(y=-30, line_dash="dash", line_color="orange",
                          annotation_text="观望线 (-30 元)")
        fig_价差.add_hline(y=-10, line_dash="dash", line_color="green",
                          annotation_text="采购线 (-10 元)")
        
        fig_价差.update_layout(
            height=350,
            xaxis_title="日期",
            yaxis_title="倒挂幅度 (元/吨)",
            showlegend=False,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig_价差,use_container_width=True)
    
    with col2:
        st.subheader("💰 到岸成本快速测算")
        
        # 输入参数
        col_a, col_b = st.columns(2)
        with col_a:
            fob_input = st.slider("FOB 价格 (美元/吨)", 55, 65, 58, 1)
        with col_b:
            freight_input = st.slider("海运费 (美元/吨)", 8.0, 12.0, 10.0, 0.5)
        
        # 计算到岸成本
        汇率 = 7.75
        增值税 = 1.13
        港杂费 = 25
        到岸成本 = (fob_input + freight_input) * 汇率 * 增值税 + 港杂费
        
        # 利润测算
        招标价 = 540
        毛利润 = 招标价 - 到岸成本
        
        st.markdown(f"""
        <div class="metric-card" style="background-color: {'#e8f5e9' if 毛利润 > 0 else '#ffebee'};">
            <h4>📊 成本测算结果</h4>
            <p><strong>FOB 价格：</strong>{fob_input} 美元/吨</p>
            <p><strong>海运费：</strong>{freight_input} 美元/吨</p>
            <p><strong>到岸成本：</strong><h3 style="color: {'#2ca02c' if 毛利润 > 0 else '#d62728'};">{到岸成本:.0f} 元/吨</h3></p>
            <p><strong>销售价格：</strong>{招标价} 元/吨</p>
            <p><strong>毛利润：</strong><h3 style="color: {'#2ca02c' if 毛利润 > 0 else '#d62728'};">{毛利润:.0f} 元/吨</h3></p>
        </div>
        """, unsafe_allow_html=True)
        
        # 操作建议
        if 毛利润 < 10:
            st.warning("⚠️ 利润微薄，建议谨慎操作")
        elif 毛利润 < 20:
            st.info("ℹ️ 利润合理，可适度操作")
        else:
            st.success("✅ 利润良好，可积极操作")
    
    st.markdown("---")
    
    # 第三行：供应和需求指标
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🏭 RKAB 审批进度")
        
        # RKAB 进度数据
        rkab_data = pd.DataFrame({
            '时间': ['2 月初', '2 月末', '3/12', '3/27', '4/7', '当前'],
            '已批额度 (亿吨)': [2.5, 3.0, 3.0, 5.8, 5.8, 5.8],
        })
        
        fig_rkab = go.Figure()
        fig_rkab.add_trace(go.Scatter(
            x=rkab_data['时间'],
            y=rkab_data['已批额度 (亿吨)'],
            mode='lines+markers',
            name='已批额度',
            line=dict(color='#1f77b4', width=3),
            fill='tozeroy',
            fillcolor='rgba(31, 119, 180, 0.2)'
        ))
        
        # 添加目标线
        fig_rkab.add_hline(y=6.0, line_dash="dash", line_color="orange", 
                          annotation_text="初始目标 6 亿吨")
        fig_rkab.add_hline(y=7.0, line_dash="dash", line_color="green", 
                          annotation_text="增产预期 7 亿吨")
        
        fig_rkab.update_layout(
            height=300,
            xaxis_title="时间",
            yaxis_title="已批额度 (亿吨)",
            showlegend=False
        )
        
        st.plotly_chart(fig_rkab, use_container_width=True)
        
        st.info("""
        **当前状态：** 审批进度已接近完成，5.8 亿吨接近 6 亿吨目标
        **贸易意义：** 
        - 低于 6 亿吨：供应收紧，价格上涨
        - 6-6.5 亿吨：供需平衡
        - 超过 7 亿吨：供应宽松，价格承压
        """)
    
    with col2:
        st.subheader("🏭 电厂库存可用天数")
        
        # 电厂库存数据
        inventory_data = pd.DataFrame({
            '日期': ['3/15', '3/22', '3/29', '4/5', '4/10', '当前'],
            '中国电厂': [18, 17, 17, 18, 17, 17.5],
            '印度电厂': [18.66, 18.85, 19.04, 19.2, 19.0, 19.2],
        })
        
        fig_inventory = go.Figure()
        fig_inventory.add_trace(go.Scatter(
            x=inventory_data['日期'],
            y=inventory_data['中国电厂'],
            mode='lines+markers',
            name='中国电厂',
            line=dict(color='#d62728', width=2),
            marker=dict(size=8)
        ))
        fig_inventory.add_trace(go.Scatter(
            x=inventory_data['日期'],
            y=inventory_data['印度电厂'],
            mode='lines+markers',
            name='印度电厂',
            line=dict(color='#1f77b4', width=2),
            marker=dict(size=8)
        ))
        
        # 添加阈值区域
        fig_inventory.add_hrect(y0=12, y1=15, fillcolor="yellow", opacity=0.2,
                               annotation_text="刚需补库区")
        fig_inventory.add_hrect(y0=15, y1=20, fillcolor="green", opacity=0.2,
                               annotation_text="正常水平")
        fig_inventory.add_hrect(y0=20, y1=25, fillcolor="red", opacity=0.2,
                               annotation_text="库存压力区")
        
        fig_inventory.update_layout(
            height=300,
            xaxis_title="日期",
            yaxis_title="可用天数",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        st.plotly_chart(fig_inventory, use_container_width=True)
        
        st.info("""
        **当前状态：** 中国 17-18 天（正常），印度 19.2 天（安全）
        **贸易意义：**
        - 低于 12 天：紧急补库，价格大涨
        - 12-15 天：刚需补库
        - 15-20 天：正常水平，价格震荡
        - 超过 25 天：库存压力，价格下跌
        """)

# ==================== 标签页 2: 贸易利润测算 ====================
with tabs[1]:
    st.header("💰 贸易利润测算工具")
    
    # 利润公式说明
    st.markdown("""
    ### 📐 贸易利润核心公式
    
    ```
    贸易利润 = (销售价格 - 采购成本 - 海运费用 - 政策成本) × 贸易量
    ```
    
    **拆解到印尼动力煤贸易：**
    - **销售价格**：中国南方港到岸价（CFR）
    - **采购成本**：印尼离岸价（FOB）+ 矿方溢价
    - **海运费用**：巴拿马型船运费（受油价、地缘政治影响）
    - **政策成本**：出口税 + DMO 隐性成本 + RKAB 审批延迟成本
    """)
    
    st.markdown("---")
    
    # 利润测算器
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔧 参数设置")
        
        fob_price = st.number_input("FOB 采购价 (美元/吨)", value=58.0, min_value=50.0, max_value=80.0, step=0.5)
        freight = st.number_input("海运费 (美元/吨)", value=10.0, min_value=7.0, max_value=15.0, step=0.5)
        tax_rate = st.number_input("出口税率 (%)", value=0.0, min_value=0.0, max_value=5.0, step=0.5)
        trade_volume = st.number_input("贸易量 (万吨)", value=10.0, min_value=1.0, max_value=100.0, step=1.0)
        
        sales_price = st.number_input("销售价格 (元/吨，舱底含税)", value=540.0, min_value=450.0, max_value=650.0, step=5.0)
    
    with col2:
        # 计算
        汇率 = 7.75
        增值税 = 1.13
        港杂费 = 25
        
        # 到岸成本
        到岸成本美元 = fob_price + freight + (fob_price * tax_rate / 100)
        到岸成本元 = 到岸成本美元 * 汇率 * 增值税 + 港杂费
        
        # 利润
        单位利润 = sales_price - 到岸成本元
        总利润 = 单位利润 * trade_volume * 10000  # 转换为元
        
        # 利润率
        利润率 = (单位利润 / sales_price) * 100 if sales_price > 0 else 0
        
        st.subheader("📊 测算结果")
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("到岸成本", f"{到岸成本元:.0f} 元/吨")
            st.metric("单位利润", f"{单位利润:.0f} 元/吨")
        with col_b:
            st.metric("总利润", f"{总利润/10000:.1f} 万元")
            st.metric("利润率", f"{利润率:.1f}%")
        
        # 利润评估
        st.markdown("### 评估建议")
        if 单位利润 < 0:
            st.error(f"❌ 亏损交易！每吨亏损 {abs(单位利润):.0f} 元，建议放弃")
        elif 单位利润 < 10:
            st.warning(f"⚠️ 微利交易！每吨利润 {单位利润:.0f} 元，建议谨慎操作")
        elif 单位利润 < 20:
            st.info(f"ℹ️ 合理利润！每吨利润 {单位利润:.0f} 元，可适度操作")
        else:
            st.success(f"✅ 良好利润！每吨利润 {单位利润:.0f} 元，可积极操作")
    
    st.markdown("---")
    
    # 敏感性分析
    st.subheader("📊 利润敏感性分析")
    
    # 创建 FOB 和海运费的敏感性分析矩阵
    fob_range = np.arange(55, 65, 1)
    freight_range = np.arange(8, 12, 0.5)
    
    profit_matrix = np.zeros((len(fob_range), len(freight_range)))
    
    for i, fob in enumerate(fob_range):
        for j, freight in enumerate(freight_range):
            成本 = (fob + freight) * 汇率 * 增值税 + 港杂费
            profit_matrix[i, j] = sales_price - 成本
    
    fig_sensitivity = go.Figure(data=
        go.Heatmap(
            z=profit_matrix,
            x=freight_range,
            y=fob_range,
            colorscale='RdYlGn',
            zmid=0,
            text=profit_matrix,
            texttemplate='%{text:.0f}',
            textfont={"size": 10},
            hovertemplate='FOB: %{y} 美元<br>运费：%{x} 美元<br>利润：%{z:.0f} 元<extra></extra>'
        )
    )
    
    fig_sensitivity.update_layout(
        title="不同 FOB 价格和海运费下的单位利润 (元/吨)",
        xaxis_title="海运费 (美元/吨)",
        yaxis_title="FOB 价格 (美元/吨)",
        height=400
    )
    
    st.plotly_chart(fig_sensitivity, use_container_width=True)
    
    st.markdown("""
    **使用说明：**
    - 绿色区域：盈利区间，可积极操作
    - 黄色区域：微利区间，谨慎操作
    - 红色区域：亏损区间，建议放弃
    """)

# ==================== 标签页 3: 价格预测与走势 ====================
with tabs[2]:
    st.header("📊 价格预测与走势分析")
    
    # 价格预测表格
    st.subheader("📈 4 月下旬价格预测")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card" style="background-color: #e3f2fd;">
            <h4>🔥 CCI3800 FOB</h4>
            <table style="width: 100%;">
                <tr><td>低位</td><td style="text-align: center; color: #d62728;">55 美元</td></tr>
                <tr><td>基准</td><td style="text-align: center; color: #1f77b4;">58 美元</td></tr>
                <tr><td>高位</td><td style="text-align: center; color: #2ca02c;">61 美元</td></tr>
            </table>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card" style="background-color: #fff3e0;">
            <h4>🔥 CCI4700 FOB</h4>
            <table style="width: 100%;">
                <tr><td>低位</td><td style="text-align: center; color: #d62728;">73 美元</td></tr>
                <tr><td>基准</td><td style="text-align: center; color: #ff7f0e;">76 美元</td></tr>
                <tr><td>高位</td><td style="text-align: center; color: #2ca02c;">79 美元</td></tr>
            </table>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card" style="background-color: #e8f5e9;">
            <h4>🚢 海运费</h4>
            <table style="width: 100%;">
                <tr><td>低位</td><td style="text-align: center; color: #d62728;">8.5 美元</td></tr>
                <tr><td>基准</td><td style="text-align: center; color: #2ca02c;">9.5 美元</td></tr>
                <tr><td>高位</td><td style="text-align: center; color: #2ca02c;">10.5 美元</td></tr>
            </table>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.subheader("📈 5 月价格预测")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card" style="background-color: #e3f2fd;">
            <h4>🔥 CCI3800 FOB (5 月)</h4>
            <table style="width: 100%;">
                <tr><td>低位</td><td style="text-align: center;">57 美元</td></tr>
                <tr><td>基准</td><td style="text-align: center; color: #2ca02c;">60 美元</td></tr>
                <tr><td>高位</td><td style="text-align: center; color: #2ca02c;">64 美元</td></tr>
            </table>
            <p style="color: #666; font-size: 12px;">↑ 迎峰度夏预期支撑</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card" style="background-color: #fff3e0;">
            <h4>🔥 CCI4700 FOB (5 月)</h4>
            <table style="width: 100%;">
                <tr><td>低位</td><td style="text-align: center;">75 美元</td></tr>
                <tr><td>基准</td><td style="text-align: center; color: #2ca02c;">78 美元</td></tr>
                <tr><td>高位</td><td style="text-align: center; color: #2ca02c;">82 美元</td></tr>
            </table>
            <p style="color: #666; font-size: 12px;">↑ 印度需求支撑</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card" style="background-color: #e8f5e9;">
            <h4>🚢 海运费 (5 月)</h4>
            <table style="width: 100%;">
                <tr><td>低位</td><td style="text-align: center;">8 美元</td></tr>
                <tr><td>基准</td><td style="text-align: center;">9 美元</td></tr>
                <tr><td>高位</td><td style="text-align: center;">10 美元</td></tr>
            </table>
            <p style="color: #666; font-size: 12px;">↓ 局势缓和预期</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 价格走势模拟图
    st.subheader("📊 二季度价格走势模拟")
    
    # 生成模拟数据
    dates = pd.date_range(start='2026-04-01', end='2026-06-30', freq='D')
    np.random.seed(42)
    
    # 3800 FOB 价格模拟
    base_price_3800 = 58
    trend_3800 = np.linspace(0, 4, len(dates))  # 上涨趋势
    noise_3800 = np.random.normal(0, 1.5, len(dates))
    price_3800 = base_price_3800 + trend_3800 + noise_3800
    
    # 4700 FOB 价格模拟
    base_price_4700 = 76
    trend_4700 = np.linspace(0, 4, len(dates))
    noise_4700 = np.random.normal(0, 2, len(dates))
    price_4700 = base_price_4700 + trend_4700 + noise_4700
    
    fig_trend = make_subplots(rows=2, cols=1, subplot_titles=('CCI3800 FOB 价格走势模拟', 'CCI4700 FOB 价格走势模拟'))
    
    fig_trend.add_trace(go.Scatter(
        x=dates,
        y=price_3800,
        mode='lines',
        name='3800 FOB',
        line=dict(color='#d62728', width=2),
        fill='tozeroy',
        fillcolor='rgba(214, 39, 40, 0.1)'
    ), row=1, col=1)
    
    fig_trend.add_trace(go.Scatter(
        x=dates,
        y=price_4700,
        mode='lines',
        name='4700 FOB',
        line=dict(color='#ff7f0e', width=2),
        fill='tozeroy',
        fillcolor='rgba(255, 127, 14, 0.1)'
    ), row=2, col=1)
    
    # 添加预测区间
    fig_trend.add_trace(go.Scatter(
        x=dates,
        y=base_price_3800 + trend_3800 + 3,
        mode='lines',
        name='预测上限',
        line=dict(color='green', width=1, dash='dash'),
        showlegend=False
    ), row=1, col=1)
    
    fig_trend.add_trace(go.Scatter(
        x=dates,
        y=base_price_3800 + trend_3800 - 3,
        mode='lines',
        name='预测下限',
        line=dict(color='red', width=1, dash='dash'),
        fill='tonexty',
        showlegend=False
    ), row=1, col=1)
    
    fig_trend.update_layout(height=600, showlegend=False)
    fig_trend.update_xaxes(title_text="日期", row=2, col=1)
    fig_trend.update_yaxes(title_text="价格 (美元/吨)", row=1, col=1)
    fig_trend.update_yaxes(title_text="价格 (美元/吨)", row=2, col=1)
    
    st.plotly_chart(fig_trend, use_container_width=True)
    
    st.markdown("""
    **核心逻辑：**
    1. **供应端**：RKAB 审批完成后供应边际宽松，限制涨幅
    2. **需求端**：5 月进入迎峰度夏预期，印度夏季备库启动
    3. **成本端**：出口税政策若落地，将推高成本支撑
    4. **海运费**：中东局势缓和预期下，运费有回落空间
    """)

# ==================== 标签页 4: 贸易策略建议 ====================
with tabs[3]:
    st.header("🎯 贸易策略与操作建议")
    
    # 总体判断
    st.markdown("""
    ### 📊 总体判断：震荡偏强，存在阶段性机会
    
    **核心逻辑：**
    1. ✅ 供应端：RKAB 审批接近完成，但 5.8 亿吨仍低于预期，4 月下旬供应可能边际收紧
    2. ✅ 需求端：中国处于淡季，但 5 月后迎峰度夏预期增强；印度夏季备库即将启动
    3. ✅ 成本端：海运费高位，出口税政策不确定性支撑价格
    """)
    
    st.markdown("---")
    
    # 操作建议时间表
    st.subheader("📅 操作建议时间表")
    
    strategy_data = pd.DataFrame({
        '时间窗口': ['4 月 15-20 日', '4 月 25-30 日', '5 月上旬', '5 月中旬'],
        '策略': ['试探性采购', '加大采购量', '逢高出货', '根据库存调整'],
        '目标价格': ['FOB 56-58 美元', 'FOB 55-57 美元', 'CFR 72-75 美元', '-'],
        '止损位': ['FOB 55 美元', 'FOB 54 美元', '-', '-'],
    })
    
    st.table(strategy_data)
    
    st.markdown("---")
    
    # 两种贸易方案
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🛡️ 方案 A：保守型（适合中小贸易商）
        
        **采购计划：**
        - 采购量：5-10 万吨（3800 大卡）
        - 目标 FOB：56-58 美元/吨
        - 目标海运费：9-9.5 美元/吨
        - 到岸成本：约 515-530 元/吨
        
        **销售计划：**
        - 目标客户：华南中小电厂
        - 目标价格：535-545 元/吨（舱底含税）
        - 预期利润：10-20 元/吨
        
        **风险控制：**
        - ⚠️ 若 FOB 突破 60 美元，暂停采购
        - ⚠️ 若海运费突破 10.5 美元，推迟发运
        - ⚠️ 若出口税政策落地，重新测算成本
        """)
    
    with col2:
        st.markdown("""
        ### 🚀 方案 B：激进型（适合大型贸易商）
        
        **采购计划：**
        - 采购量：20-30 万吨（3800 大卡 +4700 大卡混合）
        - 目标 FOB：55-57 美元/吨
        - 目标海运费：8.5-9.5 美元/吨
        - 到岸成本：约 510-525 元/吨
        
        **销售计划：**
        - 目标客户：大型电企 + 贸易商分销
        - 目标价格：540-550 元/吨（舱底含税）
        - 预期利润：20-35 元/吨
        
        **风险控制：**
        - ⚠️ 设置止损：若到岸成本超过 535 元/吨，停止采购
        - ⚠️ 套期保值：考虑利用期货市场对冲价格风险
        - ⚠️ 若出口税政策落地，与下游协商价格联动
        """)
    
    st.markdown("---")
    
    # 套利机会
    st.subheader("💹 套利机会")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### 1️⃣ 内外贸套利
        
        **当前条件：**
        - 内贸 3800 大卡港口价：约 550 元/吨
        - 进口 3800 大卡到岸成本：约 525 元/吨
        - 价差：顺挂约 25 元/吨
        
        **操作建议：**
        - ✅ 若价差扩大至 30 元以上，可加大进口采购
        - ⚠️ 若价差收窄至 10 元以内，转向内贸采购
        """)
    
    with col2:
        st.markdown("""
        #### 2️⃣ 跨期套利
        
        **逻辑：**
        - 4 月价格相对低位（淡季）
        - 5-6 月价格预期走高（迎峰度夏）
        
        **操作建议：**
        - ✅ 4 月采购 4-5 月船期，锁定低价
        - 🎯 目标价差：15-25 元/吨
        """)

# ==================== 标签页 5: 风险预警 ====================
with tabs[4]:
    st.header("⚠️ 风险预警与应对")
    
    # 风险概览
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="alert-box">
            <h4>🔴 最大风险：出口税政策落地</h4>
            <p><strong>概率评估：</strong>40%</p>
            <p><strong>影响：</strong>增加 3-4 美元/吨成本</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="warning-box">
            <h4>🟡 次要风险：中东局势缓和</h4>
            <p><strong>概率评估：</strong>50%</p>
            <p><strong>影响：</strong>海运费回落，价格支撑减弱</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="warning-box">
            <h4>🟡 尾部风险：中国需求不及预期</h4>
            <p><strong>概率评估：</strong>30%</p>
            <p><strong>影响：</strong>夏季需求疲软</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 出口税影响测算
    st.subheader("📊 出口税政策影响测算")
    
    tax_impact_data = pd.DataFrame({
        '税率': ['0%', '1%', '2%', '3%', '4%', '5%'],
        '增加成本 (美元/吨)': [0, 0.6, 1.2, 1.8, 2.4, 3.0],
        '增加成本 (元/吨)': [0, 5, 10, 14, 19, 23],
        '建议': ['正常操作', '正常操作', '谨慎操作', '重新测算', '协商联动', '暂停采购'],
    })
    
    st.table(tax_impact_data)
    
    st.markdown("""
    **应对方案：**
    1. ✅ 若税率≤3%，可消化成本，继续执行原计划
    2. ⚠️ 若税率>3%，与下游协商价格联动
    3. ❌ 若税率>5%，暂停新采购，观望政策走向
    """)
    
    st.markdown("---")
    
    # 风险应对流程图
    st.subheader("🔄 风险应对流程")
    
    st.markdown("""
    ### 出口税政策应对流程
    
    ```
    政策公布 → 评估税率 → 测算成本 → 调整策略
                ↓
    ┌───────────┼───────────┬───────────┐
    ↓           ↓           ↓           ↓
    ≤3%        3%-5%       >5%        观望
    继续执行    协商联动     暂停采购    等待明确
    ```
    
    ### 中东局势应对流程
    
    ```
    局势变化 → 评估运费 → 调整采购节奏
                ↓
    ┌───────────┼───────────┐
    ↓           ↓           ↓
    缓和       持续        升级
    加快出货    正常执行     加大采购
    ```
    
    ### 中国需求应对流程
    
    ```
    监测日耗 → 评估库存 → 调整出货节奏
                ↓
    ┌───────────┼───────────┐
    ↓           ↓           ↓
    超预期     符合预期    不及预期
    加大出货    正常执行    提前出货
    ```
    """)

# ==================== 标签页 6: 决策检查清单 ====================
with tabs[5]:
    st.header("✅ 贸易决策检查清单")
    
    # 每日必查
    st.subheader("📅 每日必查（下单前确认）")
    
    st.markdown("""
    <div class="metric-card">
        <table style="width: 100%;">
            <tr>
                <td style="width: 30px;">☐</td>
                <td><strong>CCI3800/4700 离岸价是否稳定</strong></td>
                <td style="text-align: right; color: #1f77b4;">当前：58.7/76.7 美元</td>
            </tr>
            <tr>
                <td>☐</td>
                <td><strong>海运费是否超过 10.5 美元/吨</strong></td>
                <td style="text-align: right; color: #ff7f0e;">当前：9.5-10.5 美元</td>
            </tr>
            <tr>
                <td>☐</td>
                <td><strong>内外贸价差是否有利于进口</strong></td>
                <td style="text-align: right; color: #d62728;">当前：倒挂 10 元</td>
            </tr>
            <tr>
                <td>☐</td>
                <td><strong>中国电企招标价是否有变化</strong></td>
                <td style="text-align: right; color: #2ca02c;">当前：540 元/吨</td>
            </tr>
            <tr>
                <td>☐</td>
                <td><strong>中东局势是否有新变化</strong></td>
                <td style="text-align: right; color: #666;">关注：霍尔木兹海峡</td>
            </tr>
        </table>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 每周必查
    st.subheader("📆 每周必查（调整策略）")
    
    st.markdown("""
    <div class="metric-card">
        <table style="width: 100%;">
            <tr>
                <td style="width: 30px;">☐</td>
                <td><strong>RKAB 审批进度是否更新</strong></td>
                <td style="text-align: right; color: #1f77b4;">当前：5.8 亿吨</td>
            </tr>
            <tr>
                <td>☐</td>
                <td><strong>中国沿海电厂可用天数变化</strong></td>
                <td style="text-align: right; color: #2ca02c;">当前：17-18 天</td>
            </tr>
            <tr>
                <td>☐</td>
                <td><strong>印度电厂可用天数变化</strong></td>
                <td style="text-align: right; color: #2ca02c;">当前：19.2 天</td>
            </tr>
            <tr>
                <td>☐</td>
                <td><strong>印尼出口量数据是否公布</strong></td>
                <td style="text-align: right; color: #666;">关注：月度数据</td>
            </tr>
            <tr>
                <td>☐</td>
                <td><strong>出口税政策是否有新进展</strong></td>
                <td style="text-align: right; color: #d62728;">概率：40%</td>
            </tr>
        </table>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 每月必查
    st.subheader("📋 每月必查（战略调整）")
    
    st.markdown("""
    <div class="metric-card">
        <table style="width: 100%;">
            <tr>
                <td style="width: 30px;">☐</td>
                <td><strong>印尼煤炭出口量趋势</strong></td>
                <td style="text-align: right;">当前：3668 万吨/月</td>
            </tr>
            <tr>
                <td>☐</td>
                <td><strong>中国煤炭进口量趋势</strong></td>
                <td style="text-align: right;">关注：海关数据</td>
            </tr>
            <tr>
                <td>☐</td>
                <td><strong>HBA 参考价变化</strong></td>
                <td style="text-align: right;">当前：72.28 美元 (5300 大卡)</td>
            </tr>
            <tr>
                <td>☐</td>
                <td><strong>主要矿商生产状态</strong></td>
                <td style="text-align: right;">关注：PTBA、Adaro 等</td>
            </tr>
            <tr>
                <td>☐</td>
                <td><strong>下月船期资源情况</strong></td>
                <td style="text-align: right;">关注：4-5 月船期</td>
            </tr>
        </table>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 贸易格言
    st.markdown("""
    ### 💡 贸易格言
    
    > "贸易不是预测未来，而是管理风险。"
    
    **在当前市场环境下，建议：**
    - ✅ 不赌方向，顺势而为
    - ✅ 不追高价，逢低布局
    - ✅ 不贪利润，及时出货
    - ✅ 不忽视政策，每日跟踪
    """)
    
    # 最后提醒
    st.info("""
    ### ⚠️ 最后提醒
    
    市场瞬息万变，作为贸易决策者，最重要的是：
    1. **保持信息敏感度**：每日跟踪核心指标
    2. **保持灵活性**：根据市场变化及时调整策略
    3. **保持风险意识**：永远留有退路，不孤注一掷
    """)

# 页脚
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 12px;">
    <p>报告编制：资深动力煤贸易决策者 | 编制日期：2026 年 4 月 14 日</p>
    <p>数据来源：中国煤炭资源网、汾渭 CCI、Kpler、印尼能源与矿产资源部</p>
</div>
""", unsafe_allow_html=True)