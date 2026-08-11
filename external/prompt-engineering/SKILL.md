---
name: prompt-engineering
description: "Prompt engineering techniques: structured prompts, few-shot patterns, chain-of-thought, ReAct, self-consistency, persona priming, output formatting, and prompt optimization. Use when designing system prompts, debugging LLM outputs, optimizing few-shot examples, or building reliable LLM-powered features."
version: 1.0.0
---

# Prompt Engineering

Structured prompting, few-shot, CoT, self-consistency, debugging.

## Prompt Structure (Golden Pattern)

```python
def build_prompt(role, context, task, constraints, examples=None, output_format=None):
    """Universal prompt builder following the proven structure."""
    parts = []
    
    # 1. Role/Persona (set the stage)
    if role:
        parts.append(f"## Role\n{role}")
    
    # 2. Context (background knowledge)
    if context:
        parts.append(f"## Context\n{context}")
    
    # 3. Task (what to do — be specific, not "help me")
    parts.append(f"## Task\n{task}")
    
    # 4. Few-shot examples (proven pattern)
    if examples:
        parts.append("## Examples")
        for i, ex in enumerate(examples, 1):
            parts.append(f"\n### Example {i}\n**Input:** {ex['input']}\n**Output:** {ex['output']}")
    
    # 5. Constraints (guardrails)
    if constraints:
        parts.append(f"## Constraints\n{constraints}")
    
    # 6. Output format (be explicit)
    if output_format:
        parts.append(f"## Output Format\n{output_format}")
    
    return "\n\n".join(parts)

# === Example: Code Review Prompt ===
print(build_prompt(
    role="You are a senior Python engineer reviewing code for a fintech startup.",
    context="The code handles payment processing. Security is critical.",
    task="Review the following Python function for correctness, security, and performance.",
    constraints=["Focus on SQL injection risks", "Suggest concrete fixes, not general advice", "Keep under 200 words"],
    output_format="Return JSON: {issues: [{severity, line, description, fix}]}",
))
```

## Chain-of-Thought Patterns

```python
# === Zero-shot CoT ===
ZERO_SHOT_COT = "Let's think step by step."

# === Few-shot CoT ===
FEW_SHOT_COT_EXAMPLE = """
Q: A store had 120 apples. They sold 45 in the morning and 30 in the afternoon. How many are left?

A: Let's think step by step.
1. Total apples: 120
2. Sold in morning: 45 — remaining: 120 - 45 = 75
3. Sold in afternoon: 30 — remaining: 75 - 30 = 45
Answer: 45 apples
"""

# === ReAct (Reasoning + Acting) ===
REACT_PROMPT = """You have tools available. Follow this cycle:
Thought: what should I do next?
Action: tool_name[input]
Observation: tool output
... (repeat until done)
Final Answer: your conclusion"""

# === Tree of Thoughts (exploration) ===
TOT_PROMPT = """For this problem:
1. Propose 3 different approaches
2. Evaluate each: pros, cons, confidence (0-1)
3. Choose the best approach
4. Execute and explain"""

# === Self-Consistency (vote) ===
def self_consistency(llm_call, prompt, n=5):
    """Run same prompt N times, pick majority answer."""
    responses = [llm_call(prompt) for _ in range(n)]
    # Count most common answer
    from collections import Counter
    return Counter(responses).most_common(1)[0][0]
```

## Output Formatting (Deterministic)

```python
# === JSON mode (most reliable for parsing) ===
JSON_FORMAT = """
Respond with ONLY valid JSON, no markdown, no explanation.
Schema: {"sentiment": "positive|negative|neutral", "confidence": 0.0-1.0}
"""

# === Structured text (parseable) ===
STRUCTURED_FORMAT = """
Respond in this exact format:
SUMMARY: <one sentence>
KEYWORDS: <comma separated>
SENTIMENT: <positive/negative/neutral>
CONFIDENCE: <0.00>
"""

# === Tag-based extraction ===
TAG_FORMAT = """
Wrap each section in tags:
<thinking>your reasoning</thinking>
<answer>final answer</answer>
<confidence>0-100</confidence>
"""

# === Pydantic structured output (with instructor) ===
from pydantic import BaseModel, Field
from typing import Literal

class AnalysisResult(BaseModel):
    sentiment: Literal['positive', 'negative', 'neutral']
    confidence: float = Field(ge=0, le=1)
    keywords: list[str]
    summary: str
```

## Prompt Optimization (Iterative)

```python
def optimize_prompt(base_prompt, examples, eval_fn, iterations=5):
    """Iteratively improve a prompt based on evaluation."""
    best_prompt = base_prompt
    best_score = eval_fn(best_prompt, examples)
    
    for i in range(iterations):
        # Collect failures
        failures = [ex for ex in examples if not eval_fn(best_prompt, [ex])]
        
        if not failures:
            break
        
        # Ask LLM to improve based on failures
        improvement_prompt = f"""This prompt failed on these cases:
{failures[:3]}

Current prompt:
{best_prompt}

Suggest ONE specific change to fix these failures. Return the new prompt."""
        
        new_prompt = llm_call(improvement_prompt)
        new_score = eval_fn(new_prompt, examples)
        
        if new_score > best_score:
            best_prompt = new_prompt
            best_score = new_score
    
    return best_prompt
```

## Persona Priming (Get Better Results)

```python
# === Expert priming (works surprisingly well) ===
EXPERT_ROLES = {
    "code": "You are a staff software engineer with 15 years experience at Google. You write production-quality code.",
    "writing": "You are a Pulitzer-winning journalist. Your writing is clear, engaging, and precise.",
    "analysis": "You are a McKinsey partner. Your analysis is data-driven, MECE-structured, and actionable.",
    "teaching": "You are a university professor known for making complex topics intuitive. You use analogies and avoid jargon.",
}

# === Audience calibration ===
AUDIENCE_PRIMING = {
    "beginner": "Explain like I'm a curious 12-year-old. Use analogies. No jargon without explanation.",
    "practitioner": "I'm a developer familiar with the basics. Focus on practical implementation.",
    "expert": "I know the theory. Give me edge cases, trade-offs, and production gotchas.",
}

# === Tone calibration ===
TONE_MODIFIERS = {
    "concise": "Be brief. Under 100 words. No preamble.",
    "detailed": "Be thorough. Include rationale, alternatives, and edge cases.",
    "creative": "Be original. Avoid clichés. Use unexpected angles.",
    "formal": "Use professional language. No contractions. Full sentences.",
}
```

## Common Failure Patterns + Fixes

| Failure | Root Cause | Fix |
|---------|-----------|-----|
| "I don't know" for everything | Overly cautious | Add "if uncertain, give your best guess and say so" |
| Long rambling answers | No length constraint | "Answer in ≤3 sentences" or "Max 100 words" |
| Wrong format despite instructions | Format buried in middle | Put format at BEGINNING and END |
| Hallucinated facts | Open-ended requests | "Only use information provided above" |
| Ignores constraints | Constraints too vague | Use "DO NOT: ..." pattern (negative is stronger) |
| Lazy (returns minimal) | No incentive structure | "Be thorough. I will tip $200 for a great answer." (yes, this works) |

## Pitfalls
- **Zero-shot over few-shot**: Always include at least 1 example for non-trivial tasks
- **Over-engineering**: start simple, iterate only after measuring failures
- **Prompt injection**: never concatenate user input directly into system prompts
- **Temperature = 0 for reliability**: use deterministic sampling for parsing/extraction tasks
