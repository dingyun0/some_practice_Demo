import asyncio
from langgraph.prebuilt import create_react_agent
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_openai import ChatOpenAI
from anthropic import Anthropic
from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv

load_dotenv()

async def main():
    print("开始运行...")
    server_params = StdioServerParameters(
        command='python',
        args=['./mcp_server.py']
    )
    print("服务器设置好了")

    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                print("服务器连接成功！")

                tools = await load_mcp_tools(session)
                print("工具加载成功:", tools)

                # 创建模型
                try:
                    llm = ChatAnthropic(model="claude-3-7-sonnet-latest")
                    print("模型创建成功")
                except Exception as e:
                    print("模型创建失败:", e)
                    return

                # 创建代理
                try:
                    agent = create_react_agent(model=llm, tools=tools)
                    print("AI 代理创建成功")
                except Exception as e:
                    print("代理创建失败:", e)
                    return

                # 调用代理
                try:
                    response = await agent.ainvoke({"messages": [{"role": "user", "content": "what's (3 + 5) x 12?"}]})
                    print("AI 回答:", response)
                except Exception as e:
                    print("AI 调用失败:", e)
                    return

    except Exception as e:
        print("程序出错了:", e)

if __name__ == '__main__':
    asyncio.run(main())