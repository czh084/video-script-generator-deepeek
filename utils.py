from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.utilities import WikipediaAPIWrapper
import os
import wikipedia
import warnings
# 1. 修复wikipedia解析器警告
wikipedia.set_lang("zh")
wikipedia.requests_timeout = 10  # 设置超时时间

# 2. 抑制BeautifulSoup警告
warnings.filterwarnings("ignore", category=UserWarning, module="wikipedia")

def generate_script(subject,video_length,creativity,api_key):
    # 1. 标题生成模板
    title_template =ChatPromptTemplate.from_messages(
        [
            ("human", "请为'{subject}'这个主题的视频想一个吸引人的标题")
        ]
    )
    # 2. 脚本生成模板
    script_template = ChatPromptTemplate.from_messages(
        [
            ("human",
             """
             你是一位短视频频道的博主。根据以下标题和相关信息，为短视频频道写一个视频脚本。
             视频标题：{title},视频时长：{duration}分钟，生成的脚本的长度尽量遵循视频时长的要求。
             要求开头抓住限球，中间提供干货内容，结尾有惊喜，脚本格式也请按照【开头、中间，结尾】分隔。
             整体内容的表达方式要尽量轻松有趣，吸引年轻人。
             脚本内容可以结合以下维基百科搜索出的信息，但仅作为参考，只结合相关的即可，对不相关的进行忽略：
             '''{wikipedia_search}'''
             """)
        ]
    )
    # 3. 配置DeepSeek模型
    model = ChatOpenAI(
        openai_api_key=api_key,
        openai_api_base="https://api.deepseek.com",  # DeepSeek专用API端点
        model_name="deepseek-chat",  # 或使用"deepseek-reasoner"（推理专用模型）
        temperature=creativity
    )
    # model = ChatOpenAI(openai_api_key=api_key,temperature=creativity)
    # 4. 创建处理链
    title_chain = title_template | model

    script_chain = script_template | model
    # 5. 生成标题
    title = title_chain.invoke({"subject":subject}).content
    # 6. 获取维基百科信息
    # search = WikipediaAPIWrapper(lang="zh")
    # search_result = search.run(subject)
    # 获取维基百科信息（使用优化后的查询）
    try:
        search = WikipediaAPIWrapper(lang="zh")
        search_result = search.run(subject)
    except Exception as e:
        print(f"维基百科查询错误: {e}")
        search_result = "未找到相关信息"
    # 7. 生成脚本
    script = script_chain.invoke({"title":title, "duration": video_length,
                                  "wikipedia_search":search_result}).content

    return search_result,title, script
# 使用示例
# print(generate_script("sora",1,0.7,os.getenv("DeepSeek API Key")))