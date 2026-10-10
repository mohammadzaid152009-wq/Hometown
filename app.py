import html
from datetime import datetime

import streamlit as st

st.set_page_config(page_title="Hometown Hub", page_icon="🌳", layout="centered")

# ---------- Assets (hosted on the original Lovable site; swap for your own if they change) ----------
BASE = "https://hometownhubdigitalplatform.lovable.app/assets/"
HERO_IMG = BASE + "community-courtyard-bwrNGhLM.jpg"
HARVEST_IMG = BASE + "harvest-festival-CYo67_M8.jpg"
LAKE_IMG = BASE + "lake-cleanup-uWgSECuv.jpg"

# ---------- Styling ----------
st.markdown(
    """
<style>
:root { --accent:#b5532c; --green:#3f6b4f; --cream:#faf5ec; --ink:#2b2a26; --muted:#7a746a; }
.stApp { background: var(--cream); }
html, body, [class*="css"] { color: var(--ink); }
h1, h2, h3 { font-family: Georgia, 'Times New Roman', serif !important; letter-spacing: -0.01em; }
.brand { font-family: Georgia, serif; font-size: 1.6rem; font-weight: 700; color: var(--accent); margin: 0; }
.tagline { color: var(--muted); margin-top: -6px; font-size: 0.9rem; }
.eyebrow { text-transform: uppercase; letter-spacing: .12em; font-size: .75rem; color: var(--green); font-weight: 600; }
.card { background:#fff; border:1px solid #eadfcc; border-radius:16px; padding:16px 18px; margin-bottom:10px; box-shadow:0 1px 3px rgba(0,0,0,.04); }
.avatar { display:inline-flex; width:38px; height:38px; border-radius:50%; background:var(--green); color:#fff;
          align-items:center; justify-content:center; font-weight:600; margin-right:10px; }
.author { font-weight:600; }
.meta { color: var(--muted); font-size:.82rem; }
.tag { display:inline-block; font-size:.68rem; letter-spacing:.1em; font-weight:700; color:var(--accent);
       background:#f6e3d8; padding:2px 8px; border-radius:999px; margin:10px 0 6px; }
.date { background:#f6e3d8; color:var(--accent); border-radius:12px; text-align:center; padding:6px 12px; min-width:58px; }
.date b { display:block; font-size:1.3rem; line-height:1.1; }
.date span { font-size:.7rem; letter-spacing:.1em; }
.stButton > button { border-radius:999px; border:1px solid #d9c9ad; }
.stButton > button[kind="primary"] { background:var(--accent); border-color:var(--accent); color:#fff; }
</style>
""",
    unsafe_allow_html=True,
)

# ---------- State ----------
if "posts" not in st.session_state:
    st.session_state.posts = [
        {
            "id": 1, "author": "Meera Rao", "time": "2h", "circle": "Shivamogga Circle",
            "tag": "ANNOUNCEMENT",
            "text": "The annual Holehonnur harvest gathering is this Sunday. Bring one family recipe and a story from home — everyone is welcome.",
            "image": HARVEST_IMG, "likes": 84, "liked": False, "comments": [],
            "comment_base": 12,
        },
        {
            "id": 2, "author": "Arjun Hegde", "time": "5h", "circle": "Shivamogga Circle",
            "tag": "COMMUNITY",
            "text": "Forty-two volunteers showed up for the Tunga lake clean-up today. This is what hometown spirit looks like. Thank you, neighbors!",
            "image": LAKE_IMG, "likes": 126, "liked": False, "comments": [],
            "comment_base": 18,
        },
    ]
    st.session_state.next_id = 3

if "events" not in st.session_state:
    st.session_state.events = [
        {"id": 1, "day": "22", "mon": "SEP", "title": "Harvest stories evening", "where": "Town Library", "time": "5:30 PM", "going": False},
        {"id": 2, "day": "25", "mon": "SEP", "title": "Lake clean-up drive", "where": "Tunga Ghat", "time": "7:00 AM", "going": False},
    ]

