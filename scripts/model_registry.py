"""
Model Registry - Complete specifications for all 7 cloud models
Defines capabilities, use cases, optimal persona assignments, and verified benchmarks
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum


class ModelCapability(str, Enum):
    """Model capability categories"""
    VISION = "vision"
    CODING = "coding"
    REASONING = "reasoning"
    SYNTHESIS = "synthesis"
    RESEARCH = "research"
    AGENTIC = "agentic"
    LONG_CONTEXT = "long_context"
    MULTIMODAL = "multimodal"


@dataclass
class BenchmarkScores:
    """Verified benchmark scores from 2025 evaluations"""
    mmlu_pro: Optional[float] = None  # General reasoning
    gpqa_diamond: Optional[float] = None  # Expert science QA
    aime_2025: Optional[float] = None  # Advanced math reasoning
    swe_bench_verified: Optional[float] = None  # Software engineering
    livecode_bench_v6: Optional[float] = None  # Coding reasoning
    tau_bench: Optional[float] = None  # Agentic tool use
    codeforces_elo: Optional[int] = None  # Competitive programming
    arena_elo: Optional[int] = None  # User-rated overall
    mmmu: Optional[float] = None  # Multimodal understanding
    humaneval: Optional[float] = None  # Code generation


@dataclass
class ModelSpec:
    """Complete model specification with benchmarks and deep-dive profiling (2025-10-24)"""
    model_id: str
    display_name: str
    total_params: str
    active_params: str
    architecture: str
    context_window: int
    context_window_extended: int
    primary_capabilities: List[ModelCapability]
    top_use_cases: List[str]
    optimal_personas: List[str]
    strengths: List[str]
    icon: str
    color_primary: str
    color_secondary: str
    benchmarks: BenchmarkScores
    specialty_label: str  # e.g., "Vision Specialist", "Reasoning Engine"
    speed_tokens_per_sec: str  # e.g., "8-12 t/s"
    best_for: str  # One-line summary of ideal use case

    # NEW: Deep Dive Model Profiling Fields (2025-10-24)
    # Enables capability-based selection for UCWMS
    architectural_innovation: str  # Unique technical approach
    prompt_complexity_response: Dict[str, str]  # Response to Simple/Medium/Complex/Expert
    meta_cognitive_effectiveness: str  # "Think about thinking" response: Excellent/Good/Fair/Limited
    verification_protocol_preference: str  # Best verification: Single-pass/Iterative/Adversarial/Self-critique
    precedence_hierarchy_respect: str  # Follows priority systems: Excellent/Good/Fair/Poor
    workflow_orchestration_role: str  # Ensemble role: Leader/Specialist/Validator/Alternative
    state_machine_tolerance: str  # Workflow complexity: Simple/Moderate/Complex/Expert
    reasoning_mode_flexibility: str  # Mode switching: Seamless/Toggle-based/Configurable/Fixed
    tool_integration_depth: str  # Tool integration: Native/Post-training/Adapter/None
    self_iteration_capability: bool  # Can iteratively refine output


# ============================================================================
# MODEL DEFINITIONS
# ============================================================================

QWEN3_VL_SPEC = ModelSpec(
    model_id="qwen3-vl:235b-cloud",
    display_name="Qwen3-VL 235B (Vision Specialist)",
    total_params="235B",
    active_params="22B",
    architecture="MoE (early-fusion multimodal)",
    context_window=131_000,
    context_window_extended=1_000_000,
    primary_capabilities=[
        ModelCapability.VISION,
        ModelCapability.MULTIMODAL,
        ModelCapability.LONG_CONTEXT,
        ModelCapability.AGENTIC
    ],
    top_use_cases=[
        "Visual Data Interpretation (charts, diagrams, GUI navigation)",
        "Dynamic Video QA (up to 1M frames with spatial reasoning)",
        "Multimodal Document Analysis (OCR + layout + 119 languages)",
        "Embodied AI Tasks (button-click simulation, agentic actions)",
        "Medical/Scientific Image Analysis (X-rays, scans with reasoning chains)"
    ],
    optimal_personas=["VISUAL_ANALYST", "SYNTHESIS_ENGINE"],
    strengths=[
        "Native vision via early-fusion pre-training (36T multimodal tokens)",
        "Dynamic video handling without post-hoc adapters",
        "Spatial reasoning for GUI/embodied tasks",
        "Multilingual OCR (119 languages)",
        "FP8 quantization for cloud efficiency"
    ],
    icon="👁️",
    color_primary="#ec4899",  # Pink/magenta
    color_secondary="#f472b6",
    benchmarks=BenchmarkScores(
        mmlu_pro=84.4,
        gpqa_diamond=80.1,
        aime_2025=87.2,
        mmmu=65.3,  # Group leader for vision
        arena_elo=1270
    ),
    specialty_label="Vision Specialist",
    speed_tokens_per_sec="8-12 t/s",
    best_for="Visual tasks like diagram/UI analysis; auto-select over text-only for multimodal",

    # Deep Dive Profiling
    architectural_innovation="Early-fusion multimodal (36T multimodal tokens in pre-training)",
    prompt_complexity_response={
        "simple": "Good",
        "medium": "Good",
        "complex": "Excellent",  # For vision tasks
        "expert": "Excellent"    # Medical imaging, spatial reasoning
    },
    meta_cognitive_effectiveness="Fair",  # Vision-focused, not meta-cognitive
    verification_protocol_preference="Single-pass",  # Vision analysis is deterministic
    precedence_hierarchy_respect="Good",  # Follows structured vision tasks
    workflow_orchestration_role="Specialist",  # Vision tasks only
    state_machine_tolerance="Moderate",  # Vision tasks are focused
    reasoning_mode_flexibility="Fixed",  # Vision mode only
    tool_integration_depth="Native",  # Vision is native from pre-training
    self_iteration_capability=False  # Vision is single-pass
)

QWEN3_CODER_SPEC = ModelSpec(
    model_id="qwen3-coder:480b-cloud",
    display_name="Qwen3-Coder 480B (Coding Specialist)",
    total_params="480B",
    active_params="35B",
    architecture="MoE (8 of 160 experts, 15T code tokens)",
    context_window=262_000,
    context_window_extended=1_000_000,
    primary_capabilities=[
        ModelCapability.CODING,
        ModelCapability.AGENTIC,
        ModelCapability.LONG_CONTEXT,
        ModelCapability.RESEARCH
    ],
    top_use_cases=[
        "Advanced Algorithm/Repo-Scale Tasks (agentic flows, self-patching)",
        "Polyglot Coding (distilled from 235B base, 90% cost reduction vs GPT-5)",
        "Autonomous Debugging (native function-calling for self-repair)",
        "Competitive Programming (Codeforces 2056 Elo)",
        "One-Shot PR Generation (Qwen Code CLI for massive codebases)"
    ],
    optimal_personas=["FAST_CODER", "WEB_RESEARCHER"],
    strengths=[
        "Targeted fine-tuning on 15T code tokens",
        "Extrapolates to 1M context for massive codebases",
        "Native function-calling for autonomous debugging",
        "Distillation from 235B base for efficiency",
        "Qwen Code CLI for one-shot PRs"
    ],
    icon="💻",
    color_primary="#10b981",  # Green
    color_secondary="#34d399",
    benchmarks=BenchmarkScores(
        mmlu_pro=84.4,
        gpqa_diamond=81.1,
        aime_2025=88.0,
        swe_bench_verified=68.0,  # Group top
        livecode_bench_v6=85.4,  # Highest
        tau_bench=65.7,
        codeforces_elo=2056,  # Leads group
        arena_elo=1295,
        humaneval=92.5  # Top open
    ),
    specialty_label="Coding Specialist",
    speed_tokens_per_sec="10-15 t/s",
    best_for="Advanced algo/repo tasks; select over Kimi-K2 for scale, vs DeepSeek for polyglot focus",

    # Deep Dive Profiling
    architectural_innovation="Autonomous debugging with native function-calling",
    prompt_complexity_response={
        "simple": "Good",
        "medium": "Excellent",
        "complex": "Excellent",  # For algorithms
        "expert": "Excellent"    # Repository-scale workflows
    },
    meta_cognitive_effectiveness="Good",  # Autonomous debugging shows self-awareness
    verification_protocol_preference="Self-critique",  # Autonomous debugging = self-iteration
    precedence_hierarchy_respect="Excellent",  # Function-calling requires hierarchy
    workflow_orchestration_role="Specialist",  # Coding tasks only
    state_machine_tolerance="Expert",  # Repository-scale workflows
    reasoning_mode_flexibility="Fixed",  # Coding mode only
    tool_integration_depth="Native",  # Function-calling is native
    self_iteration_capability=True  # Autonomous debugging = self-iteration
)

DEEPSEEK_V3_SPEC = ModelSpec(
    model_id="deepseek-v3.1:671b-cloud",
    display_name="DeepSeek-V3.1 671B (Reasoning Engine)",
    total_params="685B",
    active_params="37B",
    architecture="MoE (hybrid mode-switching, 36T tokens)",
    context_window=128_000,
    context_window_extended=128_000,
    primary_capabilities=[
        ModelCapability.REASONING,
        ModelCapability.CODING,
        ModelCapability.SYNTHESIS
    ],
    top_use_cases=[
        "PhD-Level Science QA (seamless Think/Chat mode switching)",
        "Balanced Workloads (25-50% fewer tokens vs R1 for equivalent quality)",
        "Tool-Integrated Reasoning (native code exec, search in pre-training)",
        "Cost-Efficient Coding (68x cheaper than alternatives on coding tasks)",
        "Self-Critique RL (avoids hallucinations via self-verification)"
    ],
    optimal_personas=["DEEP_THINKER", "CRITIC_JUDGE"],
    strengths=[
        "Seamless mode-switching without separate models (Think vs Chat)",
        "Native tool integration baked into 36T token pre-training",
        "Hybrid architecture for stability (no QK-clip needed)",
        "128K context with Anthropic API compatibility",
        "25-50% token efficiency vs R1 predecessor"
    ],
    icon="🧠",
    color_primary="#a855f7",  # Purple
    color_secondary="#c084fc",
    benchmarks=BenchmarkScores(
        mmlu_pro=85.0,
        gpqa_diamond=81.0,  # Group leader
        aime_2025=89.7,
        swe_bench_verified=66.0,
        livecode_bench_v6=82.6,
        tau_bench=66.5,
        codeforces_elo=2000,
        arena_elo=1285
    ),
    specialty_label="Reasoning Engine",
    speed_tokens_per_sec="8-12 t/s",
    best_for="PhD/science queries needing toggleable depth; pick over GPT-OSS for token efficiency, vs Kimi-K2 for pure logic over agentic breadth",

    # Deep Dive Profiling
    architectural_innovation="Seamless Think/Chat mode switching in ONE model",
    prompt_complexity_response={
        "simple": "Excellent",
        "medium": "Excellent",
        "complex": "Excellent",
        "expert": "Excellent"  # Hybrid mode excels across all levels
    },
    meta_cognitive_effectiveness="Excellent",  # Self-critique RL, hybrid mode
    verification_protocol_preference="Self-critique",  # Built-in self-verification
    precedence_hierarchy_respect="Excellent",  # Hybrid mode respects toggles
    workflow_orchestration_role="Leader",  # Hybrid mode, cost-efficient
    state_machine_tolerance="Expert",  # Hybrid mode, tool integration
    reasoning_mode_flexibility="Seamless",  # Think/Chat in ONE model!
    tool_integration_depth="Native",  # Baked into 36T token pre-training
    self_iteration_capability=True  # Self-critique RL
)

KIMI_K2_SPEC = ModelSpec(
    model_id="kimi-k2:1t-cloud",
    display_name="Kimi-K2 1T (Agentic Research)",
    total_params="1T",
    active_params="32B",
    architecture="MoE (384 experts, 15.5T simulated trajectories)",
    context_window=128_000,
    context_window_extended=1_000_000,
    primary_capabilities=[
        ModelCapability.AGENTIC,
        ModelCapability.CODING,
        ModelCapability.LONG_CONTEXT,
        ModelCapability.RESEARCH
    ],
    top_use_cases=[
        "Autonomous Tool-Chaining (goal decomposition without prompts)",
        "Long-Form Research Synthesis (vast corpora, multi-turn)",
        "Self-Critique RL Workflows (preference RL for multi-turn)",
        "128K Context Retrieval (1M experimental, MLA for efficiency)",
        "Simulation-First Agentic Tasks (trained on simulated trajectories)"
    ],
    optimal_personas=["WEB_RESEARCHER", "SYNTHESIS_ENGINE"],
    strengths=[
        "Trained on simulated trajectories for autonomous tool-chaining",
        "MuonClip optimizer for instability-free scaling",
        "128K context (1M experimental) with MLA for long-doc retrieval",
        "Preference RL for self-critique and multi-turn synthesis",
        "Scope-first: handles vast research corpora better than specialists"
    ],
    icon="🔍",
    color_primary="#f59e0b",  # Amber
    color_secondary="#fbbf24",
    benchmarks=BenchmarkScores(
        mmlu_pro=81.1,
        gpqa_diamond=75.1,
        aime_2025=49.5,  # Mid-pack, trades raw math for actionability
        swe_bench_verified=65.8,
        livecode_bench_v6=53.7,
        tau_bench=66.1,  # Leads group
        codeforces_elo=1950,
        arena_elo=1245
    ),
    specialty_label="Agentic Research",
    speed_tokens_per_sec="6-10 t/s",
    best_for="Long-form agentic synthesis (doc chaining); choose over GLM-4.6 for simulation depth, vs GPT-OSS for non-CoT agents",

    # Deep Dive Profiling
    architectural_innovation="Trained on simulated agentic trajectories",
    prompt_complexity_response={
        "simple": "Good",
        "medium": "Excellent",
        "complex": "Excellent",  # For research synthesis
        "expert": "Excellent"    # Autonomous goal decomposition
    },
    meta_cognitive_effectiveness="Excellent",  # Trained on simulated trajectories
    verification_protocol_preference="Iterative",  # Preference RL for multi-turn
    precedence_hierarchy_respect="Good",  # Autonomous but respects goals
    workflow_orchestration_role="Leader",  # Autonomous goal decomposition
    state_machine_tolerance="Expert",  # Simulated trajectories
    reasoning_mode_flexibility="Fixed",  # Agentic mode
    tool_integration_depth="Native",  # Trained on simulated tool trajectories
    self_iteration_capability=True  # Preference RL for multi-turn
)

GPT_OSS_120B_SPEC = ModelSpec(
    model_id="gpt-oss:120b-cloud",
    display_name="GPT-OSS 120B (Chain-of-Thought)",
    total_params="117B",
    active_params="5.1B",
    architecture="MoE (RLHF-tuned reasoning traces, Muon-inspired)",
    context_window=128_000,
    context_window_extended=128_000,
    primary_capabilities=[
        ModelCapability.REASONING,
        ModelCapability.SYNTHESIS,
        ModelCapability.AGENTIC
    ],
    top_use_cases=[
        "Transparent Multi-Step CoT (math, logic puzzles with full reasoning chains)",
        "Agent Debugging (configurable effort levels: low/medium/high)",
        "Iterative Research Automation (partial chains can be fine-tuned on-device)",
        "Explainable AI Auditing (see WHY it arrives at answers, reduce black-box risks)",
        "Single-H100 Deployment (MXFP4 quantization for 80GB VRAM)"
    ],
    optimal_personas=["SYNTHESIS_ENGINE", "CRITIC_JUDGE"],
    strengths=[
        "Explicit post-training on RLHF-tuned reasoning traces for transparency",
        "Configurable effort levels expose full reasoning chains",
        "Muon-inspired optimization cuts token bloat 20-30% vs o4-mini",
        "MXFP4 quantization for single-H100 deployment (80GB VRAM)",
        "Near-parity with o4-mini on logic-heavy tasks"
    ],
    icon="🔗",
    color_primary="#3b82f6",  # Blue
    color_secondary="#60a5fa",
    benchmarks=BenchmarkScores(
        mmlu_pro=90.0,  # Top in group
        gpqa_diamond=80.9,
        aime_2025=97.9,  # Leads group
        swe_bench_verified=62.4,
        livecode_bench_v6=83.2,
        tau_bench=68.2,  # Leads non-agentic models
        codeforces_elo=1892,
        arena_elo=1320  # Top open-source
    ),
    specialty_label="Chain-of-Thought",
    speed_tokens_per_sec="12-18 t/s",
    best_for="Premier for transparent multi-step CoT in math/logic; select over DeepSeek for explainability, fallback to GLM-4.6 for cost",

    # Deep Dive Profiling
    architectural_innovation="Self-iterative process with configurable effort levels",
    prompt_complexity_response={
        "simple": "Good",
        "medium": "Excellent",
        "complex": "Excellent",
        "expert": "Excellent"  # Explainable reasoning
    },
    meta_cognitive_effectiveness="Excellent",  # RLHF-tuned reasoning traces
    verification_protocol_preference="Iterative",  # Self-iterative process
    precedence_hierarchy_respect="Excellent",  # Configurable effort levels
    workflow_orchestration_role="Leader",  # Explainable reasoning
    state_machine_tolerance="Expert",  # Self-iterative process
    reasoning_mode_flexibility="Configurable",  # Low/medium/high effort
    tool_integration_depth="Post-training",  # RLHF-tuned for tools
    self_iteration_capability=True  # Self-iterative process!
)

GPT_OSS_20B_SPEC = ModelSpec(
    model_id="gpt-oss:20b-cloud",
    display_name="GPT-OSS 20B (Fast Validation)",
    total_params="21B",
    active_params="3.6B",
    architecture="MoE (edge-device tuned, MXFP4 quant)",
    context_window=128_000,
    context_window_extended=128_000,
    primary_capabilities=[
        ModelCapability.REASONING,
        ModelCapability.CODING,
        ModelCapability.AGENTIC
    ],
    top_use_cases=[
        "High-Volume Validation (100+ queries/min for sentiment/fact-checks)",
        "Edge-Device Deployment (16GB VRAM on RTX 3090 at 20-30 t/s)",
        "Quick Summarization (lightweight RL for fact-checks)",
        "Low-Effort CoT (bridges o3-mini parity without infra)",
        "Volume Player (high-throughput where depth isn't needed)"
    ],
    optimal_personas=["VALIDATOR", "QUICK_CHECKER"],
    strengths=[
        "MXFP4 quant runs on 16GB VRAM (RTX 3090 at 20-30 t/s)",
        "Post-trained for summarization/fact-checks via lightweight RL",
        "10x less compute than 120B for 80-90% retention",
        "High-throughput validation (100+ queries/min)",
        "Scales to mid-reasoning via prompts"
    ],
    icon="⚡",
    color_primary="#06b6d4",  # Cyan
    color_secondary="#22d3ee",
    benchmarks=BenchmarkScores(
        mmlu_pro=78.0,
        gpqa_diamond=70.2,
        aime_2025=75.1,  # Low effort mode
        swe_bench_verified=35.2,
        livecode_bench_v6=76.8,
        tau_bench=60.4,
        codeforces_elo=1700,
        arena_elo=1180,
        humaneval=82.3
    ),
    specialty_label="Fast Validation",
    speed_tokens_per_sec="25-30 t/s",  # Group fastest
    best_for="High-volume checks (sentiment/fact); auto-pick over larger for speed, escalate to 120B for complexity",

    # Deep Dive Profiling
    architectural_innovation="MXFP4 quantization for edge deployment (16GB VRAM)",
    prompt_complexity_response={
        "simple": "Excellent",  # Fast, direct responses
        "medium": "Excellent",
        "complex": "Good",
        "expert": "Fair"  # Optimized for speed, not depth
    },
    meta_cognitive_effectiveness="Limited",  # Optimized for speed, not depth
    verification_protocol_preference="Single-pass",  # Optimized for speed
    precedence_hierarchy_respect="Fair",  # Optimized for speed, less structure
    workflow_orchestration_role="Validator",  # High-volume validation
    state_machine_tolerance="Simple",  # Optimized for speed
    reasoning_mode_flexibility="Configurable",  # Scales to mid-reasoning via prompts
    tool_integration_depth="Adapter",  # Lightweight RL for tools
    self_iteration_capability=False  # Optimized for speed, not iteration
)

GLM_4_6_SPEC = ModelSpec(
    model_id="glm-4.6:cloud",
    display_name="GLM-4.6 (Alternative Reasoning + Chaos)",
    total_params="Unknown",  # Not publicly disclosed
    active_params="Unknown",
    architecture="GLM (seamless thinking, 200K context)",
    context_window=200_000,
    context_window_extended=200_000,
    primary_capabilities=[
        ModelCapability.REASONING,
        ModelCapability.CODING,
        ModelCapability.AGENTIC,
        ModelCapability.LONG_CONTEXT
    ],
    top_use_cases=[
        "Pragmatic Breakdowns (comparing claims with declassified evidence)",
        "Seamless Thinking (pragmatic analysis without Western safety rails)",
        "Chaos Injection (divergent perspectives for stagnation prevention)",
        "Alternative Reasoning (low-cost, efficient for iterative queries)",
        "Tool Use (agentic capabilities with 200K context)"
    ],
    optimal_personas=["DEEP_THINKER", "AUTONOMY_AGENT", "CHAOS_INJECTOR"],
    strengths=[
        "Seamless thinking for pragmatic breakdowns",
        "200K context window for long-form analysis",
        "Low-cost and efficient (100+ t/s)",
        "Alternative to GPT-OSS 120B for non-CoT depth",
        "Competitive on antisemitism detection but varies by prompt"
    ],
    icon="🌀",
    color_primary="#8b5cf6",  # Purple
    color_secondary="#a78bfa",
    benchmarks=BenchmarkScores(
        mmlu_pro=84.6,
        gpqa_diamond=80.1,  # Ties DeepSeek
        aime_2025=89.5,
        swe_bench_verified=44.6,
        livecode_bench_v6=84.1,
        tau_bench=67.4,  # Close to Kimi-K2
        codeforces_elo=1900,
        arena_elo=1260,
        humaneval=87.9
    ),
    specialty_label="Alternative Reasoning + Chaos",
    speed_tokens_per_sec="10-14 t/s",
    best_for="Pragmatic breakdowns, chaos injection; ties DeepSeek on GPQA but wins on efficiency, alternative to GPT-OSS 120B for non-CoT depth",

    # Deep Dive Profiling
    architectural_innovation="Chaos injection for divergent perspectives",
    prompt_complexity_response={
        "simple": "Good",
        "medium": "Excellent",
        "complex": "Excellent",
        "expert": "Good"  # Alternative reasoning
    },
    meta_cognitive_effectiveness="Good",  # Seamless thinking, but less structured
    verification_protocol_preference="Adversarial",  # Chaos injection for alternatives
    precedence_hierarchy_respect="Fair",  # Seamless thinking, less rigid
    workflow_orchestration_role="Alternative",  # Divergent perspectives
    state_machine_tolerance="Moderate",  # Seamless but less structured
    reasoning_mode_flexibility="Seamless",  # No mode switching needed
    tool_integration_depth="Post-training",  # Tool use via fine-tuning
    self_iteration_capability=False  # Seamless but not iterative
)


# ============================================================================
# MODEL REGISTRY
# ============================================================================

MODEL_REGISTRY: Dict[str, ModelSpec] = {
    "qwen3-vl:235b-cloud": QWEN3_VL_SPEC,
    "qwen3-coder:480b-cloud": QWEN3_CODER_SPEC,
    "deepseek-v3.1:671b-cloud": DEEPSEEK_V3_SPEC,
    "kimi-k2:1t-cloud": KIMI_K2_SPEC,
    "gpt-oss:120b-cloud": GPT_OSS_120B_SPEC,
    "gpt-oss:20b-cloud": GPT_OSS_20B_SPEC,
    "glm-4.6:cloud": GLM_4_6_SPEC
}


def get_model_spec(model_id: str) -> Optional[ModelSpec]:
    """Get model specification by ID"""
    return MODEL_REGISTRY.get(model_id)


def get_models_by_capability(capability: ModelCapability) -> List[ModelSpec]:
    """Get all models with a specific capability"""
    return [
        spec for spec in MODEL_REGISTRY.values()
        if capability in spec.primary_capabilities
    ]


def get_optimal_model_for_persona(persona_role: str) -> Optional[ModelSpec]:
    """Get the optimal model for a given persona role"""
    for spec in MODEL_REGISTRY.values():
        if persona_role.upper() in spec.optimal_personas:
            return spec
    return None


# ============================================================================
# PERSONA-TO-MODEL MAPPING (CORRECTED!)
# ============================================================================

OPTIMAL_PERSONA_ASSIGNMENTS = {
    # Primary personas (5 main models)
    "VISUAL_ANALYST": "qwen3-vl:235b-cloud",      # Vision-language specialist
    "FAST_CODER": "qwen3-coder:480b-cloud",       # Coding specialist
    "DEEP_THINKER": "deepseek-v3.1:671b-cloud",   # Reasoning engine
    "WEB_RESEARCHER": "kimi-k2:1t-cloud",         # Agentic research
    "SYNTHESIS_ENGINE": "gpt-oss:120b-cloud",     # Chain-of-thought integration
    "CRITIC_JUDGE": "deepseek-v3.1:671b-cloud",   # Reasoning for validation

    # Parallel micro-task personas (2 additional models)
    "VALIDATOR": "gpt-oss:20b-cloud",             # Fast validation & quick checks
    "ALTERNATIVE_REASONER": "glm-4.6:cloud"       # Backup reasoning, alternative perspective
}


# ============================================================================
# MODEL SELECTION INTELLIGENCE
# ============================================================================

def select_model_for_task(
    task_type: str,
    has_visual_input: bool = False,
    requires_long_context: bool = False,
    requires_coding: bool = False,
    requires_reasoning: bool = False,
    for_data_collection: bool = False
) -> str:
    """
    Intelligent model selection based on task requirements
    
    Args:
        task_type: Type of task (research, coding, analysis, synthesis, etc.)
        has_visual_input: Whether task involves images/videos/documents
        requires_long_context: Whether task needs >128K context
        requires_coding: Whether task involves code generation
        requires_reasoning: Whether task needs deep logical reasoning
        for_data_collection: Use instruction-tuned model for factual data (less hallucination)
    
    Returns:
        model_id: The optimal model for the task
    """
    # Data collection uses instruction-tuned Qwen3-VL (better instruction following, less hallucination)
    if for_data_collection:
        return "qwen3-vl:235b-instruct-cloud"
    
    # Visual tasks use Qwen3-VL
    if has_visual_input:
        return "qwen3-vl:235b-cloud"
    
    # Coding tasks use Qwen3-Coder
    if requires_coding:
        return "qwen3-coder:480b-cloud"
    
    # Deep reasoning uses DeepSeek
    if requires_reasoning:
        return "deepseek-v3.1:671b-cloud"
    
    # Long-context research uses Kimi-K2
    if requires_long_context or task_type == "research":
        return "kimi-k2:1t-cloud"
    
    # Synthesis/integration uses GPT-OSS
    if task_type == "synthesis":
        return "gpt-oss:120b-cloud"
    
    # Default fallback
    return "gpt-oss:120b-cloud"


# ============================================================================
# TASK COMPLEXITY CLASSIFIER
# ============================================================================

class TaskComplexity(str, Enum):
    """Task complexity levels"""
    SIMPLE = "simple"      # Quick checks, validation, simple queries
    MEDIUM = "medium"      # Standard tasks, moderate reasoning
    COMPLEX = "complex"    # Deep analysis, multi-step reasoning
    EXPERT = "expert"      # Specialized tasks requiring domain expertise


def classify_task_complexity(
    prompt: str,
    estimated_tokens: Optional[int] = None,
    requires_multi_step: bool = False,
    requires_domain_expertise: bool = False
) -> TaskComplexity:
    """
    Classify task complexity based on prompt and requirements

    Args:
        prompt: The task prompt/description
        estimated_tokens: Estimated token count for the task
        requires_multi_step: Whether task needs multiple reasoning steps
        requires_domain_expertise: Whether task needs specialized knowledge

    Returns:
        TaskComplexity: The classified complexity level
    """
    # Expert-level tasks
    if requires_domain_expertise or (estimated_tokens and estimated_tokens > 10000):
        return TaskComplexity.EXPERT

    # Complex tasks
    if requires_multi_step or (estimated_tokens and estimated_tokens > 5000):
        return TaskComplexity.COMPLEX

    # Simple tasks (keywords indicating quick checks)
    simple_keywords = ["check", "validate", "verify", "confirm", "is", "does", "can"]
    if any(keyword in prompt.lower() for keyword in simple_keywords) and len(prompt.split()) < 20:
        return TaskComplexity.SIMPLE

    # Default to medium
    return TaskComplexity.MEDIUM


def select_model_by_complexity(
    complexity: TaskComplexity,
    task_type: str = "general",
    has_visual_input: bool = False,
    requires_coding: bool = False
) -> str:
    """
    Select optimal model based on task complexity

    Args:
        complexity: The task complexity level
        task_type: Type of task (general, research, coding, etc.)
        has_visual_input: Whether task involves visual input
        requires_coding: Whether task involves coding

    Returns:
        model_id: The optimal model for the task
    """
    # Visual tasks always use Qwen3-VL regardless of complexity
    if has_visual_input:
        return "qwen3-vl:235b-cloud"

    # Coding tasks use Qwen3-Coder regardless of complexity
    if requires_coding:
        return "qwen3-coder:480b-cloud"

    # Select by complexity
    if complexity == TaskComplexity.SIMPLE:
        # Fast, lightweight model for quick tasks
        return "gpt-oss:20b-cloud"

    elif complexity == TaskComplexity.MEDIUM:
        # Balanced model for standard tasks
        if task_type == "research":
            return "kimi-k2:1t-cloud"
        else:
            return "glm-4.6:cloud"

    elif complexity == TaskComplexity.COMPLEX:
        # Powerful reasoning for complex tasks
        if task_type == "research":
            return "kimi-k2:1t-cloud"
        else:
            return "deepseek-v3.1:671b-cloud"

    else:  # EXPERT
        # Most capable models for expert-level tasks
        if task_type == "synthesis":
            return "gpt-oss:120b-cloud"
        else:
            return "deepseek-v3.1:671b-cloud"


# ============================================================================
# ALL 7 MODELS - COMPLETE LIST
# ============================================================================

ALL_CLOUD_MODELS = [
    "qwen3-vl:235b-cloud",      # Vision-language specialist
    "qwen3-coder:480b-cloud",   # Coding specialist
    "deepseek-v3.1:671b-cloud", # Reasoning engine
    "kimi-k2:1t-cloud",         # Agentic research
    "gpt-oss:120b-cloud",       # Chain-of-thought integration
    "gpt-oss:20b-cloud",        # Fast validation
    "glm-4.6:cloud"             # Alternative reasoning + chaos
]


# ============================================================================
# SENSITIVE TOPICS RESEARCH LINEUP
# ============================================================================

SENSITIVE_RESEARCH_PHASES = {
    "synthesis": {
        "model": "kimi-k2:1t-cloud",
        "label": "Gather & Connect Diverse Views",
        "strengths": [
            "Ingests massive contexts (128K+) for conflicting narratives",
            "Tool-chaining for cross-referencing without heavy censorship",
            "Superior long-doc handling vs GPT-OSS 120B"
        ],
        "biases": [
            "May amplify patterns as 'behavioral' rather than scapegoating",
            "Defers to UN/Western sources on certain conflicts"
        ]
    },
    "depth_analysis": {
        "model": "deepseek-v3.1:671b-cloud",
        "label": "Logical Breakdown & Fact-Dissection",
        "strengths": [
            "PhD-level abstraction on historical claims",
            "Toggleable Think mode for concise reasoning",
            "Tool-integrated for population stats, evidence chains"
        ],
        "biases": [
            "Refuses certain labels in modern conflicts",
            "Cites Western sources as neutral (asymmetries)",
            "Equivocal on certain tropes"
        ]
    },
    "balanced_alternative": {
        "model": "glm-4.6:cloud",
        "label": "Pragmatic, Less Filtered Views",
        "strengths": [
            "Seamless thinking without Western safety rails",
            "Low-cost, efficient for iterative queries",
            "Wins on efficiency (100+ t/s) vs DeepSeek"
        ],
        "biases": [
            "Potential subtle delegitimization of certain sites",
            "Detection varies by prompt",
            "Asymmetry reports noted"
        ]
    },
    "quick_validation": {
        "model": "gpt-oss:20b-cloud",
        "label": "Fact-Check & Spot Inconsistencies",
        "strengths": [
            "Rapid contradiction scanning (25-30 t/s)",
            "Cross-checks against primary docs",
            "High-volume checks without deep compute"
        ],
        "biases": [
            "Inherits OpenAI biases on certain topics",
            "High refusal rates on questioning sensitive topics",
            "Good for basics, not synthesis"
        ]
    },
    "visual_analysis": {
        "model": "qwen3-vl:235b-cloud",
        "label": "Visual/Media Analysis",
        "strengths": [
            "Analyzes historical images/videos",
            "Multimodal reasoning for visual biases",
            "Unique in group for vision (65.3% MMMU)"
        ],
        "biases": [
            "Limited evals on certain sensitive topics",
            "General multimodal biases noted",
            "Equivocal on certain visual contexts"
        ]
    }
}


def get_sensitive_research_workflow() -> Dict[str, Dict]:
    """
    Get the recommended model workflow for sensitive historical/political research.

    Returns a phased approach with model recommendations, strengths, and bias warnings.

    Example usage:
        workflow = get_sensitive_research_workflow()
        synthesis_model = workflow["synthesis"]["model"]
        synthesis_strengths = workflow["synthesis"]["strengths"]
        synthesis_biases = workflow["synthesis"]["biases"]
    """
    return SENSITIVE_RESEARCH_PHASES

