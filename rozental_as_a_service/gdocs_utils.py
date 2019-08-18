import os

import pickle
import re

from typing import List, Optional

from googleapiclient.discovery import Resource
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from rozental_as_a_service.common_types import GoogleDocumentContent
from rozental_as_a_service.config import GOOGLE_DOC_URL_REGEXP
from rozental_as_a_service.extractors_utils import extract_words


def is_google_doc_link(some_path_or_url: str) -> bool:
    return re.match(GOOGLE_DOC_URL_REGEXP, some_path_or_url) is not None


def extract_all_constants_from_google_document(google_document_url: str) -> List[str]:
    docs_service = get_authorized_google_docs_service()
    document_id = get_document_id_from_url(google_document_url)
    if document_id:
        document_content = get_google_document_content(docs_service, document_id)
        document_text_constants = get_text_from_google_document(document_content)
        return list(set(extract_words(document_text_constants)))
    return []


def get_authorized_google_docs_service() -> Resource:
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            credentials = pickle.load(token)
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'client_secrets.json',
            scopes=['https://www.googleapis.com/auth/documents.readonly'])
        credentials = flow.run_console()
        with open('token.pickle', 'wb') as token:
            pickle.dump(credentials, token)
    return build('docs', 'v1', credentials=credentials)


def get_document_id_from_url(google_document_url: str) -> Optional[str]:
    match = re.match(GOOGLE_DOC_URL_REGEXP, google_document_url)
    return match.groups()[0] if match else None


def get_google_document_content(docs_service: Resource, document_id: str) -> GoogleDocumentContent:
    return docs_service.documents().get(documentId=document_id).execute()


def get_text_from_google_document(document_content: GoogleDocumentContent) -> List[str]:
    text_items: List[str] = []
    for content_item in document_content['body']['content']:
        if 'paragraph' not in content_item:
            continue
        for paragraph_element in content_item['paragraph']['elements']:
            text = paragraph_element.get('textRun', {}).get('content', '').strip()
            if not text:
                continue
            text_items.append(text)
    return text_items
