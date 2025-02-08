import streamlit as st
import requests
import pandas as pd

def check_website_authority():
    st.title("网站权限检查器")
    
    # 用户输入区域
    with st.form("authority_checker_form"):
        url = st.text_input("请输入网站域名", placeholder="例如：ahrefs.com")
        submit_button = st.form_submit_button("检查权限")
        
    if submit_button and url:
        # 移除 http:// 或 https:// 前缀
        url = url.replace("http://", "").replace("https://", "")
        
        with st.spinner("正在获取网站权限数据..."):
            try:
                # API请求
                api_url = "https://ahrefs-data.p.rapidapi.com/v1/website-authority-checker"
                querystring = {"url": url}
                headers = {
                    "x-rapidapi-key": "182fa22ea6mshdce8df5a2e82abfp1f702cjsnc2033e38a999",
                    "x-rapidapi-host": "ahrefs-data.p.rapidapi.com"
                }
                
                response = requests.get(api_url, headers=headers, params=querystring)
                data = response.json()
                
                if response.status_code == 200 and data.get("status") == "success":
                    overview = data.get("overview", {})
                    
                    if overview:
                        # 创建三列布局显示主要指标
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.metric(
                                "域名评分",
                                overview.get("domainRating", 0)
                            )
                            
                        with col2:
                            st.metric(
                                "URL评分",
                                overview.get("urlRating", 0)
                            )
                            
                        with col3:
                            st.metric(
                                "反向链接数",
                                f"{overview.get('backlinks', 0):,}"
                            )
                        
                        # 创建详细信息表格
                        st.markdown("""
                        <div class='result-card'>
                            <h3>详细数据</h3>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        details = {
                            "指标": [
                                "引用域名数",
                                "DoFollow反向链接",
                                "DoFollow引用域名"
                            ],
                            "数值": [
                                f"{overview.get('refdomains', 0):,}",
                                f"{overview.get('dofollowBacklinks', 0):,}",
                                f"{overview.get('dofollowRefdomains', 0):,}"
                            ]
                        }
                        
                        df = pd.DataFrame(details)
                        st.table(df)
                    else:
                        st.warning("未找到网站权限数据")
                else:
                    st.error("获取数据失败，请稍后重试")
                    
            except Exception as e:
                st.error(f"发生错误: {str(e)}")
                
    # 添加使用说明
    with st.expander("使用说明"):
        st.markdown("""
        ### 如何使用网站权限检查器
        1. 输入要检查的网站域名（不需要包含 http:// 或 https://）
        2. 点击"检查权限"按钮
        
        ### 数据说明
        - 域名评分：网站的整体权威度评分（0-100）
        - URL评分：特定页面的权威度评分（0-100）
        - 反向链接数：指向该网站的外部链接总数
        - 引用域名数：链接到该网站的唯一域名数量
        - DoFollow反向链接：具有传递权重的反向链接数量
        - DoFollow引用域名：具有传递权重链接的域名数量
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
    check_website_authority()
