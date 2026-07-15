
import random
from dataclasses import dataclass
from typing import Dict, List

import streamlit as st


st.set_page_config(
    page_title="Sigorta Ekosistemi",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)


st.markdown(
    """
    <style>
    .stApp {
        background:
            radial-gradient(circle at 10% 10%, rgba(56,189,248,.12), transparent 28%),
            radial-gradient(circle at 90% 10%, rgba(168,85,247,.12), transparent 28%),
            linear-gradient(145deg, #07111f, #0f172a 55%, #111827);
        color: #f8fafc;
    }

    .main .block-container {
        max-width: 1120px;
        padding-top: 1.6rem;
        padding-bottom: 3rem;
    }

    .hero {
        padding: 1.35rem 1.5rem;
        border-radius: 24px;
        background: linear-gradient(135deg, rgba(14,165,233,.18), rgba(124,58,237,.18));
        border: 1px solid rgba(125,211,252,.25);
        box-shadow: 0 18px 50px rgba(0,0,0,.22);
        margin-bottom: 1rem;
    }

    .hero h1 {
        margin: 0;
        font-size: 2.4rem;
        line-height: 1.05;
    }

    .hero p {
        margin: .7rem 0 0 0;
        color: #cbd5e1;
        font-size: 1rem;
    }

    .role-card, .scenario-card, .result-card, .score-card {
        border-radius: 20px;
        background: rgba(15,23,42,.78);
        border: 1px solid rgba(148,163,184,.16);
        box-shadow: 0 12px 30px rgba(0,0,0,.18);
    }

    .role-card {
        padding: 1.2rem 1.3rem;
        margin-bottom: 1rem;
    }

    .scenario-card {
        padding: 1.25rem 1.35rem;
        margin: .8rem 0 1rem 0;
        border-left: 5px solid #22d3ee;
    }

    .result-card {
        padding: 1.1rem 1.2rem;
        margin-top: 1rem;
    }

    .score-card {
        padding: .9rem 1rem;
        min-height: 112px;
    }

    .tag {
        display: inline-block;
        padding: .32rem .62rem;
        border-radius: 999px;
        margin-right: .35rem;
        margin-bottom: .35rem;
        background: rgba(34,211,238,.12);
        border: 1px solid rgba(34,211,238,.25);
        color: #a5f3fc;
        font-size: .78rem;
        font-weight: 700;
    }

    .role-title {
        font-size: 1.45rem;
        font-weight: 800;
        margin-bottom: .5rem;
    }

    .muted {
        color: #94a3b8;
    }

    div.stButton > button {
        width: 100%;
        min-height: 3.2rem;
        border-radius: 15px;
        border: 1px solid rgba(125,211,252,.26);
        background: linear-gradient(135deg, #0e7490, #6d28d9);
        color: white;
        font-weight: 750;
        box-shadow: 0 10px 24px rgba(0,0,0,.18);
    }

    div.stButton > button:hover {
        transform: translateY(-1px);
        border-color: rgba(255,255,255,.5);
    }

    [data-testid="stProgressBar"] > div > div {
        background: linear-gradient(90deg, #22d3ee, #8b5cf6);
    }

    .footer {
        text-align:center;
        color:#64748b;
        font-size:.78rem;
        margin-top:2rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@dataclass(frozen=True)
class Option:
    text: str
    result: str
    scores: Dict[str, int]


@dataclass(frozen=True)
class Scenario:
    title: str
    category: str
    story: str
    options: List[Option]
    lesson: str


ROLES = [
    {
        "name": "Sigorta Yaptıran Müşteri",
        "icon": "👤",
        "mission": "Karşılaşabileceğin riskleri değerlendirerek ihtiyacına uygun sigorta ürününü seçmek.",
        "expectation": "Açık bilgi, uygun prim, yeterli teminat ve adil hasar ödemesi.",
        "responsibility": "Doğru bilgi vermek, poliçeyi incelemek, primi ödemek ve hasarı zamanında bildirmek.",
        "function": "Prim ödeyerek ortak risk havuzuna katılır ve büyük mali kayıpları sigorta sistemine aktarır.",
        "badge": "Bilinçli Sigortalı",
    },
    {
        "name": "Sigorta Şirketi",
        "icon": "🏢",
        "mission": "Riskleri değerlendirerek poliçe düzenlemek ve geçerli hasarları karşılamak.",
        "expectation": "Müşterilerin doğru bilgi vermesi, primlerini ödemesi ve risk azaltıcı önlemlere uyması.",
        "responsibility": "Poliçe şartlarını açık belirlemek, yeterli fon bulundurmak ve geçerli hasarları zamanında ödemek.",
        "function": "Çok sayıda kişinin primini ortak havuzda toplar ve zarar yaşayan sigortalılara ödeme yapar.",
        "badge": "Adil Sigortacı",
    },
    {
        "name": "Aktüer",
        "icon": "📊",
        "mission": "Riskleri ölçmek ve risk düzeyine uygun primlerin belirlenmesine katkı sağlamak.",
        "expectation": "Doğru müşteri bilgileri, güvenilir geçmiş veriler ve düzenli hasar kayıtları.",
        "responsibility": "Gerçekçi varsayımlar kullanmak, riskleri adil değerlendirmek ve gelecekteki yükümlülükleri dikkate almak.",
        "function": "Risk ile prim arasında bilimsel ve sayısal bağlantı kurar.",
        "badge": "Risk Dedektifi",
    },
    {
        "name": "Reasürans Şirketi",
        "icon": "🌍",
        "mission": "Sigorta şirketlerinin üstlendiği büyük risklerin bir bölümünü devralmak.",
        "expectation": "Doğru risk bilgisi, güvenilir hasar verisi ve açık sözleşme koşulları.",
        "responsibility": "Devraldığı riskleri dikkatle değerlendirmek ve büyük hasarlarda sözleşmedeki payını karşılamak.",
        "function": "Büyük ve katastrofik riskleri daha geniş piyasalara dağıtarak sigorta şirketlerini korur.",
        "badge": "Reasürans Stratejisti",
    },
]


SCENARIOS = {
    "Sigorta Yaptıran Müşteri": [
        Scenario(
            "Sel Riskindeki Ev",
            "🌧️ Afet Riski",
            "Ayşe Hanım dere yatağına yakın bir bölgede ev satın aldı. Konutunu nasıl korumalı?",
            [
                Option("En ucuz poliçeyi seç", "Bir yıl sonra sel meydana geldi. Poliçede sel teminatı olmadığı için zarar karşılanmadı.", {"Risk Bilgisi": -10, "Müşteri Güveni": -5}),
                Option("Sel teminatı bulunan poliçeyi seç", "Sel hasarının büyük bölümü sigorta şirketi tarafından karşılandı.", {"Risk Bilgisi": 10, "Sistem Güvenliği": 5}),
                Option("Sigorta yaptırma", "Prim ödenmedi; ancak zarar gerçekleştiğinde bütün maliyet müşterinin üzerinde kaldı.", {"Risk Bilgisi": -10, "Sistem Güvenliği": -5}),
            ],
            "Poliçenin teminat kapsamı, prim tutarı kadar önemlidir.",
        ),
        Scenario(
            "Eski Otomobil",
            "🚗 Klasik Risk",
            "Mehmet Bey'in 12 yaşında ve piyasa değeri düşük bir otomobili vardır.",
            [
                Option("Yalnızca zorunlu trafik sigortası yaptır", "Üçüncü kişilere verilen zarar korunur; kendi araç hasarı korunmaz.", {"Risk Bilgisi": 5, "Sistem Güvenliği": 5}),
                Option("Dar kapsamlı kasko yaptır", "Aracın değeriyle uyumlu ve dengeli bir koruma sağlandı.", {"Risk Bilgisi": 10, "Adil Karar": 5}),
                Option("En geniş kapsamlı kaskoyu seç", "Geniş koruma sağlandı; fakat aracın değerine göre yüksek prim ödendi.", {"Risk Bilgisi": 3, "Adil Karar": -2}),
            ],
            "En kapsamlı poliçe her zaman en uygun ekonomik seçim olmayabilir.",
        ),
        Scenario(
            "Küçük İşletme",
            "🏪 Ticari Risk",
            "Bir kafe sahibi yangın, hırsızlık ve faaliyet kesintisi riskleriyle karşı karşıyadır.",
            [
                Option("Yalnızca yangın sigortası yaptır", "Yangın korundu; ancak diğer önemli riskler kapsam dışında kaldı.", {"Risk Bilgisi": 3, "Sistem Güvenliği": 2}),
                Option("Yangın ve hırsızlık teminatı al", "İşletmenin temel fiziksel riskleri daha kapsamlı korundu.", {"Risk Bilgisi": 10, "Sistem Güvenliği": 7}),
                Option("Sigorta yaptırmadan devam et", "Hırsızlık sonrası ekipman kaybının tamamı işletme sahibi tarafından karşılandı.", {"Risk Bilgisi": -10, "Sistem Güvenliği": -10}),
            ],
            "İşletmelerde birden fazla risk birlikte değerlendirilmelidir.",
        ),
        Scenario(
            "Sağlık Poliçesi",
            "🏥 Sağlık Riski",
            "Bir poliçe düşük primli ancak yüksek katılım paylı; diğeri daha pahalı ve daha kapsamlıdır.",
            [
                Option("Yalnızca düşük prime bak", "Tedavi gerektiğinde beklenenden daha fazla ödeme yapıldı.", {"Risk Bilgisi": -5, "Müşteri Güveni": -3}),
                Option("Kapsamlı poliçeyi seç", "Daha yüksek prim ödendi; tedavi masrafının daha büyük kısmı karşılandı.", {"Risk Bilgisi": 7, "Sistem Güvenliği": 4}),
                Option("Koşulları karşılaştır ve ihtiyaca uygun olanı seç", "Bütçe, ihtiyaç ve katılım payı birlikte değerlendirildi.", {"Risk Bilgisi": 12, "Adil Karar": 8}),
            ],
            "Bilinçli sigortalı, prim ve teminatı birlikte değerlendirir.",
        ),
        Scenario(
            "Veri İhlali",
            "💻 Siber Risk",
            "Bir e-ticaret işletmesi müşteri bilgilerinin çalınması ve satışların durması riskine karşı korunmak istiyor.",
            [
                Option("Siber sigorta yaptırma", "Veri ihlali sonrası hukuki giderler, müşteri kaybı ve iş durması işletmenin üzerinde kaldı.", {"Risk Bilgisi": -10, "Sistem Güvenliği": -8}),
                Option("Yalnızca temel teminat al", "Bazı teknik giderler karşılandı; iş durması ve hukuki giderler kapsam dışında kaldı.", {"Risk Bilgisi": 4, "Sistem Güvenliği": 2}),
                Option("Veri ihlali, iş durması ve hukuki giderleri kapsayan poliçeyi seç", "Siber olayın farklı mali sonuçlarına karşı daha geniş koruma sağlandı.", {"Risk Bilgisi": 12, "Sistem Güvenliği": 8}),
            ],
            "Siber olaylar yalnızca teknik zarar değil, gelir kaybı ve hukuki sorumluluk da doğurabilir.",
        ),
        Scenario(
            "Elektrikli Araç",
            "🔋 Yeni Nesil Risk",
            "Yeni bir elektrikli aracın batarya, şarj ve yazılım riskleri bulunuyor.",
            [
                Option("Geleneksel araç poliçesini aynen seç", "Bazı yeni teknoloji riskleri poliçe kapsamı dışında kaldı.", {"Risk Bilgisi": -5}),
                Option("Elektrikli araca özel teminatları incele", "Batarya ve şarj ekipmanı gibi özel riskler dikkate alındı.", {"Risk Bilgisi": 10, "Adil Karar": 5}),
                Option("Sigorta yaptırma", "Yüksek maliyetli batarya hasarı tamamen araç sahibine kaldı.", {"Risk Bilgisi": -10, "Sistem Güvenliği": -5}),
            ],
            "Yeni teknolojiler, yeni teminat ihtiyaçları oluşturabilir.",
        ),
    ],
    "Sigorta Şirketi": [
        Scenario(
            "Yangın Önlemi Olmayan Fabrika",
            "🔥 Klasik Risk",
            "Bir fabrika sigorta başvurusu yaptı; yangın alarmı ve söndürme sistemi bulunmuyor.",
            [
                Option("Riski aynı koşullarla kabul et", "Şirket prim kazandı; fakat büyük yangın riski kontrol edilmedi.", {"Sistem Güvenliği": -10, "Risk Bilgisi": -5}),
                Option("Güvenlik önlemi şartıyla kabul et", "Fabrika önlem aldı ve yangın riski azaldı.", {"Risk Bilgisi": 10, "Sistem Güvenliği": 10, "Adil Karar": 5}),
                Option("Başvuruyu doğrudan reddet", "Şirket riskten kaçındı; ancak risk azaltıcı çözüm sunmadı.", {"Sistem Güvenliği": 3, "Adil Karar": -5, "Müşteri Güveni": -5}),
            ],
            "Sigorta şirketi risk azaltıcı önlemleri teşvik ederek hem müşteriyi hem sistemi koruyabilir.",
        ),
        Scenario(
            "Şüpheli Hasar Bildirimi",
            "🔍 Hasar Süreci",
            "Bir müşteri poliçeyi aldıktan kısa süre sonra yüksek tutarlı hasar bildirdi.",
            [
                Option("Hasarı hemen reddet", "İnceleme yapılmadan verilen karar müşteri güvenini zedeledi.", {"Adil Karar": -10, "Müşteri Güveni": -10}),
                Option("Hasarı hemen öde", "Müşteri memnun oldu; ancak gerekli kontrol yapılmadı.", {"Müşteri Güveni": 4, "Sistem Güvenliği": -8}),
                Option("Eksper incelemesine gönder", "Hasarın nedeni ve tutarı kanıta dayalı biçimde incelendi.", {"Adil Karar": 10, "Risk Bilgisi": 7, "Sistem Güvenliği": 5}),
            ],
            "Hasar kararları varsayıma değil, inceleme ve kanıta dayanmalıdır.",
        ),
        Scenario(
            "Deprem Bölgesinde Yoğunlaşma",
            "🌍 Katastrofik Risk",
            "Şirket aynı deprem bölgesinde çok sayıda konut sigortaladı.",
            [
                Option("Yeni poliçe satışına sınırsız devam et", "Prim geliri arttı; ancak tek bir olayda çok sayıda hasar riski büyüdü.", {"Sistem Güvenliği": -12, "Risk Bilgisi": -7}),
                Option("Bölgedeki poliçeleri tamamen durdur", "Risk azaldı; fakat müşterilerin sigortaya erişimi zorlaştı.", {"Sistem Güvenliği": 5, "Adil Karar": -5, "Müşteri Güveni": -5}),
                Option("Riski reasürans şirketiyle paylaş", "Şirket hizmet vermeye devam ederken büyük kayıp riskinin bir kısmını devretti.", {"Sistem Güvenliği": 12, "Risk Bilgisi": 10}),
            ],
            "Aynı bölgede yoğunlaşan riskler reasürans yoluyla daha geniş alana dağıtılabilir.",
        ),
        Scenario(
            "Geciken Hasar Ödemesi",
            "🤝 Müşteri İlişkisi",
            "Geçerli olduğu belirlenen bir hasar dosyası uzun süredir bekliyor.",
            [
                Option("Dosyayı bekletmeye devam et", "Kısa vadede ödeme yapılmadı; müşteri güveni ciddi biçimde azaldı.", {"Müşteri Güveni": -12, "Adil Karar": -8}),
                Option("Müşteriye bilgi ver ve ödemeyi hızlandır", "Hasar süreci şeffaf biçimde tamamlandı.", {"Müşteri Güveni": 12, "Adil Karar": 10}),
                Option("Gerekçe göstermeden reddet", "Müşteri itiraz etti ve şirketin itibarı zarar gördü.", {"Müşteri Güveni": -15, "Adil Karar": -15, "Sistem Güvenliği": -5}),
            ],
            "Sigortacılığın temelinde verilen sözün yerine getirilmesi ve güven vardır.",
        ),
        Scenario(
            "Siber Güvenliği Zayıf İşletme",
            "💻 Siber Risk",
            "Bir işletme siber sigorta istiyor; düzenli yedekleme ve çok faktörlü doğrulama kullanmıyor.",
            [
                Option("Riski doğrudan kabul et", "Şirket önlem almadan sigortalandı ve hasar olasılığı yüksek kaldı.", {"Risk Bilgisi": -8, "Sistem Güvenliği": -8}),
                Option("Güvenlik önlemleri şartıyla kabul et", "İşletme siber güvenliğini güçlendirdi ve risk azaldı.", {"Risk Bilgisi": 12, "Sistem Güvenliği": 10, "Adil Karar": 5}),
                Option("Başvuruyu incelemeden reddet", "Riskten kaçınıldı; ancak çözüm geliştirilemedi.", {"Adil Karar": -4, "Müşteri Güveni": -4}),
            ],
            "Siber sigorta, güvenlik önlemlerinin geliştirilmesini teşvik edebilir.",
        ),
        Scenario(
            "Tedarik Zinciri Kesintisi",
            "🚚 Küresel Risk",
            "Bir üretici, ana tedarikçisinin faaliyetinin durması nedeniyle üretim kaybı yaşayabilir.",
            [
                Option("Bu riski hiç dikkate alma", "Dolaylı iş durması riski poliçe dışında kaldı.", {"Risk Bilgisi": -10}),
                Option("Tedarikçi bağımlılığını incele", "İş kesintisi riski daha doğru değerlendirildi.", {"Risk Bilgisi": 10, "Sistem Güvenliği": 8}),
                Option("Her işletmeye aynı poliçeyi ver", "İşletmeler arasındaki farklı tedarik bağımlılıkları gözden kaçtı.", {"Risk Bilgisi": -7, "Adil Karar": -4}),
            ],
            "Modern işletme riskleri yalnızca fiziksel varlıklardan kaynaklanmaz.",
        ),
    ],
    "Aktüer": [
        Scenario(
            "İki Farklı Sürücü",
            "🚗 Klasik Risk",
            "Bir sürücü 15 yıldır kazasız; diğerinin son iki yılda üç kazası var.",
            [
                Option("İkisine aynı prim uygula", "Risk düzeyleri farklı olmasına rağmen aynı fiyat uygulandı.", {"Risk Bilgisi": -8, "Adil Karar": -5}),
                Option("Kazası fazla olana daha yüksek prim öner", "Prim geçmiş hasar deneyimiyle uyumlu hâle geldi.", {"Risk Bilgisi": 10, "Sistem Güvenliği": 6}),
                Option("Kazasız sürücüye daha yüksek prim uygula", "Daha düşük riskli müşteri haksız biçimde cezalandırıldı.", {"Risk Bilgisi": -12, "Adil Karar": -10}),
            ],
            "Prim belirlenirken riskle ilişkili geçmiş bilgiler dikkate alınabilir.",
        ),
        Scenario(
            "Yeni ve Eski Bina",
            "🏠 Klasik Risk",
            "Yeni binada yangın alarmı var; eski binada güvenlik önlemi bulunmuyor.",
            [
                Option("İki bina aynı risk düzeyindedir", "Yapısal özellikler ve önlemler dikkate alınmadı.", {"Risk Bilgisi": -8}),
                Option("Yeni bina daha yüksek risklidir", "Risk azaltıcı önlemler yanlış değerlendirildi.", {"Risk Bilgisi": -10}),
                Option("Eski bina daha yüksek risklidir", "Binanın yaşı ve güvenlik önlemleri birlikte değerlendirildi.", {"Risk Bilgisi": 10, "Sistem Güvenliği": 5}),
            ],
            "Risk azaltıcı önlemler, hasar olasılığını ve prim düzeyini etkiler.",
        ),
        Scenario(
            "Sel Bölgesindeki İşyeri",
            "🌧️ Afet Riski",
            "Bir işyeri sık sık sel yaşanan bir bölgede bulunuyor.",
            [
                Option("Düşük risk olarak değerlendir", "Prim beklenen zararı karşılamayabilir.", {"Risk Bilgisi": -10, "Sistem Güvenliği": -8}),
                Option("Orta risk olarak değerlendir", "Risk kısmen dikkate alındı.", {"Risk Bilgisi": 3}),
                Option("Yüksek risk ve özel şart öner", "Prim ve koşullar risk düzeyine uygun belirlendi.", {"Risk Bilgisi": 10, "Sistem Güvenliği": 7}),
            ],
            "Hasar olasılığı arttıkça prim ve poliçe şartları değişebilir.",
        ),
        Scenario(
            "Primler Hasarları Karşılamıyor",
            "📉 Finansal Risk",
            "Şirketin topladığı primler uzun süredir hasar ödemelerine yetmiyor.",
            [
                Option("Primleri daha da düşür", "Müşteri sayısı artabilir; ödeme gücü daha da zayıflar.", {"Sistem Güvenliği": -12, "Risk Bilgisi": -10}),
                Option("Hasar ve risk verilerini yeniden incele", "Yetersiz fiyatlamanın nedeni belirlenir.", {"Risk Bilgisi": 12, "Sistem Güvenliği": 10}),
                Option("Hasarları ödememeye başla", "Şirket sözleşme yükümlülüğünü ihlal eder.", {"Adil Karar": -15, "Müşteri Güveni": -15, "Sistem Güvenliği": -10}),
            ],
            "Yeterli prim, sigorta sisteminin hasar ödeme kapasitesi için gereklidir.",
        ),
        Scenario(
            "Siber Güvenlik Düzeyi",
            "💻 Siber Risk",
            "Bir işletme düzenli yedekleme ve personel eğitimi yapıyor; diğer işletme hiçbir önlem almıyor.",
            [
                Option("İkisine aynı prim uygula", "Güvenlik düzeyleri arasındaki fark dikkate alınmadı.", {"Risk Bilgisi": -8, "Adil Karar": -5}),
                Option("Önlem almayan işletmeye daha yüksek prim öner", "Fiyatlama risk azaltıcı önlemleri dikkate aldı.", {"Risk Bilgisi": 12, "Sistem Güvenliği": 8}),
                Option("Güvenli işletmeye daha yüksek prim uygula", "Risk azaltan işletme haksız biçimde cezalandırıldı.", {"Risk Bilgisi": -12, "Adil Karar": -10}),
            ],
            "Siber sigorta fiyatlamasında güvenlik önlemleri ve geçmiş olaylar önemlidir.",
        ),
        Scenario(
            "İklim Riskindeki Artış",
            "🌡️ Yeni Nesil Risk",
            "Son yıllarda aşırı yağış ve dolu hasarlarının sıklığı artıyor.",
            [
                Option("Eski verileri hiç değiştirmeden kullan", "Değişen risk koşulları fiyatlamaya yansıtılmadı.", {"Risk Bilgisi": -10, "Sistem Güvenliği": -8}),
                Option("Yeni eğilimleri ve güncel verileri incele", "Prim ve rezervler değişen risk düzeyine göre güncellendi.", {"Risk Bilgisi": 12, "Sistem Güvenliği": 10}),
                Option("Bütün müşterilere aynı artışı uygula", "Risk farkları gözetilmeden genel bir fiyatlama yapıldı.", {"Risk Bilgisi": -3, "Adil Karar": -6}),
            ],
            "Aktüeryal değerlendirme değişen çevresel koşullara uyum sağlamalıdır.",
        ),
    ],
    "Reasürans Şirketi": [
        Scenario(
            "Büyük Fabrika",
            "🔥 Büyük Risk",
            "Bir sigorta şirketi çok yüksek bedelli bir fabrikayı reasüransa devretmek istiyor.",
            [
                Option("Riskin tamamını kabul et", "Tek bir büyük riske aşırı bağımlılık oluştu.", {"Sistem Güvenliği": -8, "Risk Bilgisi": -5}),
                Option("Riskin belirli bir bölümünü kabul et", "Risk dengeli biçimde paylaşıldı.", {"Sistem Güvenliği": 10, "Risk Bilgisi": 10}),
                Option("İnceleme yapmadan reddet", "Uygun paylaşım fırsatı değerlendirilmedi.", {"Risk Bilgisi": -3, "Adil Karar": -3}),
            ],
            "Reasüransın temel amacı büyük riskleri uygun oranlarda paylaşmaktır.",
        ),
        Scenario(
            "Deprem Portföyü",
            "🌍 Katastrofik Risk",
            "Bir sigorta şirketinin çok sayıda poliçesi aynı deprem bölgesinde bulunuyor.",
            [
                Option("Her poliçeyi tamamen bağımsız değerlendir", "Tek bir olayda hepsinin hasar görebileceği gözden kaçtı.", {"Risk Bilgisi": -12, "Sistem Güvenliği": -10}),
                Option("Bölgesel yoğunlaşma riskini dikkate al", "Olası toplam kayıp daha gerçekçi değerlendirildi.", {"Risk Bilgisi": 12, "Sistem Güvenliği": 10}),
                Option("Yalnızca poliçe sayısına bak", "Poliçelerin aynı olaydan etkilenme ihtimali dikkate alınmadı.", {"Risk Bilgisi": -8}),
            ],
            "Çok sayıda küçük risk, aynı olayda birleşerek büyük kayıp yaratabilir.",
        ),
        Scenario(
            "Büyük Enerji Tesisi",
            "⚡ Küresel Risk",
            "Bir enerji tesisinin riski tek bir reasürans şirketinin taşıma kapasitesini aşıyor.",
            [
                Option("Riski başka reasürörlerle paylaş", "Risk uluslararası piyasalara dağıtıldı.", {"Sistem Güvenliği": 12, "Risk Bilgisi": 10}),
                Option("Riski tek başına taşı", "Büyük bir hasar mali yapıyı ciddi biçimde zorlayabilir.", {"Sistem Güvenliği": -12}),
                Option("Hasar gerçekleşince karar ver", "Koruma hasardan önce kurulmadığı için işe yaramadı.", {"Risk Bilgisi": -12, "Sistem Güvenliği": -10}),
            ],
            "Reasürans koruması hasar gerçekleşmeden önce sözleşmeyle kurulmalıdır.",
        ),
        Scenario(
            "Eksik Risk Bilgisi",
            "📄 Bilgi Riski",
            "Sigorta şirketi devretmek istediği risk hakkında yeterli bilgi sunmadı.",
            [
                Option("Riski hemen kabul et", "Üstlenilen yükümlülüğün büyüklüğü tam bilinmedi.", {"Risk Bilgisi": -10, "Sistem Güvenliği": -8}),
                Option("Ek bilgi ve risk raporu iste", "Risk güvenilir bilgiler üzerinden değerlendirildi.", {"Risk Bilgisi": 12, "Sistem Güvenliği": 8}),
                Option("Rastgele bir fiyat belirle", "Reasürans bedeli gerçek riskle uyumsuz kaldı.", {"Risk Bilgisi": -12, "Adil Karar": -5}),
            ],
            "Sigorta ve reasürans kararları eksiksiz ve doğru bilgiye dayanmalıdır.",
        ),
        Scenario(
            "Ortak Bulut Hizmeti",
            "☁️ Siber Risk",
            "Binlerce işletme aynı bulut hizmetini kullanıyor ve ortak bir siber saldırı riski taşıyor.",
            [
                Option("Her işletmeyi tamamen bağımsız değerlendir", "Ortak altyapıdan doğan toplu zarar riski gözden kaçtı.", {"Risk Bilgisi": -12, "Sistem Güvenliği": -10}),
                Option("Ortak altyapı yoğunlaşmasını dikkate al", "Tek saldırının çok sayıda sigortalıyı etkileyebileceği hesaba katıldı.", {"Risk Bilgisi": 12, "Sistem Güvenliği": 10}),
                Option("Yalnızca müşteri sayısına bak", "Teknolojik bağımlılık ve ortak hata noktası değerlendirilmedi.", {"Risk Bilgisi": -8}),
            ],
            "Tek bir siber olay, aynı altyapıyı kullanan çok sayıda sigortalıyı aynı anda etkileyebilir.",
        ),
        Scenario(
            "Küresel Fidye Yazılımı",
            "🧩 Küresel Siber Risk",
            "Aynı fidye yazılımı birçok ülkedeki işletmeleri aynı anda etkiliyor.",
            [
                Option("Riski yalnızca ülke bazında değerlendir", "Saldırının sınır ötesi etkisi yeterince görülmedi.", {"Risk Bilgisi": -8}),
                Option("Küresel birikimli zararı dikkate al ve paylaş", "Risk farklı reasürörler arasında dağıtıldı.", {"Risk Bilgisi": 12, "Sistem Güvenliği": 12}),
                Option("Hasar ihtimalini önemsiz say", "Büyük ve eş zamanlı zarar riski küçümsendi.", {"Risk Bilgisi": -12, "Sistem Güvenliği": -10}),
            ],
            "Siber riskler sınır tanımayabilir ve küresel risk paylaşımı gerektirebilir.",
        ),
    ],
}


DEFAULT_SCORES = {
    "Risk Bilgisi": 50,
    "Adil Karar": 50,
    "Sistem Güvenliği": 50,
    "Müşteri Güveni": 50,
}

if "started" not in st.session_state:
    st.session_state.started = False
if "player_name" not in st.session_state:
    st.session_state.player_name = ""
if "role_index" not in st.session_state:
    st.session_state.role_index = 0
if "scenario_index" not in st.session_state:
    st.session_state.scenario_index = 0
if "scores" not in st.session_state:
    st.session_state.scores = DEFAULT_SCORES.copy()
if "answered" not in st.session_state:
    st.session_state.answered = False
if "selected_option" not in st.session_state:
    st.session_state.selected_option = None
if "role_intro_seen" not in st.session_state:
    st.session_state.role_intro_seen = False
if "badges" not in st.session_state:
    st.session_state.badges = []


def clamp(value: int) -> int:
    return max(0, min(100, value))


def reset_game():
    st.session_state.started = False
    st.session_state.player_name = ""
    st.session_state.role_index = 0
    st.session_state.scenario_index = 0
    st.session_state.scores = DEFAULT_SCORES.copy()
    st.session_state.answered = False
    st.session_state.selected_option = None
    st.session_state.role_intro_seen = False
    st.session_state.badges = []
    st.rerun()


def score_cards():
    cols = st.columns(4)
    icons = ["🧠", "⚖️", "🛡️", "🤝"]
    for col, icon, (name, value) in zip(cols, icons, st.session_state.scores.items()):
        with col:
            st.markdown(
                f"""
                <div class="score-card">
                    <div class="muted">{icon} {name}</div>
                    <div style="font-size:1.7rem;font-weight:800;margin-top:.35rem;">{value}/100</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


if not st.session_state.started:
    st.markdown(
        """
        <div class="hero">
            <h1>🛡️ Sigorta Ekosistemi</h1>
            <p>Aynı riski farklı tarafların gözünden değerlendir ve sigorta sisteminin nasıl çalıştığını keşfet.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4 = st.columns(4)
    for col, role in zip([c1, c2, c3, c4], ROLES):
        with col:
            st.markdown(
                f"""
                <div class="role-card">
                    <div style="font-size:2rem;">{role['icon']}</div>
                    <div class="role-title">{role['name']}</div>
                    <div class="muted">{role['mission']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("### Nasıl oynanır?")
    st.write(
        "Dört rolü sırayla tamamla. Her rolde altı kısa senaryo göreceksin. "
        "Üç seçenekten birini seç, sonucu oku ve puanlarını geliştir."
    )

    player = st.text_input("Adın veya öğrenci numaran", placeholder="Örn. Ayşe Yılmaz")
    if st.button("Oyuna Başla"):
        st.session_state.player_name = player.strip() or "Öğrenci"
        st.session_state.started = True
        st.rerun()

    st.stop()


role = ROLES[st.session_state.role_index]
role_scenarios = SCENARIOS[role["name"]]

total_steps = len(ROLES) * 6
completed_steps = st.session_state.role_index * 6 + st.session_state.scenario_index
st.progress(completed_steps / total_steps)

st.markdown(
    f"""
    <div class="hero">
        <h1>{role['icon']} {role['name']}</h1>
        <p>{st.session_state.player_name} · Rol {st.session_state.role_index + 1}/4 · Senaryo {st.session_state.scenario_index + 1}/6</p>
    </div>
    """,
    unsafe_allow_html=True,
)

score_cards()

if not st.session_state.role_intro_seen:
    st.markdown(
        f"""
        <div class="role-card">
            <div class="role-title">Rol Kartı</div>
            <p><b>Görevin:</b> {role['mission']}</p>
            <p><b>Beklentin:</b> {role['expectation']}</p>
            <p><b>Sorumluluğun:</b> {role['responsibility']}</p>
            <p><b>Sistemdeki işlevin:</b> {role['function']}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Rolü Anladım, Senaryolara Geç"):
        st.session_state.role_intro_seen = True
        st.rerun()
    st.stop()


scenario = role_scenarios[st.session_state.scenario_index]

st.markdown(
    f"""
    <div class="scenario-card">
        <span class="tag">{scenario.category}</span>
        <h2 style="margin:.4rem 0 .6rem 0;">{scenario.title}</h2>
        <p style="font-size:1.05rem;color:#e2e8f0;">{scenario.story}</p>
    </div>
    """,
    unsafe_allow_html=True,
)

if not st.session_state.answered:
    st.markdown("### Kararın ne olur?")
    for idx, option in enumerate(scenario.options):
        if st.button(option.text, key=f"opt_{st.session_state.role_index}_{st.session_state.scenario_index}_{idx}"):
            st.session_state.selected_option = idx
            for score_name, delta in option.scores.items():
                st.session_state.scores[score_name] = clamp(
                    st.session_state.scores[score_name] + delta
                )
            st.session_state.answered = True
            st.rerun()
else:
    option = scenario.options[st.session_state.selected_option]
    score_text = " · ".join(
        [f"{name} {delta:+d}" for name, delta in option.scores.items()]
    )

    st.markdown(
        f"""
        <div class="result-card">
            <div class="role-title">Kararının sonucu</div>
            <p>{option.result}</p>
            <p><b>Puan etkisi:</b> {score_text}</p>
            <p><b>Öğrenme mesajı:</b> {scenario.lesson}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("Sonraki Senaryo"):
        st.session_state.answered = False
        st.session_state.selected_option = None
        st.session_state.scenario_index += 1

        if st.session_state.scenario_index >= 6:
            if role["badge"] not in st.session_state.badges:
                st.session_state.badges.append(role["badge"])

            st.session_state.role_index += 1
            st.session_state.scenario_index = 0
            st.session_state.role_intro_seen = False

            if st.session_state.role_index >= len(ROLES):
                st.session_state.role_index = len(ROLES)

        st.rerun()


if st.session_state.role_index >= len(ROLES):
    st.markdown(
        """
        <div class="hero">
            <h1>🏆 Sigorta Ekosistemi Tamamlandı</h1>
            <p>Dört farklı rolü tamamladın ve sigorta sisteminin nasıl birlikte çalıştığını gördün.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    score_cards()
    average_score = round(sum(st.session_state.scores.values()) / 4)

    if average_score >= 80:
        title = "Sigorta Ekosistemi Ustası"
    elif average_score >= 65:
        title = "Güçlü Risk Yöneticisi"
    else:
        title = "Sigorta Kaşifi"

    st.success(f"Genel unvanın: **{title}**")

    st.markdown("### Kazandığın rozetler")
    for badge in st.session_state.badges:
        st.write(f"🏅 {badge}")

    st.info(
        "Sigorta sistemi; müşteriler, sigorta şirketleri, aktüerler ve reasürans şirketlerinin "
        "birbirini tamamlayan görevleri sayesinde çalışır. Risk değerlendirilir, primlerle ortak "
        "bir fon oluşturulur ve büyük zararlar taraflar arasında paylaşılır."
    )

    if st.button("Oyunu Yeniden Başlat"):
        reset_game()


st.markdown(
    """
    <div class="footer">
        Eğitim amaçlı hazırlanmıştır. Senaryolar gerçek poliçe veya fiyatlama tavsiyesi değildir.
    </div>
    """,
    unsafe_allow_html=True,
)
