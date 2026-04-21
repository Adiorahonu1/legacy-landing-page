import os
import sys
import json
import time
import requests

ENV_PATH = "/Users/macbook/Documents/new workflows/.env"
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
API_URL = "https://api.kie.ai/api/v1/jobs/createTask"
POLL_URL = "https://api.kie.ai/api/v1/jobs/recordInfo"

PROFILES = [
    {
        "filename": "profile-protector.jpg",
        "prompt": {
            "prompt": (
                "Photojournalistic documentary portrait. A Black father in his early 40s, "
                "solid warm build, wearing a navy blue button-up shirt with the sleeves rolled "
                "to his forearms, stands in a softly lit suburban living room. His right arm rests "
                "gently around the shoulders of his wife, a Black woman in her mid-30s with natural "
                "locs, wearing a cream blouse, her face showing a warm relaxed smile. Their young son, "
                "approximately 8 years old, stands slightly in front of them, leaning his back into his "
                "father's leg with easy comfort. The living room around them is real and lived-in: a "
                "fabric couch visible to the right, a wooden side table with a lamp, family photographs "
                "hanging on the wall behind them. Late-afternoon golden window light streams in from the "
                "left, casting long warm shadows across the room and creating soft highlights on their "
                "faces and clothes. The mood is settled, protected, loved. The father's expression is "
                "calm and steady. Shallow depth of field softens the background. Skin has visible natural "
                "texture, natural pores, real complexion variations. No retouching. No smoothing. No "
                "studio lighting. 85mm lens f/1.8 ISO 400. Documentary feel."
            ),
            "negative_prompt": (
                "airbrushed skin, plastic skin, CGI, illustration, studio backdrop, beauty filter, "
                "fashion editorial proportions, symmetrical lighting, overexposed, harsh shadows, "
                "HDR processing, skin smoothing, anatomy normalization, stylized realism, "
                "editorial fashion, stock photo pose"
            ),
            "api_parameters": {
                "aspect_ratio": "4:5",
                "resolution": "1K",
                "output_format": "jpg"
            }
        }
    },
    {
        "filename": "profile-legacy-builder.jpg",
        "prompt": {
            "prompt": (
                "Documentary portrait. A distinguished Black couple in their early 50s sit together "
                "at a polished dark wooden dining table. The man wears a well-fitted charcoal blazer "
                "over a dark shirt, no tie. His reading glasses rest on the table beside an open "
                "leather planning folder. The woman wears an elegant deep navy wrap dress, her natural "
                "hair in silver-streaked locs pinned loosely. Between them on the table: two or three "
                "framed family photographs, a page of handwritten notes, and a fountain pen. On the "
                "wall directly behind them hangs a framed family tree document with visible names "
                "across multiple generations. Both look slightly toward the wall with expressions of "
                "purposeful pride, as if reviewing something they have built. Warm amber incandescent "
                "lamp light falls on the table and documents. Soft natural window light from the right "
                "side creates gentle rim light on their faces. The mood is intentional, legacy-oriented, "
                "visionary. Skin texture is natural with visible pores, natural complexion variations. "
                "No retouching. No studio setup. 50mm lens f/2.2 ISO 320. Documentary portrait style."
            ),
            "negative_prompt": (
                "airbrushed skin, plastic skin, CGI, illustration, symmetrical studio lighting, "
                "beauty filter, fashion editorial, stock photo, overhead lighting, harsh shadows, "
                "skin smoothing, anatomy normalization, stylized realism"
            ),
            "api_parameters": {
                "aspect_ratio": "4:5",
                "resolution": "1K",
                "output_format": "jpg"
            }
        }
    },
    {
        "filename": "profile-freedom-planner.jpg",
        "prompt": {
            "prompt": (
                "Lifestyle editorial photograph. A Black woman in her early 40s sits on a wide wooden "
                "deck that looks out over a calm lake or open countryside. She has a full natural afro, "
                "slightly wind-touched. She wears a breezy cream linen shirt, loosely buttoned, and her "
                "feet are bare on the worn wooden planks. A thin laptop sits open on the table beside "
                "her, tilted away, mostly forgotten. She holds a warm ceramic coffee mug in both hands "
                "and looks toward the horizon with a quiet, private smile, the expression of someone "
                "exactly where they intended to be. Golden hour light bathes the entire scene in warm "
                "orange-pink tones. Long shadows stretch across the deck. The light catches the natural "
                "texture of her hair and the weave of her linen shirt. The mood is liberation, peace, "
                "chosen freedom. Skin has natural texture, real imperfections, unretouched. No makeup "
                "filters. No studio. No posed stiffness. 50mm lens f/2.0 ISO 250. Warm lifestyle "
                "editorial photography."
            ),
            "negative_prompt": (
                "airbrushed skin, plastic skin, CGI, illustration, studio lighting, beauty filter, "
                "fashion editorial proportions, overexposed sky, blown highlights, stock photo pose, "
                "symmetrical composition, skin smoothing, anatomy normalization, stylized realism"
            ),
            "api_parameters": {
                "aspect_ratio": "4:5",
                "resolution": "1K",
                "output_format": "jpg"
            }
        }
    },
    {
        "filename": "profile-wealth-creator.jpg",
        "prompt": (
            "Business editorial portrait. A sharp Black man in his mid-30s stands at floor-to-ceiling "
            "windows in a modern mid-rise office. He wears a fitted dark charcoal suit, no tie, the "
            "top button of his shirt open. His posture is confident with a slight forward lean, weight "
            "balanced on both feet, hands loosely at his sides or one hand in a pocket. He looks "
            "directly into the camera with focused, quiet intensity, the expression of someone who "
            "knows exactly what they are building. The city skyline is visible through the glass behind "
            "him, slightly blurred. A glass whiteboard with business diagrams and arrows is partially "
            "visible to the right edge of frame. Strong directional natural window light from the left "
            "creates sharp highlights on one side of his face and suit and deep natural shadow on the "
            "other. Skin has visible natural texture, natural pores, real complexion. No airbrushing. "
            "No retouching. No studio setup. 85mm lens f/2.2 ISO 320. Business editorial portrait style."
        )
    },
]


