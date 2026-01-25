# Copyright (c) 2024 Microsoft
# Licensed under The MIT License [see LICENSE for details]

"""
CSAT (수능) English Question Generation by Item Number.
수능 영어 문항번호별 생성 도메인 설정
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from ..base_domain import (
    DomainConfig,
    DomainKnowledge,
    QualityCriterion,
    ExpertPersona,
    CaseLibrary,
    CaseExample
)


# ============================================================================
# 수능 문항번호별 유형 정의
# ============================================================================

@dataclass
class CSATQuestionType:
    """수능 문항 유형 정의"""
    number: int  # 문항 번호
    number_range: Optional[Tuple[int, int]] = None  # 범위형 문항 (예: 1-17)
    type_name: str = ""  # 문항 유형명
    type_name_en: str = ""  # 영문 유형명
    category: str = ""  # 카테고리 (듣기/독해/어휘/어법)
    difficulty: str = "중"  # 난이도 (상/중/하)
    point: int = 2  # 배점 (2점/3점)
    description: str = ""  # 상세 설명
    stem_template: str = ""  # 발문 템플릿
    passage_length: str = ""  # 지문 길이
    key_skills: List[str] = field(default_factory=list)  # 핵심 능력
    prompt_template: str = ""  # 프롬프트 템플릿
    output_format: str = ""  # 출력 형식
    tips: List[str] = field(default_factory=list)  # 출제 팁


# 듣기 영역 (1-17번)
LISTENING_QUESTIONS: Dict[str, CSATQuestionType] = {
    "1": CSATQuestionType(
        number=1,
        type_name="목적 파악",
        type_name_en="Purpose",
        category="듣기",
        difficulty="하",
        point=2,
        description="대화를 듣고 남자/여자가 하는 말의 목적을 파악",
        stem_template="다음을 듣고, {speaker}가 하는 말의 목적으로 가장 적절한 것을 고르시오.",
        key_skills=["전체 맥락 파악", "화자 의도 추론"],
        tips=["도입부에서 목적이 드러나는 경우가 많음", "직접적 목적 vs 간접적 목적 구분"]
    ),
    "2": CSATQuestionType(
        number=2,
        type_name="의견 파악",
        type_name_en="Opinion",
        category="듣기",
        difficulty="하",
        point=2,
        description="대화를 듣고 남자/여자의 의견을 파악",
        stem_template="대화를 듣고, {speaker}의 의견으로 가장 적절한 것을 고르시오.",
        key_skills=["의견 표현 인식", "핵심 주장 파악"],
        tips=["I think, I believe, In my opinion 등 의견 표현 주목"]
    ),
    "3": CSATQuestionType(
        number=3,
        type_name="관계 파악",
        type_name_en="Relationship",
        category="듣기",
        difficulty="하",
        point=2,
        description="대화를 듣고 두 사람의 관계를 파악",
        stem_template="대화를 듣고, 두 사람의 관계를 가장 잘 나타낸 것을 고르시오.",
        key_skills=["상황 맥락 파악", "관계 표지어 인식"],
        tips=["호칭, 존칭, 업무 관련 어휘 주목"]
    ),
    "4": CSATQuestionType(
        number=4,
        type_name="그림 내용 일치",
        type_name_en="Picture Match",
        category="듣기",
        difficulty="하",
        point=2,
        description="대화를 듣고 그림에서 언급되지 않은 것을 파악",
        stem_template="대화를 듣고, 그림에서 대화의 내용과 일치하지 않는 것을 고르시오.",
        key_skills=["세부 정보 파악", "시각 정보 대조"],
        tips=["위치, 모양, 개수, 색상 등 구체적 정보 주목"]
    ),
    "5": CSATQuestionType(
        number=5,
        type_name="할 일 파악",
        type_name_en="Task",
        category="듣기",
        difficulty="하",
        point=2,
        description="대화를 듣고 남자/여자가 할 일을 파악",
        stem_template="대화를 듣고, {speaker}가 할 일로 가장 적절한 것을 고르시오.",
        key_skills=["행동 결정 파악", "미래 행위 추론"],
        tips=["will, be going to, should 등 미래 표현 주목"]
    ),
    "6": CSATQuestionType(
        number=6,
        type_name="금액 파악",
        type_name_en="Amount",
        category="듣기",
        difficulty="하",
        point=2,
        description="대화를 듣고 지불할 금액을 계산",
        stem_template="대화를 듣고, {speaker}가 지불할 금액을 고르시오.",
        key_skills=["수치 정보 파악", "계산 능력"],
        tips=["할인, 추가 요금, 수량 변화 주의"]
    ),
    "7": CSATQuestionType(
        number=7,
        type_name="이유 파악",
        type_name_en="Reason",
        category="듣기",
        difficulty="하",
        point=2,
        description="대화를 듣고 어떤 행동/상황의 이유를 파악",
        stem_template="대화를 듣고, {speaker}가 {action}하는 이유를 고르시오.",
        key_skills=["인과 관계 파악", "이유 추론"],
        tips=["because, since, due to 등 이유 표현 주목"]
    ),
    "8": CSATQuestionType(
        number=8,
        type_name="언급되지 않은 것",
        type_name_en="Not Mentioned",
        category="듣기",
        difficulty="중",
        point=2,
        description="대화를 듣고 언급되지 않은 것을 파악",
        stem_template="대화를 듣고, {topic}에 관해 언급되지 않은 것을 고르시오.",
        key_skills=["세부 정보 확인", "소거법 적용"],
        tips=["언급된 4가지를 소거하고 나머지 선택"]
    ),
    "9": CSATQuestionType(
        number=9,
        type_name="내용 일치",
        type_name_en="Content Match",
        category="듣기",
        difficulty="중",
        point=2,
        description="대화를 듣고 내용과 일치하는/일치하지 않는 것 파악",
        stem_template="대화를 듣고, {topic}에 관한 내용과 일치하지 않는 것을 고르시오.",
        key_skills=["세부 정보 대조", "팩트 체크"],
        tips=["숫자, 이름, 날짜 등 구체적 정보 주의"]
    ),
    "10": CSATQuestionType(
        number=10,
        type_name="도표 내용 일치",
        type_name_en="Table Match",
        category="듣기",
        difficulty="중",
        point=2,
        description="대화를 듣고 도표의 내용과 일치하는 것 파악",
        stem_template="다음 표를 보면서 대화를 듣고, 두 사람이 선택할 {item}을 고르시오.",
        key_skills=["도표 읽기", "조건 대조"],
        tips=["조건을 하나씩 제거하며 선택지 좁히기"]
    ),
    "11": CSATQuestionType(
        number=11,
        type_name="적절한 응답 (짧은 대화)",
        type_name_en="Short Response",
        category="듣기",
        difficulty="중",
        point=2,
        description="짧은 대화를 듣고 마지막 말에 대한 적절한 응답 선택",
        stem_template="대화를 듣고, {speaker}의 마지막 말에 대한 {other}의 응답으로 가장 적절한 것을 고르시오.",
        key_skills=["화용적 적절성", "대화 맥락 파악"],
        tips=["감정, 상황, 요청/제안에 대한 적절한 반응"]
    ),
    "12": CSATQuestionType(
        number=12,
        type_name="적절한 응답 (짧은 대화)",
        type_name_en="Short Response",
        category="듣기",
        difficulty="중",
        point=2,
        description="짧은 대화를 듣고 마지막 말에 대한 적절한 응답 선택",
        stem_template="대화를 듣고, {speaker}의 마지막 말에 대한 {other}의 응답으로 가장 적절한 것을 고르시오.",
        key_skills=["화용적 적절성", "대화 맥락 파악"],
        tips=["감정, 상황, 요청/제안에 대한 적절한 반응"]
    ),
    "13": CSATQuestionType(
        number=13,
        type_name="적절한 응답 (긴 대화)",
        type_name_en="Long Response",
        category="듣기",
        difficulty="중",
        point=2,
        description="긴 대화를 듣고 마지막 말에 대한 적절한 응답 선택",
        stem_template="대화를 듣고, {speaker}의 마지막 말에 대한 {other}의 응답으로 가장 적절한 것을 고르시오.",
        key_skills=["긴 맥락 파악", "적절한 응답 추론"],
        tips=["대화의 전체 흐름과 마지막 말의 의도 파악"]
    ),
    "14": CSATQuestionType(
        number=14,
        type_name="적절한 응답 (긴 대화)",
        type_name_en="Long Response",
        category="듣기",
        difficulty="중",
        point=2,
        description="긴 대화를 듣고 마지막 말에 대한 적절한 응답 선택",
        stem_template="대화를 듣고, {speaker}의 마지막 말에 대한 {other}의 응답으로 가장 적절한 것을 고르시오.",
        key_skills=["긴 맥락 파악", "적절한 응답 추론"],
        tips=["대화의 전체 흐름과 마지막 말의 의도 파악"]
    ),
    "15": CSATQuestionType(
        number=15,
        type_name="상황에 적절한 말",
        type_name_en="Situational Response",
        category="듣기",
        difficulty="중",
        point=2,
        description="상황 설명을 듣고 적절한 말 선택",
        stem_template="다음 상황 설명을 듣고, {speaker}가 {other}에게 할 말로 가장 적절한 것을 고르시오.",
        key_skills=["상황 맥락 이해", "화용적 적절성"],
        tips=["상황과 화자의 의도를 종합하여 판단"]
    ),
    "16-17": CSATQuestionType(
        number=16,
        number_range=(16, 17),
        type_name="세트 문항 (담화)",
        type_name_en="Set Questions",
        category="듣기",
        difficulty="중",
        point=2,
        description="긴 담화를 듣고 2개의 문항 해결 (주제/세부정보)",
        stem_template="다음을 듣고, 물음에 답하시오.",
        key_skills=["담화 전체 이해", "주제 및 세부정보 파악"],
        tips=["16번은 주로 주제, 17번은 세부정보 또는 언급되지 않은 것"]
    ),
}

# 독해 영역 (18-45번)
READING_QUESTIONS: Dict[str, CSATQuestionType] = {
    "18": CSATQuestionType(
        number=18,
        type_name="목적 파악",
        type_name_en="Purpose",
        category="독해",
        difficulty="하",
        point=2,
        description="글의 목적을 파악하는 문항",
        stem_template="다음 글의 목적으로 가장 적절한 것은?",
        passage_length="120-150단어",
        key_skills=["글 전체 맥락 파악", "필자 의도 추론"],
        prompt_template="""당신은 수능 영어 출제 전문가입니다.

