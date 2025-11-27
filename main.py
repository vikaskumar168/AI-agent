from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_agent, AgentExecutor

# Load environment variables from .env file
load_dotenv()  

llm = ChatOpenAI(model="gpt-4o-mini")
llm2 = ChatAnthropic(model="claude-3-5-sonnet-20241022")
#add gemini also 

class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]

response = llm.invoke("What is the meaning of life?")

parser = ChatPromptTemplate(pydantic_object=ResearchResponse)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            you are a research assistant that will help generate a research paper.
            answer the user query and use neccesary tools.
            Wrap the output in this format and provide no other text\n{format_instructions}
            """,
        ),
        (
            "placeholder", "{chat_history}"
        ),
        ("human","{query}"),
        ("placeholder","{agent_scratchpad}"),
    ]
).partial(format_instructions=parser.get_format_instructions())


agent = create_tool_agent(
    llm=llm,
    prompt=prompt,
    tools=[]
)


agent_executor = AgentExecutor(agent=agent,tools=[],verbose=True)
raw_response = agent_executor.invoke({"query":"What is the capital of France?"})


print("Response from OpenAI:", raw_response)