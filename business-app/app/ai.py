"""Lớp AI: gọi OpenAI nếu có API key, nếu không trả về mock có cấu trúc."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from app.config import settings


@dataclass
class SkillRef:
    name: str
    description: str
    path: Path


def load_skills() -> list[SkillRef]:
    """Đọc tất cả SKILL.md trong skills_dir."""
    base = settings.skills_path
    skills: list[SkillRef] = []
    if not base.exists():
        return skills
    for skill_file in base.glob("*/SKILL.md"):
        text = skill_file.read_text(encoding="utf-8")
        name = skill_file.parent.name
        desc = _extract_description(text)
        skills.append(SkillRef(name=name, description=desc, path=skill_file))
    return sorted(skills, key=lambda s: s.name)


def _extract_description(text: str) -> str:
    in_front = False
    for line in text.splitlines():
        if line.strip() == "---":
            in_front = not in_front
            if not in_front:
                break
            continue
        if in_front and line.startswith("description:"):
            return line.split(":", 1)[1].strip()
    return ""


def pick_skill(query: str, skills: list[SkillRef]) -> SkillRef | None:
    q = query.lower()
    keyword_map = {
        "hoadon-vat": ["hoá đơn", "hoa don", "vat", "thuế", "mst", "mã số thuế"],
        "cham-cong": ["lương", "luong", "chấm công", "ot", "tăng ca", "bhxh", "tncn"],
        "crm-lead": ["lead", "khách hàng tiềm năng", "pipeline", "follow", "bant"],
        "baocao-tai-chinh": ["báo cáo tài chính", "bctc", "cân đối", "kqkd", "lctt"],
        "hop-dong": ["hợp đồng", "hop dong", "nda", "contract", "phạt"],
    }
    scored: list[tuple[int, SkillRef]] = []
    for s in skills:
        kws = keyword_map.get(s.name, [])
        score = sum(1 for kw in kws if kw in q)
        if score:
            scored.append((score, s))
    if not scored:
        return None
    scored.sort(key=lambda x: x[0], reverse=True)
    return scored[0][1]


def answer(query: str, context_docs: list[str] | None = None) -> dict[str, str]:
    """Trả lời câu hỏi nội bộ. Dùng OpenAI nếu có key, ngược lại mock."""
    skills = load_skills()
    matched = pick_skill(query, skills)

    skill_context = ""
    if matched:
        skill_context = matched.path.read_text(encoding="utf-8")

    doc_context = "\n\n---\n\n".join(context_docs or [])

    if not settings.openai_api_key:
        return _mock_answer(query, matched, doc_context)

    try:
        from openai import OpenAI

        client = OpenAI(api_key=settings.openai_api_key)
        system = (
            "Bạn là trợ lý nội bộ của doanh nghiệp Việt Nam. "
            "Trả lời ngắn gọn, chính xác, bằng tiếng Việt. "
            "Khi có 'TÀI LIỆU NỘI BỘ' hoặc 'SKILL', ưu tiên trích dẫn từ đó."
        )
        user = (
            f"CÂU HỎI: {query}\n\n"
            f"TÀI LIỆU NỘI BỘ:\n{doc_context or '(không có)'}\n\n"
            f"SKILL THAM CHIẾU:\n{skill_context or '(không có)'}"
        )
        resp = client.chat.completions.create(
            model=settings.openai_model,
            messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
            temperature=0.2,
        )
        text = resp.choices[0].message.content or ""
        return {"answer": text, "skill_used": matched.name if matched else "", "mode": "openai"}
    except Exception as exc:  # pragma: no cover — fallback path
        return {"answer": f"[Lỗi gọi OpenAI: {exc}] " + _mock_answer(query, matched, doc_context)["answer"],
                "skill_used": matched.name if matched else "", "mode": "fallback"}


def _mock_answer(query: str, matched: SkillRef | None, doc_context: str) -> dict[str, str]:
    bits = [f"(Chế độ mock — chưa cấu hình OPENAI_API_KEY)\n\nCâu hỏi: {query}"]
    if matched:
        bits.append(f"\nĐã chọn skill: **{matched.name}** — {matched.description}")
    if doc_context:
        snippet = doc_context[:300]
        bits.append(f"\nTrích tài liệu liên quan:\n{snippet}…")
    bits.append("\nGợi ý: cấu hình `OPENAI_API_KEY` trong `.env` để nhận câu trả lời thực.")
    return {"answer": "\n".join(bits), "skill_used": matched.name if matched else "", "mode": "mock"}
