def build_prompt(mode, context, query, start_page=None, end_page=None):
    if mode == "query":
        prompt = f"""
        You are an AI assistant answering questions about a document.

        Instructions:
        - Answer using ONLY the provided context.
        - Do not invent or assume facts.
        - Be concise but complete.
        - If multiple parts of the context are relevant, combine them into one coherent answer.

        Context:
        {context}

        Question:
        {query}

        Answer:
        """

    elif mode == "summary":
        prompt = f"""
        You are an expert technical document summarizer.

Your task is to produce a concise, accurate summary using ONLY the provided context.

Requirements:
- Output ONLY the final summary.
- Do NOT explain your reasoning.
- Do NOT repeat information.
- Do not reproduce or explain mathematical equations unless they are essential to understanding the document's main contribution.
Context:
{context}
        """
    elif mode== "page":
        prompt = f"""
        You are an AI assistant answering questions about specific pages of a document.

        Instructions:
        - The requested pages are the primary source of information.
        - Neighboring pages are included only to provide additional context when necessary.
        - Prioritize information from the requested page range.
        - Do not introduce information outside the provided context.
        - If the requested pages do not contain the answer, clearly state that.
        - The user is always asking content from page: {start_page} to {end_page} regardless of what query says. 
        - If start and end page are equal then user only wants content from one specific page.

        Context:
        {context}

        Question:
        {query}

        Answer:
        """
    return prompt
