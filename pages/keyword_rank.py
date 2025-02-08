import streamlit as st
import requests
import pandas as pd
from datetime import datetime

def check_keyword_rank():
    st.title("关键词排名检查器")
    
    # 用户输入区域
    with st.form("rank_checker_form"):
        domain = st.text_input("请输入网站域名", placeholder="例如：ahrefs.com")
        keyword = st.text_input("请输入关键词", placeholder="例如：keyword research")
        country = st.selectbox(
            "选择国家/地区",
            ["us", "cn", "hk", "tw"],
            format_func=lambda x: {
                "us": "美国",
                "cn": "中国",
                "hk": "香港",
                "tw": "台湾"
            }.get(x, x)
        )
        
        submit_button = st.form_submit_button("检查排名")
        
    if submit_button and domain and keyword:
        # 移除 http:// 或 https:// 前缀
        domain = domain.replace("http://", "").replace("https://", "")
        
        with st.spinner("正在获取排名数据..."):
            try:
                # API请求
                url = "https://ahrefs-data.p.rapidapi.com/v1/keyword-rank-checker"
                querystring = {
                    "domain": domain,
                    "keyword": keyword,
                    "country": country
                }
                headers = {
                    "x-rapidapi-key": "182fa22ea6mshdce8df5a2e82abfp1f702cjsnc2033e38a999",
                    "x-rapidapi-host": "ahrefs-data.p.rapidapi.com"
                }
                
                response = requests.get(url, headers=headers, params=querystring)
                data = response.json()
                
                if response.status_code == 200 and data.get("status") == "success":
                    # 获取排名数据
                    serp_results = data.get("serp", {}).get("results", [])
                    top_position = data.get("topPosition", {})
                    
                    if serp_results:
                        # 查找目标域名的排名
                        target_domain = domain.lower()
                        target_rank = None
                        target_url = None
                        target_metrics = None
                        
                        # 首先检查 topPosition
                        if top_position and "content" in top_position:
                            content = top_position.get("content", [])
                            if len(content) > 1 and isinstance(content[1], dict):
                                link_data = content[1].get("link", [])
                                if len(link_data) > 1 and isinstance(link_data[1], dict):
                                    link_info = link_data[1]
                                    url_data = link_info.get("url", [])
                                    if len(url_data) > 1:
                                        url = url_data[1].get("url", "").lower()
                                        if target_domain in url:
                                            target_rank = top_position.get("pos")
                                            target_url = url
                                            target_metrics = link_info.get("metrics", {})
                        
                        # 如果在 topPosition 中没找到，遍历所有结果
                        if not target_rank:
                            for result in serp_results:
                                content = result.get("content", [])
                                if len(content) > 1 and isinstance(content[1], dict):
                                    link_data = content[1].get("link", [])
                                    if len(link_data) > 1 and isinstance(link_data[1], dict):
                                        link_info = link_data[1]
                                        url_data = link_info.get("url", [])
                                        if len(url_data) > 1:
                                            url = url_data[1].get("url", "").lower()
                                            if target_domain in url:
                                                target_rank = result.get("pos")
                                                target_url = url
                                                target_metrics = link_info.get("metrics", {})
                                                break
                        
                        if target_rank:
                            # 显示排名信息
                            st.markdown(f"""
                            <div class='result-card'>
                                <h3>排名结果</h3>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # 创建结果表格
                            rank_info = {
                                "指标": ["当前排名", "URL", "域名评分", "流量", "关键词数"],
                                "数值": [
                                    target_rank,
                                    target_url,
                                    target_metrics.get("domainRating", ""),
                                    target_metrics.get("traffic", ""),
                                    target_metrics.get("keywords", "")
                                ]
                            }
                            
                            df = pd.DataFrame(rank_info)
                            st.table(df)
                        else:
                            st.warning(f"在前 {len(serp_results)} 名搜索结果中未找到该网站")
                    else:
                        st.warning("未找到搜索结果数据")
                else:
                    st.error("获取数据失败，请稍后重试")
                    
            except Exception as e:
                st.error(f"发生错误: {str(e)}")
                
    # 添加使用说明
    with st.expander("使用说明"):
        st.markdown("""
        ### 如何使用关键词排名检查器
        1. 输入要检查的网站域名（不需要包含 http:// 或 https://）
        2. 输入要查询的关键词
        3. 选择目标国家/地区
        4. 点击"检查排名"按钮
        
        ### 结果说明
        - 当前排名：网站在该关键词下的搜索排名
        - URL：排名页面的网址
        - 域名评分：网站的域名评分
        - 流量：网站的流量
        - 关键词数：网站的关键词数
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
    check_keyword_rank()
