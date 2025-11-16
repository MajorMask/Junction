from pymilvus import MilvusClient
from langchain_huggingface import HuggingFaceEmbeddings
from tqdm import tqdm
import json
from anthropic import Anthropic

# --- Milvus setup ---
milvus_client = MilvusClient(
    uri="my_uri",
    token="my_token"
)

collection_name = "my_rag_collection"
embedding_dim = 384

# --- Improved Flattening function ---
def flatten_product(product):
    parts = []
    for key in ['salesUnitGtin', 'salesUnit', 'baseUnit', 'category', 'vendorName', 'countryOfOrigin', 'brand']:
        if key in product:
            parts.append(f"{key}:{product[key]}")
    for key in ['allowedLotSize', 'temperatureCondition']:
        if key in product:
            parts.append(f"{key}:{product[key]}")
    if 'units' in product and isinstance(product['units'], list):
        for unit in product['units']:
            parts.append(f"unit:{unit.get('unitId','')} size:{unit.get('sizeInBaseUnits','')}")
    synkka = product.get('synkkaData', {})
    for key in ['names', 'marketingTexts', 'keyIngredients', 'storageInstructions']:
        if key in synkka and isinstance(synkka[key], list):
            for item in synkka[key]:
                parts.append(item.get('value', ''))
    if 'nutritionalContent' in synkka and isinstance(synkka['nutritionalContent'], list):
        nut_parts = []
        for nut in synkka['nutritionalContent']:
            nut_parts.append(f"{nut.get('id','')}: {nut.get('value','')} {nut.get('unit','')}")
        if nut_parts:
            parts.append("Nutrition: " + ", ".join(nut_parts))
    if 'classifications' in synkka and isinstance(synkka['classifications'], list):
        for cls in synkka['classifications']:
            name = cls.get('name','')
            values = cls.get('values',[])
            if values:
                val_str = ", ".join([str(v.get('id',v)) for v in values])
                parts.append(f"{name}: {val_str}")
    if 'ingredients' in synkka and isinstance(synkka['ingredients'], list):
        for ing in synkka['ingredients']:
            for name in ing.get('names', []):
                parts.append(name.get('value', ''))
    return " ".join([str(p) for p in parts if p])

# --- Load and process JSON ---
json_path = "/Users/untitled_folder/Abroad/Masters/EIT Digital Masters/ETE HU/Sem 3/Junction/valio_aimo_product_data_junction_2025.json"
with open(json_path, "r") as f:
    products = json.load(f)

text_lines = [flatten_product(prod) for prod in products]

# --- Embedding ---
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
text_embeddings = embedding_model.embed_documents(text_lines)

# --- Prepare data for Milvus ---
data = []
for i, (prod, line, embedding) in enumerate(tqdm(zip(products, text_lines, text_embeddings), desc="Creating embeddings")):
    data.append({
        "id": i,
        "vector": embedding,
        "text": line,
        "category": str(prod.get("category", "")),
        "brand": str(prod.get("brand", "")) if "brand" in prod else str(prod.get("synkkaData", {}).get("brand", "")),
        "countryOfOrigin": str(prod.get("countryOfOrigin", "")),
        "vendorName": str(prod.get("vendorName", ""))
    })

# Insert data into Milvus (skip if already inserted)
if not milvus_client.has_collection(collection_name):
    milvus_client.create_collection(
        collection_name=collection_name,
        dimension=embedding_dim,
        metric_type="IP",
        consistency_level="Strong",
    )
    milvus_client.insert(collection_name=collection_name, data=data)

# --- RAG Query ---
question = "Give a good substitute for RED ONION SMALL NETHERLANDS"
query_embedding = embedding_model.embed_query(question)

search_res = milvus_client.search(
    collection_name=collection_name,
    data=[query_embedding],
    limit=3,
    search_params={"metric_type": "IP", "params": {}},
    output_fields=["text"],
)

retrieved_lines_with_distances = [
    (res["entity"]["text"], res["distance"]) for res in search_res[0]
]
print(json.dumps(retrieved_lines_with_distances, indent=4))

# --- Claude LLM Call ---
claude_client = Anthropic(api_key="claude_key")
context = "\n".join([line_with_distance[0] for line_with_distance in retrieved_lines_with_distances])

SYSTEM_PROMPT = "You are an AI assistant. Use the provided context to answer the user's question about product substitutes."
USER_PROMPT = f"""
Use the following pieces of information enclosed in <context> tags to provide an answer to the question enclosed in <question> tags.
<context>
{context}
</context>
<question>
{question}
</question>
"""

response = claude_client.messages.create(
    model="claude-3-opus-20240229",
    max_tokens=512,
    system=SYSTEM_PROMPT,
    messages=[
        {"role": "user", "content": USER_PROMPT}
    ]
)

print(response.content[0].text)