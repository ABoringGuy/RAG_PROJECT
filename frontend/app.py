import streamlit as st
import requests
import os

#backend_url = "http://127.0.0.1:8000"
backend_url = os.getenv(
    "BACKEND_URL",
    "http://127.0.0.1:8000"
)

st.set_page_config(page_title="Smart Document Summarizer",
                   layout="wide")

st.title("Smart Document Summarizer")

if "uploaded_hash" not in st.session_state:
    st.session_state.uploaded_hash = None

if "total_pages" not in st.session_state:
    st.session_state.total_pages = 1

uploaded_file = st.file_uploader("Upload a document",
                                 type=["pdf","docx","txt"])

current_hash= None

if uploaded_file is not None:
    current_hash = hash(uploaded_file.getvalue())
    if current_hash != st.session_state.uploaded_hash:
        with st.spinner("Processing Document"):
            files={
                "file":(uploaded_file.name,
                         uploaded_file,
                         uploaded_file.type)
            }
            response = requests.post(f"{backend_url}/upload", files=files)

        if response.status_code == 200:
            data = response.json()
            st.session_state.uploaded_hash = current_hash
            st.session_state.total_pages = data["total_pages"]
            st.success(f"Uploaded Successfully ({data['total_pages']} pages)")
            st.rerun()

        else:
            st.error("Upload Failed")
            st.stop()

if st.session_state.uploaded_hash is None:
    st.warning("Please upload a document to continue.")
    st.stop()

st.info(
    """
    "Ask Query" is optimized to answer specific topic within the document.
    "Generate Summary" is optimized to give full Document Summary
    "Page Retrieval" helps give more precise answer for specified Pages.
    """
)

st.divider()

st.subheader("Generate Summary")

if st.button("Generate Summary", use_container_width=True):
    with st.spinner("Generating Summary"):
        response = requests.post(f"{backend_url}/summary")

    if response.status_code == 200:
        summary = response.json()["answer"]
        st.success("Summary Generated")
        st.write(summary)

    else:
        st.error("Failed to generate summary.")

st.divider()

st.subheader("Ask Query related to Document:")

query = st.text_area("Enter Query",
                     key="query_box")



if st.button("Ask Query", use_container_width=True):
    if query.strip() == "":
        st.warning("Please enter a question")

    else:
        with st.spinner("Generating Answer"):
            response = requests.post(f"{backend_url}/query",
                                     json={"query": query})

        if response.status_code == 200:
            answer = response.json()["answer"]
            st.success("Answer Generated")
            st.write(answer)
        else:
            st.error("Query failed.")

# st.subheader("Page Retrieval")
# start_page = st.number_input(
#     "Start Page",
#     min_value=1,
#     max_value=st.session_state.total_pages,
#     value=1
# )
#
# use_end = st.checkbox(
#     "Specify End Page"
# )
#
# if use_end:
#     end_page = st.number_input(
#         "End Page",
#         min_value=start_page,
#         max_value=st.session_state.total_pages,
#         value=start_page
#     )
# else:
#     end_page = start_page
#

page_numbers = list(range(1, st.session_state.total_pages + 1))
st.subheader("Page Retrieval")
start_page = st.selectbox(
    "Start Page",
    options=page_numbers
)

use_end = st.checkbox(
    "Specify End Page"
)

if use_end:
    end_page = st.selectbox(
        "End Page",
        options=range(start_page, st.session_state.total_pages + 1)
    )
else:
    end_page = start_page

page_query= st.text_area("Question",
                         key= "page_query_box")


if st.button("Retrieve Pages", use_container_width=True):
    if page_query.strip() == "":
        st.warning("Please enter a question")

    else:
        with st.spinner("Generating Answer"):
            response = requests.post(
                f"{backend_url}/page",
                json={
                    "start_page": start_page,
                    "end_page": end_page,
                    "query": page_query
                }
            )

        if response.status_code == 200:
            answer = response.json()["answer"]
            st.success("Answer Generated")
            st.write(answer)

        else:
            st.error("Query failed.")