import requests
import hashlib
import PyPDF2
import os


def extract_title_from_pdf(file_path):
    """
    从 PDF 文件中提取标题。

    :param file_path: PDF 文件路径
    :return: 提取的标题
    """
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        metadata = reader.metadata
        if "/Title" in metadata:
            return metadata["/Title"]
        else:
            return None


def search_paper_id(title, api_key=None):
    """
    使用 Semantic Scholar API 搜索论文 ID。

    :param title: 论文标题
    :param api_key: Semantic Scholar API 密钥
    :return: 论文 ID
    """
    base_url = "https://api.semanticscholar.org/graph/v1/paper/search"
    headers = {}
    if api_key:
        headers["x-api-key"] = api_key

    params = {"query": title, "limit": 1, "fields": "paperId"}

    response = requests.get(base_url, params=params, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if data.get("data"):
            return data["data"][0]["paperId"]
        else:
            return None
    else:
        print(f"Error: {response.status_code}")
        return None


def get_paper_ids(directory, api_key=None):
    """
    获取目录中所有 PDF 文件的论文 ID。

    :param directory: PDF 文件所在的目录
    :param api_key: Semantic Scholar API 密钥
    :return: 文件路径到论文 ID 的映射
    """
    paper_ids = {}
    for filename in os.listdir(directory):
        if filename.endswith(".pdf"):
            file_path = os.path.join(directory, filename)
            title = extract_title_from_pdf(file_path)
            if title:
                paper_id = search_paper_id(title, api_key)
                if paper_id:
                    paper_ids[file_path] = paper_id
                else:
                    paper_ids[file_path] = "Not Found"
            else:
                paper_ids[file_path] = "Title Not Found"
    return paper_ids


if __name__ == "__main__":
    directory = "/home/wch/3.8t_1/Workspace/wch/fish_llm/data/论文打包/RTL文献资料"
    api_key = ""

    paper_ids = get_paper_ids(directory, api_key)
    for file_path, paper_id in paper_ids.items():
        print(f"{file_path}: {paper_id}")