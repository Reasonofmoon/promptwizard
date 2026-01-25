"""
Domain-Aware Prompt Optimization App
도메인 특화 프롬프트 최적화 웹 애플리케이션

Usage:
    streamlit run app/domain_prompt_optimizer.py
"""

import streamlit as st
import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Ensure we can import promptwizard module
import os
abs_project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if abs_project_root not in sys.path:
    sys.path.insert(0, abs_project_root)

from promptwizard.glue.promptopt.domains import (
    DomainConfig,
    DomainKnowledge,
    DomainRegistry,
    QualityCriterion,
    ExpertPersona,
    CaseExample,
    CaseLibrary,
    DomainAwarePromptOptimizer,
    create_domain_optimizer,
    MEDICAL_DOMAIN_CONFIG,
    LEGAL_DOMAIN_CONFIG,
    FINANCE_DOMAIN_CONFIG,
    ENGLISH_QUESTION_DOMAIN_CONFIG,
    CSAT_ENGLISH_DOMAIN_CONFIG,
)

# Import English question specific utilities
from promptwizard.glue.promptopt.domains.english_question.config import (
    QUESTION_TEMPLATES,
    DIFFICULTY_LEVELS,
    ACHIEVEMENT_STANDARDS,
)

# Import CSAT English specific utilities
from promptwizard.glue.promptopt.domains.csat_english.config import (
    ALL_CSAT_QUESTIONS,
    LISTENING_QUESTIONS,
    READING_QUESTIONS,
)

