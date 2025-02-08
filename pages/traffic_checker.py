import streamlit as st
import requests
import pandas as pd
from datetime import datetime

def check_website_traffic():
    st.title("网站流量检查器")
    
    # 用户输入区域
    with st.form("traffic_checker_form"):
        url = st.text_input("请输入网站域名", placeholder="例如：ahrefs.com")
        
        # 模式选择
        modes = st.multiselect(
            "选择检查模式",
            ["subdomains", "exact"],
            default=["subdomains", "exact"],
            format_func=lambda x: {
                "subdomains": "包含子域名",
                "exact": "精确匹配"
            }.get(x, x)
        )
        
        submit_button = st.form_submit_button("检查流量")
        
    if submit_button and url:
        # 移除 http:// 或 https:// 前缀
        url = url.replace("http://", "").replace("https://", "")
        
        with st.spinner("正在获取流量数据..."):
            try:
                # API请求
                api_url = "https://ahrefs-data.p.rapidapi.com/v1/website-traffic-checker"
                querystring = {
                    "mode": ",".join(modes),
                    "url": url
                }
                headers = {
                    "x-rapidapi-key": "182fa22ea6mshdce8df5a2e82abfp1f702cjsnc2033e38a999",
                    "x-rapidapi-host": "ahrefs-data.p.rapidapi.com"
                }
                
                response = requests.get(api_url, headers=headers, params=querystring)
                data = response.json()
                
                if response.status_code == 200 and data.get("status") == "success":
                    # 获取流量数据
                    traffic_data = data.get("traffic", {})
                    traffic_history = data.get("traffic_history", [])
                    top_pages = data.get("top_pages", [])
                    top_countries = data.get("top_countries", [])
                    
                    if traffic_data:
                        # 显示月均访问量
                        st.metric(
                            "月均访问量",
                            f"{traffic_data.get('trafficMonthlyAvg', 0):,}"
                        )
                        
                        # 显示流量历史
                        if traffic_history:
                            st.markdown("""
                            <div class='result-card'>
                                <h3>流量历史</h3>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            history_df = pd.DataFrame(traffic_history)
                            history_df['date'] = pd.to_datetime(history_df['date']).dt.strftime('%Y-%m')
                            st.line_chart(history_df.set_index('date')['organic'])
                        
                        # 显示热门页面
                        if top_pages:
                            st.markdown("""
                            <div class='result-card'>
                                <h3>热门页面</h3>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            pages_df = pd.DataFrame(top_pages)
                            pages_df = pages_df[['url', 'traffic']].rename(columns={
                                'url': '页面',
                                'traffic': '访问量'
                            })
                            st.dataframe(pages_df, use_container_width=True)
                        
                        # 显示主要国家/地区
                        if top_countries:
                            st.markdown("""
                            <div class='result-card'>
                                <h3>主要国家/地区</h3>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            countries_df = pd.DataFrame(top_countries)
                            countries_df['share'] = countries_df['share'].round(2)
                            countries_df['country'] = countries_df['country'].map({
                                'us': '美国',
                                'gb': '英国',
                                'ca': '加拿大',
                                'au': '澳大利亚',
                                'in': '印度'
                            }).fillna(countries_df['country'])
                            countries_df = countries_df.rename(columns={
                                'country': '国家',
                                'share': '占比(%)'
                            })
                            st.dataframe(countries_df, use_container_width=True)
                    else:
                        st.warning("未找到该网站的流量数据")
                else:
                    st.error("获取数据失败，请稍后重试")
                    
            except Exception as e:
                st.error(f"发生错误: {str(e)}")
                
    # 添加使用说明
    with st.expander("使用说明"):
        st.markdown("""
        ### 如何使用网站流量检查器
        1. 输入要检查的网站域名（不需要包含 http:// 或 https://）
        2. 选择检查模式：
           - 包含子域名：检查包括子域名在内的所有流量
           - 精确匹配：只检查主域名的流量
        3. 点击"检查流量"按钮
        
        ### 数据说明
        - 月均访问量：每月的预估访问量
        - 流量历史：网站过去12个月的流量趋势
        - 热门页面：网站最受欢迎的页面
        - 主要国家/地区：网站流量来源的主要国家/地区
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

.stMetric {
    background-color: #1e1e1e;
    padding: 1rem;
    border-radius: 0.5rem;
}

.stMetric label {
    color: #ffffff !important;
}

.stMetric .metric-value {
    font-size: 1.5rem !important;
    font-weight: bold !important;
}
</style>
""", unsafe_allow_html=True)

# 运行主函数
if __name__ == "__main__":
    check_website_traffic()
