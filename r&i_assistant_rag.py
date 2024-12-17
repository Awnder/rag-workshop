from langchain.document_loaders import PyPDFLoader, UnstructuredExcelLoader, Docx2txtLoader
from langchain_community.document_loaders import UnstructuredImageLoader, GithubFileLoader
from langchain_pinecone import PineconeVectorStore
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone
import os

def init_pinecone(pinecone_namespace: str = "", pinecone_index: str = "ri-assist"):
    load_dotenv()
    self._embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
    self._pinecone_client = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    self._pinecone_index = pinecone_index
    self._pinecone_namespace = pinecone_namespace # vectorstore.add_documents upserts docs w/o namespace
    self.VectorStore = PineconeVectorStore(self._pinecone_index, embedding=self._embeddings)

def add_documents():
    
def update_documents():


def _process_directory(self, directory_path: str = "./r&i_assistant_docs") -> list:
    ''' resursively processes all files in a local directory '''
    data = []
    # other docs
    for root, _, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            if file.endswith(".pdf"):
                loader = PyPDFLoader(file_path)
                data.append(build_directory_document(file_path, loader))
            # elif file[-3:] == 'png':
            #     loader = UnstructuredImageLoader(file_path)
            #     data.append({"File": file_path, "Data": loader.load()})
            elif file.endswith(".docx"):
                loader = Docx2txtLoader(file_path)
                data.append(build_directory_document(file_path, loader))
            elif file.endswith(".xlsx"):
                loader = UnstructuredExcelLoader(file_path)
                data.append(build_directory_document(file_path, loader))

    return data

def _process_github(self, repo_name: str = "reportingandinsights/common-code") -> list:
    ''' recursively processes all files in a github repo. repo_name will break if includes a frontslash at the end'''
    data = []
    loader = GithubFileLoader(
        repo=repo_name,
        branch="main",
        access_token=os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN"),
        file_filter=lambda file_path: file_path.endswith(".md") or file_path.endswith(".txt") or file_path.endswith(".xml"),
    )
    
    for gitdoc in loader.load():
        data.append(build_github_doc(repo_name + "/", gitdoc))

    return data

def _build_directory_document(file_path: str, loader: object) -> Document:
    ''' create a Document object with metadata and page content '''
    return Document(
        metadata={
            "source": file_path
        },
        page_content=f"Source: {file_path}\n{loader.load()[0].page_content}"
    )

def _build_github_doc(repo_name: str, gitdoc: list) -> Document:
    ''' create a Document object with metadata and page content. github loader loads all documents so requires a different function'''
    return Document(
        metadata={
            "source": f"{repo_name}{gitdoc.metadata['path']}"
        },
        page_content=f"Source: {repo_name}{gitdoc.metadata['path']}\n{[gitdoc][0].page_content}" # convert the doc to a 1-element list to access the page_content
    )