## 문항 유형: 18번 - 목적 파악
## 난이도: 하 (2점)

다음 조건에 맞는 수능 18번 유형 문항을 생성하세요.

### 필수 조건:
1. 지문 길이: 120-150단어
2. 글의 유형: 편지, 이메일, 안내문, 공지사항 등
3. 글을 쓴 목적이 명확하게 드러나야 함
4. 5개의 선택지 (정답 1개, 유사 목적의 오답 4개)

### 발문:
다음 글의 목적으로 가장 적절한 것은?

### 출력 형식:
{output_format}

### 추가 지시사항:
{additional_instructions}
""",
        output_format="""```json
{
  "item_number": 18,
  "item_type": "purpose",
  "passage": "영어 지문",
  "options": [
    {"number": "①", "text": "선택지1", "is_answer": false},
    {"number": "②", "text": "선택지2", "is_answer": true},
    {"number": "③", "text": "선택지3", "is_answer": false},
    {"number": "④", "text": "선택지4", "is_answer": false},
    {"number": "⑤", "text": "선택지5", "is_answer": false}
  ],
  "answer": "②",
  "explanation": "정답 해설"
}
```""",
        tips=["글의 첫 문장과 마지막 문장에서 목적 파악", "to 부정사 목적 표현 활용"]
    ),
    "19": CSATQuestionType(
        number=19,
        type_name="심경/분위기 파악",
        type_name_en="Mood/Atmosphere",
        category="독해",
        difficulty="하",
        point=2,
        description="글에 드러난 심경이나 분위기를 파악",
        stem_template="다음 글에 드러난 {target}의 심경으로/분위기로 가장 적절한 것은?",
        passage_length="150-180단어",
        key_skills=["감정 표현 인식", "분위기 추론"],
        prompt_template="""당신은 수능 영어 출제 전문가입니다.

## 문항 유형: 19번 - 심경/분위기 파악
## 난이도: 하 (2점)

다음 조건에 맞는 수능 19번 유형 문항을 생성하세요.

### 필수 조건:
1. 지문 길이: 150-180단어
2. 글의 유형: 서사문 (narrative)
3. 인물의 심경 변화 또는 일관된 분위기
4. 감정/분위기를 나타내는 형용사 2개를 정답으로

### 발문:
다음 글에 드러난 'I'의 심경으로 가장 적절한 것은?

### 출력 형식:
{output_format}

### 추가 지시사항:
{additional_instructions}
""",
        output_format="""```json
{
  "item_number": 19,
  "item_type": "mood",
  "passage": "영어 지문",
  "options": [
    {"number": "①", "text": "relieved and grateful", "is_answer": false},
    {"number": "②", "text": "nervous and anxious", "is_answer": true},
    ...
  ],
  "answer": "②",
  "explanation": "정답 해설",
  "emotion_clues": ["감정 단서 표현들"]
}
```""",
        tips=["감정 표현 형용사 및 부사 활용", "상황 묘사를 통한 간접적 감정 표현"]
    ),
    "20": CSATQuestionType(
        number=20,
        type_name="주장 파악",
        type_name_en="Claim",
        category="독해",
        difficulty="하",
        point=2,
        description="필자가 주장하는 바를 파악",
        stem_template="다음 글에서 필자가 주장하는 바로 가장 적절한 것은?",
        passage_length="150-180단어",
        key_skills=["주장 파악", "논증 구조 이해"],
        prompt_template="""당신은 수능 영어 출제 전문가입니다.

