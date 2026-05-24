#!/usr/bin/env python3
"""Prepare one Creative Art run for Codex automation.

This ports the OpenClaw Creative Art prompt picker into a repo-local,
Codex-friendly script. It intentionally does not generate the image.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import re
import time
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


ROOT = Path(__file__).resolve().parents[2]
STATE_DIR = ROOT / ".codex-creative-art"
RUNS_DIR = STATE_DIR / "runs"
HISTORY_PATH = STATE_DIR / "prompt_history.json"
OPENCLAW_HISTORY_PATH = Path(
    "/Users/cubix/.openclaw/workspace/memory/prompt_to_channel_history.json"
)

SKILLS = [
    {
        "name": "draw-soft-anime",
        "source_model": "Codex draw-soft-anime",
        "description": "soft atmospheric anime",
    },
    {
        "name": "draw-cinema-anime",
        "source_model": "Codex draw-cinema-anime",
        "description": "cinematic cel anime",
    },
]

GENRES = [
    {
        "key": "urban-fantasy",
        "label": "도시 판타지",
        "theme": "비 갠 밤의 유리 아케이드 거리",
        "bg": "wet glass arcade, reflected shop lights, faint mist",
        "accents": ["teal", "amber", "violet"],
    },
    {
        "key": "eastern-fantasy",
        "label": "동양 판타지",
        "theme": "안개 낀 새벽의 나루터 회랑",
        "bg": "misty riverside pavilion, damp stone path, lantern glow",
        "accents": ["jade", "crimson", "gold"],
    },
    {
        "key": "steampunk",
        "label": "스팀펑크",
        "theme": "노을빛 정비 격납고",
        "bg": "brass hangar, warm steam haze, riveted metal reflections",
        "accents": ["copper", "cyan", "orange"],
    },
    {
        "key": "ocean-gothic",
        "label": "해양 고딕",
        "theme": "해무 낀 절벽 등대 산책로",
        "bg": "sea fog, wet stone railing, distant lighthouse beam",
        "accents": ["sea-green", "silver", "navy"],
    },
    {
        "key": "forest-fantasy",
        "label": "숲 판타지",
        "theme": "이슬 맺힌 수목원 오솔길",
        "bg": "botanical greenhouse path, dew sparkle, soft foliage haze",
        "accents": ["emerald", "cream", "sky"],
    },
    {
        "key": "desert-ruins",
        "label": "사막 유적 판타지",
        "theme": "황혼의 협곡 유적 길목",
        "bg": "sand-worn ruins, dusk dust haze, warm canyon light",
        "accents": ["sand", "turquoise", "bronze"],
    },
    {
        "key": "school-daily",
        "label": "일상/학원물",
        "theme": "비 그친 방과후 강변 산책로",
        "bg": "riverside walkway after rain, soft breeze, distant city haze",
        "accents": ["navy", "mint", "sunset"],
    },
    {
        "key": "urban-noir",
        "label": "어반 느와르",
        "theme": "트램이 지나는 구시장 골목",
        "bg": "old tram street, pale daylight reflections, light dust haze",
        "accents": ["charcoal", "rust", "olive"],
    },
    {
        "key": "sky-fantasy",
        "label": "스카이 판타지",
        "theme": "구름바다 위 성채 망루",
        "bg": "floating bastion deck, cloud sea, dawn haze",
        "accents": ["sky", "white", "gold"],
    },
    {
        "key": "holy-archive",
        "label": "천문/성소 판타지",
        "theme": "황혼의 대리석 천문 도서관",
        "bg": "marble observatory hall, warm dusk glow, quiet reflecting pool",
        "accents": ["azure", "gold", "ivory"],
    },
]

SF_GENRES = [
    {
        "key": "hard-sf",
        "label": "하드 SF",
        "theme": "거대 궤도 구조물과 정비 플랫폼",
        "bg": "orbital dock, giant megastructure, cold vacuum glow",
        "accents": ["cobalt", "orange", "white"],
    },
    {
        "key": "retro-sf",
        "label": "레트로 SF",
        "theme": "고공 발사 테라스와 중형 수송선",
        "bg": "launch terrace, retro hull plating, sky glare",
        "accents": ["white", "cyan", "red"],
    },
    {
        "key": "military-sf",
        "label": "군사 SF",
        "theme": "중무장 전함과 호위 편대",
        "bg": "warship hull, escort drones, tactical beacon lights",
        "accents": ["gunmetal", "amber", "ice blue"],
    },
    {
        "key": "colony-sf",
        "label": "콜로니 SF",
        "theme": "환형 스페이스 콜로니와 도킹 링",
        "bg": "space colony ring, docking bridges, habitat windows",
        "accents": ["teal", "orange", "silver"],
    },
    {
        "key": "mecha-sf",
        "label": "메카 SF",
        "theme": "대형 메카 격납고와 정비 암",
        "bg": "mecha hangar, service arms, caution lights",
        "accents": ["lime", "white", "charcoal"],
    },
]

PROMPT_TYPES = [
    ("character", "캐릭터"),
    ("creature", "생물"),
    ("scene", "장면"),
    ("sf", "SF"),
]

SHOTS_CHARACTER = [
    ("close-up", "close-up, eye-level"),
    ("half-body", "half-body, eye-level"),
    ("thigh-up", "thigh-up, eye-level"),
    ("knee-up", "knee-up, eye-level"),
    ("full-body", "full-body, eye-level"),
    ("wide-establishing", "wide establishing shot, eye-level"),
]
SHOTS_CREATURE = [
    ("profile", "profile view, eye-level"),
    ("full-body", "full-body, eye-level"),
    ("dynamic", "dynamic action pose, eye-level"),
    ("wide-establishing", "wide establishing shot, eye-level"),
]
SHOTS_SCENE = [
    ("wide-establishing", "wide establishing shot"),
    ("cinematic-wide", "cinematic wide shot"),
    ("eye-level-street", "eye-level environmental shot"),
    ("slight-high-view", "slight high view environmental shot"),
]
SHOTS_SF = [
    ("wide-establishing", "wide establishing shot"),
    ("cinematic-wide", "cinematic wide shot"),
    ("dock-view", "dockside cinematic wide shot"),
    ("orbital-view", "orbital panoramic shot"),
]

AGE_GROUPS = [
    ("child", "아동"),
    ("teen", "10대"),
    ("young-adult", "20대"),
    ("adult", "30대"),
    ("mature", "40대 이상"),
]
GENDERS = [
    ("female", "여성"),
    ("male", "남성"),
    ("androgynous", "중성적 인상"),
]
SPECIES_MAP = {
    "human": "인간",
    "elf": "엘프",
    "android": "안드로이드",
    "beastfolk": "수인",
    "spirit": "정령",
    "vampire": "흡혈귀",
    "angelic": "천사형",
}

CREATURE_CATEGORIES = [
    {
        "key": "animal",
        "label": "동물",
        "classes": [
            {
                "key": "mammal",
                "label": "포유류",
                "body": ["소형", "중형", "대형"],
                "texture": ["furred", "short fur", "shaggy fur"],
                "features": ["horns", "tail plume", "striped markings"],
            },
            {
                "key": "bird",
                "label": "조류",
                "body": ["소형", "중형", "대형"],
                "texture": ["feathered", "soft plumage", "glossy feathers"],
                "features": ["crest", "broad wings", "talons"],
            },
            {
                "key": "reptile",
                "label": "파충류",
                "body": ["소형", "중형", "대형"],
                "texture": ["scaled", "armored scales", "smooth scales"],
                "features": ["frill", "horns", "spine ridge"],
            },
            {
                "key": "insect",
                "label": "곤충류",
                "body": ["소형", "중형"],
                "texture": ["shell", "iridescent shell", "translucent wing membrane"],
                "features": ["antennae", "compound eyes", "wing shimmer"],
            },
        ],
    },
    {
        "key": "aquatic",
        "label": "수생 생물",
        "classes": [
            {
                "key": "fish",
                "label": "물고기",
                "body": ["소형", "중형", "대형"],
                "texture": ["scaled", "silvery scales", "bioluminescent skin"],
                "features": ["long fins", "glowing stripe", "forked tail"],
            },
            {
                "key": "deepsea",
                "label": "심해 생물",
                "body": ["소형", "중형", "부유형"],
                "texture": ["translucent", "slick skin", "gelatinous body"],
                "features": ["lure light", "tendrils", "large eye"],
            },
            {
                "key": "crustacean",
                "label": "갑각류",
                "body": ["소형", "중형", "대형"],
                "texture": ["shell", "rough shell", "wet carapace"],
                "features": ["claws", "antennae", "segment limbs"],
            },
            {
                "key": "jelly",
                "label": "해파리류",
                "body": ["소형", "중형", "부유형"],
                "texture": ["translucent", "gelatinous glow", "semi-transparent"],
                "features": ["trailing tendrils", "bell dome", "particle glow"],
            },
        ],
    },
    {
        "key": "plant",
        "label": "식물",
        "classes": [
            {
                "key": "flower",
                "label": "꽃",
                "body": ["소형", "중형"],
                "texture": ["soft petals", "translucent petals", "velvet petals"],
                "features": ["glowing stamens", "wide blossom", "dewdrops"],
            },
            {
                "key": "vine",
                "label": "덩굴",
                "body": ["중형", "대형"],
                "texture": ["wet leaves", "fibrous stem", "thick vine skin"],
                "features": ["hanging tendrils", "thorned stem", "flower buds"],
            },
            {
                "key": "mushroom",
                "label": "버섯",
                "body": ["소형", "중형"],
                "texture": ["soft cap", "spore dust", "rubbery stem"],
                "features": ["glow under cap", "spore halo", "layered cap rings"],
            },
            {
                "key": "treeform",
                "label": "나무형 식물",
                "body": ["중형", "대형", "거목형"],
                "texture": ["rough bark", "crystal bark", "mossy bark"],
                "features": ["glowing veins", "hollow trunk", "broad canopy"],
            },
            {
                "key": "waterplant",
                "label": "수생 식물",
                "body": ["소형", "중형"],
                "texture": ["floating leaves", "glasslike petals", "ribbon leaves"],
                "features": ["surface blossoms", "long stems", "soft bioluminescence"],
            },
        ],
    },
    {
        "key": "fantasy",
        "label": "환상 생물",
        "classes": [
            {
                "key": "spirit",
                "label": "정령체",
                "body": ["소형", "중형", "대형", "부유형"],
                "texture": ["mist body", "light body", "semi-transparent"],
                "features": ["floating fragments", "halo", "particle trail"],
            },
            {
                "key": "beast",
                "label": "환수",
                "body": ["중형", "대형"],
                "texture": ["crystal fur", "feathered hide", "scaled fur"],
                "features": ["horns", "wings", "glowing markings"],
            },
            {
                "key": "mechabeast",
                "label": "기계 생명체",
                "body": ["소형", "중형", "대형"],
                "texture": ["brushed metal", "ceramic shell", "segment armor"],
                "features": ["sensor eye", "thruster fins", "modular limbs"],
            },
        ],
    },
]

HABITATS = [
    "숲 수관층",
    "해저 회랑",
    "협곡 유적",
    "부유섬 가장자리",
    "구시장 지붕 위",
    "설원 절벽",
    "온실 수로",
    "고대 정원 유적",
]
CREATURE_MOODS = [
    "경계하는 고요함",
    "신비로운 부유감",
    "사냥 직전의 정적",
    "온순하지만 낯선 아름다움",
]
SCENE_MODES = [
    ("empty", "순수 환경 장면"),
    ("with-figures", "인물/생물 소수 포함 장면"),
    ("crowded", "다수의 인물/생물/군중이 있는 장면"),
]
PLACES = [
    "골목",
    "아케이드 거리",
    "온실 회랑",
    "성채 망루",
    "절벽 산책로",
    "구시장",
    "정비 격납고",
    "수로 정원",
    "신전 외곽",
    "플랫폼",
]
TIMES_OF_DAY = ["새벽", "아침", "오후", "노을", "밤", "심야"]
WEATHERS = ["맑음", "비 갠 뒤", "안개", "해무", "먼지 낀 공기", "가벼운 눈발"]
LIGHTINGS = [
    "natural daylight",
    "soft dusk glow",
    "cold moonlight",
    "warm lantern glow",
    "neon mixed light",
]
SCENE_ELEMENTS = [
    "유리돔",
    "난간",
    "수로",
    "트램 레일",
    "탑",
    "현수 깃발",
    "아치 회랑",
    "부유 구조물",
    "시장 천막",
    "정원 석상",
]
SCENE_MOODS = [
    "고요한 긴장감",
    "몽환적인 공기감",
    "분주하지만 절제된 분위기",
    "웅장한 적막",
    "생활감 있는 활기",
]
SCENE_GROUP_ELEMENTS = [
    "멀리 물고기 떼가 지나감",
    "새 떼가 하늘을 가로지름",
    "버섯 군락이 바닥을 덮음",
    "꽃밭이 넓게 퍼져 있음",
    "작은 시장 군중이 공간을 채움",
]
SF_SUBJECTS = [
    ("mecha", "대형 메카"),
    ("warship", "우주 전함"),
    ("freighter", "수송선"),
    ("colony", "스페이스 콜로니"),
    ("station", "우주 정거장"),
    ("carrier", "항공모함급 함선"),
]
SF_MOODS = [
    "차갑고 장엄한 정적",
    "거대한 구조물 앞의 압도감",
    "작전 직전의 긴장감",
    "개척 전야의 고요함",
]
MOODS = [
    "차분한 결의",
    "잔잔한 긴장감",
    "피곤하지만 단단한 집중",
    "조용한 자신감",
    "은근한 장난기",
    "고요한 경계심",
]


def read_json(path: Path, default):
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default
    return value if isinstance(value, type(default)) else default


def load_history() -> list[dict]:
    if HISTORY_PATH.exists():
        return read_json(HISTORY_PATH, [])
    if OPENCLAW_HISTORY_PATH.exists():
        value = read_json(OPENCLAW_HISTORY_PATH, [])
        return value[-100:]
    return []


def write_history(history: list[dict]) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    HISTORY_PATH.write_text(
        json.dumps(history[-100:], ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def weighted_pick_type(recent_types: list[str], last: dict) -> tuple[str, str]:
    pool: list[tuple[str, str]] = []
    for item in PROMPT_TYPES:
        key = item[0]
        weight = 10
        if recent_types.count(key) >= 2:
            weight = 4
        if last.get("type") == key:
            weight = max(2, weight - 5)
        pool.extend([item] * weight)
    return random.choice(pool)


def pick_genre(pool_list: list[dict], recent_genres: list[str], last: dict) -> dict:
    best = None
    best_score = None
    for _ in range(80):
        genre = random.choice(pool_list)
        score = recent_genres.count(genre["label"]) * 4
        if last.get("genre_key") == genre["key"]:
            score += 8
        if best is None or score < best_score:
            best = genre
            best_score = score
    assert best is not None
    return best


def build_character(genre: dict, recent_shots: list[str], recent_species: list[str], last: dict):
    best = None
    best_score = None
    for _ in range(200):
        shot = random.choice(SHOTS_CHARACTER)
        age_key, age_label = random.choice(AGE_GROUPS)
        gender_key, gender_label = random.choice(GENDERS)
        species_key, species_label = random.choice(list(SPECIES_MAP.items()))
        score = 0
        if recent_shots.count(shot[1]):
            score += 2
        if recent_species.count(species_label):
            score += 2
        if last.get("species") == species_label:
            score += 4
        if best is None or score < best_score:
            best = (shot, age_key, age_label, gender_key, gender_label, species_key, species_label)
            best_score = score
    shot, age_key, age_label, gender_key, gender_label, species_key, species_label = best
    mood = random.choice(MOODS)
    template = (
        "프롬프트 입력 템플릿\n"
        "- 유형: 캐릭터\n"
        f"- 장르/테마: {genre['label']}/{genre['theme']}\n"
        "- 작화/스타일: 2D anime illustration(비실사), cinematic key visual, "
        "캐릭터 선명/배경 soft atmospheric, clear cel shading 2~3단\n"
        f"- 분위기: {mood}\n"
        f"- 구도: {shot[1]}\n"
        "- 옵션: age/gender/species 중심 랜덤 조합 + background 포함 + high resolution, "
        "ultra detailed, no text, no logo, no watermark"
    )
    prompt = (
        f"2D anime illustration(비실사), cinematic key visual, {shot[1]}. "
        f"{age_label} {gender_label} {species_label} 캐릭터 1명. "
        f"Genre/theme: {genre['label']}, {genre['theme']}. "
        f"Background keywords: {genre['bg']}, character crisp and background soft atmospheric. "
        f"Mood: {mood}. clear cel shading 2~3단, ambient lighting + ambient occlusion, "
        "high resolution, ultra detailed, no text, no logo, no watermark"
    )
    item = {
        "type": "character",
        "genre": genre["label"],
        "genre_key": genre["key"],
        "theme": genre["theme"],
        "shot": shot[1],
        "shot_key": shot[0],
        "age_group": age_key,
        "gender": gender_key,
        "species": species_label,
        "species_key": species_key,
        "mood": mood,
        "accent": None,
    }
    return template, prompt, item


def build_creature(genre: dict):
    category = random.choice(CREATURE_CATEGORIES)
    base = random.choice(category["classes"])
    shot = random.choice(SHOTS_CREATURE)
    body = random.choice(base["body"])
    texture = random.choice(base["texture"])
    features = ", ".join(random.sample(base["features"], 2 if len(base["features"]) >= 2 else 1))
    habitat = random.choice(HABITATS)
    mood = random.choice(CREATURE_MOODS)
    accent = random.choice(genre["accents"])
    template = (
        "프롬프트 입력 템플릿\n"
        "- 유형: 생물\n"
        f"- 장르/테마: {genre['label']}/{genre['theme']}\n"
        "- 작화/스타일: 2D anime creature/nature illustration(비실사), cinematic creature key visual, "
        "개체 중심, clear cel shading 2~3단\n"
        f"- 분위기: {mood}\n"
        f"- 구도: {shot[1]}\n"
        "- 옵션: 단일 개체 중심 + 분류/체형/질감/특징기관/서식 환경 랜덤 조합 + "
        "high resolution, ultra detailed, no text, no logo, no watermark"
    )
    if category["key"] == "plant":
        prompt = (
            f"2D anime botanical illustration(비실사), cinematic nature key visual, {shot[1]}. "
            f"{genre['label']} 분위기의 {category['label']} / {base['label']}, 단일 개체 중심. "
            f"Growth scale/form: {body}. Surface/leaf/petal texture: {texture}. "
            f"Distinct traits: {features}. Accent color: {accent}. Habitat: {habitat}. "
            f"Background keywords: {genre['bg']}. Mood: {mood}. Plant morphology, leaf/petal "
            "structure, stem growth pattern, and silhouette readability prioritized. "
            "No large colony/field composition; focus on one main botanical subject. "
            "clear cel shading 2~3단, ambient lighting + ambient occlusion, high resolution, "
            "ultra detailed, no text, no logo, no watermark"
        )
    else:
        prompt = (
            f"2D anime creature illustration(비실사), cinematic creature key visual, {shot[1]}. "
            f"{genre['label']} 분위기의 {category['label']} / {base['label']}, 단일 개체 중심. "
            f"Body scale/type: {body}. Surface texture: {texture}. Distinct features: {features}. "
            f"Accent color: {accent}. Habitat: {habitat}. Background keywords: {genre['bg']}. "
            f"Mood: {mood}. Anatomy, species traits, and single-subject silhouette prioritized. "
            "No flock, school, swarm, or colony scene composition. clear cel shading 2~3단, "
            "ambient lighting + ambient occlusion, high resolution, ultra detailed, no text, no logo, no watermark"
        )
    item = {
        "type": "creature",
        "genre": genre["label"],
        "genre_key": genre["key"],
        "theme": genre["theme"],
        "shot": shot[1],
        "shot_key": shot[0],
        "species": f"{category['label']}/{base['label']}",
        "species_key": f"{category['key']}:{base['key']}",
        "creature_category": category["label"],
        "mood": mood,
        "accent": accent,
    }
    return template, prompt, item


def build_scene(genre: dict):
    shot = random.choice(SHOTS_SCENE)
    place = random.choice(PLACES)
    tod = random.choice(TIMES_OF_DAY)
    weather = random.choice(WEATHERS)
    lighting = random.choice(LIGHTINGS)
    mood = random.choice(SCENE_MOODS)
    scene_mode = random.choice(SCENE_MODES)
    elems = ", ".join(random.sample(SCENE_ELEMENTS, 3))
    group_event = random.choice(SCENE_GROUP_ELEMENTS)
    subject_clause = {
        "empty": "순수 환경 중심, 전경 피사체 없음",
        "with-figures": f"장면 보조용 인물이나 생물 1~3개체를 작게 포함 가능, 또는 {group_event}",
        "crowded": f"장면 속 인물/생물/군중이 여러 개체 존재하는 서사적 환경 장면, 또는 {group_event}",
    }[scene_mode[0]]
    template = (
        "프롬프트 입력 템플릿\n"
        "- 유형: 장면\n"
        f"- 장르/테마: {genre['label']}/{genre['theme']}\n"
        "- 작화/스타일: 2D anime environment illustration(비실사), cinematic environmental key visual, "
        "공간감 중심, clear cel shading 2~3단\n"
        f"- 분위기: {mood}\n"
        f"- 구도: {shot[1]}\n"
        f"- 옵션: 장소/시간/날씨/광원/랜드마크 랜덤 조합 + 장면 모드={scene_mode[1]} + "
        "high resolution, ultra detailed, no text, no logo, no watermark"
    )
    prompt = (
        f"2D anime environment illustration(비실사), cinematic environmental key visual, {shot[1]}. "
        f"{genre['label']} 장르의 {tod} {place}. Weather: {weather}. Lighting: {lighting}. "
        f"Core theme: {genre['theme']}. Background keywords: {genre['bg']}. "
        f"Environmental landmarks: {elems}. Mood: {mood}. Scene mode: {scene_mode[1]} - {subject_clause}. "
        "Group elements like schools of fish, flocks of birds, mushroom fields, flower meadows, "
        "or creature clusters belong here when they support the environment as a scene. "
        "strong sense of place, layered depth, soft atmospheric separation, clear cel shading 2~3단, "
        "ambient lighting + ambient occlusion, high resolution, ultra detailed, no text, no logo, no watermark"
    )
    item = {
        "type": "scene",
        "genre": genre["label"],
        "genre_key": genre["key"],
        "theme": genre["theme"],
        "shot": shot[1],
        "shot_key": shot[0],
        "scene_mode": scene_mode[0],
        "scene_mode_label": scene_mode[1],
        "place": place,
        "time_of_day": tod,
        "weather": weather,
        "lighting": lighting,
        "species": None,
        "mood": mood,
    }
    return template, prompt, item


def build_sf(genre: dict):
    shot = random.choice(SHOTS_SF)
    subject_key, subject_label = random.choice(SF_SUBJECTS)
    mood = random.choice(SF_MOODS)
    template = (
        "프롬프트 입력 템플릿\n"
        "- 유형: SF\n"
        f"- 장르/테마: {genre['label']}/{genre['theme']}\n"
        "- 작화/스타일: 2D anime SF illustration(비실사), cinematic sci-fi key visual, "
        "구조물/메카/함선 중심, clear cel shading 2~3단\n"
        f"- 분위기: {mood}\n"
        f"- 구도: {shot[1]}\n"
        "- 옵션: 메카/전함/수송선/콜로니/정거장 랜덤 + high resolution, ultra detailed, "
        "no text, no logo, no watermark"
    )
    prompt = (
        f"2D anime sci-fi illustration(비실사), cinematic sci-fi key visual, {shot[1]}. "
        f"{genre['label']} 분위기의 {subject_label} 중심 장면. Core theme: {genre['theme']}. "
        f"Background keywords: {genre['bg']}. Mood: {mood}. Foreground structure crisp and readable, "
        "background space/megastructure softly separated with atmospheric depth. Mecha, warship, "
        "freighter, colony, or station subject prioritized over organic scenery. clear cel shading 2~3단, "
        "ambient lighting + ambient occlusion, high resolution, ultra detailed, no text, no logo, no watermark"
    )
    item = {
        "type": "sf",
        "genre": genre["label"],
        "genre_key": genre["key"],
        "theme": genre["theme"],
        "shot": shot[1],
        "shot_key": shot[0],
        "species": subject_label,
        "species_key": subject_key,
        "mood": mood,
        "accent": None,
    }
    return template, prompt, item


def safe_slug(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value or "creative-art"


def title_for(item: dict) -> str:
    genre = item.get("genre") or "창작 이미지"
    species = item.get("species")
    theme = item.get("theme") or ""
    if item["type"] == "character":
        return f"{genre}의 {species}"
    if item["type"] == "creature":
        return f"{genre}의 {species}"
    if item["type"] == "sf":
        return f"{genre}의 {species}"
    if theme:
        return f"{genre}의 {theme}"
    return f"{genre}의 장면"


def slug_for(item: dict, run_stamp: str) -> str:
    parts = [
        item.get("genre_key", ""),
        item.get("type", ""),
        item.get("species_key", "") or item.get("scene_mode", "") or item.get("shot_key", ""),
        run_stamp,
    ]
    return safe_slug("-".join(parts))


def prepare_run() -> dict:
    history = load_history()
    recent = history[-10:]
    recent_types = [h.get("type") for h in recent if h.get("type")]
    recent_genres = [h.get("genre") for h in recent if h.get("genre")]
    recent_shots = [h.get("shot") for h in recent if h.get("shot")]
    recent_species = [h.get("species") for h in recent if h.get("species")]
    last = recent[-1] if recent else {}

    type_key, _ = weighted_pick_type(recent_types, last)
    if type_key == "sf":
        genre = pick_genre(SF_GENRES, recent_genres, last)
        template, prompt, item = build_sf(genre)
    elif type_key == "character":
        genre = pick_genre(GENRES, recent_genres, last)
        template, prompt, item = build_character(genre, recent_shots, recent_species, last)
    elif type_key == "creature":
        genre = pick_genre(GENRES, recent_genres, last)
        template, prompt, item = build_creature(genre)
    else:
        genre = pick_genre(GENRES, recent_genres, last)
        template, prompt, item = build_scene(genre)

    now = datetime.now(ZoneInfo("Asia/Seoul"))
    run_stamp = now.strftime("%Y%m%d_%H%M%S")
    run_id = f"{run_stamp}_{hashlib.sha1(prompt.encode('utf-8')).hexdigest()[:8]}"
    selected_skill = random.choice(SKILLS)

    item["ts"] = int(time.time())
    history.append(item)
    write_history(history)

    run_dir = RUNS_DIR / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    marker_path = run_dir / "image_marker"
    marker_path.write_text(str(time.time()), encoding="utf-8")

    title = title_for(item)
    slug = slug_for(item, run_stamp)
    run = {
        "ok": True,
        "run_id": run_id,
        "created_at": now.isoformat(),
        "root": str(ROOT),
        "run_dir": str(run_dir),
        "marker_path": str(marker_path),
        "history_path": str(HISTORY_PATH),
        "item": item,
        "template": template,
        "prompt": prompt,
        "selected_skill": selected_skill,
        "title": title,
        "slug": slug,
    }

    (run_dir / "run.json").write_text(json.dumps(run, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (run_dir / "prompt.txt").write_text(prompt + "\n", encoding="utf-8")
    (run_dir / "template.txt").write_text(template + "\n", encoding="utf-8")
    (STATE_DIR / "current_run.json").write_text(
        json.dumps(run, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return run


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--print-prompt", action="store_true")
    args = parser.parse_args()

    run = prepare_run()
    if args.print_prompt:
        print(run["prompt"])
    else:
        print(json.dumps(run, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
