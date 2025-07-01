from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from config import LLM_MODEL_NAME

# Prompt template for validation
prompt_template = (
    "You are a search engine query validator. Decide whether this user query is a valid search engine query.\n"
    "Queries are valid if they only seek information which can be provided by a search engine.\n"
    "Respond with 'Yes' or 'No' only.\n\nQuery: {query}"
)
prompt = PromptTemplate(input_variables=["query"], template=prompt_template)

# LLM instance for validation
llm = ChatGroq(model=LLM_MODEL_NAME)

# Chain pipeline: prompt -> llm -> output parser
chain = prompt | llm | StrOutputParser()

def is_valid_query(query: str) -> bool:
    result = chain.invoke({"query": query})
    return "yes" in result.lower()
