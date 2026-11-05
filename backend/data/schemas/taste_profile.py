
from typing import Literal
from pydantic import BaseModel, Field, ConfigDict


# ============================================================
# 1. EVIDENCE
# ============================================================

class BookEvidence(BaseModel):
    """A specific book or observation supporting a taste inference."""

    model_config = ConfigDict(extra="forbid")

    book_title: str
    author: str | None = None

    user_rating: float | None = Field(
        default=None,
        ge=0,
        le=5
    )

    evidence_type: Literal[
        "explicit_positive_rating",
        "explicit_negative_rating",
        "neutral_rating",
        "unrated_shelf_presence",
        "repeated_author",
        "repeated_series",
        "book_metadata",
        "other"
    ]

    explanation: str = Field(
        description="Why this book provides evidence for the observation."
    )


# ============================================================
# 2. GENERAL PREFERENCE SIGNAL
# ============================================================

class PreferenceSignal(BaseModel):
    """
    Represents one specific preference, such as:
    psychological thrillers, unreliable narrators,
    morally ambiguous protagonists, or slow pacing.
    """

    model_config = ConfigDict(extra="forbid")

    category: Literal[
        "genre",
        "subgenre",
        "theme",
        "topic",
        "writing_style",
        "narrative_voice",
        "tone",
        "mood",
        "pacing",
        "plot_structure",
        "point_of_view",
        "character_type",
        "character_development",
        "setting",
        "historical_period",
        "book_length",
        "literary_complexity",
        "ending_type",
        "author",
        "series",
        "other"
    ]

    value: str = Field(
        description="A precise preference, not a broad generic label."
    )

    preference: Literal[
        "strong_like",
        "like",
        "mixed",
        "dislike",
        "strong_dislike",
        "interest_only",
        "unknown"
    ]

    strength: int = Field(
        default=1,
        ge=1,
        le=5,
        description="Strength of the observed preference."
    )

    confidence: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
        description="Confidence that this preference is genuinely representative."
    )

    evidence_count: int = Field(default=0, ge=0)

    evidence: list[BookEvidence] = Field(default_factory=list)

    explanation: str = Field(
        description="Reasoning behind this preference and its limitations."
    )


# ============================================================
# 3. AUTHOR PROFILE
# ============================================================

class AuthorPreference(BaseModel):
    model_config = ConfigDict(extra="forbid")

    author: str

    relationship: Literal[
        "strongly_preferred",
        "preferred",
        "mixed",
        "disliked",
        "strongly_disliked",
        "exploring",
        "insufficient_evidence"
    ]

    books_on_shelf: list[str] = Field(default_factory=list)

    positively_rated_books: list[str] = Field(default_factory=list)

    negatively_rated_books: list[str] = Field(default_factory=list)

    neutral_books: list[str] = Field(default_factory=list)

    unrated_books: list[str] = Field(default_factory=list)

    confidence: float = Field(default=0.0, ge=0.0, le=1.0)

    observations: list[str] = Field(default_factory=list)


# ============================================================
# 4. SERIES AND FRANCHISE PREFERENCES
# ============================================================

class SeriesPreference(BaseModel):
    model_config = ConfigDict(extra="forbid")

    series_name: str

    books_on_shelf: list[str] = Field(default_factory=list)

    relationship: Literal[
        "strong_interest",
        "positive",
        "mixed",
        "negative",
        "exploring",
        "unknown"
    ]

    confidence: float = Field(default=0.0, ge=0.0, le=1.0)

    observations: list[str] = Field(default_factory=list)


# ============================================================
# 5. READING BEHAVIOR
# ============================================================

class ReadingBehavior(BaseModel):
    model_config = ConfigDict(extra="forbid")

    preferred_book_length: Literal[
        "short",
        "medium",
        "long",
        "very_long",
        "no_clear_preference",
        "unknown"
    ] = "unknown"

    preferred_complexity: Literal[
        "accessible",
        "moderate",
        "complex",
        "highly_complex",
        "varied",
        "unknown"
    ] = "unknown"

    preferred_pacing: Literal[
        "fast",
        "moderate",
        "slow",
        "varied",
        "unknown"
    ] = "unknown"

    reading_period_preferences: list[str] = Field(
        default_factory=list,
        description="Publication periods or historical periods supported by evidence."
    )

    recurring_reading_interests: list[str] = Field(default_factory=list)

    reading_habits: list[str] = Field(
        default_factory=list,
        description="Observed patterns, not assumptions about reading frequency."
    )

    exploration_level: Literal[
        "exploratory",
        "focused",
        "balanced",
        "unknown"
    ] = "unknown"

    observations: list[str] = Field(default_factory=list)


# ============================================================
# 6. RATING BEHAVIOR
# ============================================================

