import streamlit as st
import requests
import pandas as pd

def check_backlinks():
    st.title("反向链接检查器")
    
    # 用户输入区域
    with st.form("backlink_checker_form"):
        url = st.text_input("请输入网站域名", placeholder="例如：ahrefs.com")
        mode = st.selectbox(
            "选择检查模式",
            ["exact", "subdomains", "subdomains,exact"],
            format_func=lambda x: {
                "exact": "精确匹配",
                "subdomains": "包含子域名",
                "subdomains,exact": "精确匹配和子域名"
            }.get(x, x)
        )
        submit_button = st.form_submit_button("检查反向链接")
        
    if submit_button and url:
        # 移除 http:// 或 https:// 前缀
        url = url.replace("http://", "").replace("https://", "")
        
        with st.spinner("正在获取反向链接数据..."):
            try:
                # API请求
                api_url = "https://ahrefs-data.p.rapidapi.com/v1/backlink-checker"
                querystring = {
                    "url": url,
                    "mode": mode
                }
                headers = {
                    "x-rapidapi-key": "182fa22ea6mshdce8df5a2e82abfp1f702cjsnc2033e38a999",
                    "x-rapidapi-host": "ahrefs-data.p.rapidapi.com"
                }
                
                response = requests.get(api_url, headers=headers, params=querystring)
                data = response.json()
                
                if response.status_code == 200 and data.get("status") == "success":
                    overview = data.get("overview", {})
                    backlinks = data.get("topBacklinks", {}).get("backlinks", [])
                    
                    if overview:
                        # 创建三列布局显示主要指标
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.metric(
                                "反向链接数",
                                f"{overview.get('backlinks', 0):,}"
                            )
                            
                        with col2:
                            st.metric(
                                "引用域名数",
                                f"{overview.get('refdomains', 0):,}"
                            )
                            
                        with col3:
                            st.metric(
                                "域名评分",
                                overview.get("domainRating", 0)
                            )
                        
                        # 显示反向链接列表
                        if backlinks:
                            st.markdown("""
                            <div class='result-card'>
                                <h3>热门反向链接</h3>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # 处理反向链接数据
                            backlinks_data = []
                            for link in backlinks:
                                backlinks_data.append({
                                    "锚文本": link.get("anchor", ""),
                                    "来源网址": link.get("urlFrom", ""),
                                    "目标网址": link.get("urlTo", ""),
                                    "域名评分": link.get("domainRating", ""),
                                    "标题": link.get("title", "")
                                })
                            
                            df = pd.DataFrame(backlinks_data)
                            st.dataframe(df, use_container_width=True)
                    else:
                        st.warning("未找到反向链接数据")
                else:
                    st.error("获取数据失败，请稍后重试")
                    
            except Exception as e:
                st.error(f"发生错误: {str(e)}")
                
    # 添加使用说明
    with st.expander("使用说明"):
        st.markdown("""
        ### 如何使用反向链接检查器
        1. 输入要检查的网站域名（不需要包含 http:// 或 https://）
        2. 选择检查模式：
           - 精确匹配：只检查输入的确切域名
           - 包含子域名：包括所有子域名
           - 精确匹配和子域名：同时检查两种模式
        3. 点击"检查反向链接"按钮
        
        ### 数据说明
        - 反向链接数：指向该网站的外部链接总数
        - 引用域名数：链接到该网站的唯一域名数量
        - 域名评分：网站的整体权威度评分（0-100）
        - 热门反向链接：按域名评分排序的重要反向链接列表
        """)

# 添加页面样式
st.markdown("""
<style>
.result-card {
    padding: 1rem;
    border-radius: 0.5rem;
    background-color: #1e1e1e;
    margin: 1rem 0;
}

.result-card h3 {
    margin: 0;
    color: #ffffff;
}
</style>
""", unsafe_allow_html=True)

# 运行主函数
if __name__ == "__main__":
    check_backlinks()