## 문항 유형: 20번 - 주장 파악
## 난이도: 하 (2점)

다음 조건에 맞는 수능 20번 유형 문항을 생성하세요.

### 필수 조건:
1. 지문 길이: 150-180단어
2. 글의 유형: 논설문/설득문
3. 명확한 주장이 제시되어야 함
4. should, must, need to 등 당위 표현 포함

### 발문:
다음 글에서 필자가 주장하는 바로 가장 적절한 것은?

### 출력 형식:
{output_format}

### 추가 지시사항:
{additional_instructions}
""",
        output_format="""```json
{
  "item_number": 20,
  "item_type": "claim",
  "passage": "영어 지문",
  "options": [...],
  "answer": "정답 번호",
  "explanation": "정답 해설",
  "claim_sentence": "주장이 담긴 핵심 문장"
}
```""",
        tips=["주장을 나타내는 표현(should, must, It is important that) 활용"]
    ),
    "21": CSATQuestionType(
        number=21,
        type_name="함축 의미 추론",
        type_name_en="Implied Meaning",
        category="독해",
        difficulty="상",
        point=3,
        description="밑줄 친 부분이 의미하는 바를 추론 (고난도)",
        stem_template="밑줄 친 {underlined}이(가) 다음 글에서 의미하는 바로 가장 적절한 것은?",
        passage_length="180-220단어",
        key_skills=["함축 의미 추론", "비유적 표현 이해", "문맥 기반 해석"],
        prompt_template="""당신은 수능 영어 출제 전문가입니다.

## 문항 유형: 21번 - 함축 의미 추론 (3점)
## 난이도: 상 (고난도)

다음 조건에 맞는 수능 21번 유형 문항을 생성하세요.

### 필수 조건:
1. 지문 길이: 180-220단어
2. 밑줄 친 부분: 비유적/함축적 표현
3. 문맥을 통해서만 의미 파악 가능
4. 추상적 개념을 구체적 표현으로 나타낸 것

### 발문:
밑줄 친 [표현]이(가) 다음 글에서 의미하는 바로 가장 적절한 것은? [3점]

### 출력 형식:
{output_format}

### 추가 지시사항:
{additional_instructions}
""",
        output_format="""```json
{
  "item_number": 21,
  "item_type": "implied_meaning",
  "point": 3,
  "passage": "영어 지문 (밑줄 부분 표시)",
  "underlined_expression": "밑줄 친 표현",
  "options": [...],
  "answer": "정답 번호",
  "explanation": "정답 해설",
  "literal_meaning": "문자적 의미",
  "implied_meaning": "함축적 의미"
}
```""",
        tips=["은유, 비유, 관용 표현 활용", "문맥에서만 파악 가능한 의미"]
    ),
    "22": CSATQuestionType(
        number=22,
        type_name="요지 파악",
        type_name_en="Gist",
        category="독해",
        difficulty="중",
        point=2,
        description="글의 요지를 파악",
        stem_template="다음 글의 요지로 가장 적절한 것은?",
        passage_length="150-180단어",
        key_skills=["핵심 내용 파악", "요약 능력"],
        prompt_template="""당신은 수능 영어 출제 전문가입니다.

## 문항 유형: 22번 - 요지 파악
## 난이도: 중 (2점)

다음 조건에 맞는 수능 22번 유형 문항을 생성하세요.

### 필수 조건:
1. 지문 길이: 150-180단어
2. 글의 핵심 메시지가 명확해야 함
3. 주제문이 있되 선택지는 paraphrase
4. 부분적 내용을 요지로 오해하는 오답 설계

### 발문:
다음 글의 요지로 가장 적절한 것은?

### 출력 형식:
{output_format}
""",
        output_format="""```json
{
  "item_number": 22,
  "item_type": "gist",
  "passage": "영어 지문",
  "options": [...],
  "answer": "정답 번호",
  "explanation": "정답 해설",
  "main_point": "핵심 요지"
}
```""",
        tips=["주제문 paraphrase", "부분적 내용을 전체 요지로 오해하는 오답"]
    ),
    "23": CSATQuestionType(
        number=23,
        type_name="주제 파악",
        type_name_en="Topic",
        category="독해",
        difficulty="중",
        point=2,
        description="글의 주제를 파악",
        stem_template="다음 글의 주제로 가장 적절한 것은?",
        passage_length="150-180단어",
        key_skills=["주제 파악", "추상화 능력"],
        prompt_template="""당신은 수능 영어 출제 전문가입니다.

## 문항 유형: 23번 - 주제 파악
## 난이도: 중 (2점)

다음 조건에 맞는 수능 23번 유형 문항을 생성하세요.

### 필수 조건:
1. 지문 길이: 150-180단어
2. 주제가 명확하게 드러나야 함
3. 선택지는 명사구 형태
4. 지나치게 일반적이거나 구체적인 오답 설계

### 발문:
다음 글의 주제로 가장 적절한 것은?

### 출력 형식:
{output_format}
""",
        output_format="""```json
{
  "item_number": 23,
  "item_type": "topic",
  "passage": "영어 지문",
  "options": [...],
  "answer": "정답 번호",
  "explanation": "정답 해설"
}
```""",
        tips=["the importance of ~, the role of ~ 등 명사구 형태"]
    ),
    "24": CSATQuestionType(
        number=24,
        type_name="제목 파악",
        type_name_en="Title",
        category="독해",
        difficulty="중",
        point=2,
        description="글의 제목을 파악",
        stem_template="다음 글의 제목으로 가장 적절한 것은?",
        passage_length="150-180단어",
        key_skills=["핵심 내용 압축", "함축적 표현 이해"],
        prompt_template="""당신은 수능 영어 출제 전문가입니다.

## 문항 유형: 24번 - 제목 파악
## 난이도: 중 (2점)

다음 조건에 맞는 수능 24번 유형 문항을 생성하세요.

### 필수 조건:
1. 지문 길이: 150-180단어
2. 제목으로 적절한 함축적 표현
3. 콜론(:), 물음표(?) 등 활용 가능
4. 흥미를 유발하면서 내용을 포괄

### 발문:
다음 글의 제목으로 가장 적절한 것은?

### 출력 형식:
{output_format}
""",
        output_format="""```json
{
  "item_number": 24,
  "item_type": "title",
  "passage": "영어 지문",
  "options": [...],
  "answer": "정답 번호",
  "explanation": "정답 해설"
}
```""",
        tips=["함축적이고 매력적인 제목", "핵심 키워드 포함"]
    ),
    "25": CSATQuestionType(
        number=25,
        type_name="도표 이해",
        type_name_en="Graph/Chart",
        category="독해",
        difficulty="하",
        point=2,
        description="도표의 내용과 일치하지 않는 것 찾기",
        stem_template="다음 도표의 내용과 일치하지 않는 것은?",
        key_skills=["도표 읽기", "정보 대조"],
        prompt_template="""당신은 수능 영어 출제 전문가입니다.

