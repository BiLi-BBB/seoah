import streamlit as st

# Set page config
st.set_page_config(
    page_title="SEO工具箱",
    page_icon="🔍",
    layout="wide"
)

# Custom CSS for dark theme and improved card styling
st.markdown("""
<style>
    /* Dark theme */
    .stApp {
        background-color: #1a1a1a;
        color: white;
    }
    
    .card {
        padding: 1rem;
        border-radius: 8px;
        background: #1E1E1E;
        margin-bottom: 1rem;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border: 1px solid #333;
    }
    
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        background: #2A2A2A;
    }
    
    .card h3 {
        margin: 0;
        color: #FFFFFF;
        font-size: 1.2rem;
    }
    
    .card p {
        margin: 0.5rem 0 0 0;
        color: #CCCCCC;
        font-size: 0.9rem;
    }
    
    /* Remove default Streamlit padding */
    .block-container {
        padding-top: 2rem !important;
    }
    
    /* Title styling */
    h1 {
        font-size: 2.5rem !important;
        font-weight: 600 !important;
        margin-bottom: 2rem !important;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.title("🔍 SEO工具箱")

# Function to create feature cards
def create_feature_card(title, description, feature, icon):
    st.markdown(f"""
    <div class="card" onclick="window.location.href='{feature}'" style="cursor: pointer;">
        <a href="{feature}" style="text-decoration: none; color: inherit;">
            <h3>{icon} {title}</h3>
            <p>{description}</p>
        </a>
    </div>
    """, unsafe_allow_html=True)

# First row
col1, col2 = st.columns(2)

with col1:
    create_feature_card(
        "关键词生成器",
        "生成相关的关键词建议",
        "keyword_generator",
        "🔍"
    )
        
    create_feature_card(
        "关键词排名检查器",
        "检查关键词的搜索排名",
        "keyword_rank",
        "📊"
    )
        
    create_feature_card(
        "反向链接检查器",
        "分析网站的反向链接",
        "backlink_checker",
        "🔗"
    )
    
with col2:
    create_feature_card(
        "关键字难度检查",
        "分析关键字竞争难度，助您选择最佳目标关键字",
        "keyword_difficulty",
        "🎯"
    )
        
    create_feature_card(
        "网站权限检查器",
        "检查网站的权威度",
        "authority_checker",
        "🏆"
    )
        
    create_feature_card(
        "流量检查器",
        "分析网站流量数据",
        "traffic_checker",
        "📈"
    )
