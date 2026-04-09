"""Hotel English Response Trainer (Streamlit).

Usage:
    streamlit run app/hotel_english_trainer.py
"""

from __future__ import annotations

import random
from dataclasses import dataclass

import streamlit as st


@dataclass(frozen=True)
class Scenario:
    topic: str
    guest_question: str
    model_answer: str
    alternatives: list[str]
    bad_option: str


SCENARIOS: list[Scenario] = [
    Scenario("Check-in", "Hi, I have a reservation under Kim.", "Welcome! May I see your passport, please? I’ll complete your check-in right away.", ["Certainly, Mr. Kim. May I see your ID, please?", "Welcome, Mr. Kim. Let me pull up your reservation and get your room ready.", "Of course. I can help you check in now if you share your passport."], "Wait there. I’m busy now."),
    Scenario("Check-in", "Could I check in early?", "Certainly. Let me check room availability, and I’ll do my best to arrange early check-in.", ["I’d be happy to check if an early check-in room is available.", "Yes, let me verify availability and update you in a moment.", "I’ll check our system now and see what we can do."], "No. Check-in time is check-in time."),
    Scenario("Check-in", "What time is breakfast?", "Breakfast is served from 6:30 to 10:00 a.m. on the second floor restaurant.", ["Breakfast runs from 6:30 to 10:00 a.m. at our restaurant on floor 2.", "Our breakfast service is available until 10:00 a.m. on weekdays.", "You can enjoy breakfast on the second floor starting at 6:30 a.m."], "I don’t know. Ask someone else."),
    Scenario("Room Request", "Can I get extra towels?", "Absolutely. I’ll have extra towels sent to your room right away.", ["Certainly, I’ll ask housekeeping to deliver them shortly.", "Of course. How many extra towels would you like?", "No problem, I can arrange that immediately."], "Get them yourself from housekeeping."),
    Scenario("Room Request", "The room is too cold.", "I’m sorry for the inconvenience. I can send engineering staff or help adjust the thermostat now.", ["I apologize. Let me help you fix the temperature right away.", "I’m sorry about that. I can send a staff member to assist immediately.", "Thank you for letting us know; we’ll make it comfortable for you."], "Then wear more clothes."),
    Scenario("Room Request", "Can I have a late checkout?", "Certainly. Late checkout is available until 1 p.m. today at no extra charge.", ["I’d be happy to arrange a late checkout for you.", "Yes, I can extend your checkout time to 1 p.m.", "Let me confirm availability for a late checkout."], "No, leave by 11. Rules are rules."),
    Scenario("Facilities", "Where is the gym?", "Our fitness center is on the 3rd floor and is open 24 hours.", ["The gym is on floor 3, just past the elevators.", "You can access the fitness center anytime; it’s open 24/7.", "It’s on the third floor. Please use your key card for entry."], "Somewhere in the building."),
    Scenario("Facilities", "Do you have airport shuttle service?", "Yes, we do. The shuttle departs every hour from the main entrance.", ["Certainly. Our airport shuttle leaves hourly from the lobby entrance.", "Yes, and I can reserve a seat for your preferred time.", "We provide shuttle service; may I help you book it?"], "Maybe. Check online."),
    Scenario("Facilities", "Is there a convenience store nearby?", "Yes, there’s one two blocks away. I can mark it on your map.", ["Certainly. It’s about a 3-minute walk from here.", "Yes, I can show you the quickest route.", "There is one nearby, and I can print directions for you."], "I’m not from this area."),
    Scenario("Transportation", "Can you call a taxi for me?", "Of course. May I know your destination so I can request the best route?", ["Certainly, I can call one now.", "Absolutely. A taxi should arrive in about 5 minutes.", "I’ll arrange it right away. Where are you heading?"], "Use your phone app."),
    Scenario("Tourist Info", "What places do you recommend nearby?", "If you like local culture, I recommend the city museum and riverside market.", ["I’d recommend the old town, the museum, and the night market.", "Certainly. May I suggest a few spots based on your interests?", "I can provide a short list with travel times."], "No idea. I never go out."),
    Scenario("Dining", "Can I book a table at your restaurant tonight?", "Certainly. May I have your preferred time and number of guests?", ["I’d be happy to reserve a table for you.", "Of course. What time would you like to dine?", "Yes, I can arrange that right now."], "Restaurant is full. Probably."),
    Scenario("Housekeeping", "Could you clean my room now?", "Certainly. I’ll inform housekeeping to prioritize your room immediately.", ["Of course. I’ll request immediate room service cleaning.", "I can arrange cleaning now; it should be done shortly.", "Absolutely. Would the next 20 minutes work for you?"], "Cleaning is only in the morning."),
    Scenario("Complaint", "The Wi-Fi is not working.", "I’m sorry for the trouble. Let me reset your connection and guide you through it.", ["I apologize for the inconvenience. I’ll assist right away.", "Thank you for reporting this. I’ll contact IT immediately.", "Let me help you reconnect step by step."], "Wi-Fi is usually fine, maybe your device."),
    Scenario("Complaint", "My room is noisy.", "I’m very sorry. I can offer a quieter room or provide earplugs right away.", ["I apologize. Let me check a quieter room for you.", "Thank you for telling us. We’ll resolve this promptly.", "I’m sorry for the disturbance; I can relocate you if you prefer."], "That’s normal in hotels."),
    Scenario("Billing", "Can you explain this charge on my bill?", "Certainly. Let me review the details with you line by line.", ["Of course. I’ll clarify each item on your invoice.", "I’d be happy to explain this charge in detail.", "Let me check the billing record and confirm for you."], "If it’s there, you have to pay."),
    Scenario("Billing", "Can I pay in a different currency?", "Yes, we support major currencies. I can confirm today’s exchange rate for you.", ["Certainly. We accept several currencies at today’s rate.", "Yes, I can show you the available payment options.", "Of course. Let me explain the conversion before payment."], "Only local currency. No exceptions."),
    Scenario("Checkout", "I need a receipt emailed to me.", "Certainly. Please share your email address, and I’ll send it immediately.", ["Of course. I can email the receipt right away.", "Yes, I’ll send a digital copy after checkout.", "Happy to help. Please confirm your email address."], "Printed receipt only."),
    Scenario("Emergency", "I lost my room key.", "No worries. I’ll issue a new key after verifying your identity.", ["Certainly. For security, may I see your ID first?", "I can help immediately and deactivate the lost key.", "Of course. I’ll provide a replacement key now."], "That’s your problem."),
    Scenario("General", "Can you store my luggage after checkout?", "Absolutely. We can store your luggage safely until this evening.", ["Yes, luggage storage is available at the front desk.", "Certainly. We’ll tag your bags and keep them secure.", "Of course. Please bring your bags here and we’ll assist you."], "No storage service."),
]