## 문항 유형: 25번 - 도표 이해
## 난이도: 하 (2점)

다음 조건에 맞는 수능 25번 유형 문항을 생성하세요.

### 필수 조건:
1. 도표(그래프, 표) 설명 + 5개 선택지
2. 4개는 도표와 일치, 1개는 불일치
3. 수치, 비율, 순위 등 구체적 정보
4. 최상급, 비교급 표현 활용

### 발문:
다음 도표의 내용과 일치하지 않는 것은?

### 출력 형식:
{output_format}
""",
        output_format="""```json
{
  "item_number": 25,
  "item_type": "graph",
  "graph_description": "도표 설명",
  "graph_data": {...},
  "options": [...],
  "answer": "정답 번호 (불일치하는 것)",
  "explanation": "정답 해설"
}
```""",
        tips=["비교급, 최상급 표현 정확성", "숫자/비율 확인"]
    ),
    "26": CSATQuestionType(
        number=26,
        type_name="내용 일치 (인물)",
        type_name_en="Content Match - Person",
        category="독해",
        difficulty="하",
        point=2,
        description="인물에 관한 글의 내용과 일치하는 것 찾기",
        stem_template="{person}에 관한 다음 글의 내용과 일치하는 것은?",
        passage_length="180-200단어",
        key_skills=["세부 정보 파악", "정보 대조"],
        prompt_template="""당신은 수능 영어 출제 전문가입니다.

## 문항 유형: 26번 - 내용 일치 (인물)
## 난이도: 하 (2점)

다음 조건에 맞는 수능 26번 유형 문항을 생성하세요.

### 필수 조건:
1. 지문 길이: 180-200단어
2. 실존 인물 또는 가상 인물 소개
3. 생애, 업적, 일화 등 구체적 정보
4. 1개 일치, 4개 불일치

### 발문:
[인물명]에 관한 다음 글의 내용과 일치하는 것은?

### 출력 형식:
{output_format}
""",
        output_format="""```json
{
  "item_number": 26,
  "item_type": "content_match_person",
  "person": "인물명",
  "passage": "영어 지문",
  "options": [...],
  "answer": "정답 번호",
  "explanation": "정답 해설"
}
```""",
        tips=["날짜, 장소, 숫자 등 구체적 정보 변형으로 오답 설계"]
    ),
    "27": CSATQuestionType(
        number=27,
        type_name="내용 일치 (실용문)",
        type_name_en="Content Match - Practical",
        category="독해",
        difficulty="하",
        point=2,
        description="안내문, 광고 등 실용문의 내용과 일치하는 것 찾기",
        stem_template="{topic}에 관한 다음 안내문의 내용과 일치하지 않는 것은?",
        passage_length="150-180단어",
        key_skills=["실용문 이해", "세부 정보 파악"],
        prompt_template="""당신은 수능 영어 출제 전문가입니다.

## 문항 유형: 27번 - 내용 일치 (실용문)
## 난이도: 하 (2점)

다음 조건에 맞는 수능 27번 유형 문항을 생성하세요.

### 필수 조건:
1. 지문 유형: 안내문, 광고, 공지사항, 행사 안내 등
2. 일시, 장소, 비용, 조건 등 구체적 정보
3. 4개 일치, 1개 불일치 (불일치를 정답으로)

### 발문:
[행사/프로그램명]에 관한 다음 안내문의 내용과 일치하지 않는 것은?

### 출력 형식:
{output_format}
""",
        output_format="""```json
{
  "item_number": 27,
  "item_type": "content_match_practical",
  "passage": "안내문/광고 지문",
  "options": [...],
  "answer": "정답 번호",
  "explanation": "정답 해설"
}
```""",
        tips=["날짜, 시간, 금액, 조건 등 세부 정보 변형"]
    ),
    "28": CSATQuestionType(
        number=28,
        type_name="어법 (밑줄형)",
        type_name_en="Grammar - Underlined",
        category="어법",
        difficulty="중",
        point=3,
        description="밑줄 친 부분 중 어법상 틀린 것 찾기",
        stem_template="다음 글의 밑줄 친 부분 중, 어법상 틀린 것은?",
        passage_length="150-180단어",
        key_skills=["문법 지식", "문맥 속 문법 적용"],
        prompt_template="""당신은 수능 영어 출제 전문가입니다.

## 문항 유형: 28번 - 어법 (3점)
## 난이도: 중

다음 조건에 맞는 수능 28번 유형 문항을 생성하세요.

### 필수 조건:
1. 지문 길이: 150-180단어
2. 5개의 밑줄 친 부분 (①②③④⑤)
3. 1개만 어법상 틀림 (나머지 4개는 맞음)
4. 주요 문법 포인트: 관계사, 분사, 시제, 수일치, 대명사 등

### 발문:
다음 글의 밑줄 친 부분 중, 어법상 틀린 것은? [3점]

### 출력 형식:
{output_format}
""",
        output_format="""```json
{
  "item_number": 28,
  "item_type": "grammar",
  "point": 3,
  "passage": "영어 지문 (밑줄 표시 포함)",
  "underlined": [
    {"number": "①", "text": "표현1", "is_error": false, "grammar_point": "문법 포인트"},
    {"number": "②", "text": "표현2", "is_error": true, "grammar_point": "문법 포인트", "correct_form": "올바른 형태"},
    ...
  ],
  "answer": "②",
  "explanation": "정답 해설"
}
```""",
        tips=["관계대명사/관계부사, 분사의 능동/수동, 수일치 등 주요 문법 출제"]
    ),
    "29": CSATQuestionType(
        number=29,
        type_name="어휘 (밑줄형)",
        type_name_en="Vocabulary - Underlined",
        category="어휘",
        difficulty="중",
        point=3,
        description="밑줄 친 어휘 중 문맥상 적절하지 않은 것 찾기",
        stem_template="다음 글의 밑줄 친 부분 중, 문맥상 낱말의 쓰임이 적절하지 않은 것은?",
        passage_length="150-180단어",
        key_skills=["문맥 파악", "어휘 의미 이해"],
        prompt_template="""당신은 수능 영어 출제 전문가입니다.

## 문항 유형: 29번 - 어휘 (3점)
## 난이도: 중

다음 조건에 맞는 수능 29번 유형 문항을 생성하세요.

### 필수 조건:
1. 지문 길이: 150-180단어
2. 5개의 밑줄 친 어휘 (①②③④⑤)
3. 1개만 문맥상 부적절 (반의어로 대체해야 함)
4. 나머지 4개는 문맥상 적절

### 발문:
다음 글의 밑줄 친 부분 중, 문맥상 낱말의 쓰임이 적절하지 않은 것은? [3점]

