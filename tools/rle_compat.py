"""Optional NumPy 2-compatible RLE string adapter; not original coursework."""


def list_to_string(run_lengths):
    """Serialize integer scalars without depending on their container repr."""
    return " ".join(str(int(value)) for value in run_lengths) if len(run_lengths) else "-"
