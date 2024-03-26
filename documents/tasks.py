from project.celeryconf import app


@app.task
def calculate_shasum_for_document_version(document_version_id: int) -> None:
    from documents.models.document_version import DocumentVersion

    document_version = DocumentVersion.objects.get(id=document_version_id)
    document_version.shasum = document_version.get_shasum_of_file()
    document_version.save()