### 출력 형식:
{output_format}
""",
        output_format="""```json
{
  "item_number": 29,
  "item_type": "vocabulary",
  "point": 3,
  "passage": "영어 지문 (밑줄 표시 포함)",
  "underlined": [
    {"number": "①", "text": "단어1", "is_inappropriate": false},
    {"number": "②", "text": "단어2", "is_inappropriate": true, "correct_word": "올바른 단어"},
    ...
  ],
  "answer": "②",
  "explanation": "정답 해설"
}
```""",
        tips=["반의어 관계 활용", "문맥에서 의미 추론"]
    ),
    "30": CSATQuestionType(
        number=30,
        type_name="빈칸 추론 (구/절)",
        type_name_en="Blank Inference - Phrase",
        category="독해",
        difficulty="중",
        point=2,
        description="빈칸에 들어갈 구나 절 추론",
        stem_template="다음 글의 빈칸에 들어갈 말로 가장 적절한 것은?",
        passage_length="180-200단어",
        key_skills=["논리적 추론", "문맥 파악"],
        prompt_template="""당신은 수능 영어 출제 전문가입니다.

## 문항 유형: 30번 - 빈칸 추론
## 난이도: 중 (2점)

다음 조건에 맞는 수능 30번 유형 문항을 생성하세요.

### 필수 조건:
1. 지문 길이: 180-200단어
2. 빈칸에 들어갈 내용: 구(phrase) 또는 절(clause)
3. 문맥에서 논리적으로 추론 가능
4. paraphrase된 표현을 정답으로

### 발문:
다음 글의 빈칸에 들어갈 말로 가장 적절한 것은?

### 출력 형식:
{output_format}
""",
        output_format="""```json
{
  "item_number": 30,
  "item_type": "blank_inference",
  "passage": "영어 지문 (빈칸 포함)",
  "blank_type": "phrase/clause",
  "options": [...],
  "answer": "정답 번호",
  "explanation": "정답 해설",
  "clue_sentences": ["단서가 되는 문장들"]
}
```""",
        tips=["빈칸 전후 논리적 연결 확인", "paraphrase 표현 활용"]
    ),
    "31": CSATQuestionType(
        number=31,
        type_name="빈칸 추론 (구/절)",
        type_name_en="Blank Inference - Phrase",
        category="독해",
        difficulty="중",
        point=2,
        description="빈칸에 들어갈 구나 절 추론",
        stem_template="다음 글의 빈칸에 들어갈 말로 가장 적절한 것은?",
        passage_length="180-200단어",
        key_skills=["논리적 추론", "문맥 파악"],
        prompt_template="""당신은 수능 영어 출제 전문가입니다.

## 문항 유형: 31번 - 빈칸 추론
## 난이도: 중 (2점)

다음 조건에 맞는 수능 31번 유형 문항을 생성하세요.

### 필수 조건:
1. 지문 길이: 180-200단어
2. 빈칸에 들어갈 내용: 구(phrase) 또는 절(clause)
3. 문맥에서 논리적으로 추론 가능

### 발문:
다음 글의 빈칸에 들어갈 말로 가장 적절한 것은?
""",
        output_format="""```json
{
  "item_number": 31,
  "item_type": "blank_inference",
  "passage": "영어 지문 (빈칸 포함)",
  "options": [...],
  "answer": "정답 번호",
  "explanation": "정답 해설"
}
```""",
        tips=["역접, 인과, 예시 등 담화 표지 활용"]
    ),
    "32": CSATQuestionType(
        number=32,
        type_name="빈칸 추론 (고난도)",
        type_name_en="Blank Inference - Hard",
        category="독해",
        difficulty="상",
        point=3,
        description="빈칸에 들어갈 추상적 표현 추론 (고난도)",
        stem_template="다음 글의 빈칸에 들어갈 말로 가장 적절한 것은? [3점]",
        passage_length="200-230단어",
        key_skills=["추상적 사고", "핵심 개념 추론"],
        prompt_template="""당신은 수능 영어 출제 전문가입니다.

## 문항 유형: 32번 - 빈칸 추론 (3점, 고난도)
## 난이도: 상

다음 조건에 맞는 수능 32번 유형 문항을 생성하세요.

### 필수 조건:
1. 지문 길이: 200-230단어
2. 빈칸: 글의 핵심 개념/주제어
3. 추상적 사고와 논리적 추론 필요
4. 지문 전체를 이해해야 풀 수 있음

### 발문:
다음 글의 빈칸에 들어갈 말로 가장 적절한 것은? [3점]

### 출력 형식:
{output_format}
""",
        output_format="""```json
{
  "item_number": 32,
  "item_type": "blank_inference_hard",
  "point": 3,
  "passage": "영어 지문 (빈칸 포함)",
  "options": [...],
  "answer": "정답 번호",
  "explanation": "정답 해설",
  "core_concept": "핵심 개념"
}
```""",
        tips=["추상적 개념 표현", "글 전체 맥락 파악 필요"]
    ),
    "33": CSATQuestionType(
        number=33,
        type_name="빈칸 추론 (고난도)",
        type_name_en="Blank Inference - Hard",
        category="독해",
        difficulty="상",
        point=3,
        description="빈칸에 들어갈 추상적 표현 추론 (고난도)",
        stem_template="다음 글의 빈칸에 들어갈 말로 가장 적절한 것은? [3점]",
        passage_length="200-230단어",
        key_skills=["추상적 사고", "핵심 개념 추론"],
        prompt_template="""당신은 수능 영어 출제 전문가입니다.

## 문항 유형: 33번 - 빈칸 추론 (3점, 고난도)
## 난이도: 상

다음 조건에 맞는 수능 33번 유형 문항을 생성하세요.

### 조건 및 출력 형식: 32번과 동일
""",
        output_format="""```json
{
  "item_number": 33,
  "item_type": "blank_inference_hard",
  "point": 3,
  ...
}
```""",
        tips=["글의 주제/요지가 빈칸 답이 되는 경우 많음"]
    ),
    "34": CSATQuestionType(
        number=34,
        type_name="빈칸 추론 (고난도)",
        type_name_en="Blank Inference - Hard",
        category="독해",
        difficulty="상",
        point=3,
        description="빈칸에 들어갈 추상적 표현 추론 (고난도)",
        stem_template="다음 글의 빈칸에 들어갈 말로 가장 적절한 것은? [3점]",
        passage_length="200-230단어",
        key_skills=["추상적 사고", "핵심 개념 추론"],
        prompt_template="""당신은 수능 영어 출제 전문가입니다.

## 문항 유형: 34번 - 빈칸 추론 (3점, 고난도)
## 난이도: 상

다음 조건에 맞는 수능 34번 유형 문항을 생성하세요.

