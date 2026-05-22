from nerd_scroll.state import RuntimeState


def test_runtime_state_rewinds() -> None:
    state = RuntimeState(source_path="source.txt", source_line_count=2)
    state.advance_line()
    state.advance_line()
    assert state.rewind_if_needed() is True
    assert state.loop_count == 1
