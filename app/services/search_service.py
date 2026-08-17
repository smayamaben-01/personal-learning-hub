from app.repositories import search_repository
from app.utils import validation

def search_all(user_id, keyword, search_type):
    validation.require_non_empty(keyword, "Search query")
    validation.require_min_length(keyword, 2, "Search query")

    results = {}
    if search_type in ('all', 'dsa'):
        results['dsa_topics'] = search_repository.search_dsa_topics(user_id, keyword)
    if search_type in ('all', 'company'):
        results['companies'] = search_repository.search_companies(user_id, keyword)
    if search_type in ('all', 'note'):
        results['notes'] = search_repository.search_notes(user_id, keyword)
    return results