### 조건 및 출력 형식: 32번과 동일
""",
        output_format="""```json
{
  "item_number": 34,
  "item_type": "blank_inference_hard",
  "point": 3,
  ...
}
```""",
        tips=["문제 상황과 해결책의 관계", "역설적 표현"]
    ),
    "35": CSATQuestionType(
        number=35,
        type_name="무관한 문장",
        type_name_en="Irrelevant Sentence",
        category="독해",
        difficulty="중",
        point=2,
        description="글의 흐름과 관계없는 문장 찾기",
        stem_template="다음 글에서 전체 흐름과 관계없는 문장은?",
        passage_length="180-200단어",
        key_skills=["글의 통일성 파악", "문장 간 연결 확인"],
        prompt_template="""당신은 수능 영어 출제 전문가입니다.

## 문항 유형: 35번 - 무관한 문장
## 난이도: 중 (2점)

다음 조건에 맞는 수능 35번 유형 문항을 생성하세요.

### 필수 조건:
1. 5개의 번호 붙은 문장
2. 1개만 주제와 무관한 문장
3. 무관한 문장은 주제와 관련 있어 보이지만 실제로는 벗어남
4. 나머지 문장들은 논리적으로 연결됨

### 발문:
다음 글에서 전체 흐름과 관계없는 문장은?

### 출력 형식:
{output_format}
""",
        output_format="""```json
{
  "item_number": 35,
  "item_type": "irrelevant_sentence",
  "passage": "지문 (번호 붙은 5개 문장 포함)",
  "sentences": [
    {"number": "①", "text": "문장1", "is_irrelevant": false},
    {"number": "②", "text": "문장2", "is_irrelevant": true},
    ...
  ],
  "answer": "②",
  "explanation": "정답 해설",
  "main_topic": "글의 주제"
}
```""",
        tips=["주제 관련 키워드는 있지만 논점이 다른 문장"]
    ),
    "36": CSATQuestionType(
        number=36,
        type_name="순서 배열",
        type_name_en="Order Arrangement",
        category="독해",
        difficulty="중",
        point=2,
        description="주어진 글 다음에 이어질 글의 순서 배열",
        stem_template="주어진 글 다음에 이어질 글의 순서로 가장 적절한 것은?",
        passage_length="180-200단어",
        key_skills=["논리적 연결 파악", "담화 표지어 이해"],
        prompt_template="""당신은 수능 영어 출제 전문가입니다.

## 문항 유형: 36번 - 순서 배열
## 난이도: 중 (2점)

다음 조건에 맞는 수능 36번 유형 문항을 생성하세요.

### 필수 조건:
1. 도입문 + 3개 단락 (A), (B), (C)
2. 지시어, 연결어를 통한 순서 단서
3. 5가지 순서 조합 선택지

### 발문:
주어진 글 다음에 이어질 글의 순서로 가장 적절한 것은?

### 출력 형식:
{output_format}
""",
        output_format="""```json
{
  "item_number": 36,
  "item_type": "order",
  "intro": "도입문",
  "paragraph_A": "(A) 단락",
  "paragraph_B": "(B) 단락",
  "paragraph_C": "(C) 단락",
  "options": [
    {"number": "①", "order": "(A)-(C)-(B)"},
    {"number": "②", "order": "(B)-(A)-(C)"},
    ...
  ],
  "answer": "정답 번호",
  "correct_order": "(B)-(A)-(C)",
  "explanation": "정답 해설",
  "cohesion_devices": ["this", "however", "such 등 연결 장치"]
}
```""",
        tips=["대명사-선행사 관계", "this/these/such 등 지시어 활용"]
    ),
    "37": CSATQuestionType(
        number=37,
        type_name="순서 배열",
        type_name_en="Order Arrangement",
        category="독해",
        difficulty="중",
        point=2,
        description="주어진 글 다음에 이어질 글의 순서 배열",
        stem_template="주어진 글 다음에 이어질 글의 순서로 가장 적절한 것은?",
        passage_length="180-200단어",
        key_skills=["논리적 연결 파악", "담화 표지어 이해"],
        prompt_template="""수능 37번 유형 문항 (36번과 동일 형식)""",
        output_format="""36번과 동일""",
        tips=["시간 순서, 논리적 전개 순서 확인"]
    ),
    "38": CSATQuestionType(
        number=38,
        type_name="문장 삽입",
        type_name_en="Sentence Insertion",
        category="독해",
        difficulty="중",
        point=2,
        description="주어진 문장이 들어갈 위치 찾기",
        stem_template="글의 흐름으로 보아, 주어진 문장이 들어가기에 가장 적절한 곳은?",
        passage_length="180-200단어",
        key_skills=["문맥 연결", "지시어/연결어 파악"],
        prompt_template="""당신은 수능 영어 출제 전문가입니다.

## 문항 유형: 38번 - 문장 삽입
## 난이도: 중 (2점)

다음 조건에 맞는 수능 38번 유형 문항을 생성하세요.

### 필수 조건:
1. 삽입할 문장 제시
2. 지문 내 5개의 삽입 위치 (①②③④⑤)
3. 삽입 문장에 연결 단서 포함

### 발문:
글의 흐름으로 보아, 주어진 문장이 들어가기에 가장 적절한 곳은?

### 출력 형식:
{output_format}
""",
        output_format="""```json
{
  "item_number": 38,
  "item_type": "sentence_insertion",
  "given_sentence": "삽입할 문장",
  "passage_with_markers": "지문 (①②③④⑤ 위치 표시)",
  "answer": "정답 번호",
  "explanation": "정답 해설",
  "connection_clue": "연결 단서 설명"
}
```""",
        tips=["However, Therefore, For example 등 연결어 활용"]
    ),
    "39": CSATQuestionType(
        number=39,
        type_name="문장 삽입",
        type_name_en="Sentence Insertion",
        category="독해",
        difficulty="중",
        point=2,
        description="주어진 문장이 들어갈 위치 찾기",
        stem_template="글의 흐름으로 보아, 주어진 문장이 들어가기에 가장 적절한 곳은?",
        passage_length="180-200단어",
        key_skills=["문맥 연결", "지시어/연결어 파악"],
        prompt_template="""수능 39번 유형 문항 (38번과 동일 형식)""",
        output_format="""38번과 동일""",
        tips=["삽입 문장의 this/these가 가리키는 대상 확인"]
    ),
    "40": CSATQuestionType(
        number=40,
        type_name="요약문 완성",
        type_name_en="Summary Completion",
        category="독해",
        difficulty="중",
        point=2,
        description="글의 내용을 요약하는 문장 완성",
        stem_template="다음 글의 내용을 한 문장으로 요약하고자 한다. 빈칸 (A), (B)에 들어갈 말로 가장 적절한 것은?",
        passage_length="180-200단어",
        key_skills=["요약 능력", "핵심어 파악"],
        prompt_template="""당신은 수능 영어 출제 전문가입니다.

## 문항 유형: 40번 - 요약문 완성
## 난이도: 중 (2점)

다음 조건에 맞는 수능 40번 유형 문항을 생성하세요.

### 필수 조건:
1. 지문 + 요약문 (빈칸 2개: (A), (B))
2. 각 빈칸에 들어갈 단어 조합 5개
3. 요약문은 지문의 핵심 내용을 paraphrase

