# document_template_engine.py

from modules.authentication.google_utils import get_docs_service

def generate_document_from_template(doc_id, placeholders, replacements):
    service = get_docs_service()

    copied = service.documents().copy(
        body={"name": f"AI-Ausgabe: {replacements.get('NAME', 'Dokument')}"}
    ).execute()

    document_id = copied["documentId"]

    requests = []
    for placeholder in placeholders:
        value = replacements.get(placeholder.strip("[]"), "")
        requests.append({
            "replaceAllText": {
                "containsText": {"text": placeholder, "matchCase": True},
                "replaceText": value
            }
        })

    service.documents().batchUpdate(
        documentId=document_id,
        body={"requests": requests}
    ).execute()

    return {
        "status": "success",
        "document_id": document_id,
        "url": f"https://docs.google.com/document/d/{document_id}"
    }