class RatingBehavior(BaseModel):
    model_config = ConfigDict(extra="forbid")

    total_books: int = Field(default=0, ge=0)

    rated_books: int = Field(default=0, ge=0)

    unrated_books: int = Field(default=0, ge=0)

    positive_ratings: int = Field(default=0, ge=0)

    negative_ratings: int = Field(default=0, ge=0)

    neutral_ratings: int = Field(default=0, ge=0)

    average_user_rating: float | None = None

    rating_distribution: dict[str, int] = Field(
        default_factory=dict,
        description="Counts for individual ratings, such as {'1': 2, '2': 3, '5': 4}."
    )

    rating_interpretation: list[str] = Field(default_factory=list)

    rating_reliability: Literal[
        "high",
        "medium",
        "low",
        "insufficient_data"
    ] = "insufficient_data"


# ============================================================
# 7. BOOK-LEVEL PREFERENCES
# ============================================================

class BookPreference(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str

    author: str | None = None

    user_rating: float | None = None

    relationship: Literal[
        "favorite",
        "liked",
        "mixed",
        "disliked",
        "strongly_disliked",
        "unrated",
        "unknown"
    ]

    significance: str = Field(
        description="Why this book matters when understanding the user's taste."
    )


# ============================================================
# 8. PROFILE COVERAGE AND LIMITATIONS
# ============================================================

class ProfileCoverage(BaseModel):
    model_config = ConfigDict(extra="forbid")

    available_information: list[str] = Field(default_factory=list)

    missing_information: list[str] = Field(default_factory=list)

    weakly_supported_dimensions: list[str] = Field(default_factory=list)

    dimensions_with_no_evidence: list[str] = Field(default_factory=list)

    limitations: list[str] = Field(default_factory=list)


# ============================================================
# 9. RECOMMENDATION GUIDANCE
# ============================================================

class RecommendationGuidance(BaseModel):
    model_config = ConfigDict(extra="forbid")

    prioritize: list[str] = Field(
        default_factory=list,
        description="Characteristics that should be prioritized in recommendations."
    )

    avoid: list[str] = Field(
        default_factory=list,
        description="Characteristics supported by reliable negative preference evidence."
    )

    explore: list[str] = Field(
        default_factory=list,
        description="Potential interests worth testing in recommendations."
    )

    diversity_suggestions: list[str] = Field(
        default_factory=list,
        description="Ways to diversify recommendations without ignoring established preferences."
    )

    recommendation_constraints: list[str] = Field(default_factory=list)


# ============================================================
# 10. COMPLETE TASTE PROFILE
# ============================================================

class TasteProfile(BaseModel):
    model_config = ConfigDict(extra="forbid")

    # General overview
    profile_summary: str = Field(
        description="A detailed synthesis of the reader's literary taste."
    )

    distinctive_traits: list[str] = Field(
        default_factory=list,
        description="Specific characteristics that distinguish this reader's taste."
    )

    # Main preferences
    positive_preferences: list[PreferenceSignal] = Field(
        default_factory=list
    )

    negative_preferences: list[PreferenceSignal] = Field(
        default_factory=list
    )

    mixed_preferences: list[PreferenceSignal] = Field(
        default_factory=list
    )

    potential_interests: list[PreferenceSignal] = Field(
        default_factory=list,
        description="Possible interests inferred from shelf presence, not confirmed enjoyment."
    )

    # Authors and series
    author_preferences: list[AuthorPreference] = Field(
        default_factory=list
    )

    series_preferences: list[SeriesPreference] = Field(
        default_factory=list
    )

    # Book-level evidence
    favorite_books: list[BookPreference] = Field(default_factory=list)

    liked_books: list[BookPreference] = Field(default_factory=list)

    disliked_books: list[BookPreference] = Field(default_factory=list)

    neutral_books: list[BookPreference] = Field(default_factory=list)

    influential_unrated_books: list[BookPreference] = Field(
        default_factory=list
    )

    # Reading behavior
    reading_behavior: ReadingBehavior = Field(
        default_factory=ReadingBehavior
    )

    rating_behavior: RatingBehavior = Field(
        default_factory=RatingBehavior
    )

    # Evidence quality
    overall_confidence: Literal[
        "very_low",
        "low",
        "medium",
        "high"
    ] = "very_low"

    confidence_explanation: str = ""

    profile_coverage: ProfileCoverage = Field(
        default_factory=ProfileCoverage
    )

    # Recommendations
    recommendation_guidance: RecommendationGuidance = Field(
        default_factory=RecommendationGuidance
    )

    # Final interpretation
    uncertain_observations: list[str] = Field(
        default_factory=list
    )

    questions_for_better_personalization: list[str] = Field(
        default_factory=list,
        description="Information that would improve future recommendations."
    )
