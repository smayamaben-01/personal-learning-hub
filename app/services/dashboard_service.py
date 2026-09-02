from app.repositories import dashboard_repository

def get_dashboard_stats(user_id):
    funnel = dashboard_repository.get_company_status(user_id)
    company_funnel = {
    "applied": int(funnel["applied"] or 0),
    "oa": int(funnel["oa"] or 0),
    "interview": int(funnel["interview"] or 0),
    "selected": int(funnel["selected"] or 0),
    "rejected": int(funnel["rejected"] or 0)
        }

    return {
        "topics_by_status": dashboard_repository.get_topics_by_status(user_id),
        "total_questions_solved": int(dashboard_repository.get_total_questions_solved(user_id)["total_questions_solved"] or 0),
        "topics_ranked": dashboard_repository.get_topics_by_rank(user_id),
        "company_funnel": company_funnel,
        "notes_per_week": dashboard_repository.get_notes_per_week(user_id)
    }