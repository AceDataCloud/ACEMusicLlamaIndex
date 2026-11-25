import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

from llama_index.tools.acemusic_acedatacloud import AceMusicToolSpec


def test_native_tool_discovery_and_original_task(monkeypatch):
    monkeypatch.setenv("ACEDATACLOUD_API_TOKEN", "offline-example")
    collection = AceMusicToolSpec().to_tool_list()
    named = {t.metadata.name: t for t in collection}
    assert set(named) == {
        "acemusic_generate_custom_music",
        "acemusic_cover_audio",
        "acemusic_generate_music",
        "acemusic_get_task",
        "acemusic_upload_audio",
        "acemusic_generate_lyrics",
        "acemusic_mashup_audio",
    }
    with patch("llama_index.tools.acemusic_acedatacloud.base.AceDataCloud") as constructor:
        api = constructor.return_value.__enter__.return_value.acemusic
        api.generate.return_value = MagicMock(id="original")
        api.tasks.return_value = {"status": "partial_failed", "response": {"data": []}}
        result = named["acemusic_generate_music"].call(prompt="sample").raw_output
        assert result == {"task_id": "original"}
        api.generate.assert_called_once_with(action="generate", prompt="sample", model="acemusic-v1.1", async_=True)
        record = named["acemusic_get_task"].call(task_id="original").raw_output
        assert record["status"] == "partial_failed"
        api.tasks.assert_called_once_with(action="retrieve", id="original")
        assert constructor.call_args.kwargs["max_retries"] == 0


def test_reference_and_lyrics_requests_keep_platform_ids(monkeypatch):
    monkeypatch.setenv("ACEDATACLOUD_API_TOKEN", "offline-example")
    collection = AceMusicToolSpec().to_tool_list()
    named = {t.metadata.name: t for t in collection}

    def invoke(name, **kwargs):
        tool = named["acemusic_" + name]
        return tool.call(**kwargs).raw_output

    with patch("llama_index.tools.acemusic_acedatacloud.base.AceDataCloud") as constructor:
        api = constructor.return_value.__enter__.return_value.acemusic
        api.generate.return_value = MagicMock(id="original")
        assert invoke("generate_custom_music", lyric="verse", style="rock", title="song") == {"task_id": "original"}
        api.generate.assert_called_once_with(
            action="generate",
            custom=True,
            lyric="verse",
            style="rock",
            title="song",
            model="acemusic-v1.1",
            async_=True,
        )
        invoke("upload_audio", audio_url="https://example.org/ref.mp3")
        api.generate.assert_called_with(
            action="upload", audio_url="https://example.org/ref.mp3", name=None, async_=True
        )
        invoke("cover_audio", audio_id="track1", lyric="verse", style="rock")
        api.generate.assert_called_with(
            action="cover",
            audio_id="track1",
            lyric="verse",
            style="rock",
            model="acemusic-v1.1",
            title=None,
            async_=True,
        )
        invoke("mashup_audio", first_audio_id="track1", second_audio_id="track2", lyric="verse", style="rock")
        api.generate.assert_called_with(
            action="mashup",
            mashup_audio_ids=["track1", "track2"],
            lyric="verse",
            style="rock",
            model="acemusic-v1.1",
            title=None,
            async_=True,
        )
        api.lyrics.return_value = {"success": True, "data": [{"title": "song", "text": "verse"}]}
        assert invoke("generate_lyrics", prompt="rock song")["data"][0]["text"] == "verse"
        api.lyrics.assert_called_once_with(prompt="rock song", style=None)
        assert api.generate.call_count == 4


def test_async_task_result_matches_the_sync_group_contract(monkeypatch):
    monkeypatch.setenv("ACEDATACLOUD_API_TOKEN", "offline-example")
    spec = AceMusicToolSpec()
    record = {"status": "partial_failed", "response": {"data": [{"audio_url": "https://example.org/track.mp3"}]}}
    with patch("llama_index.tools.acemusic_acedatacloud.base.AsyncAceDataCloud") as constructor:
        api = constructor.return_value.__aenter__.return_value.acemusic
        api.tasks = AsyncMock(return_value=record)
        assert asyncio.run(spec.aacemusic_get_task("original")) == record
        api.tasks.assert_awaited_once_with(action="retrieve", id="original")