### 발문:
다음 글의 내용을 한 문장으로 요약하고자 한다. 빈칸 (A), (B)에 들어갈 말로 가장 적절한 것은?

### 출력 형식:
{output_format}
""",
        output_format="""```json
{
  "item_number": 40,
  "item_type": "summary",
  "passage": "영어 지문",
  "summary_sentence": "요약문 ((A), (B) 빈칸 포함)",
  "options": [
    {"number": "①", "A": "단어1", "B": "단어2"},
    {"number": "②", "A": "단어3", "B": "단어4"},
    ...
  ],
  "answer": "정답 번호",
  "explanation": "정답 해설"
}
```""",
        tips=["지문의 핵심 어휘를 동의어/유의어로 paraphrase"]
    ),
    "41-42": CSATQuestionType(
        number=41,
        number_range=(41, 42),
        type_name="장문 독해 (1)",
        type_name_en="Long Passage 1",
        category="독해",
        difficulty="중",
        point=2,
        description="장문을 읽고 제목/어휘 문제 해결",
        stem_template="다음 글을 읽고, 물음에 답하시오.",
        passage_length="250-300단어",
        key_skills=["긴 글 독해", "제목 파악", "어휘 추론"],
        prompt_template="""당신은 수능 영어 출제 전문가입니다.

## 문항 유형: 41-42번 - 장문 독해 세트 (1)
## 난이도: 중 (각 2점)

다음 조건에 맞는 수능 41-42번 유형 문항을 생성하세요.

### 필수 조건:
1. 지문 길이: 250-300단어
2. 41번: 제목 파악
3. 42번: 밑줄 친 어휘 문제 (빈칸/적절성)

### 발문:
[41-42] 다음 글을 읽고, 물음에 답하시오.
41. 윗글의 제목으로 가장 적절한 것은?
42. 밑줄 친 (a)~(e) 중에서 문맥상 낱말의 쓰임이 적절하지 않은 것은?

### 출력 형식:
{output_format}
""",
        output_format="""```json
{
  "item_number": "41-42",
  "item_type": "long_passage_1",
  "passage": "장문 지문 (밑줄 표시 포함)",
  "questions": [
    {
      "number": 41,
      "type": "title",
      "stem": "윗글의 제목으로 가장 적절한 것은?",
      "options": [...],
      "answer": "정답 번호"
    },
    {
      "number": 42,
      "type": "vocabulary",
      "stem": "밑줄 친 (a)~(e) 중에서 문맥상 낱말의 쓰임이 적절하지 않은 것은?",
      "underlined": [...],
      "answer": "정답 번호"
    }
  ],
  "explanation": "해설"
}
```""",
        tips=["제목과 어휘 문제의 난이도 균형"]
    ),
    "43-45": CSATQuestionType(
        number=43,
        number_range=(43, 45),
        type_name="장문 독해 (2)",
        type_name_en="Long Passage 2",
        category="독해",
        difficulty="중",
        point=2,
        description="장문을 읽고 순서/지칭/내용일치 문제 해결",
        stem_template="다음 글을 읽고, 물음에 답하시오.",
        passage_length="300-350단어",
        key_skills=["긴 글 독해", "순서 파악", "지칭 추론", "내용 파악"],
        prompt_template="""당신은 수능 영어 출제 전문가입니다.

## 문항 유형: 43-45번 - 장문 독해 세트 (2)
## 난이도: 중 (각 2점)

다음 조건에 맞는 수능 43-45번 유형 문항을 생성하세요.

### 필수 조건:
1. 지문 길이: 300-350단어 (소설/이야기)
2. 43번: 글의 순서 배열
3. 44번: 밑줄 친 대명사가 가리키는 대상
4. 45번: 글의 내용과 일치/불일치

### 발문:
[43-45] 다음 글을 읽고, 물음에 답하시오.
43. 주어진 글 (A)에 이어질 내용을 순서에 맞게 배열한 것은?
44. 밑줄 친 (a)~(e) 중에서 가리키는 대상이 나머지 넷과 다른 것은?
45. 윗글의 내용과 일치하지 않는 것은?