def init_state() -> None:
    if "answers" not in st.session_state:
        st.session_state.answers = {}
    if "attempts" not in st.session_state:
        st.session_state.attempts = {}


def evaluate_free_text(user_text: str, target: str) -> tuple[bool, str]:
    if not user_text.strip():
        return False, "응답이 비어 있어요. 핵심 표현을 1문장 이상 작성해보세요."

    key_tokens = [token.lower().strip(".,!?'") for token in target.split() if len(token) >= 5]
    user_lower = user_text.lower()
    matched = sum(1 for token in set(key_tokens) if token in user_lower)
    ratio = matched / max(1, len(set(key_tokens)))

    if ratio >= 0.35:
        return True, "좋아요! 핵심 표현이 충분히 포함되어 있어 자연스러운 응대입니다."
    if ratio >= 0.2:
        return False, "부분적으로 좋아요. 정중 표현과 구체적 안내(시간/행동)를 더 넣어보세요."
    return False, "핵심 표현 반영이 부족해요. 모범 답안을 참고해 다시 말해보세요."


def render_progress() -> None:
    total = len(SCENARIOS)
    solved = len(st.session_state.answers)
    correct = sum(1 for result in st.session_state.answers.values() if result)
    accuracy = (correct / solved * 100) if solved else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("완료 문항", f"{solved}/{total}")
    col2.metric("정확도", f"{accuracy:.1f}%")
    col3.metric("남은 문항", f"{total - solved}")
    st.progress(solved / total)


