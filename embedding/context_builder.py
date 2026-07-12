def build_context(retrieved_docs, include_pages=False):
    context = []
    current_page = None

    for doc in retrieved_docs:
        page = doc.metadata["page"]

        if include_pages and page != current_page:
            context.append(f"Page: {page}")
            current_page = page

        context.append(doc.page_content)

    return "\n\n".join(context)