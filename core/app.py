import os
import sys
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fontana_brain import FontanaBrain
from tokenizer import FontanaTokenizer

app = FastAPI(
    title="The Fontana Engine Core REST API",
    version="2.0",
    description="Asynchronous Background Network Daemon Gateway Layer"
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

class GenerationRequest(BaseModel):
    seed: str
    max_tokens: int = 75

class TrainingRequest(BaseModel):
    text: str

@app.get("/")
async def root_status():
    return {
        "status": "ONLINE",
        "engine": "The Fontana Engine Core",
        "architecture": "512-HD Spatial Tensors",
        "ipc_channel": "Unix Named Pipes (/tmp/fontana_*.fifo)"
    }

@app.post("/v1/generate")
async def network_generate(req: GenerationRequest):
    seed_phrase = req.seed.strip()
    if not seed_phrase:
        raise HTTPException(status_code=400, detail="Seed phrase cannot be empty.")

    current_text = seed_phrase + " "
    suffixes = ["ing", "tion", "ent", "yst", "sta", "ook", "ine", "tio", "ste"]
    generated_phrases = []

    for _ in range(req.max_tokens):
        token_ids = tokenizer.encode(current_text)
        token_string = " ".join(map(str, token_ids))

        stdout_output = brain.submit_prompt(token_string)

        if "[ERROR]" in stdout_output:
            raise HTTPException(status_code=500, detail=f"C++ Daemon Failure: {stdout_output}")

        try:
            predicted_id = int(stdout_output.strip())

            # FIXED: STABLE ARRAY TERMINATION CHECK CONDITIONS
            if predicted_id == 0 or predicted_id == 1 or predicted_id == 2:
                break

            if predicted_id == tokenizer.vocab["[EOS]"]:
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

    return {
        "seed_input": seed_phrase,
        "completed_text": current_text.strip(),
        "tokens_evaluated": len(generated_phrases)
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