if "communities" not in st.session_state:
    st.session_state.communities = [
        {"name": "Shivamogga Circle", "members": 1280, "blurb": "Stories and updates from the heart of Malnad.", "joined": True},
        {"name": "Holehonnur Neighbors", "members": 342, "blurb": "Harvest, festivals and village news.", "joined": False},
        {"name": "Tunga Riverside Volunteers", "members": 215, "blurb": "Clean-ups, plantations and river care.", "joined": False},
    ]

if "alerts" not in st.session_state:
    st.session_state.alerts = [
        ("🚧", "Road work near Town Library", "Expect diversions on Saturday morning."),
        ("🎉", "Harvest gathering is this Sunday", "Bring a family recipe and a story."),
        ("💧", "Water supply maintenance", "Interrupted tomorrow, 10 AM – 2 PM."),
    ]


def card_html(inner: str) -> str:
    return f'<div class="card">{inner}</div>'


def initials(name: str) -> str:
    parts = [p for p in name.split() if p]
    return "".join(p[0] for p in parts[:2]).upper() or "?"


# ---------- Header ----------
st.markdown('<p class="brand">Hometown Hub</p><p class="tagline">Your people. Your place.</p>', unsafe_allow_html=True)

tab_home, tab_comm, tab_events, tab_alerts = st.tabs(["🏡 Home", "👥 Communities", "📅 Events", "🔔 Alerts"])

# ---------- HOME ----------
with tab_home:
    st.image(HERO_IMG, use_container_width=True)
    st.markdown('<div class="eyebrow">Shivamogga, Karnataka</div>', unsafe_allow_html=True)
    st.title("Where your roots still feel close.")
    st.write("Local stories, familiar faces, and meaningful ways to show up for the place that made you.")

    st.markdown("### The town square")

    with st.expander("✍️ Share an update"):
        with st.form("new_post", clear_on_submit=True):
            name = st.text_input("Your name")
            circle = st.selectbox("Community", [c["name"] for c in st.session_state.communities])
            tag = st.selectbox("Category", ["COMMUNITY", "ANNOUNCEMENT", "EVENT", "HELP"])
            text = st.text_area("What's happening back home?")
            img = st.file_uploader("Photo (optional)", type=["jpg", "jpeg", "png"])
            if st.form_submit_button("Post", type="primary"):
                if not name.strip() or not text.strip():
                    st.warning("Please add your name and an update.")
                else:
                    st.session_state.posts.insert(0, {
                        "id": st.session_state.next_id, "author": name.strip(), "time": "now",
                        "circle": circle, "tag": tag, "text": text.strip(),
                        "image": img.getvalue() if img else None,
                        "likes": 0, "liked": False, "comments": [], "comment_base": 0,
                    })
                    st.session_state.next_id += 1
                    st.rerun()

    for p in st.session_state.posts:
        st.markdown(
            card_html(
                f'<span class="avatar">{html.escape(initials(p["author"]))}</span>'
                f'<span class="author">{html.escape(p["author"])}</span> '
                f'<span class="meta">&nbsp;{p["time"]} · {html.escape(p["circle"])}</span><br>'
                f'<span class="tag">{html.escape(p["tag"])}</span>'
                f'<p style="margin:0">{html.escape(p["text"])}</p>'
            ),
            unsafe_allow_html=True,
        )
        if p["image"]:
            st.image(p["image"], use_container_width=True)

        c1, c2, c3 = st.columns([1, 1, 1])
        if c1.button(f'{"❤️" if p["liked"] else "🤍"} {p["likes"]}', key=f'like_{p["id"]}'):
            p["liked"] = not p["liked"]
            p["likes"] += 1 if p["liked"] else -1
            st.rerun()
        total_comments = p["comment_base"] + len(p["comments"])
        c2.markdown(f'<div style="padding-top:6px">💬 {total_comments}</div>', unsafe_allow_html=True)
        c3.link_button("Share", f"https://wa.me/?text={html.escape(p['text'][:140])}")

        with st.expander("Comments"):
            for who, msg in p["comments"]:
                st.markdown(f"**{who}:** {msg}")
            who = st.text_input("Name", key=f'cn_{p["id"]}')
            msg = st.text_input("Add a comment", key=f'cm_{p["id"]}')
            if st.button("Reply", key=f'cb_{p["id"]}'):
                if who.strip() and msg.strip():
                    p["comments"].append((who.strip(), msg.strip()))
                    st.rerun()

    st.markdown("### Happening nearby")
    for e in st.session_state.events:
        st.markdown(
            card_html(
                f'<div style="display:flex;gap:14px;align-items:center">'
                f'<div class="date"><b>{e["day"]}</b><span>{e["mon"]}</span></div>'
                f'<div><b>{html.escape(e["title"])}</b><br><span class="meta">{html.escape(e["where"])} · {e["time"]}</span></div>'
                f'</div>'
            ),
            unsafe_allow_html=True,
        )

    st.markdown("### Know someone from home?")
    st.write("Invite them into the circle and keep local stories alive.")
    invitee = st.text_input("Their email or phone", key="invitee")
    if st.button("Invite a neighbor", type="primary"):
        if invitee.strip():
            st.success(f"Invitation noted for {invitee}. (Hook this up to email/SMS to actually send it.)")
        else:
            st.warning("Enter an email or phone number first.")

