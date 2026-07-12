import re
from collections import defaultdict
from embedding.constants import IGNORE_SECTIONS, IMPORTANT_SECTIONS, IMPORTANT_SECTION_MULTIPLIER

def get_representative_chunks(documents, section_index, max_summary_chunks= 25, MAX_PER_SECTION=2):
    if not documents:
        return []

    max_chunk_size = max((len(doc.page_content) for doc in documents), default=1)

    if max_chunk_size==0:
        max_chunk_size=1

    total_chunks = len(documents)
    chunk_to_section={}
    scored_chunks = []

    for section_id, chunk_indices in section_index.items():
        for chunk_idx in chunk_indices:
            chunk_to_section[chunk_idx]=section_id

    for idx, doc in enumerate(documents):
        heading = doc.metadata["heading"]

        if skip_section(heading):
            print(f"""============================================================
    Skipping section: {heading}
    ============================================================""")
            continue

        size_score = len(doc.page_content) / max_chunk_size

        if total_chunks == 1:
            position = 0.5
        else:
            position = idx / (total_chunks - 1)

        score = size_score * position_multiplier(position)

        if important_section(heading):
            score *= IMPORTANT_SECTION_MULTIPLIER
        scored_chunks.append((score, idx))

    scored_chunks.sort(reverse=True)
    selected = []
    seen = set()

    while len(selected)< max_summary_chunks:
        section_counts = defaultdict(int)
        added_this_pass= False

        for score, idx in scored_chunks:
            if idx in seen:
                continue

            if len(selected) >= max_summary_chunks:
                break

            section= chunk_to_section[idx]

            if section_counts[section] >= MAX_PER_SECTION:
                continue
            selected.append(documents[idx])
            seen.add(idx)
            section_counts[section] +=1
            added_this_pass= True

        if not added_this_pass:
            break
    selected.sort(key=lambda doc: doc.metadata["chunk_id"])
    return selected

def retrieve_documents(scores, indices, documents, section_index,chunk_position, max_selection_size=8, neighbour_radius=2,relative_threshold=0.85):
    expanded= []
    seen= set()
    best_score= scores[0][0]

    for score, idx in zip(scores[0], indices[0]):
        if idx==-1:
            continue

        section_id=documents[idx].metadata["section_id"]
        section_chunks= section_index[section_id]
        relative_score= score/best_score

        if relative_score>=relative_threshold:
            if idx not in seen:
                expanded.append(documents[idx])
                seen.add(idx)
            continue

        if len(section_chunks)<=max_selection_size:
            for chunk_idx in section_chunks:
                if chunk_idx not in seen:
                    expanded.append(documents[chunk_idx])
                    seen.add(chunk_idx)
            continue

        neighbour_chunks=get_neighbour(idx, section_chunks, chunk_position,radius=neighbour_radius)

        for chunk_idx in neighbour_chunks:
            if chunk_idx not in seen:
                expanded.append(documents[chunk_idx])
                seen.add(chunk_idx)

    expanded.sort(key=lambda doc: doc.metadata["chunk_id"])
    return expanded

def get_neighbour(idx, section_chunks,chunk_position, radius=2):
    pos= chunk_position[idx]
    start=max(0, pos-radius)
    end= min(len(section_chunks), pos+radius+1)
    return section_chunks[start:end]

def reduce_page_chunks(candidate_chunks,  start, end, max_chunks=15, max_per_section=3,):
    if len(candidate_chunks)<=max_chunks:
        return candidate_chunks

    max_chunk_size= max(len(doc.page_content) for doc in candidate_chunks)

    scored_chunks=[]

    for doc in candidate_chunks:
        score= len(doc.page_content) / max_chunk_size
        if start <= doc.metadata["page"] <= end:
            score *= 1.2
        scored_chunks.append((score, doc))

    scored_chunks.sort(key=lambda x:x[0], reverse=True)

    section_counts= defaultdict(int)
    selected=[]

    for score, doc in scored_chunks:
        section = doc.metadata["section_id"]

        if section_counts[section]>=max_per_section:
            continue

        selected.append(doc)
        section_counts[section]+=1

        if len(selected)>=max_chunks:
            break
    selected.sort(key=lambda doc: doc.metadata["chunk_id"])
    return selected

def retrieve_page_chunks(start_page, end_page, page_index, documents, neighbour_radius=1, max_chunks=15):
    start= max(1, start_page-neighbour_radius)
    end= min(max(page_index.keys()), end_page+neighbour_radius)

    candidate_chunks =[]

    for page in range(start, end+1):
        indices = page_index.get(page, [])

        for idx in indices:
            candidate_chunks.append(documents[idx])

    candidate_chunks.sort(key=lambda doc: doc.metadata["chunk_id"])
    return reduce_page_chunks(candidate_chunks, start_page, end_page, max_chunks=max_chunks)

def position_multiplier(position):
    distance_from_center= abs(position - 0.5)*2
    return 1.0+0.3 * distance_from_center

def skip_section(heading):
    heading= heading.lower().strip()
    heading = re.sub(r"[^a-z0-9 ]", "", heading)
    heading = re.sub(r"\s+", " ", heading)
    return heading in IGNORE_SECTIONS

def important_section(heading):
    heading = heading.lower().strip()
    """Here any() makes 1) INTRODUCTION or CHAPTER 1: INTRODUCTION both valid"""
    return any(keyword in heading for keyword in IMPORTANT_SECTIONS)