def load_api_key():
    with open(ENV_PATH, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('KIE_AI_API_KEY='):
                return line.split('=', 1)[1].strip('"\'')
    return None


def generate_image(api_key, prompt_data, output_path):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    # Handle both dict-with-api_parameters and raw string prompts
    if isinstance(prompt_data, dict):
        api_params = prompt_data.pop("api_parameters", {})
        prompt_string = json.dumps(prompt_data)
        aspect_ratio = api_params.get("aspect_ratio", "4:5")
        resolution = api_params.get("resolution", "1K")
        output_format = api_params.get("output_format", "jpg")
    else:
        prompt_string = prompt_data
        aspect_ratio = "4:5"
        resolution = "1K"
        output_format = "jpg"

    payload = {
        "model": "nano-banana-2",
        "input": {
            "prompt": prompt_string,
            "aspect_ratio": aspect_ratio,
            "resolution": resolution,
            "output_format": output_format
        }
    }

    print(f"  Submitting task to KIE.ai...")
    resp = requests.post(API_URL, headers=headers, json=payload, timeout=30)
    resp.raise_for_status()
    result = resp.json()

    task_id = result.get("data", {}).get("taskId")
    if not task_id:
        print(f"  ERROR: No taskId returned. Response: {result}")
        return False

    print(f"  Task ID: {task_id} — polling...")

    for attempt in range(1, 61):
        time.sleep(4)
        try:
            poll = requests.get(POLL_URL, headers=headers, params={"taskId": task_id}, timeout=15)
            poll.raise_for_status()
            data = poll.json().get("data", {})
        except Exception as e:
            print(f"  Poll {attempt}: error — {e}")
            continue

        state = data.get("state", "")
        print(f"  Poll {attempt}: {state}")

        if state in ("success", "completed"):
            try:
                urls = json.loads(data.get("resultJson", "{}")).get("resultUrls", [])
            except Exception:
                urls = []
            if not urls:
                print("  ERROR: No result URLs found.")
                return False
            img_resp = requests.get(urls[0], timeout=30)
            img_resp.raise_for_status()
            with open(output_path, "wb") as f:
                f.write(img_resp.content)
            print(f"  Saved to {os.path.basename(output_path)}")
            return True

        if state in ("failed", "error"):
            print(f"  ERROR: Task failed. {json.dumps(data, indent=2)}")
            return False

    print("  ERROR: Timed out.")
    return False


def main():
    api_key = load_api_key()
    if not api_key:
        print("ERROR: KIE_AI_API_KEY not found in .env")
        sys.exit(1)

    print(f"Generating {len(PROFILES)} profile images...\n")

    for i, profile in enumerate(PROFILES, 1):
        name = profile["filename"]
        output_path = os.path.join(OUTPUT_DIR, name)

        print(f"[{i}/{len(PROFILES)}] {name}")

        if os.path.exists(output_path):
            print(f"  Already exists — skipping.\n")
            continue

        # Deep copy prompt data since generate_image mutates it
        import copy
        prompt_data = copy.deepcopy(profile["prompt"])

        ok = generate_image(api_key, prompt_data, output_path)
        if not ok:
            print(f"  FAILED to generate {name}\n")
        else:
            print()

    print("Done.")


if __name__ == "__main__":
    main()
