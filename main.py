import streamlit as st
from utils import generate_script

st.title("hp-视频脚本生成器")
with st.sidebar:
    DeepSeek_API_Key = st.text_input("请输入DeepSeek API密钥：",type="password")
    st.markdown("[获取DeepSeek API密钥](https://platform.deepseek.com/api_keys)")

subject = st.text_input("请输入视频主题")
video_length = st.number_input("请输入视频大致时长（单位：分钟）",min_value=0.1,step=0.1)
creativity = st.slider("请输入视频脚本的创造力（数字越小说明更严谨，数字大说明更多样）",min_value=0.0,
                       max_value=1.0,value=0.2,step=0.1)
submit = st.button("生成脚本")

# 新增API密钥格式验证
def is_valid_deepseek_key(api_key):
    """验证DeepSeek API密钥格式"""
    # DeepSeek API密钥通常以"sk-"开头，长度为35个字符
    return api_key.startswith("sk-") and len(api_key) == 35
if submit:
    # 检查API密钥是否存在且格式正确
    if not DeepSeek_API_Key:
        st.error("❌ 请输入你的DeepSeek API密钥")
        st.stop()
    elif not is_valid_deepseek_key(DeepSeek_API_Key.strip()):
        st.error("❌ 无效的API密钥格式！请确保输入的是DeepSeek API密钥（以'sk-'开头，共35个字符）")
        st.stop()


if submit and not subject:
    st.info("❌ 请输入视频的主题")
    st.stop()

if submit and not video_length >=0.1:
    st.info("❌ 视频时长需要大于或等于0.1")
    st.stop()

if submit:
    with st.spinner(("AI正在思考中，请稍后...")):
        search_result,title,script = generate_script(subject,video_length,creativity,DeepSeek_API_Key)
    st.success("视频脚本已生成！")
    st.subheader("标题")
    st.write(title)
    st.subheader("视频脚本")
    st.write(script)
    with st.expander("维基百科搜索结果"):
        st.info(search_result)