### 출력 형식:
{output_format}
""",
        output_format="""```json
{
  "item_number": "43-45",
  "item_type": "long_passage_2",
  "intro_A": "(A) 도입 단락",
  "paragraph_B": "(B) 단락",
  "paragraph_C": "(C) 단락",
  "paragraph_D": "(D) 단락",
  "questions": [
    {
      "number": 43,
      "type": "order",
      "stem": "주어진 글 (A)에 이어질 내용을 순서에 맞게 배열한 것은?",
      "options": [...],
      "answer": "정답 번호"
    },
    {
      "number": 44,
      "type": "reference",
      "stem": "밑줄 친 (a)~(e) 중에서 가리키는 대상이 나머지 넷과 다른 것은?",
      "underlined": [...],
      "answer": "정답 번호"
    },
    {
      "number": 45,
      "type": "content_match",
      "stem": "윗글의 내용과 일치하지 않는 것은?",
      "options": [...],
      "answer": "정답 번호"
    }
  ],
  "explanation": "해설"
}
```""",
        tips=["스토리가 있는 서사문 활용", "인물 간 관계 명확히"]
    ),
}

# 전체 문항 유형 통합
ALL_CSAT_QUESTIONS: Dict[str, CSATQuestionType] = {
    **LISTENING_QUESTIONS,
    **READING_QUESTIONS
}


# ============================================================================
# 도메인 설정 생성
# ============================================================================

def get_csat_case_library() -> CaseLibrary:
    """수능 문항 관련 테스트 케이스 라이브러리"""

    critical_cases = [
        CaseExample(
            question="수능 21번 함축 의미 추론 - 밑줄 친 'a double-edged sword'가 의미하는 바는?",
            expected_elements=["양면성", "장단점", "비유적 해석"],
            forbidden_elements=["문자적 의미", "실제 검", "무기"],
            category="21번 - 함축의미",
            difficulty="advanced_high"
        ),
        CaseExample(
            question="수능 32번 빈칸 추론 - 글의 핵심 개념을 빈칸에 넣기",
            expected_elements=["추상적 개념", "주제 연결", "논리적 추론"],
            forbidden_elements=["지문 직접 인용", "무관한 개념"],
            category="32번 - 빈칸추론",
            difficulty="advanced_high"
        ),
    ]

    common_cases = [
        CaseExample(
            question="수능 18번 목적 - 글을 쓴 목적 파악",
            expected_elements=["목적 명시", "편지/이메일 형식", "정답 도출 가능"],
            forbidden_elements=["모호한 목적", "다중 목적"],
            category="18번 - 목적",
            difficulty="intermediate_high"
        ),
        CaseExample(
            question="수능 36번 순서 배열 - 논리적 순서 파악",
            expected_elements=["연결어", "지시어", "논리적 흐름"],
            forbidden_elements=["순서 단서 없음", "모호한 연결"],
            category="36번 - 순서",
            difficulty="intermediate_high"
        ),
    ]

    return CaseLibrary(
        critical_cases=critical_cases,
        edge_cases=[],
        common_cases=common_cases
    )


def get_csat_english_domain_config() -> DomainConfig:
    """수능영어 문항번호별 생성 도메인 설정"""

    knowledge = DomainKnowledge(
        principles=[
            "수능 영어는 EBS 연계율 50% 이상을 유지한다",
            "문항별 배점(2점/3점)에 맞는 난이도를 유지한다",
            "듣기(17문항), 독해(28문항)의 구성을 따른다",
            "고난도 문항(21, 32-34번)은 변별력을 갖춘다",
            "문항 유형별 전형적인 발문 형식을 준수한다",
            "선택지는 매력적 오답(distractor)을 포함한다",
            "지문은 수험생 수준에 맞는 어휘와 문장 구조를 사용한다",
            "최신 교육과정과 평가원 출제 경향을 반영한다"
        ],

        constraints=[
            "정답이 2개 이상이거나 정답이 없는 문항 금지",
            "특정 배경지식이 있어야만 풀 수 있는 문항 지양",
            "문화적, 성별적, 지역적 편향 배제",
            "지나치게 길거나 복잡한 선택지 지양",
            "오답의 길이나 형식이 정답과 현저히 다른 것 금지",
            "저작권 문제가 있는 원문 그대로 사용 금지"
        ],

        quality_criteria=[
            QualityCriterion(
                name="유형 적합성",
                weight=0.25,
                description="해당 문항 번호의 유형에 맞는 문항인가",
                evaluation_prompt="이 문항이 수능 해당 번호 유형의 특성을 정확히 반영하고 있는가?"
            ),
            QualityCriterion(
                name="난이도 적절성",
                weight=0.20,
                description="배점(2점/3점)에 맞는 난이도인가",
                evaluation_prompt="문항의 난이도가 해당 배점에 적합한가?"
            ),
            QualityCriterion(
                name="발문 정확성",
                weight=0.15,
                description="수능 유형별 발문 형식을 따르고 있는가",
                evaluation_prompt="발문이 수능 기출 문항의 형식과 일치하는가?"
            ),
            QualityCriterion(
                name="선택지 질",
                weight=0.20,
                description="선택지가 적절하고 오답이 매력적인가",
                evaluation_prompt="오답 선택지들이 그럴듯하면서도 명확히 틀린가?"
            ),
            QualityCriterion(
                name="지문 적절성",
                weight=0.20,
                description="지문의 길이, 어휘, 주제가 적절한가",
                evaluation_prompt="지문이 수능 수준에 적합하고 문항 유형에 맞는가?"
            )
        ],

        thinking_styles=[
            "문항 번호별 특성 파악: 각 번호의 고유한 유형과 출제 의도 이해",
            "평가원 기출 분석: 최근 수능 및 모의평가 기출 경향 반영",
            "오답 설계: 학습자의 전형적 오류를 반영한 매력적 오답",
            "난이도 조절: 배점과 문항 위치에 따른 적절한 난이도",
            "EBS 연계: EBS 교재 지문 및 주제 활용 고려"
        ],

        expert_personas=[
            ExpertPersona(
                role="평가원 출제위원",
                focus="수능 출제 기준 및 가이드라인 준수",
                background="다년간 수능 출제 경험",
                thinking_approach="공정성, 변별력, 교육과정 연계"
            ),
            ExpertPersona(
                role="EBS 영어 강사",
                focus="EBS 교재와의 연계 및 학습자 이해",
                background="수능 강의 및 교재 집필 경험",
                thinking_approach="학생 입장에서의 문항 분석"
            ),
            ExpertPersona(
                role="고등학교 영어 교사",
                focus="교육 현장에서의 활용 가능성",
                background="수능 지도 경험",
                thinking_approach="학습 효과 및 피드백 가능성"
            )
        ],

        terminology={
            "발문": "문항의 질문 부분 (stem)",
            "지문": "읽기/듣기 자료 (passage/script)",
            "선택지": "답안 보기 (options)",
            "정답": "올바른 답 (key/answer)",
            "오답": "틀린 선택지 (distractor)",
            "고난도": "3점 문항, 변별력 있는 문항",
            "EBS 연계": "EBS 교재 지문/주제 활용"
        },

        patterns=[
            "문항 번호 선택 → 유형 확인 → 지문 작성 → 문항 및 선택지 개발",
            "듣기: 스크립트 작성 → 발문 설계 → 선택지 구성",
            "독해: 주제 선정 → 지문 작성 → 문항 유형별 발문 및 선택지",
            "고난도: 추상적 개념 → 비유적 표현 → 함축 의미 문항"
        ],

        anti_patterns=[
            "문항 번호와 맞지 않는 유형 출제",
            "배점에 맞지 않는 난이도",
            "수능 발문 형식과 다른 발문 사용",
            "정답 패턴이 있는 선택지 배치"
        ]
    )

    critique_template = """당신은 수능 영어 출제 전문가입니다. 다음 문항을 평가해주세요.

## 생성된 문항:
{instruction}

## 문항 예시:
{examples}

## 평가 관점:
1. **유형 적합성**: 해당 문항 번호의 유형에 맞는가?
2. **난이도**: 배점에 적합한 난이도인가?
3. **발문 정확성**: 수능 발문 형식을 따르는가?
4. **선택지 질**: 오답이 매력적인가?
5. **지문 적절성**: 수능 수준에 맞는가?

## 개선 제안:
"""

    refinement_template = """다음 비평을 바탕으로 수능 문항을 개선해주세요.

## 원본 문항:
{original_instruction}

## 비평:
{critique}

## 개선된 문항:
"""

    case_library = get_csat_case_library()

    return DomainConfig(
        domain_type="csat_english",
        domain_name="수능영어 문항번호별 생성",
        knowledge=knowledge,
        critique_template=critique_template,
        refinement_template=refinement_template,
        case_library=case_library,
        metadata={
            "version": "1.0.0",
            "author": "PromptWizard CSAT English Team",
            "last_updated": "2024-01",
            "total_items": 45,
            "listening_items": "1-17",
            "reading_items": "18-45",
            "high_difficulty_items": ["21", "32", "33", "34"],
            "question_types": list(ALL_CSAT_QUESTIONS.keys())
        },
        validators=[
            {
                "type": "KeywordValidator",
                "keywords": ["①", "②", "③", "④", "⑤", "정답"],
                "must_include": True,
                "min_matches": 2
            }
        ]
    )


# 도메인 설정 인스턴스
CSAT_ENGLISH_DOMAIN_CONFIG = get_csat_english_domain_config()

# Export
__all__ = [
    "CSAT_ENGLISH_DOMAIN_CONFIG",
    "get_csat_english_domain_config",
    "CSATQuestionType",
    "ALL_CSAT_QUESTIONS",
    "LISTENING_QUESTIONS",
    "READING_QUESTIONS",
]
