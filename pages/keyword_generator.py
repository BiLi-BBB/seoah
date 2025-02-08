import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Google关键字生成", page_icon="🔤")

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
    /* 表格样式 */
    .dataframe {
        width: 100%;
        background-color: white;
        border-radius: 10px;
    }
    .dataframe th {
        background-color: #f8f9fa;
        padding: 12px !important;
        font-size: 14px;
        color: #333;
    }
    .dataframe td {
        padding: 12px !important;
        font-size: 14px;
        color: #666;
    }
    /* 隐藏Streamlit默认样式 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
</style>
""", unsafe_allow_html=True)

st.title("🔤 Google关键字生成")
st.markdown("智能生成相关关键字，扩展您的SEO策略")

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
    
    submit = st.form_submit_button("生成关键字")

if submit and keyword:
    try:
        url = "https://ahrefs-data.p.rapidapi.com/v1/keyword-generator/google"
        
        querystring = {
            "country": country,
            "keyword": keyword
        }
        
        headers = {
            "x-rapidapi-key": "182fa22ea6mshdce8df5a2e82abfp1f702cjsnc2033e38a999",
            "x-rapidapi-host": "ahrefs-data.p.rapidapi.com"
        }
        
        with st.spinner("正在生成相关关键字..."):
            response = requests.get(url, headers=headers, params=querystring)
            data = response.json()
            
            if response.status_code == 200 and data.get("status") == "success":
                # 获取关键字数据
                keywords_data = data.get("allIdeas", {}).get("results", [])
                
                if keywords_data:
                    # 创建DataFrame
                    df = pd.DataFrame(keywords_data)
                    
                    # 转换搜索量标签
                    volume_map = {
                        'MoreThanOneHundred': '大于100',
                        'MoreThanOneThousand': '大于1千',
                        'MoreThanTenThousand': '大于1万',
                        'MoreThanOneHundredThousand': '大于10万',
                        'LessThanOneHundred': '小于100',
                        'LessThanOneThousand': '小于1千',
                        'LessThanTenThousand': '小于1万',
                        'LessThanOneHundredThousand': '小于10万',
                        'BetweenOneAndTen': '1-10',
                        'BetweenTenAndHundred': '10-100',
                        'BetweenHundredAndThousand': '100-1千',
                        'BetweenThousandAndTenThousand': '1千-1万',
                        'BetweenTenThousandAndHundredThousand': '1万-10万'
                    }
                    
                    # 先创建搜索量的中文映射
                    df['搜索量'] = df['volumeLabel'].map(volume_map).fillna(df['volumeLabel'])
                    
                    # 选择并重命名列
                    df = df[['keyword', 'difficultyLabel', '搜索量', 'updatedAt']]
                    df = df.rename(columns={
                        'keyword': '关键字',
                        'difficultyLabel': '难度',
                        'updatedAt': '更新时间'
                    })
                    
                    # 转换难度标签
                    difficulty_map = {
                        'Hard': '困难',
                        'Medium': '中等',
                        'Easy': '简单'
                    }
                    df['难度'] = df['难度'].map(difficulty_map).fillna(df['难度'])
                    
                    # 显示结果数量
                    st.markdown(f"""
                    <div class='result-card'>
                        <h3 style='margin:0; color:#333;'>找到 {len(keywords_data)} 个相关关键字</h3>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # 显示关键字表格
                    st.dataframe(
                        df,
                        use_container_width=True,
                        column_config={
                            "关键字": st.column_config.TextColumn("关键字", width="medium"),
                            "难度": st.column_config.TextColumn("难度", width="small"),
                            "搜索量": st.column_config.TextColumn("搜索量", width="small"),
                            "更新时间": st.column_config.DatetimeColumn("更新时间", format="YYYY-MM-DD")
                        }
                    )
                    
                    # 添加下载按钮
                    csv = df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        "下载关键字列表",
                        csv,
                        f"google_keywords_{keyword}.csv",
                        "text/csv",
                        key='download-csv'
                    )
                else:
                    st.info("未找到相关关键字")
            else:
                st.error(f"API请求失败: {data.get('message', '未知错误')}")
                
    except Exception as e:
        st.error(f"发生错误: {str(e)}")

# 添加使用说明
with st.expander("使用说明"):
    st.markdown("""
    ### 如何使用Google关键字生成工具
    1. 在输入框中输入您的目标关键字
    2. 选择目标市场（国家/地区）
    3. 点击"生成关键字"按钮
    4. 查看生成的关键字列表，包括：
        - 关键字
        - 搜索量
        - 难度指数
        - CPC（每次点击成本）
    5. 可以下载关键字列表用于后续分析
    """)
