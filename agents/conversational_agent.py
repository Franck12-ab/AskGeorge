import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate
from langchain_core.prompts.base import format_document
from langchain_core.runnables import RunnableMap, RunnableLambda

class ConversationalAgent:
    def __init__(self, persist_path="chroma_index", model=os.getenv("GEMINI_MODEL", "gemini-1.5-flash")):
        # LLM setup
        self.llm = ChatGoogleGenerativeAI(
            model=model,
            temperature=0.2
        )

        # Embeddings + Vector Store
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.vectorstore = Chroma(persist_directory=persist_path, embedding_function=self.embeddings)
        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 6})

        # Memory
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

        # Prompt
        self.doc_prompt = PromptTemplate.from_template("📜 {source_file} (Chunk {chunk_id})\n{page_content}")
        self.chat_prompt = ChatPromptTemplate.from_messages([
                ("system", "You are AskGeorge, a helpful and conversational assistant for George Brown College students. Use the information below to answer questions naturally. You may say things like 'From what I know' or 'Based on available information' to make it sound natural and not robotic. Dont Say based on provided information or text or document. Cite filenames if possible."),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{question}"),
                ("system", "Context:\n{context}")
            ])

        # Chain assembly
        self.chain = (
            RunnableMap({
                "context": RunnableLambda(self._retrieve_context),
                "chat_history": RunnableLambda(lambda _: self._get_recent_memory(3)),
                "question": lambda x: x["question"]
            })
            | self.chat_prompt
            | self.llm
        )

    def _get_recent_memory(self, n=3):
        messages = self.memory.chat_memory.messages
        return messages[-n*2:] if len(messages) > n*2 else messages

    def _format_docs(self, docs):
        context = []
        for doc in docs:
            chunk = format_document(doc, self.doc_prompt)
            context.append(chunk)
        return "\n\n".join(context)

    def _retrieve_context(self, inputs: dict) -> str:
        question = inputs["question"]
        docs = self.retriever.invoke(question)
        self._latest_docs = docs  # Save for external reference
        return self._format_docs(docs)

    def run(self, question: str) -> dict:
        response = self.chain.invoke({"question": question})
        self.memory.save_context({"input": question}, {"output": response.content})

        return {
            "answer": response.content.strip(),
            "sources": getattr(self, "_latest_docs", []),
            "chat_history": self.memory.chat_memory.messages
        }