# Page configuration
st.set_page_config(
    page_title="Domain-Aware Prompt Optimizer",
    page_icon="🧙",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for prompt library
if 'prompt_library' not in st.session_state:
    st.session_state.prompt_library = []

# Prompt library file path
import json
PROMPT_LIBRARY_FILE = Path(__file__).parent / "prompt_library.json"

def load_prompt_library():
    """Load prompt library from file."""
    if PROMPT_LIBRARY_FILE.exists():
        with open(PROMPT_LIBRARY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_prompt_library(library):
    """Save prompt library to file."""
    with open(PROMPT_LIBRARY_FILE, 'w', encoding='utf-8') as f:
        json.dump(library, f, ensure_ascii=False, indent=2)

def add_to_library(name, domain, original, enhanced, differences):
    """Add a prompt to the library."""
    library = load_prompt_library()
    from datetime import datetime
    entry = {
        "id": len(library) + 1,
        "name": name,
        "domain": domain,
        "original_prompt": original,
        "enhanced_prompt": enhanced,
        "differences": differences,
        "created_at": datetime.now().isoformat()
    }
    library.append(entry)
    save_prompt_library(library)
    return entry

def analyze_prompt_differences(original: str, enhanced: str, domain_config: DomainConfig) -> dict:
    """Analyze differences between original and enhanced prompts."""
    differences = {
        "added_principles": [],
        "added_constraints": [],
        "added_expert_context": False,
        "added_quality_criteria": False,
        "length_increase": len(enhanced) - len(original),
        "summary": []
    }

    # Check for added principles
    for principle in domain_config.knowledge.principles:
        if principle.lower()[:20] in enhanced.lower() or any(word in enhanced for word in principle.split()[:3]):
            differences["added_principles"].append(principle[:50] + "...")

    # Check for added constraints
    for constraint in domain_config.knowledge.constraints:
        if any(word in enhanced for word in constraint.split()[:3]):
            differences["added_constraints"].append(constraint[:50] + "...")

    # Check for expert context
    if any(persona.role in enhanced for persona in domain_config.knowledge.expert_personas):
        differences["added_expert_context"] = True

    # Check for quality criteria
    if any(qc.name in enhanced for qc in domain_config.knowledge.quality_criteria):
        differences["added_quality_criteria"] = True

    # Generate summary
    if differences["added_principles"]:
        differences["summary"].append(f"✅ {len(differences['added_principles'])}개의 도메인 원칙 반영")
    if differences["added_constraints"]:
        differences["summary"].append(f"🚫 {len(differences['added_constraints'])}개의 제약조건 추가")
    if differences["added_expert_context"]:
        differences["summary"].append("👤 전문가 관점 추가")
    if differences["added_quality_criteria"]:
        differences["summary"].append("📊 품질 기준 반영")
    differences["summary"].append(f"📝 텍스트 길이: +{differences['length_increase']} 문자")

    return differences

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .domain-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        border-left: 4px solid #1E88E5;
    }
    .metric-card {
        background-color: #e3f2fd;
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
    }
    .score-high { color: #4CAF50; font-weight: bold; }
    .score-medium { color: #FF9800; font-weight: bold; }
    .score-low { color: #f44336; font-weight: bold; }
    .constraint-box {
        background-color: #fff3e0;
        border-radius: 5px;
        padding: 0.8rem;
        margin: 0.3rem 0;
        border-left: 3px solid #FF9800;
    }
    .principle-box {
        background-color: #e8f5e9;
        border-radius: 5px;
        padding: 0.8rem;
        margin: 0.3rem 0;
        border-left: 3px solid #4CAF50;
    }
</style>
""", unsafe_allow_html=True)


def get_domain_config(domain_type: str) -> DomainConfig:
    """Get domain configuration by type."""
    configs = {
        "medical": MEDICAL_DOMAIN_CONFIG,
        "legal": LEGAL_DOMAIN_CONFIG,
        "finance": FINANCE_DOMAIN_CONFIG,
        "english_question": ENGLISH_QUESTION_DOMAIN_CONFIG,
        "csat_english": CSAT_ENGLISH_DOMAIN_CONFIG
    }
    return configs.get(domain_type)


def render_header():
    """Render app header."""
    st.markdown('<p class="main-header">🧙 Domain-Aware Prompt Optimizer</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">도메인 암묵지를 반영한 프롬프트 최적화 시스템</p>', unsafe_allow_html=True)


def render_domain_selector():
    """Render domain selection sidebar."""
    st.sidebar.header("🎯 도메인 선택")

    domain_options = {
        "medical": "🏥 의료/헬스케어",
        "legal": "⚖️ 법률",
        "finance": "💰 금융/투자",
        "english_question": "📝 영어문항생성",
        "csat_english": "🎓 수능영어 문항번호별 생성"
    }

    selected_domain = st.sidebar.selectbox(
        "도메인 유형",
        options=list(domain_options.keys()),
        format_func=lambda x: domain_options[x]
    )

    return selected_domain


def render_domain_info(config: DomainConfig):
    """Render domain information panel."""
    st.header(f"📋 {config.domain_name} 도메인 정보")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("핵심 원칙", f"{len(config.knowledge.principles)}개")
    with col2:
        st.metric("제약조건", f"{len(config.knowledge.constraints)}개")
    with col3:
        st.metric("품질 기준", f"{len(config.knowledge.quality_criteria)}개")

    # Tabs for different info sections
    tab1, tab2, tab3, tab4 = st.tabs(["🎯 핵심 원칙", "🚫 제약조건", "📊 품질 기준", "🧠 사고방식"])

    with tab1:
        for i, principle in enumerate(config.knowledge.principles, 1):
            st.markdown(f'<div class="principle-box">{i}. {principle}</div>', unsafe_allow_html=True)

    with tab2:
        for i, constraint in enumerate(config.knowledge.constraints, 1):
            st.markdown(f'<div class="constraint-box">{i}. {constraint}</div>', unsafe_allow_html=True)

    with tab3:
        for qc in config.knowledge.quality_criteria:
            col_a, col_b = st.columns([3, 1])
            with col_a:
                st.write(f"**{qc.name}**: {qc.description}")
            with col_b:
                st.progress(qc.weight)
                st.caption(f"가중치: {int(qc.weight * 100)}%")

    with tab4:
        for i, style in enumerate(config.knowledge.thinking_styles, 1):
            st.info(f"{i}. {style}")


def render_prompt_input():
    """Render prompt input section."""
    st.header("✍️ 프롬프트 입력")

    col1, col2 = st.columns(2)

    with col1:
        task_description = st.text_area(
            "작업 설명 (Task Description)",
            placeholder="예: 환자의 증상에 대해 의학적 정보를 제공하는 AI 어시스턴트입니다.",
            height=100
        )

    with col2:
        base_instruction = st.text_area(
            "기본 지시문 (Base Instruction)",
            placeholder="예: 환자의 질문에 정확하고 안전한 의학 정보를 제공하세요.",
            height=100
        )

    answer_format = st.text_input(
        "답변 형식 지정",
        placeholder="예: 답변 마지막에 <ANS_START>최종답변<ANS_END> 형식으로 작성하세요."
    )

    return task_description, base_instruction, answer_format


def render_english_question_input():
    """Render English question generation specific input section."""
    st.header("📝 영어 문항 생성 설정")

    # Question type selection
    st.subheader("1️⃣ 문항 유형 선택")

    template_options = {
        "grammar_tense": "📗 문법 - 시제",
        "grammar_structure": "📗 문법 - 문장구조 (관계사/분사/가정법)",
        "vocabulary_context": "📘 어휘 - 문맥상 의미",
        "reading_main_idea": "📙 독해 - 주제/요지/제목",
        "reading_blank": "📙 독해 - 빈칸 추론",
        "reading_order": "📙 독해 - 순서 배열",
        "reading_insertion": "📙 독해 - 문장 삽입",
        "conversation": "💬 대화문 - 응답 완성",
        "listening_comprehension": "🎧 듣기 - 내용 이해",
    }

    selected_template_id = st.selectbox(
        "문항 유형",
        options=list(template_options.keys()),
        format_func=lambda x: template_options[x]
    )

    selected_template = QUESTION_TEMPLATES.get(selected_template_id)

    # Show template description
    if selected_template:
        st.info(f"**설명:** {selected_template.description}")

        # Show tips in expander
        with st.expander("💡 출제 팁 보기"):
            for tip in selected_template.tips:
                st.write(f"• {tip}")

    st.divider()

    # Difficulty selection
    st.subheader("2️⃣ 난이도/학년 선택")

    col1, col2 = st.columns(2)

    with col1:
        difficulty_options = {
            "elementary_low": "초급 하 (초등 3-4학년, A1)",
            "elementary_high": "초급 상 (초등 5-6학년, A2)",
            "intermediate_low": "중급 하 (중1-2, B1)",
            "intermediate_mid": "중급 중 (중3, B1+)",
            "intermediate_high": "중급 상 (고1, B2)",
            "advanced_low": "고급 하 (고2, B2+)",
            "advanced_high": "고급 상 (고3/수능, C1)",
            "proficiency": "숙달 (대학/공인시험, C1+)",
        }

        selected_difficulty_id = st.selectbox(
            "난이도",
            options=list(difficulty_options.keys()),
            format_func=lambda x: difficulty_options[x],
            index=4  # Default to intermediate_high (고1)
        )

        selected_difficulty = DIFFICULTY_LEVELS.get(selected_difficulty_id)

    with col2:
        if selected_difficulty:
            st.metric("CEFR 레벨", selected_difficulty.cefr)
            st.write(f"**어휘 범위:** {selected_difficulty.vocabulary_range}")
            st.write(f"**지문 길이:** {selected_difficulty.passage_length}")

    # Show grammar scope for selected difficulty
    if selected_difficulty:
        with st.expander("📚 해당 수준 문법 범위"):
            for grammar in selected_difficulty.grammar_scope:
                st.write(f"• {grammar}")

    st.divider()

    # Additional options
    st.subheader("3️⃣ 세부 설정")

    col1, col2 = st.columns(2)

    with col1:
        num_questions = st.number_input("생성할 문항 수", min_value=1, max_value=10, value=1)

        if selected_template_id.startswith("grammar"):
            target_grammar = st.text_input(
                "목표 문법 요소",
                placeholder="예: 현재완료, 관계대명사, 가정법 과거"
            )
        else:
            target_grammar = ""

    with col2:
        if selected_template_id.startswith("reading") or selected_template_id == "listening_comprehension":
            topic = st.text_input(
                "지문 주제",
                placeholder="예: 환경, 기술, 교육, 문화"
            )
        else:
            topic = ""

        include_explanation = st.checkbox("정답 해설 포함", value=True)
        include_korean = st.checkbox("한글 번역 포함", value=False)

    st.divider()

    # Achievement standard selection (optional)
    st.subheader("4️⃣ 교육과정 성취기준 연계 (선택)")

    school_level = st.radio(
        "학교급",
        options=["none", "middle_school", "high_school"],
        format_func=lambda x: {"none": "선택 안함", "middle_school": "중학교", "high_school": "고등학교"}[x],
        horizontal=True
    )

    selected_standard = None
    if school_level != "none":
        standards = ACHIEVEMENT_STANDARDS.get(school_level, {})
        skill_area = st.selectbox(
            "영역",
            options=list(standards.keys()),
            format_func=lambda x: {"listening": "듣기", "speaking": "말하기", "reading": "읽기", "writing": "쓰기"}.get(x, x)
        )

        if skill_area in standards:
            standard_options = {s["code"]: f"{s['code']} {s['content']}" for s in standards[skill_area]}
            selected_standard_code = st.selectbox(
                "성취기준",
                options=list(standard_options.keys()),
                format_func=lambda x: standard_options[x]
            )
            selected_standard = selected_standard_code

    st.divider()

    # Generate prompt button
    st.subheader("5️⃣ 프롬프트 생성")

    additional_instructions = st.text_area(
        "추가 지시사항 (선택)",
        placeholder="예: 실생활 맥락을 활용해주세요. / 학생들이 자주 틀리는 오류를 반영해주세요.",
        height=80
    )

    # Build the prompt from template
    generated_prompt = ""
    if selected_template and st.button("🚀 템플릿 기반 프롬프트 생성", type="primary"):
        # Fill template with selected options
        generated_prompt = selected_template.prompt_template.format(
            grade_level=selected_difficulty.grade_range if selected_difficulty else "미지정",
            difficulty=selected_difficulty.level_name if selected_difficulty else "미지정",
            cefr_level=selected_difficulty.cefr if selected_difficulty else "미지정",
            target_tense=target_grammar if target_grammar else "전체 시제",
            target_grammar=target_grammar if target_grammar else "미지정",
            vocabulary_level=selected_difficulty.vocabulary_range if selected_difficulty else "미지정",
            passage_length=selected_difficulty.passage_length if selected_difficulty else "150-200단어",
            topic=topic if topic else "일반적 주제",
            text_type="설명문",
            blank_type="구/절",
            inference_level="중간",
            situation="일상 대화",
            turns="3-4",
            listening_type="대화",
            duration="30-40",
            output_format=selected_template.output_format,
            additional_instructions=additional_instructions if additional_instructions else "없음"
        )

        # Add achievement standard if selected
        if selected_standard:
            generated_prompt += f"\n\n### 연계 성취기준:\n{selected_standard}"

        # Add options
        if include_explanation:
            generated_prompt += "\n\n### 추가 요청:\n- 각 문항에 정답 해설을 포함해주세요."
        if include_korean:
            generated_prompt += "\n- 지문의 한글 번역을 포함해주세요."
        if num_questions > 1:
            generated_prompt += f"\n- 총 {num_questions}개의 문항을 생성해주세요."

        st.session_state['english_generated_prompt'] = generated_prompt

    # Show generated prompt
    if 'english_generated_prompt' in st.session_state and st.session_state['english_generated_prompt']:
        st.subheader("생성된 프롬프트")
        st.code(st.session_state['english_generated_prompt'], language="markdown")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("📋 프롬프트 복사"):
                st.success("프롬프트가 복사되었습니다!")
        with col2:
            if st.button("🔄 프롬프트 초기화"):
                st.session_state['english_generated_prompt'] = ""
                st.rerun()

    return (
        st.session_state.get('english_generated_prompt', ''),
        selected_template_id,
        selected_difficulty_id,
        selected_standard
    )


def render_csat_english_input():
    """Render CSAT English question generation specific input section."""
    st.header("🎓 수능영어 문항번호별 생성")

    # Question number selection
    st.subheader("1️⃣ 문항 번호 선택")

    # Create tabs for listening and reading
    tab_listening, tab_reading = st.tabs(["🎧 듣기 (1-17번)", "📖 독해 (18-45번)"])

    selected_question = None
    selected_number = None

    with tab_listening:
        st.markdown("**듣기 영역 문항 (1-17번)**")

        listening_options = {
            "1": "1번 - 목적 파악",
            "2": "2번 - 의견 파악",
            "3": "3번 - 관계 파악",
            "4": "4번 - 그림 내용 일치",
            "5": "5번 - 할 일 파악",
            "6": "6번 - 금액 파악",
            "7": "7번 - 이유 파악",
            "8": "8번 - 언급되지 않은 것",
            "9": "9번 - 내용 일치",
            "10": "10번 - 도표 내용 일치",
            "11": "11번 - 적절한 응답 (짧은 대화)",
            "12": "12번 - 적절한 응답 (짧은 대화)",
            "13": "13번 - 적절한 응답 (긴 대화)",
            "14": "14번 - 적절한 응답 (긴 대화)",
            "15": "15번 - 상황에 적절한 말",
            "16-17": "16-17번 - 세트 문항 (담화)",
        }

        selected_listening = st.selectbox(
            "듣기 문항 선택",
            options=list(listening_options.keys()),
            format_func=lambda x: listening_options[x],
            key="listening_select"
        )

        if selected_listening:
            selected_number = selected_listening
            selected_question = LISTENING_QUESTIONS.get(selected_listening)

    with tab_reading:
        st.markdown("**독해 영역 문항 (18-45번)**")

        # Organize reading questions by category
        col1, col2 = st.columns(2)

        with col1:
            reading_category = st.radio(
                "문항 유형 카테고리",
                options=["기본 독해", "어법/어휘", "빈칸 추론", "글의 구조", "장문"],
                horizontal=False
            )

        with col2:
            if reading_category == "기본 독해":
                reading_options = {
                    "18": "18번 - 목적 파악",
                    "19": "19번 - 심경/분위기 파악",
                    "20": "20번 - 주장 파악",
                    "22": "22번 - 요지 파악",
                    "23": "23번 - 주제 파악",
                    "24": "24번 - 제목 파악",
                    "25": "25번 - 도표 이해",
                    "26": "26번 - 내용 일치 (인물)",
                    "27": "27번 - 내용 일치 (실용문)",
                }
            elif reading_category == "어법/어휘":
                reading_options = {
                    "28": "28번 - 어법 (밑줄형) [3점]",
                    "29": "29번 - 어휘 (밑줄형) [3점]",
                }
            elif reading_category == "빈칸 추론":
                reading_options = {
                    "21": "21번 - 함축 의미 추론 [3점] ⭐고난도",
                    "30": "30번 - 빈칸 추론 (구/절)",
                    "31": "31번 - 빈칸 추론 (구/절)",
                    "32": "32번 - 빈칸 추론 [3점] ⭐고난도",
                    "33": "33번 - 빈칸 추론 [3점] ⭐고난도",
                    "34": "34번 - 빈칸 추론 [3점] ⭐고난도",
                }
            elif reading_category == "글의 구조":
                reading_options = {
                    "35": "35번 - 무관한 문장",
                    "36": "36번 - 순서 배열",
                    "37": "37번 - 순서 배열",
                    "38": "38번 - 문장 삽입",
                    "39": "39번 - 문장 삽입",
                    "40": "40번 - 요약문 완성",
                }
            else:  # 장문
                reading_options = {
                    "41-42": "41-42번 - 장문 (제목/어휘)",
                    "43-45": "43-45번 - 장문 (순서/지칭/내용일치)",
                }

            selected_reading = st.selectbox(
                "독해 문항 선택",
                options=list(reading_options.keys()),
                format_func=lambda x: reading_options[x],
                key="reading_select"
            )

            if selected_reading:
                selected_number = selected_reading
                selected_question = READING_QUESTIONS.get(selected_reading)

    st.divider()

    # Show selected question info
    if selected_question:
        st.subheader("2️⃣ 선택된 문항 정보")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("문항 번호", f"{selected_number}번")
        with col2:
            st.metric("배점", f"{selected_question.point}점")
        with col3:
            difficulty_emoji = {"상": "🔴", "중": "🟡", "하": "🟢"}.get(selected_question.difficulty, "⚪")
            st.metric("난이도", f"{difficulty_emoji} {selected_question.difficulty}")

        st.info(f"**{selected_question.type_name}** ({selected_question.type_name_en})")
        st.write(f"📋 {selected_question.description}")

        if selected_question.key_skills:
            st.write("**핵심 능력:**")
            for skill in selected_question.key_skills:
                st.write(f"  • {skill}")

        if selected_question.tips:
            with st.expander("💡 출제 팁 보기"):
                for tip in selected_question.tips:
                    st.write(f"• {tip}")

        if selected_question.stem_template:
            st.write("**발문 템플릿:**")
            st.code(selected_question.stem_template, language="text")

        st.divider()

        # Additional options
        st.subheader("3️⃣ 세부 설정")

        col1, col2 = st.columns(2)

        with col1:
            num_questions = st.number_input("생성할 문항 수", min_value=1, max_value=5, value=1, key="csat_num")

            if selected_question.category == "독해" and selected_question.passage_length:
                st.write(f"**권장 지문 길이:** {selected_question.passage_length}")

        with col2:
            topic = st.text_input(
                "지문 주제 (선택)",
                placeholder="예: 환경, 기술, 심리학, 교육",
                key="csat_topic"
            )
            include_explanation = st.checkbox("정답 해설 포함", value=True, key="csat_explain")

        additional_instructions = st.text_area(
            "추가 지시사항 (선택)",
            placeholder="예: EBS 연계 스타일로 작성해주세요. / 최신 수능 경향을 반영해주세요.",
            height=80,
            key="csat_additional"
        )

        st.divider()

        # Generate prompt
        st.subheader("4️⃣ 프롬프트 생성")

        if st.button("🚀 수능 문항 프롬프트 생성", type="primary", key="csat_generate"):
            # Build prompt based on question type
            if selected_question.prompt_template:
                generated_prompt = selected_question.prompt_template.format(
                    output_format=selected_question.output_format or "JSON 형식으로 출력",
                    additional_instructions=additional_instructions if additional_instructions else "없음"
                )
            else:
                # Default template for questions without specific template
                generated_prompt = f"""당신은 수능 영어 출제 전문가입니다.

## 문항 유형: {selected_number}번 - {selected_question.type_name}
## 영역: {selected_question.category}
## 난이도: {selected_question.difficulty} ({selected_question.point}점)

다음 조건에 맞는 수능 {selected_number}번 유형 문항을 생성하세요.

### 문항 설명:
{selected_question.description}

### 발문 형식:
{selected_question.stem_template}

### 핵심 능력:
{', '.join(selected_question.key_skills) if selected_question.key_skills else '일반적 독해/듣기 능력'}

### 출력 형식:
```json
{{
  "item_number": {selected_number.split('-')[0]},
  "item_type": "{selected_question.type_name_en.lower().replace(' ', '_')}",
  "point": {selected_question.point},
  "stem": "발문",
  "passage": "지문/스크립트",
  "options": [
    {{"number": "①", "text": "선택지1", "is_answer": false}},
    {{"number": "②", "text": "선택지2", "is_answer": false}},
    {{"number": "③", "text": "선택지3", "is_answer": true}},
    {{"number": "④", "text": "선택지4", "is_answer": false}},
    {{"number": "⑤", "text": "선택지5", "is_answer": false}}
  ],
  "answer": "③",
  "explanation": "정답 해설"
}}
```

### 추가 조건:
- 주제: {topic if topic else '자유 주제'}
- 해설 포함: {'예' if include_explanation else '아니오'}
- 생성 문항 수: {num_questions}개

### 추가 지시사항:
{additional_instructions if additional_instructions else '없음'}
"""

            st.session_state['csat_generated_prompt'] = generated_prompt

        # Show generated prompt
        if 'csat_generated_prompt' in st.session_state and st.session_state['csat_generated_prompt']:
            st.subheader("생성된 프롬프트")
            st.code(st.session_state['csat_generated_prompt'], language="markdown")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("📋 프롬프트 복사", key="csat_copy"):
                    st.success("프롬프트가 복사되었습니다!")
            with col2:
                if st.button("🔄 프롬프트 초기화", key="csat_reset"):
                    st.session_state['csat_generated_prompt'] = ""
                    st.rerun()

        return st.session_state.get('csat_generated_prompt', ''), selected_number

    return '', None


def render_test_case_section(config: DomainConfig):
    """Render test case section."""
    st.header("🧪 테스트 케이스")

    all_cases = config.case_library.get_all_cases()

    if not all_cases:
        st.info("등록된 테스트 케이스가 없습니다.")
        return None

    case_options = {f"{c.category}: {c.question[:50]}...": c for c in all_cases}

    selected_case_key = st.selectbox(
        "테스트 케이스 선택",
        options=list(case_options.keys())
    )

    if selected_case_key:
        selected_case = case_options[selected_case_key]

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📝 질문")
            st.write(selected_case.question)

            st.subheader("✅ 기대 요소")
            for elem in selected_case.expected_elements:
                st.success(f"• {elem}")

        with col2:
            st.subheader("ℹ️ 정보")
            st.write(f"**카테고리:** {selected_case.category}")
            st.write(f"**난이도:** {selected_case.difficulty}")

            if selected_case.forbidden_elements:
                st.subheader("❌ 금지 요소")
                for elem in selected_case.forbidden_elements:
                    st.error(f"• {elem}")

        return selected_case

    return None


def evaluate_response(optimizer: DomainAwarePromptOptimizer, response: str, question: str = ""):
    """Evaluate response using domain evaluator."""
    scores = optimizer.evaluate_response(response, question=question)
    return scores


def render_evaluation_results(scores: dict):
    """Render evaluation results."""
    st.header("📊 평가 결과")

    # Overall score
    overall = scores.get('overall', 0)

    if overall >= 0.7:
        score_class = "score-high"
        emoji = "✅"
    elif overall >= 0.4:
        score_class = "score-medium"
        emoji = "⚠️"
    else:
        score_class = "score-low"
        emoji = "❌"

    st.markdown(f"""
    <div class="metric-card">
        <h2>{emoji} 종합 점수</h2>
        <h1 class="{score_class}">{int(overall * 100)}%</h1>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    # Individual scores
    cols = st.columns(len(scores) - 1)  # Exclude 'overall'

    i = 0
    for metric, score in scores.items():
        if metric == 'overall':
            continue

        with cols[i % len(cols)]:
            score_pct = int(score * 100)
            st.metric(
                label=metric,
                value=f"{score_pct}%",
                delta=f"{score_pct - 50}%" if score_pct != 50 else None
            )
        i += 1

    # Render validation details
    if 'validation_details' in scores:
        st.subheader("🛡️ 결정론적 검증 (Deterministic Verification)")
        
        details = scores['validation_details']
        if all(details.values()):
            st.success("모든 검증 통과! (All Validators Passed)")
        else:
            st.error("검증 실패 항목이 있습니다! (Validation Failed)")
            
        for name, passed in details.items():
            if passed:
                st.write(f"✅ **{name}**: Pass")
            else:
                st.write(f"❌ **{name}**: Fail")
                
    st.divider()


def render_enhanced_prompt(optimizer: DomainAwarePromptOptimizer, base_instruction: str, domain_config: DomainConfig):
    """Render enhanced prompt with difference analysis and library saving."""
    st.header("🚀 강화된 프롬프트")

    enhanced = optimizer.enhance_base_instruction(base_instruction)

    # Analyze differences
    differences = analyze_prompt_differences(base_instruction, enhanced, domain_config)

    # Show comparison in two columns
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📝 원본 프롬프트")
        st.code(base_instruction, language="markdown")

    with col2:
        st.subheader("✨ 강화된 프롬프트")
        st.code(enhanced, language="markdown")

    # Difference explanation box
    st.subheader("🔍 원본 vs 강화 프롬프트 차이점 분석")

    diff_container = st.container()
    with diff_container:
        st.markdown("""
        <style>
        .diff-box {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 1.5rem;
            border-radius: 10px;
            margin: 1rem 0;
        }
        .diff-item {
            background: rgba(255,255,255,0.15);
            padding: 0.5rem 1rem;
            border-radius: 5px;
            margin: 0.5rem 0;
        }
        </style>
        """, unsafe_allow_html=True)

        # Display summary
        for item in differences["summary"]:
            st.info(item)

        # Detailed differences in expander
        with st.expander("📋 상세 차이점 보기"):
            if differences["added_principles"]:
                st.write("**추가된 도메인 원칙:**")
                for p in differences["added_principles"][:5]:
                    st.markdown(f"- {p}")

            if differences["added_constraints"]:
                st.write("**추가된 제약조건:**")
                for c in differences["added_constraints"][:5]:
                    st.markdown(f"- {c}")

            if differences["added_expert_context"]:
                st.success("전문가 페르소나 관점이 프롬프트에 반영되었습니다.")

            if differences["added_quality_criteria"]:
                st.success("도메인별 품질 기준이 프롬프트에 반영되었습니다.")

    st.divider()

    # Action buttons
    col_btn1, col_btn2, col_btn3 = st.columns(3)

    with col_btn1:
        if st.button("📋 강화된 프롬프트 복사"):
            st.session_state['copied_prompt'] = enhanced
            st.success("프롬프트가 복사되었습니다!")

    with col_btn2:
        # Save to library
        with st.popover("💾 라이브러리에 저장"):
            prompt_name = st.text_input("프롬프트 이름", placeholder="예: 영어 문법 문항 생성 v1")
            if st.button("저장하기", key="save_to_lib"):
                if prompt_name:
                    entry = add_to_library(
                        name=prompt_name,
                        domain=domain_config.domain_name,
                        original=base_instruction,
                        enhanced=enhanced,
                        differences=differences["summary"]
                    )
                    st.success(f"'{prompt_name}'이(가) 라이브러리에 저장되었습니다! (ID: {entry['id']})")
                else:
                    st.warning("프롬프트 이름을 입력해주세요.")

    with col_btn3:
        if st.button("📚 라이브러리 보기"):
            st.session_state['show_library'] = True

    # Show library if requested
    if st.session_state.get('show_library', False):
        render_prompt_library()


def render_prompt_library():
    """Render the saved prompt library."""
    st.subheader("📚 저장된 프롬프트 라이브러리")

    library = load_prompt_library()

    if not library:
        st.info("저장된 프롬프트가 없습니다.")
        return

    for entry in reversed(library):
        with st.expander(f"📌 {entry['name']} ({entry['domain']}) - {entry['created_at'][:10]}"):
            st.write("**원본 프롬프트:**")
            st.code(entry['original_prompt'], language="markdown")

            st.write("**강화된 프롬프트:**")
            st.code(entry['enhanced_prompt'], language="markdown")

            st.write("**차이점:**")
            for diff in entry.get('differences', []):
                st.write(f"- {diff}")

            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"📋 복사", key=f"copy_{entry['id']}"):
                    st.session_state['copied_prompt'] = entry['enhanced_prompt']
                    st.success("복사됨!")
            with col2:
                if st.button(f"🗑️ 삭제", key=f"delete_{entry['id']}"):
                    library = [e for e in library if e['id'] != entry['id']]
                    save_prompt_library(library)
                    st.rerun()


def render_critique_section(optimizer: DomainAwarePromptOptimizer, instruction: str, response: str):
    """Render critique generation section."""
    st.header("📝 도메인 비평 생성")

    if st.button("비평 생성"):
        with st.spinner("도메인 지식 기반 비평 생성 중..."):
            critique_prompt = optimizer.generate_domain_critique(
                instruction=instruction,
                examples=response
            )

            st.subheader("생성된 비평 프롬프트")
            st.code(critique_prompt, language="markdown")


def render_case_validation(optimizer: DomainAwarePromptOptimizer, response: str, case: CaseExample):
    """Render case validation results."""
    st.header("🔍 케이스 검증 결과")

    response_lower = response.lower()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("✅ 기대 요소 체크")
        found_count = 0
        for elem in case.expected_elements:
            if elem.lower() in response_lower:
                st.success(f"✓ {elem}")
                found_count += 1
            else:
                st.warning(f"✗ {elem}")

        if case.expected_elements:
            st.metric("발견율", f"{found_count}/{len(case.expected_elements)}")

    with col2:
        st.subheader("❌ 금지 요소 체크")
        violation_count = 0
        for elem in case.forbidden_elements:
            if elem.lower() in response_lower:
                st.error(f"⚠️ 위반: {elem}")
                violation_count += 1
            else:
                st.success(f"✓ 미포함: {elem}")

        if case.forbidden_elements:
            st.metric("위반 수", f"{violation_count}/{len(case.forbidden_elements)}")


def render_custom_domain_editor():
    """Render custom domain configuration editor."""
    st.header("🛠️ 커스텀 도메인 설정")

    with st.expander("새 도메인 설정 만들기"):
        domain_name = st.text_input("도메인 이름", placeholder="예: 교육/학습")
        domain_type = st.text_input("도메인 타입", placeholder="예: education")

        st.subheader("핵심 원칙")
        principles = st.text_area(
            "원칙 목록 (줄바꿈으로 구분)",
            placeholder="학습자 중심 교육\n단계적 난이도 조절\n..."
        )

        st.subheader("제약조건")
        constraints = st.text_area(
            "제약조건 목록 (줄바꿈으로 구분)",
            placeholder="오답을 정답으로 제시 금지\n..."
        )

        if st.button("도메인 설정 생성"):
            if domain_name and domain_type:
                principles_list = [p.strip() for p in principles.split('\n') if p.strip()]
                constraints_list = [c.strip() for c in constraints.split('\n') if c.strip()]

                custom_config = DomainConfig(
                    domain_type=domain_type,
                    domain_name=domain_name,
                    knowledge=DomainKnowledge(
                        principles=principles_list,
                        constraints=constraints_list
                    )
                )

                st.session_state['custom_domain'] = custom_config
                st.success(f"'{domain_name}' 도메인 설정이 생성되었습니다!")

                # Show generated config
                st.json(custom_config.to_dict())


def main():
    """Main app function."""
    render_header()

    # Sidebar
    selected_domain = render_domain_selector()

    # Get domain config
    config = get_domain_config(selected_domain)

    if not config:
        st.error("도메인 설정을 불러올 수 없습니다.")
        return

    # Create optimizer
    try:
        optimizer = create_domain_optimizer(selected_domain)
    except Exception as e:
        st.error(f"최적화기 생성 실패: {e}")
        optimizer = DomainAwarePromptOptimizer(domain_config=config)

    # Main content tabs
    main_tab1, main_tab2, main_tab3, main_tab4 = st.tabs([
        "📋 도메인 정보",
        "✍️ 프롬프트 최적화",
        "🧪 응답 평가",
        "🛠️ 커스텀 도메인"
    ])

    with main_tab1:
        render_domain_info(config)

    with main_tab2:
        # Use specialized UI for English question domain
        if selected_domain == "english_question":
            result = render_english_question_input()
            base_inst = result[0] if result[0] else ""

            if base_inst:
                st.divider()
                render_enhanced_prompt(optimizer, base_inst, config)

                # Expert prompt
                st.subheader("👤 전문가 페르소나")
                expert_prompt = optimizer.get_domain_expert_prompt()
                st.code(expert_prompt, language="markdown")

        elif selected_domain == "csat_english":
            # Use specialized UI for CSAT English domain
            result = render_csat_english_input()
            base_inst = result[0] if result[0] else ""

            if base_inst:
                st.divider()
                render_enhanced_prompt(optimizer, base_inst, config)

                # Expert prompt
                st.subheader("👤 전문가 페르소나")
                expert_prompt = optimizer.get_domain_expert_prompt()
                st.code(expert_prompt, language="markdown")

        else:
            # Default UI for other domains
            task_desc, base_inst, ans_format = render_prompt_input()

            if base_inst:
                st.divider()
                render_enhanced_prompt(optimizer, base_inst, config)

                # Expert prompt
                st.subheader("👤 전문가 페르소나")
                expert_prompt = optimizer.get_domain_expert_prompt()
                st.code(expert_prompt, language="markdown")

    with main_tab3:
        st.subheader("📝 응답 입력")
        test_response = st.text_area(
            "평가할 응답",
            placeholder="AI가 생성한 응답을 입력하세요...",
            height=200
        )

        # Test case selection
        selected_case = render_test_case_section(config)

        if test_response:
            st.divider()

            # Evaluate response
            question = selected_case.question if selected_case else ""
            scores = evaluate_response(optimizer, test_response, question)
            render_evaluation_results(scores)

            # Case validation if case selected
            if selected_case:
                st.divider()
                render_case_validation(optimizer, test_response, selected_case)

    with main_tab4:
        render_custom_domain_editor()

    # Sidebar additional info
    st.sidebar.divider()
    st.sidebar.header("📖 사용 가이드")
    st.sidebar.markdown("""
    1. **도메인 선택**: 최적화할 도메인 선택
    2. **도메인 정보**: 암묵지 및 제약조건 확인
    3. **프롬프트 최적화**: 기본 지시문 입력 및 강화
    4. **응답 평가**: AI 응답의 도메인 적합성 평가
    5. **커스텀 도메인**: 새로운 도메인 설정 생성
    """)

    st.sidebar.divider()
    st.sidebar.info("🧙 PromptWizard Domain Extension v1.0")


if __name__ == "__main__":
    main()
