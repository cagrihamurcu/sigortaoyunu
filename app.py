
import random
from dataclasses import dataclass
from typing import Dict, List

import pandas as pd
import plotly.graph_objects as go
import streamlit as st


# ------------------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------------------
st.set_page_config(
    page_title="Sigorta Ekosistemi | Yönetim Simülasyonu",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ------------------------------------------------------------
# VISUAL DESIGN
# ------------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background:
            radial-gradient(circle at 15% 10%, rgba(34,211,238,.10), transparent 28%),
            radial-gradient(circle at 85% 15%, rgba(139,92,246,.13), transparent 30%),
            linear-gradient(145deg, #07111f 0%, #0b1728 55%, #111827 100%);
        color: #f8fafc;
    }

    [data-testid="stSidebar"] {
        background: rgba(7, 17, 31, .96);
        border-right: 1px solid rgba(148,163,184,.14);
    }

    .hero {
        padding: 1.35rem 1.5rem;
        border-radius: 24px;
        background: linear-gradient(135deg, rgba(14,165,233,.18), rgba(124,58,237,.18));
        border: 1px solid rgba(125,211,252,.22);
        box-shadow: 0 18px 50px rgba(0,0,0,.22);
        margin-bottom: 1rem;
    }

    .hero h1 {
        margin: 0;
        font-size: clamp(2rem, 4vw, 3.5rem);
        line-height: 1.02;
        letter-spacing: -0.045em;
        background: linear-gradient(90deg, #ffffff, #67e8f9, #c4b5fd);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero p {
        margin: .75rem 0 0 0;
        color: #cbd5e1;
        font-size: 1.03rem;
        max-width: 900px;
    }

    .glass-card {
        min-height: 132px;
        padding: 1rem 1.05rem;
        border-radius: 20px;
        background: rgba(15, 23, 42, .70);
        border: 1px solid rgba(148,163,184,.15);
        box-shadow: 0 12px 28px rgba(0,0,0,.18);
        backdrop-filter: blur(12px);
    }

    .glass-card .label {
        color: #94a3b8;
        font-size: .78rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: .08em;
    }

    .glass-card .value {
        margin-top: .35rem;
        color: #f8fafc;
        font-size: 1.75rem;
        font-weight: 800;
        letter-spacing: -.035em;
    }

    .glass-card .sub {
        margin-top: .2rem;
        color: #cbd5e1;
        font-size: .82rem;
    }

    .event-card {
        padding: 1.1rem 1.25rem;
        border-radius: 20px;
        background: linear-gradient(135deg, rgba(30,41,59,.94), rgba(15,23,42,.90));
        border-left: 5px solid #22d3ee;
        box-shadow: 0 14px 35px rgba(0,0,0,.20);
        margin: .5rem 0 1rem 0;
    }

    .event-card h3 {
        margin: 0 0 .35rem 0;
        color: #f8fafc;
    }

    .event-card p {
        color: #cbd5e1;
        margin: 0;
    }

    .lesson-chip {
        display: inline-block;
        padding: .35rem .62rem;
        border-radius: 999px;
        margin: .15rem .2rem .15rem 0;
        background: rgba(34,211,238,.11);
        border: 1px solid rgba(34,211,238,.24);
        color: #a5f3fc;
        font-size: .78rem;
        font-weight: 600;
    }

    .feedback-good {
        padding: .85rem 1rem;
        border-radius: 16px;
        background: rgba(16,185,129,.12);
        border: 1px solid rgba(52,211,153,.26);
        color: #d1fae5;
    }

    .feedback-warn {
        padding: .85rem 1rem;
        border-radius: 16px;
        background: rgba(245,158,11,.12);
        border: 1px solid rgba(251,191,36,.26);
        color: #fef3c7;
    }

    .feedback-bad {
        padding: .85rem 1rem;
        border-radius: 16px;
        background: rgba(239,68,68,.12);
        border: 1px solid rgba(248,113,113,.26);
        color: #fee2e2;
    }

    div.stButton > button {
        border-radius: 14px;
        border: 1px solid rgba(103,232,249,.32);
        background: linear-gradient(135deg, #0891b2, #6d28d9);
        color: white;
        font-weight: 750;
        min-height: 3rem;
        box-shadow: 0 10px 22px rgba(8,145,178,.18);
        transition: all .18s ease;
    }

    div.stButton > button:hover {
        transform: translateY(-2px);
        border-color: rgba(255,255,255,.55);
        box-shadow: 0 14px 28px rgba(109,40,217,.25);
    }

    [data-testid="stMetric"] {
        background: rgba(15,23,42,.64);
        border: 1px solid rgba(148,163,184,.13);
        padding: .85rem;
        border-radius: 16px;
    }

    [data-testid="stProgressBar"] > div > div {
        background: linear-gradient(90deg, #22d3ee, #8b5cf6);
    }

    .small-note {
        color: #94a3b8;
        font-size: .78rem;
    }

    .footer {
        text-align: center;
        color: #64748b;
        font-size: .76rem;
        padding: 2rem 0 1rem 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ------------------------------------------------------------
# GAME DATA
# ------------------------------------------------------------
@dataclass(frozen=True)
class Scenario:
    title: str
    description: str
    claim_multiplier: float
    demand_shift: float
    market_return: float
    trust_shift: float
    lesson: str
    institution: str


SCENARIOS: List[Scenario] = [
    Scenario(
        "Sakin Piyasa",
        "Hasar frekansı beklentilere yakın. Müşteriler fiyat ve hizmet kalitesini karşılaştırıyor.",
        0.90, 0.03, 0.018, 1.0,
        "Risk havuzlama ve doğru fiyatlama normal dönemlerde görünür hâle gelir.",
        "Sigorta şirketi",
    ),
    Scenario(
        "Bölgesel Sel",
        "Bir bölgede yoğun yağışlar konut ve işyeri hasarlarını artırdı.",
        1.42, 0.10, -0.006, -1.0,
        "Katastrofik olaylar risk yoğunlaşmasını ve reasürans ihtiyacını gösterir.",
        "Reasürans şirketi",
    ),
    Scenario(
        "Siber Saldırı Dalgası",
        "KOBİ müşterilerinde fidye yazılımı vakaları hızla yayılıyor.",
        1.25, 0.14, 0.008, 0.0,
        "Yeni risklerde veri yetersizliği primlendirmeyi ve teminat tasarımını zorlaştırır.",
        "Aktüer ve broker",
    ),
    Scenario(
        "Faizlerde Yükseliş",
        "Tahvil getirileri yükseldi; yatırım portföyü için yeni fırsatlar oluştu.",
        0.95, -0.01, 0.032, 0.0,
        "Sigortacılar yalnızca risk üstlenmez; aynı zamanda kurumsal yatırımcıdır.",
        "Finansal piyasalar",
    ),
    Scenario(
        "Sosyal Medyada Hasar Krizi",
        "Geciken bir hasar dosyası sosyal medyada geniş yankı buldu.",
        1.02, -0.08, 0.006, -8.0,
        "Hasar yönetimi, tüketici güveni ve kurum itibarı sigortanın sürekliliği için kritiktir.",
        "Eksper ve hasar birimi",
    ),
    Scenario(
        "Düzenleyici Stres Testi",
        "Otorite, sermaye yeterliliği ve teknik karşılıklar için kapsamlı inceleme başlattı.",
        1.00, 0.00, 0.004, 0.0,
        "Düzenleme ve denetim, sigortalıların haklarını ve sistemin ödeme gücünü korur.",
        "Düzenleyici otorite",
    ),
    Scenario(
        "Deprem Senaryosu",
        "Düşük olasılıklı fakat yüksek şiddetli bir deprem çok sayıda poliçeyi etkiledi.",
        2.05, 0.18, -0.020, -2.0,
        "Büyük risklerin ulusal ve uluslararası reasürans kapasitesiyle paylaşılması gerekir.",
        "DASK ve reasürans piyasası",
    ),
    Scenario(
        "Sağlık Enflasyonu",
        "Tedavi maliyetleri beklenenden hızlı arttı; sağlık branşında hasar maliyeti yükseliyor.",
        1.32, -0.03, 0.010, -1.0,
        "Primlerin geçmiş veriye değil, beklenen gelecekteki maliyetlere göre belirlenmesi gerekir.",
        "Aktüerya birimi",
    ),
    Scenario(
        "Acentelerden Büyüme Hamlesi",
        "Acenteler yeni müşteri kazanmak için kampanya desteği talep ediyor.",
        0.98, 0.12, 0.009, 1.0,
        "Dağıtım kanalları sigorta bilincinin ve penetrasyonun artmasında etkilidir.",
        "Sigorta acenteleri",
    ),
    Scenario(
        "Kredi Daralması",
        "Bankalar kredi standartlarını sıkılaştırdı; teminat niteliği taşıyan sigortalara ilgi arttı.",
        1.03, 0.05, -0.008, 0.0,
        "Sigorta, kredi sistemini ve ekonomik faaliyetlerin devamlılığını destekler.",
        "Bankalar ve finansal sistem",
    ),
]

QUIZ = [
    {
        "q": "Sigorta şirketinin üstlendiği riskin bir bölümünü başka bir kuruma devretmesine ne ad verilir?",
        "options": ["Koasürans", "Reasürans", "Subrogasyon", "Arbitraj"],
        "answer": "Reasürans",
        "explanation": "Reasürans, sigorta şirketinin taşıdığı riskin bir bölümünü başka bir sigortacıya veya reasüröre devretmesidir.",
    },
    {
        "q": "Sigorta sözleşmesini yapan ve genellikle primi ödeyen taraf hangisidir?",
        "options": ["Lehtar", "Sigortalı", "Sigorta ettiren", "Eksper"],
        "answer": "Sigorta ettiren",
        "explanation": "Sigorta ettiren sözleşmenin tarafıdır; sigortalı ve lehtar aynı ya da farklı kişiler olabilir.",
    },
    {
        "q": "Aşağıdakilerden hangisi sigortacılığın finansal sistem içindeki rolüdür?",
        "options": [
            "Yalnızca hasar tespiti yapmak",
            "Uzun vadeli fonları sermaye piyasalarına aktarmak",
            "Para basmak",
            "Vergi oranlarını belirlemek",
        ],
        "answer": "Uzun vadeli fonları sermaye piyasalarına aktarmak",
        "explanation": "Sigorta ve emeklilik fonları, topladıkları kaynakları finansal varlıklara yönlendirerek piyasaları derinleştirir.",
    },
    {
        "q": "Hasarın nedenini ve parasal büyüklüğünü teknik olarak inceleyen uzman kimdir?",
        "options": ["Aktüer", "Broker", "Eksper", "Lehtar"],
        "answer": "Eksper",
        "explanation": "Eksper hasarın nedenini, kapsamını ve tutarını inceler; tazminat kararının teknik girdisini sağlar.",
    },
    {
        "q": "Sermaye yeterliliğini çok düşük tutmanın temel sonucu nedir?",
        "options": [
            "Şirketin ödeme gücü riskinin artması",
            "Her zaman daha yüksek müşteri güveni",
            "Hasarların tamamen ortadan kalkması",
            "Prim ihtiyacının sona ermesi",
        ],
        "answer": "Şirketin ödeme gücü riskinin artması",
        "explanation": "Yetersiz sermaye ve rezerv, beklenmeyen hasarlarda yükümlülüklerin karşılanmasını zorlaştırır.",
    },
]


# ------------------------------------------------------------
# STATE
# ------------------------------------------------------------
DEFAULTS: Dict = {
    "started": False,
    "company_name": "Pusula Sigorta",
    "round": 1,
    "max_rounds": 10,
    "capital": 100.0,
    "reserve": 45.0,
    "customers": 10000,
    "trust": 72.0,
    "solvency": 150.0,
    "score": 0,
    "xp": 0,
    "streak": 0,
    "history": [],
    "event": None,
    "feedback": "",
    "feedback_type": "good",
    "quiz_index": 0,
    "quiz_score": 0,
    "quiz_answered": False,
    "achievements": [],
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value.copy() if isinstance(value, list) else value


def reset_game():
    for key, value in DEFAULTS.items():
        st.session_state[key] = value.copy() if isinstance(value, list) else value
    st.rerun()


def current_level() -> int:
    return 1 + st.session_state.xp // 250


def money(value: float) -> str:
    return f"{value:,.1f} mn TL".replace(",", "X").replace(".", ",").replace("X", ".")


def choose_event():
    st.session_state.event = random.choice(SCENARIOS)


def add_achievement(name: str):
    if name not in st.session_state.achievements:
        st.session_state.achievements.append(name)
        st.toast(f"🏆 Yeni başarı: {name}", icon="🎉")


def decision_engine(
    premium_level: int,
    reinsurance: int,
    reserve_ratio: int,
    service_quality: int,
    investment_risk: int,
):
    event = st.session_state.event

    # Demand: high premiums reduce demand; service and trust increase it.
    pricing_effect = (55 - premium_level) / 190
    service_effect = (service_quality - 50) / 210
    trust_effect = (st.session_state.trust - 65) / 420
    growth_rate = event.demand_shift + pricing_effect + service_effect + trust_effect
    growth_rate = max(-0.22, min(0.26, growth_rate))

    old_customers = st.session_state.customers
    new_customers = max(2500, int(old_customers * (1 + growth_rate)))

    # Financial flows in million TL.
    exposure = new_customers / 10000
    premium_income = exposure * (premium_level / 50) * 15.5

    base_claim = exposure * 8.2 * event.claim_multiplier
    mitigation = 1 - (service_quality - 50) / 500
    gross_claim = max(1.0, base_claim * mitigation)

    ceded_share = reinsurance / 100
    reinsurance_cost = premium_income * ceded_share * 0.33
    recovered_claim = gross_claim * ceded_share * 0.76
    net_claim = gross_claim - recovered_claim

    operating_cost = 2.1 + exposure * (service_quality / 100) * 2.3
    investable_funds = max(0, st.session_state.reserve + premium_income - reinsurance_cost)
    investment_return = investable_funds * (
        event.market_return + ((investment_risk - 50) / 100) * 0.028
    )

    underwriting_result = premium_income - net_claim - reinsurance_cost - operating_cost
    period_result = underwriting_result + investment_return

    target_reserve = premium_income * (reserve_ratio / 100)
    reserve_change = (target_reserve - st.session_state.reserve) * 0.36
    new_reserve = max(3.0, st.session_state.reserve + reserve_change + max(period_result, 0) * 0.18)

    new_capital = st.session_state.capital + period_result - max(0, reserve_change) * 0.08

    # Trust and solvency.
    claim_pressure = gross_claim / max(premium_income, 0.1)
    trust_delta = event.trust_shift
    trust_delta += (service_quality - 55) / 9
    trust_delta -= max(0, premium_level - 68) / 8
    trust_delta -= max(0, claim_pressure - 0.95) * 6
    new_trust = max(0.0, min(100.0, st.session_state.trust + trust_delta))

    required_capital = max(25.0, new_customers / 10000 * 48 + gross_claim * 1.25)
    solvency = max(0.0, min(300.0, ((new_capital + new_reserve * 0.52) / required_capital) * 100))

    # Balanced decision score.
    round_score = 0
    round_score += int(max(-35, min(35, period_result * 3.2)))
    round_score += int((new_trust - 55) * 0.55)
    round_score += int((solvency - 100) * 0.24)
    round_score += 12 if 15 <= reinsurance <= 45 else -5
    round_score += 10 if 45 <= reserve_ratio <= 75 else -8
    round_score = max(-50, min(100, round_score))

    st.session_state.capital = new_capital
    st.session_state.reserve = new_reserve
    st.session_state.customers = new_customers
    st.session_state.trust = new_trust
    st.session_state.solvency = solvency
    st.session_state.score += round_score
    st.session_state.xp += max(15, round_score + 45)
    st.session_state.streak = st.session_state.streak + 1 if round_score >= 35 else 0

    st.session_state.history.append(
        {
            "Dönem": st.session_state.round,
            "Olay": event.title,
            "Müşteri": new_customers,
            "Prim Geliri": round(premium_income, 2),
            "Brüt Hasar": round(gross_claim, 2),
            "Net Hasar": round(net_claim, 2),
            "Dönem Sonucu": round(period_result, 2),
            "Sermaye": round(new_capital, 2),
            "Rezerv": round(new_reserve, 2),
            "Güven": round(new_trust, 1),
            "Solvency": round(solvency, 1),
            "Puan": round_score,
        }
    )

    if solvency >= 145 and new_trust >= 75 and period_result > 0:
        feedback_type = "good"
        feedback = (
            f"⚡ Dengeli yönetim! {event.institution} ile ilişkileri doğru yönettiniz. "
            f"Dönem sonucu {money(period_result)}, güven {new_trust:.0f}/100 ve ödeme gücü %{solvency:.0f}."
        )
    elif solvency < 100:
        feedback_type = "bad"
        feedback = (
            f"🚨 Sermaye alarmı! Ödeme gücü oranı %{solvency:.0f}'a düştü. "
            "Daha güçlü rezerv, kontrollü büyüme veya uygun reasürans koruması gerekiyor."
        )
    elif new_trust < 55:
        feedback_type = "bad"
        feedback = (
            f"📣 İtibar riski yükseldi. Güven {new_trust:.0f}/100 seviyesinde. "
            "Sigortacılıkta finansal sonuç kadar adil fiyatlama ve hasar hizmeti de önemlidir."
        )
    else:
        feedback_type = "warn"
        feedback = (
            f"🧭 Şirket ayakta, fakat dengeniz kırılgan. Dönem sonucu {money(period_result)}, "
            f"güven {new_trust:.0f}/100 ve ödeme gücü %{solvency:.0f}."
        )

    st.session_state.feedback = feedback
    st.session_state.feedback_type = feedback_type

    if st.session_state.streak >= 3:
        add_achievement("Üç Dönemlik İstikrar")
    if st.session_state.solvency >= 180:
        add_achievement("Güçlü Bilanço")
    if st.session_state.trust >= 88:
        add_achievement("Sigortalının Güveni")
    if reinsurance >= 25 and event.claim_multiplier >= 1.4:
        add_achievement("Reasürans Ustası")

    st.session_state.round += 1
    choose_event()


# ------------------------------------------------------------
# SIDEBAR
# ------------------------------------------------------------
with st.sidebar:
    st.markdown("## 🛡️ Sigorta Ekosistemi")
    st.caption("Yönetim simülasyonu · Lisans düzeyi")

    if not st.session_state.started:
        company = st.text_input("Şirketinizin adı", value=st.session_state.company_name)
        rounds = st.select_slider("Oyun uzunluğu", options=[6, 8, 10, 12], value=10)
        if st.button("🚀 Simülasyonu Başlat", use_container_width=True):
            st.session_state.company_name = company.strip() or "Pusula Sigorta"
            st.session_state.max_rounds = rounds
            st.session_state.started = True
            choose_event()
            st.rerun()
    else:
        st.markdown(f"### {st.session_state.company_name}")
        st.caption(f"Seviye {current_level()} · {st.session_state.xp} XP")
        level_progress = (st.session_state.xp % 250) / 250
        st.progress(level_progress)
        st.caption(f"Sonraki seviyeye {250 - (st.session_state.xp % 250)} XP")

        st.divider()
        st.markdown("#### 🎯 Görev")
        st.write(
            "Şirketi büyütürken ödeme gücünü, müşteri güvenini ve toplumsal korumayı birlikte yönet."
        )

        st.markdown("#### 🏆 Başarılar")
        if st.session_state.achievements:
            for badge in st.session_state.achievements:
                st.markdown(f"✅ {badge}")
        else:
            st.caption("Henüz başarı rozeti kazanılmadı.")

        st.divider()
        if st.button("🔄 Oyunu Sıfırla", use_container_width=True):
            reset_game()


# ------------------------------------------------------------
# LANDING SCREEN
# ------------------------------------------------------------
if not st.session_state.started:
    st.markdown(
        """
        <div class="hero">
            <h1>Bir sigorta şirketini yönetebilir misiniz?</h1>
            <p>
                Primleri belirleyin, riskleri reasüre edin, teknik karşılıkları yönetin,
                hasar krizlerini çözün ve finansal sistemi ayakta tutun.
                Her kararınız müşterileri, kurumları ve bilançoyu etkiler.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4 = st.columns(4)
    landing_cards = [
        ("🏢", "Kurumları keşfet", "Sigorta şirketi, reasürör, acente, broker, eksper, aktüer ve düzenleyici."),
        ("⚖️", "Denge kur", "Kârlılık, güven, rezerv, büyüme ve ödeme gücü aynı anda yönetilir."),
        ("🌪️", "Şoklara hazırlan", "Sel, deprem, siber risk, sağlık enflasyonu ve piyasa hareketleri."),
        ("🎓", "Karardan öğren", "Her turun sonunda kavramsal ve finansal geri bildirim alın."),
    ]
    for col, (icon, title, text) in zip([c1, c2, c3, c4], landing_cards):
        with col:
            st.markdown(
                f"""
                <div class="glass-card">
                    <div class="value">{icon}</div>
                    <div style="font-weight:800; margin:.25rem 0;">{title}</div>
                    <div class="sub">{text}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("### Oyun nasıl işler?")
    st.markdown(
        """
        <span class="lesson-chip">1 · Piyasa olayını analiz et</span>
        <span class="lesson-chip">2 · Beş yönetim kararı al</span>
        <span class="lesson-chip">3 · Finansal sonucu gör</span>
        <span class="lesson-chip">4 · Kurumsal ilişkiyi öğren</span>
        <span class="lesson-chip">5 · Yeni döneme geç</span>
        """,
        unsafe_allow_html=True,
    )
    st.info("Başlamak için sol menüden şirket adını yazın ve **Simülasyonu Başlat** düğmesine basın.")
    st.stop()


# ------------------------------------------------------------
# END GAME
# ------------------------------------------------------------
if st.session_state.round > st.session_state.max_rounds:
    st.markdown(
        f"""
        <div class="hero">
            <h1>Sezon tamamlandı.</h1>
            <p>{st.session_state.company_name} için yönetim kuruluna sunulacak sonuçlar hazır.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    final_score = st.session_state.score
    if final_score >= st.session_state.max_rounds * 50:
        rank = "Sistem Mimarı"
        message = "Kârlılık, güven ve ödeme gücünü birlikte yöneterek sürdürülebilir bir sigorta sistemi kurdunuz."
    elif final_score >= st.session_state.max_rounds * 25:
        rank = "Dengeli Sigortacı"
        message = "Şirketi başarıyla yönettiniz; bazı dönemlerde daha güçlü risk dengesi kurulabilirdi."
    else:
        rank = "Risk Çırağı"
        message = "Simülasyon tamamlandı. Yeni oyunda rezerv, reasürans ve müşteri güvenini daha dengeli yönetin."

    a, b, c, d = st.columns(4)
    a.metric("Yönetici unvanı", rank)
    b.metric("Toplam puan", final_score)
    c.metric("Son sermaye", money(st.session_state.capital))
    d.metric("Müşteri güveni", f"{st.session_state.trust:.0f}/100")

    st.success(message)

    if st.session_state.history:
        hist = pd.DataFrame(st.session_state.history)
        col_chart, col_table = st.columns([1.15, 1])
        with col_chart:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=hist["Dönem"], y=hist["Sermaye"],
                mode="lines+markers", name="Sermaye"
            ))
            fig.add_trace(go.Scatter(
                x=hist["Dönem"], y=hist["Rezerv"],
                mode="lines+markers", name="Rezerv"
            ))
            fig.update_layout(
                title="Finansal gelişim",
                template="plotly_dark",
                height=390,
                margin=dict(l=20, r=20, t=55, b=20),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                legend=dict(orientation="h", y=1.1),
            )
            st.plotly_chart(fig, use_container_width=True)
        with col_table:
            st.dataframe(
                hist[["Dönem", "Olay", "Dönem Sonucu", "Güven", "Solvency", "Puan"]],
                use_container_width=True,
                hide_index=True,
            )

        csv = hist.to_csv(index=False).encode("utf-8-sig")
        st.download_button(
            "📥 Sonuçları CSV olarak indir",
            csv,
            file_name="sigorta_simulasyonu_sonuclari.csv",
            mime="text/csv",
            use_container_width=True,
        )

    if st.button("🎮 Yeni Bir Sezon Başlat", use_container_width=True):
        reset_game()
    st.stop()


# ------------------------------------------------------------
# MAIN DASHBOARD
# ------------------------------------------------------------
st.markdown(
    f"""
    <div class="hero">
        <h1>{st.session_state.company_name}</h1>
        <p>Dönem {st.session_state.round}/{st.session_state.max_rounds} · Riskleri yönetin, güveni koruyun, sistemi büyütün.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

m1, m2, m3, m4, m5 = st.columns(5)
metric_data = [
    ("💰 Sermaye", money(st.session_state.capital), "Beklenmeyen kayıplara tampon"),
    ("🏦 Teknik rezerv", money(st.session_state.reserve), "Gelecekteki hasar yükümlülüğü"),
    ("👥 Sigortalı", f"{st.session_state.customers:,}".replace(",", "."), "Risk havuzunun büyüklüğü"),
    ("🤝 Güven", f"{st.session_state.trust:.0f}/100", "Müşteri ve kamu itibarı"),
    ("🧱 Ödeme gücü", f"%{st.session_state.solvency:.0f}", "Hedef: %120 ve üzeri"),
]
for col, (label, value, sub) in zip([m1, m2, m3, m4, m5], metric_data):
    with col:
        st.markdown(
            f"""
            <div class="glass-card">
                <div class="label">{label}</div>
                <div class="value">{value}</div>
                <div class="sub">{sub}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

tab_game, tab_map, tab_lab, tab_quiz = st.tabs(
    ["🎮 Yönetim Masası", "🕸️ Sistem Haritası", "📊 Analiz Laboratuvarı", "🧠 Bilgi Arenası"]
)


# ------------------------------------------------------------
# TAB 1: GAME
# ------------------------------------------------------------
with tab_game:
    event = st.session_state.event
    st.markdown(
        f"""
        <div class="event-card">
            <h3>⚡ Dönemin olayı: {event.title}</h3>
            <p>{event.description}</p>
            <div style="margin-top:.7rem;">
                <span class="lesson-chip">Odaktaki kurum: {event.institution}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    left, right = st.columns([1.25, .75], gap="large")

    with left:
        st.subheader("Yönetim kararları")
        st.caption("Her kararın bir faydası ve fırsat maliyeti vardır.")

        premium_level = st.slider(
            "1. Ortalama prim düzeyi",
            min_value=30,
            max_value=90,
            value=55,
            help="Düşük prim talebi artırabilir; fakat hasarları karşılamak zorlaşabilir.",
        )
        reinsurance = st.slider(
            "2. Reasüransa devredilen risk (%)",
            min_value=0,
            max_value=70,
            value=25,
            help="Reasürans büyük hasarlara karşı korur; buna karşılık maliyeti vardır.",
        )
        reserve_ratio = st.slider(
            "3. Hedef teknik karşılık oranı (%)",
            min_value=20,
            max_value=95,
            value=60,
            help="Yüksek rezerv güvenliği artırır; fakat serbest sermayeyi sınırlar.",
        )
        service_quality = st.slider(
            "4. Hasar hizmeti ve müşteri deneyimi",
            min_value=20,
            max_value=100,
            value=65,
            help="Daha iyi hizmet güven yaratır; operasyon maliyetini yükseltir.",
        )
        investment_risk = st.slider(
            "5. Yatırım portföyü risk düzeyi",
            min_value=0,
            max_value=100,
            value=40,
            help="Yüksek risk daha yüksek getiri potansiyeli ve daha büyük oynaklık yaratır.",
        )

        if st.button("⚙️ Kararları Uygula ve Dönemi Kapat", use_container_width=True):
            decision_engine(
                premium_level,
                reinsurance,
                reserve_ratio,
                service_quality,
                investment_risk,
            )
            st.rerun()

    with right:
        st.subheader("Karar radarı")
        radar_values = [
            premium_level,
            reinsurance / 70 * 100,
            reserve_ratio,
            service_quality,
            investment_risk,
        ]
        radar_labels = ["Prim", "Reasürans", "Rezerv", "Hizmet", "Yatırım riski"]
        fig = go.Figure(
            data=go.Scatterpolar(
                r=radar_values + [radar_values[0]],
                theta=radar_labels + [radar_labels[0]],
                fill="toself",
                name="Karar profili",
            )
        )
        fig.update_layout(
            template="plotly_dark",
            height=360,
            margin=dict(l=20, r=20, t=35, b=20),
            paper_bgcolor="rgba(0,0,0,0)",
            polar=dict(
                bgcolor="rgba(15,23,42,.35)",
                radialaxis=dict(visible=True, range=[0, 100]),
            ),
            showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("#### Bu olayın öğretim mesajı")
        st.info(event.lesson)

        if st.session_state.feedback:
            css_class = {
                "good": "feedback-good",
                "warn": "feedback-warn",
                "bad": "feedback-bad",
            }[st.session_state.feedback_type]
            st.markdown(
                f'<div class="{css_class}">{st.session_state.feedback}</div>',
                unsafe_allow_html=True,
            )


# ------------------------------------------------------------
# TAB 2: SYSTEM MAP
# ------------------------------------------------------------
with tab_map:
    st.subheader("Sigorta sisteminin aktörleri ve değer akışı")
    st.caption("Bir aktöre ait kartı açarak görevini ve diğer taraflarla ilişkisini inceleyin.")

    institutions = {
        "🏢 Sigorta Şirketi": (
            "Prim karşılığında riski üstlenir, poliçe düzenler ve hasar gerçekleştiğinde tazminat öder.",
            "Sigortalı, acente, broker, eksper, aktüer, reasürör ve düzenleyiciyle bağlantılıdır.",
        ),
        "🌍 Reasürans Şirketi": (
            "Sigortacının üstlendiği riskin bir bölümünü devralır; katastrofik kayıpların paylaşılmasını sağlar.",
            "Yerel riskleri uluslararası risk havuzlarına ve sermayeye bağlar.",
        ),
        "🤝 Acente": (
            "Sigorta şirketi adına ürünleri tanıtır, satış ve müşteri iletişimi yürütür.",
            "Sigorta şirketini temsil eden temel dağıtım kanallarından biridir.",
        ),
        "🧭 Broker": (
            "Müşterinin risklerini analiz eder ve uygun sigorta çözümünü bulmaya çalışır.",
            "Esas olarak sigorta ettirenin menfaatini temsil eder.",
        ),
        "🔍 Eksper": (
            "Hasarın nedenini, kapsamını ve parasal büyüklüğünü teknik olarak inceler.",
            "Adil ve kanıta dayalı tazminat sürecine katkı sağlar.",
        ),
        "📐 Aktüer": (
            "Olasılık, istatistik ve finans yöntemleriyle prim, rezerv ve uzun vadeli yükümlülükleri hesaplar.",
            "Riskin ölçülmesi ile finansal sürdürülebilirlik arasında köprü kurar.",
        ),
        "⚖️ Düzenleyici Otorite": (
            "Mali yeterlilik, tüketici koruması ve piyasa disiplinini gözetir.",
            "Sigortalıların haklarını ve sistemin istikrarını korur.",
        ),
        "👤 Sigorta Ettiren / Sigortalı": (
            "Sigorta ettiren sözleşmeyi kurar ve primi öder; sigortalının ekonomik menfaati koruma altındadır.",
            "Aynı kişi olabilecekleri gibi farklı kişiler de olabilirler.",
        ),
        "🎯 Lehtar / Üçüncü Kişi": (
            "Lehtar sigorta bedelini almaya hak kazanır; zarar gören üçüncü kişi sorumluluk sigortalarında korunabilir.",
            "Sigorta sözleşmesinin etkisi yalnızca sigorta ettirenle sınırlı değildir.",
        ),
        "📈 Finansal Piyasalar": (
            "Primlerden oluşan fonların tahvil, hisse ve diğer varlıklara yönelmesini sağlar.",
            "Sigorta şirketleri kurumsal yatırımcı olarak uzun vadeli fon arz eder.",
        ),
    }

    c1, c2 = st.columns(2)
    for idx, (name, (role, relation)) in enumerate(institutions.items()):
        target = c1 if idx % 2 == 0 else c2
        with target:
            with st.expander(name):
                st.write(role)
                st.caption(relation)

    st.markdown("### Temel değer döngüsü")
    st.code(
        "Prim → Risk Havuzu → Teknik Karşılık ve Yatırım → Hasar Tespiti → Tazminat → Ekonomik Devamlılık",
        language=None,
    )


# ------------------------------------------------------------
# TAB 3: ANALYTICS
# ------------------------------------------------------------
with tab_lab:
    st.subheader("Şirket performansı ve finansal sistem göstergeleri")

    if not st.session_state.history:
        st.info("İlk dönemi tamamladığınızda grafikler burada oluşacak.")
    else:
        hist = pd.DataFrame(st.session_state.history)

        chart1, chart2 = st.columns(2)
        with chart1:
            fig_fin = go.Figure()
            fig_fin.add_trace(go.Scatter(
                x=hist["Dönem"], y=hist["Sermaye"],
                mode="lines+markers", name="Sermaye"
            ))
            fig_fin.add_trace(go.Scatter(
                x=hist["Dönem"], y=hist["Rezerv"],
                mode="lines+markers", name="Teknik rezerv"
            ))
            fig_fin.update_layout(
                title="Bilanço dayanıklılığı",
                template="plotly_dark",
                height=350,
                margin=dict(l=20, r=20, t=55, b=20),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                legend=dict(orientation="h", y=1.12),
            )
            st.plotly_chart(fig_fin, use_container_width=True)

        with chart2:
            fig_sys = go.Figure()
            fig_sys.add_trace(go.Scatter(
                x=hist["Dönem"], y=hist["Güven"],
                mode="lines+markers", name="Müşteri güveni"
            ))
            fig_sys.add_trace(go.Scatter(
                x=hist["Dönem"], y=hist["Solvency"],
                mode="lines+markers", name="Ödeme gücü"
            ))
            fig_sys.add_hline(y=120, line_dash="dash", annotation_text="Solvency referansı")
            fig_sys.update_layout(
                title="Güven ve ödeme gücü",
                template="plotly_dark",
                height=350,
                margin=dict(l=20, r=20, t=55, b=20),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                legend=dict(orientation="h", y=1.12),
            )
            st.plotly_chart(fig_sys, use_container_width=True)

        st.dataframe(hist, use_container_width=True, hide_index=True)

        latest = hist.iloc[-1]
        st.markdown("### Son dönemin finansal yorumu")
        loss_ratio = latest["Net Hasar"] / max(latest["Prim Geliri"], .01) * 100
        combined_proxy = (
            latest["Net Hasar"] + max(0, latest["Prim Geliri"] * 0.20)
        ) / max(latest["Prim Geliri"], .01) * 100

        x1, x2, x3 = st.columns(3)
        x1.metric("Yaklaşık net hasar/prim", f"%{loss_ratio:.1f}")
        x2.metric("Basitleştirilmiş birleşik oran", f"%{combined_proxy:.1f}")
        x3.metric("Dönem puanı", f"{latest['Puan']:+.0f}")

        st.caption(
            "Bu göstergeler eğitim amacıyla basitleştirilmiştir; gerçek şirket analizinde branş, dönem, "
            "kazanılmış prim, teknik karşılık, gider ve sermaye düzenlemeleri ayrıntılı biçimde ele alınır."
        )


# ------------------------------------------------------------
# TAB 4: QUIZ
# ------------------------------------------------------------
with tab_quiz:
    st.subheader("Bilgi Arenası")
    st.caption("Doğru yanıtlar oyun puanınıza ve XP seviyenize katkı sağlar.")

    q_index = st.session_state.quiz_index
    if q_index >= len(QUIZ):
        st.success(
            f"Arena tamamlandı: {st.session_state.quiz_score}/{len(QUIZ)} doğru."
        )
        if st.session_state.quiz_score == len(QUIZ):
            add_achievement("Sigorta Bilgesi")
        if st.button("Bilgi Arenasını Yeniden Başlat"):
            st.session_state.quiz_index = 0
            st.session_state.quiz_score = 0
            st.session_state.quiz_answered = False
            st.rerun()
    else:
        question = QUIZ[q_index]
        st.markdown(f"### Soru {q_index + 1}/{len(QUIZ)}")
        st.write(question["q"])

        choice = st.radio(
            "Yanıtınız",
            question["options"],
            index=None,
            key=f"quiz_{q_index}",
        )

        if not st.session_state.quiz_answered:
            if st.button("Yanıtı Kontrol Et", disabled=choice is None):
                st.session_state.quiz_answered = True
                if choice == question["answer"]:
                    st.session_state.quiz_score += 1
                    st.session_state.score += 20
                    st.session_state.xp += 35
                st.rerun()
        else:
            if choice == question["answer"]:
                st.success(f"Doğru! {question['explanation']}")
            else:
                st.error(
                    f"Doğru yanıt: {question['answer']}. {question['explanation']}"
                )

            if st.button("Sonraki Soru →"):
                st.session_state.quiz_index += 1
                st.session_state.quiz_answered = False
                st.rerun()


st.markdown(
    """
    <div class="footer">
        Eğitim amaçlı simülasyon · Sayısal sonuçlar gerçek sigorta tarifesi veya mali yeterlilik hesabı değildir.
    </div>
    """,
    unsafe_allow_html=True,
)

