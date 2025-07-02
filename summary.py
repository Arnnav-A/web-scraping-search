from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from config import LLM_MODEL_NAME

# Prompt template for summarization
summary_prompt = PromptTemplate(
    input_variables=["content"],
    template=(
        "You are a helpful assistant. A user had a query: {query}\n"
        "Using the following content, respond to the user's query with a concise summary.\n"
        "\n\n{content}\n\nSummary:"
    ),
)

# LLM instance for summarization
llm = ChatGroq(model=LLM_MODEL_NAME)

# Chain pipeline: prompt -> llm -> output parser
summarization_chain = summary_prompt | llm | StrOutputParser()


def summarize_scraped_texts(texts: list[str], query: str) -> str:

    trimmed = [t[:2000] for t in texts if t]
    combined = "\n\n".join(trimmed)

    if not combined.strip():
        return "No valid text to summarize."

    # Run LLM summarization
    summary = summarization_chain.invoke({"content": combined, "query": query})
    return summary
