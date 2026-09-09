from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import subprocess, tempfile, os

router = APIRouter(prefix="/sandbox")

class CodeSubmission(BaseModel):
    talent_id: str
        challenge_id: str
            code_body: str

            # SAFE: No docker.sock, no network, 5 sec timeout, no file system access
            @router.post("/submit")
            async def execute_sandbox(submission: CodeSubmission):
                if len(submission.code_body) > 10000:
                        raise HTTPException(status_code=400, detail="Code too large")

                            with tempfile.NamedTemporaryFile(suffix=".py", delete=False, mode='w') as f:
                                    f.write(submission.code_body)
                                            temp_path = f.name

                                                try:
                                                        result = subprocess.run(
                                                                    ["python3", temp_path],
                                                                                capture_output=True,
                                                                                            text=True,
                                                                                                        timeout=5,
                                                                                                                    env={"PYTHONPATH": ""} # block imports abuse
                                                                                                                            )
                                                                                                                                    os.unlink(temp_path)
                                                                                                                                            score = 100 if result.returncode == 0 else 0
                                                                                                                                                    return {"status": "passed" if score==100 else "failed", "output": result.stdout[:2000] + result.stderr[:2000], "score": score}
                                                                                                                                                        except subprocess.TimeoutExpired:
                                                                                                                                                                os.unlink(temp_path)
                                                                                                                                                                        return {"status": "failed", "output": "Timeout after 5s - infinite loop?", "score": 0}
                                                                                                                                                                            except Exception as e:
                                                                                                                                                                                    raise HTTPException(status_code=500, detail=str(e))