import os
from typing import Any, Literal

from acedatacloud import AceDataCloud, AsyncAceDataCloud

from llama_index.core.tools.tool_spec.base import BaseToolSpec

Model = Literal["acemusic-v1.1", "acemusic-v1"]


def _task_id(task: Any) -> dict[str, str]:
    if not task.id:
        raise ValueError("Submission returned no task ID. Check usage history before retrying.")
    return {"task_id": task.id}


class AceMusicToolSpec(BaseToolSpec):
    """Native ACE Music tools using a private application credential."""

    spec_functions = [
        ("acemusic_generate_music", "aacemusic_generate_music"),
        ("acemusic_generate_custom_music", "aacemusic_generate_custom_music"),
        ("acemusic_upload_audio", "aacemusic_upload_audio"),
        ("acemusic_cover_audio", "aacemusic_cover_audio"),
        ("acemusic_mashup_audio", "aacemusic_mashup_audio"),
        ("acemusic_generate_lyrics", "aacemusic_generate_lyrics"),
        ("acemusic_get_task", "aacemusic_get_task"),
    ]

    def __init__(self, api_token: str | None = None):
        self._token = api_token or os.environ["ACEDATACLOUD_API_TOKEN"]

    def acemusic_generate_music(self, prompt: str, model: Model = "acemusic-v1.1") -> dict[str, Any]:
        """Submit one paid idea-to-song task. Save the returned task ID."""
        with AceDataCloud(api_token=self._token, max_retries=0) as client:
            return _task_id(client.acemusic.generate(action="generate", prompt=prompt, model=model, async_=True))

    async def aacemusic_generate_music(self, prompt: str, model: Model = "acemusic-v1.1") -> dict[str, Any]:
        """Submit one paid idea-to-song task. Save the returned task ID."""
        async with AsyncAceDataCloud(api_token=self._token, max_retries=0) as client:
            return _task_id(await client.acemusic.generate(action="generate", prompt=prompt, model=model, async_=True))

    def acemusic_generate_custom_music(
        self, lyric: str, style: str, title: str, model: Model = "acemusic-v1.1"
    ) -> dict[str, Any]:
        """Submit one paid song task with original lyrics, style and title."""
        with AceDataCloud(api_token=self._token, max_retries=0) as client:
            return _task_id(
                client.acemusic.generate(
                    action="generate", custom=True, lyric=lyric, style=style, title=title, model=model, async_=True
                )
            )

    async def aacemusic_generate_custom_music(
        self, lyric: str, style: str, title: str, model: Model = "acemusic-v1.1"
    ) -> dict[str, Any]:
        """Submit one paid song task with original lyrics, style and title."""
        async with AsyncAceDataCloud(api_token=self._token, max_retries=0) as client:
            return _task_id(
                await client.acemusic.generate(
                    action="generate", custom=True, lyric=lyric, style=style, title=title, model=model, async_=True
                )
            )

    def acemusic_upload_audio(self, audio_url: str, name: str | None = None) -> dict[str, Any]:
        """Import one authorized public HTTPS MP3 as a separately priced reference."""
        if not audio_url.startswith("https://"):
            raise ValueError("Use a public HTTPS MP3 URL.")
        with AceDataCloud(api_token=self._token, max_retries=0) as client:
            return _task_id(client.acemusic.generate(action="upload", audio_url=audio_url, name=name, async_=True))

    async def aacemusic_upload_audio(self, audio_url: str, name: str | None = None) -> dict[str, Any]:
        """Import one authorized public HTTPS MP3 as a separately priced reference."""
        if not audio_url.startswith("https://"):
            raise ValueError("Use a public HTTPS MP3 URL.")
        async with AsyncAceDataCloud(api_token=self._token, max_retries=0) as client:
            return _task_id(
                await client.acemusic.generate(action="upload", audio_url=audio_url, name=name, async_=True)
            )

    def acemusic_cover_audio(self, audio_id: str, lyric: str, style: str, title: str | None = None) -> dict[str, Any]:
        """Submit one paid cover using an owned audio ID, lyrics and style."""
        with AceDataCloud(api_token=self._token, max_retries=0) as client:
            return _task_id(
                client.acemusic.generate(
                    action="cover",
                    model="acemusic-v1.1",
                    audio_id=audio_id,
                    lyric=lyric,
                    style=style,
                    title=title,
                    async_=True,
                )
            )

    async def aacemusic_cover_audio(
        self, audio_id: str, lyric: str, style: str, title: str | None = None
    ) -> dict[str, Any]:
        """Submit one paid cover using an owned audio ID, lyrics and style."""
        async with AsyncAceDataCloud(api_token=self._token, max_retries=0) as client:
            return _task_id(
                await client.acemusic.generate(
                    action="cover",
                    model="acemusic-v1.1",
                    audio_id=audio_id,
                    lyric=lyric,
                    style=style,
                    title=title,
                    async_=True,
                )
            )

    def acemusic_mashup_audio(
        self, first_audio_id: str, second_audio_id: str, lyric: str, style: str, title: str | None = None
    ) -> dict[str, Any]:
        """Blend two distinct owned audio IDs in one paid mashup task."""
        if first_audio_id == second_audio_id:
            raise ValueError("Choose two distinct owned audio IDs.")
        with AceDataCloud(api_token=self._token, max_retries=0) as client:
            return _task_id(
                client.acemusic.generate(
                    action="mashup",
                    model="acemusic-v1.1",
                    mashup_audio_ids=[first_audio_id, second_audio_id],
                    lyric=lyric,
                    style=style,
                    title=title,
                    async_=True,
                )
            )

    async def aacemusic_mashup_audio(
        self, first_audio_id: str, second_audio_id: str, lyric: str, style: str, title: str | None = None
    ) -> dict[str, Any]:
        """Blend two distinct owned audio IDs in one paid mashup task."""
        if first_audio_id == second_audio_id:
            raise ValueError("Choose two distinct owned audio IDs.")
        async with AsyncAceDataCloud(api_token=self._token, max_retries=0) as client:
            return _task_id(
                await client.acemusic.generate(
                    action="mashup",
                    model="acemusic-v1.1",
                    mashup_audio_ids=[first_audio_id, second_audio_id],
                    lyric=lyric,
                    style=style,
                    title=title,
                    async_=True,
                )
            )

    def acemusic_generate_lyrics(self, prompt: str, style: str | None = None) -> dict[str, Any]:
        """Request paid lyrics. Return the draft or the original task ID when pending."""
        with AceDataCloud(api_token=self._token, max_retries=0) as client:
            return client.acemusic.lyrics(prompt=prompt, style=style)

    async def aacemusic_generate_lyrics(self, prompt: str, style: str | None = None) -> dict[str, Any]:
        """Request paid lyrics. Return the draft or the original task ID when pending."""
        async with AsyncAceDataCloud(api_token=self._token, max_retries=0) as client:
            return await client.acemusic.lyrics(prompt=prompt, style=style)

    def acemusic_get_task(self, task_id: str) -> dict[str, Any]:
        """Read the original ACE Music task. Check group status and response before using audio URLs."""
        with AceDataCloud(api_token=self._token, max_retries=0) as client:
            return client.acemusic.tasks(action="retrieve", id=task_id)

    async def aacemusic_get_task(self, task_id: str) -> dict[str, Any]:
        """Read the original ACE Music task. Check group status and response before using audio URLs."""
        async with AsyncAceDataCloud(api_token=self._token, max_retries=0) as client:
            return await client.acemusic.tasks(action="retrieve", id=task_id)
