import streamlit as st
import requests
import json

st.set_page_config(page_title="关键字难度检查", page_icon="🎯")

# Custom CSS
st.markdown("""
<style>
    .stApp {
        background-color: #1a1a1a;
        color: white;
    }
    .result-card {
        background-color: white;
        padding: 30px;
        border-radius: 15px;
        margin: 20px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .metric-container {
        text-align: left;
        margin-bottom: 30px;
    }
    .metric-label {
        font-size: 15px;
        color: #666;
        margin-bottom: 8px;
    }
    .metric-value {
        font-size: 28px;
        font-weight: 500;
        color: #0066FF;
    }
    .metric-value.na {
        color: #0066FF;
    }
    .difficulty-label {
        font-size: 15px;
        color: #666;
        margin-top: 20px;
        margin-bottom: 8px;
    }
    .difficulty-value {
        font-size: 16px;
        color: #333;
    }
    /* 自定义表单样式 */
    .stTextInput > div > div > input {
        background-color: #2d2d2d;
        color: white;
        border: 1px solid #444;
    }
    .stSelectbox > div > div {
        background-color: #2d2d2d;
        color: white;
    }
    .stButton > button {
        width: 100%;
        background-color: #0066FF;
        color: white !important;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        font-weight: 500;
    }
    .stButton > button:hover {
        background-color: #0052cc;
        border: none;
        color: white !important;
    }
    .stButton > button:focus {
        background-color: #0052cc;
        border: none;
        box-shadow: none;
        color: white !important;
    }
    .stButton > button:active {
        background-color: #0047b3;
        border: none;
        box-shadow: none;
        color: white !important;
    }
    /* 隐藏Streamlit默认样式 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
</style>
""", unsafe_allow_html=True)

st.title("🎯 关键字难度检查")
st.markdown("分析关键字竞争难度，助您选择最佳目标关键字")

# Input fields
with st.form("keyword_form"):
    col1, col2 = st.columns([2, 1])
    with col1:
        keyword = st.text_input("输入关键字", placeholder="例如: keyword research")
    with col2:
        country = st.selectbox("选择国家/地区", 
                          options=["us", "cn", "hk", "tw", "sg", "jp"],
                          format_func=lambda x: {
                              "us": "美国",
                              "cn": "中国",
                              "hk": "香港",
                              "tw": "台湾",
                              "sg": "新加坡",
                              "jp": "日本"
                          }.get(x, x))
    
    submit = st.form_submit_button("分析关键字难度")

if submit and keyword:
    try:
        url = "https://ahrefs-data.p.rapidapi.com/v1/keyword-difficulty-checker"
        
        querystring = {
            "country": country,
            "keyword": keyword
        }
        
        headers = {
            "x-rapidapi-key": "182fa22ea6mshdce8df5a2e82abfp1f702cjsnc2033e38a999",
            "x-rapidapi-host": "ahrefs-data.p.rapidapi.com"
        }
        
        with st.spinner("正在分析关键字难度..."):
            response = requests.get(url, headers=headers, params=querystring)
            data = response.json()
            
            if response.status_code == 200:
                st.markdown("""
                <div class="result-card">
                    <div style="display: flex; align-items: center; justify-content: center; flex-direction: column; padding: 20px;">
                        <div style="text-align: center; margin-bottom: 30px;">
                            <div style="font-size: 15px; color: #666; margin-bottom: 10px;">难度指数</div>
                            <div style="font-size: 48px; font-weight: 500; color: #0066FF;">{difficulty}%</div>
                        </div>
                        <div style="text-align: center;">
                            <div style="font-size: 15px; color: #666; margin-bottom: 10px;">难度评估</div>
                            <div style="font-size: 24px; color: #333; font-weight: 500;">{assessment}</div>
                        </div>
                    </div>
                </div>
                """.format(
                    difficulty=data.get("difficulty", "2"),
                    assessment="易于排名" if data.get("difficulty", 100) < 30 else 
                             "中等难度" if data.get("difficulty", 100) < 60 else 
                             "较难排名"
                ), unsafe_allow_html=True)
                
                # 显示详细数据
                with st.expander("查看详细数据"):
                    st.json(data)
                    
            else:
                st.error(f"API请求失败: {data.get('message', '未知错误')}")
                
    except Exception as e:
        st.error(f"发生错误: {str(e)}")
        
# 添加使用说明
with st.expander("使用说明"):
    st.markdown("""
    ### 如何使用关键字难度检查工具
    1. 在输入框中输入您想要分析的关键字
    2. 选择目标市场（国家/地区）
    3. 点击"分析关键字难度"按钮
    4. 查看分析结果，包括：
        - 难度指数：0-100的评分，越高表示竞争越激烈
        - 搜索量：每月搜索次数
        - 点击量：预计可获得的点击次数
    5. 参考难度评估来决定是否将该关键字作为SEO目标
    """)