# ---------- COMMUNITIES ----------
with tab_comm:
    st.header("Communities")
    for i, c in enumerate(st.session_state.communities):
        st.markdown(
            card_html(
                f'<b>{html.escape(c["name"])}</b><br>'
                f'<span class="meta">{c["members"]:,} members</span><br>{html.escape(c["blurb"])}'
            ),
            unsafe_allow_html=True,
        )
        label = "Joined ✓" if c["joined"] else "Join"
        if st.button(label, key=f"join_{i}", type="secondary" if c["joined"] else "primary"):
            c["joined"] = not c["joined"]
            c["members"] += 1 if c["joined"] else -1
            st.rerun()

# ---------- EVENTS ----------
with tab_events:
    st.header("Events")
    with st.expander("➕ Add an event"):
        with st.form("new_event", clear_on_submit=True):
            title = st.text_input("Title")
            where = st.text_input("Where")
            d = st.date_input("Date")
            t = st.time_input("Time")
            if st.form_submit_button("Add event", type="primary") and title.strip():
                st.session_state.events.append({
                    "id": len(st.session_state.events) + 1,
                    "day": f"{d.day:02d}", "mon": d.strftime("%b").upper(),
                    "title": title.strip(), "where": where.strip() or "TBA",
                    "time": datetime.combine(d, t).strftime("%I:%M %p").lstrip("0"), "going": False,
                })
                st.rerun()

    for e in st.session_state.events:
        st.markdown(
            card_html(
                f'<div style="display:flex;gap:14px;align-items:center">'
                f'<div class="date"><b>{e["day"]}</b><span>{e["mon"]}</span></div>'
                f'<div><b>{html.escape(e["title"])}</b><br><span class="meta">{html.escape(e["where"])} · {e["time"]}</span></div>'
                f'</div>'
            ),
            unsafe_allow_html=True,
        )
        if st.button("Going ✓" if e["going"] else "RSVP", key=f'rsvp_{e["id"]}',
                     type="secondary" if e["going"] else "primary"):
            e["going"] = not e["going"]
            st.rerun()

# ---------- ALERTS ----------
with tab_alerts:
    st.header("Alerts")
    for icon, title, body in st.session_state.alerts:
        st.markdown(
            card_html(f'<b>{icon} {html.escape(title)}</b><br><span class="meta">{html.escape(body)}</span>'),
            unsafe_allow_html=True,
        )
