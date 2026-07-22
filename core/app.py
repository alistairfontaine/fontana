import os
import sys
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fontana_brain import FontanaBrain
from tokenizer import FontanaTokenizer

app = FastAPI(
    title="The Fontana Engine Core REST API",
    version="4.0",
    description="Stateful Persistent Asynchronous Background Network Daemon Gateway Layer"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

brain = FontanaBrain()
tokenizer = FontanaTokenizer()

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
dataset_path = os.path.join(project_root, "dataset.txt")

# FIXED: PHASE J - MULTI-USER ISOLATED SESSION MEMORY DICTIONARY MAPS
# Dynamic dictionary maps tracking independent history lookback channels safely in RAM
SESSION_HISTORY_MAPS = {}


class GenerationRequest(BaseModel):
    seed: str
    max_tokens: int = 75
    session_id: str = "default_vault_channel"
    temperature: float = 0.32
    top_k: int = 6
    top_p: float = 0.90




class TrainingRequest(BaseModel):
    text: str

@app.get("/")
async def root_status():
    return {
        "status": "ONLINE",
        "engine": "The Fontana Engine Core // ANTAGONIST // ISOLATED",
        "architecture": "512-HD Spatial Tensors",
        "ipc_channel": "File-Synchronized Non-Blocking RAM Subprocess",
        "total_active_sessions": len(SESSION_HISTORY_MAPS)
    }


@app.post("/v1/generate")
async def network_generate(req: GenerationRequest):
    global SESSION_HISTORY_MAPS
    seed_phrase = req.seed.strip()
    if not seed_phrase:
        raise HTTPException(status_code=400, detail="Seed phrase cannot be empty.")

    # Isolate user storage cells or instantiate a fresh scratchpad buffer map row
    sid = req.session_id.strip() if req.session_id.strip() else "default_vault_channel"
    if sid not in SESSION_HISTORY_MAPS:
        SESSION_HISTORY_MAPS[sid] = []

    active_buffer = SESSION_HISTORY_MAPS[sid]

    # Connect rolling history context strings cleanly matching current isolated cell path
    history_context = " ".join(active_buffer[-3:])
    full_prompt = f"{history_context} {seed_phrase}".strip()

    current_text = seed_phrase + " "
    suffixes = ["ing", "tion", "ent", "yst", "sta", "ook", "ine", "tio", "ste"]
    generated_phrases = []

    for _ in range(req.max_tokens):
        token_ids = tokenizer.encode(full_prompt if _ == 0 else current_text)

        # FIXED: PHASE P - EXPOSE NUCLEUS SAMPLING CHANNELS DIRECTLY OVER IPC
        # Appends dynamic top_p slider variables cleanly right behind the selection pool bounds
        token_string = " ".join(map(str, token_ids)) + f" | {req.temperature} | {req.top_k} | {req.top_p}"

        stdout_output = brain.submit_prompt(token_string)


        if "[ERROR]" in stdout_output:
            raise HTTPException(status_code=500, detail=f"C++ Daemon Failure: {stdout_output}")

        try:
            predicted_id = int(stdout_output.strip())

            # STABLE ARRAY TERMINATION CHECK CONDITIONS
            if predicted_id == 0 or predicted_id == 1 or predicted_id == 2:
                break

            if predicted_id == tokenizer.vocab.get("[EOS]", 3):
                generated_phrases.append("[EOS]")
                break

            predicted_char = tokenizer.inverse_vocab.get(predicted_id, "")

            if predicted_char.strip() and not any(predicted_char.startswith(s) for s in suffixes):
                if not current_text.endswith(" "):
                    current_text += " "

            current_text += predicted_char
            generated_phrases.append(predicted_char)

        except ValueError:
            break

    completed_sentence = current_text.strip()

    # Freeze the generated sentence natively inside its unique segregated history map track
    SESSION_HISTORY_MAPS[sid].append(completed_sentence)
    if len(SESSION_HISTORY_MAPS[sid]) > 6:
        SESSION_HISTORY_MAPS[sid].pop(0)

    return {
        "seed_input": seed_phrase,
        "completed_text": completed_sentence,
        "tokens_evaluated": len(generated_phrases),
        "session_id": sid,
        "session_memory_depth": len(SESSION_HISTORY_MAPS[sid]),
        "telemetry": {
            "prompt_token_ids": tokenizer.encode(full_prompt),
            "generated_token_count": len(generated_phrases),
            "hidden_dimensions": 512,
            "vocabulary_size": len(tokenizer.vocab)
        }
    }



@app.post("/v1/train")
async def network_train(req: TrainingRequest):
    raw_training_data = req.text.strip().lower()
    if not raw_training_data:
        raise HTTPException(status_code=400, detail="Training text payload cannot be empty.")

    word_count = len(raw_training_data.split())
    if word_count < 4:
        raise HTTPException(
            status_code=422,
            detail=f"Incomplete context trajectory detected ({word_count} words). Minimum payload required is 4 structural words."
        )

    if os.path.exists(dataset_path):
        with open(dataset_path, "a", encoding="utf-8") as dataset_f:
            dataset_f.write("\n" + raw_training_data)

    from train_link import FontanaTrainerLink
    trainer_link = FontanaTrainerLink()
    trainer_link.train_on_text(raw_training_data)

    return {
        "status": "SUCCESS",
        "message": "Matrix weight fields adjusted permanently. Text appended to dataset.txt.",
        "words_processed": word_count
    }
