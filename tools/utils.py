from typing import List, Dict, Any


def merge_data(
    invitations: List[Dict[str, Any]], resumes: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    # Преобразуем список `resumes` в словарь для быстрого поиска
    resume_dict = {resume["resume_id"]: resume for resume in resumes}

    # Объединяем данные на основе `resume_id`
    merged_data = []
    for invite in invitations:
        resume_id = invite.get("resume_id")
        vacancy_id = invite.get("vacancy_id")
        resume = resume_dict.get(resume_id, {})
        merged_data.append(
            {
                "vacancy_id": vacancy_id,
                "resume_id": resume_id,
                "created_at": invite.get("created_at"),
                "full_name": invite.get("full_name", ""),
                "age": invite.get("age", ""),
                "phone_number": resume.get("phone_number", ""),
            }
        )

    return merged_data