def build_choices(scenario: Scenario) -> list[str]:
    candidates = scenario.alternatives + [scenario.model_answer, scenario.bad_option]
    random.shuffle(candidates)
    return candidates[:4] if scenario.model_answer in candidates[:4] else [scenario.model_answer, *candidates[:3]]


def main() -> None:
    st.set_page_config(page_title="Hotel English Trainer", page_icon="🏨", layout="wide")
    init_state()

    st.title("🏨 호텔리어 고객 응대 영어 트레이너")
    st.caption("시나리오 기반으로 듣기/말하기 응대를 반복 훈련하고 즉시 피드백을 받으세요.")

    topics = sorted(set(s.topic for s in SCENARIOS))
    selected_topics = st.sidebar.multiselect("연습 주제", topics, default=topics)
    mode = st.sidebar.radio("훈련 모드", ["객관식", "자유응답/스피킹"]) 

    filtered = [s for s in SCENARIOS if s.topic in selected_topics]
    if not filtered:
        st.warning("선택된 주제가 없습니다. 사이드바에서 주제를 선택하세요.")
        return

    render_progress()

    selected_idx = st.selectbox(
        "시나리오 선택",
        range(len(filtered)),
        format_func=lambda i: f"[{filtered[i].topic}] {filtered[i].guest_question}",
    )
    scenario = filtered[selected_idx]

    st.subheader("👤 Guest says")
    st.info(scenario.guest_question)

    if mode == "객관식":
        options = build_choices(scenario)
        choice = st.radio("가장 적절한 응대를 고르세요.", options, key=f"mcq_{selected_idx}")
        if st.button("채점하기", key=f"grade_mcq_{selected_idx}"):
            is_correct = choice == scenario.model_answer or choice in scenario.alternatives
            st.session_state.answers[scenario.guest_question] = is_correct
            st.session_state.attempts[scenario.guest_question] = st.session_state.attempts.get(scenario.guest_question, 0) + 1
            if is_correct:
                st.success("정답입니다! 정중한 표현과 행동 제시가 좋습니다.")
            else:
                st.error("아쉬워요. 고객 응대에서는 공감 + 즉시 조치 표현이 중요합니다.")
            st.write("**모범 답안:**", scenario.model_answer)
    else:
        st.write("음성 입력을 지원하는 브라우저라면 아래 버튼으로 녹음할 수 있습니다.")
        audio_data = st.audio_input("응답 녹음 (선택)")
        if audio_data is not None:
            st.audio(audio_data)
            st.caption("현재 MVP에서는 음성 자동 채점 대신 텍스트 기반 피드백을 제공합니다.")

        text_answer = st.text_area("영어로 응답을 입력해 보세요.", height=120, key=f"free_{selected_idx}")
        if st.button("피드백 받기", key=f"feedback_{selected_idx}"):
            ok, feedback = evaluate_free_text(text_answer, scenario.model_answer)
            st.session_state.answers[scenario.guest_question] = ok
            st.session_state.attempts[scenario.guest_question] = st.session_state.attempts.get(scenario.guest_question, 0) + 1
            (st.success if ok else st.warning)(feedback)
            st.write("**추천 표현:**", scenario.model_answer)

    with st.expander("학습 팁"):
        st.markdown(
            """
            - 시작 문장: **Certainly / Of course / I’d be happy to help.**
            - 공감 표현: **I’m sorry for the inconvenience.**
            - 행동 제시: **Let me check / I’ll arrange that right away.**
            - 마무리 확인: **Would that work for you?**
            """
        )

    with st.expander("오답/취약 문항 보기"):
        weak = [q for q, result in st.session_state.answers.items() if not result]
        if weak:
            for item in weak:
                tries = st.session_state.attempts.get(item, 0)
                st.write(f"- {item} (시도 {tries}회)")
        else:
            st.write("아직 취약 문항이 없어요. 잘하고 있습니다! 🎉")


if __name__ == "__main__":
    main()
