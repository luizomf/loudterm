from typing import TYPE_CHECKING

import pytest
from tokenizers import Tokenizer
from tokenizers.models import WordLevel
from transformers import PreTrainedTokenizerFast

if TYPE_CHECKING:
    from pathlib import Path


def test_tokenizer_save_rejects_chat_template_path_traversal(tmp_path: Path):
    """Offline regression for GHSA-xrqw-3rrv-vx5w / CVE-2026-9856."""
    unknown_symbol = "[UNK]"
    tokenizer = PreTrainedTokenizerFast(
        tokenizer_object=Tokenizer(
            WordLevel({unknown_symbol: 0}, unk_token=unknown_symbol),
        ),
        unk_token=unknown_symbol,
    )
    tokenizer.chat_template = {"default": "safe", "../../canary": "untrusted"}
    with pytest.raises(ValueError, match="Invalid chat template name"):
        # Transformers leaves **kwargs untyped in this public API.
        tokenizer.save_pretrained(  # pyright: ignore[reportUnknownMemberType]
            tmp_path / "saved",
        )
    assert not (tmp_path / "canary.jinja").exists()
