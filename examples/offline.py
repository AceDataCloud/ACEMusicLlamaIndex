"""List native tools without making an API request."""

from llama_index.tools.acemusic_acedatacloud import AceMusicToolSpec

tools = AceMusicToolSpec(api_token="offline-example").to_tool_list()
print("\n".join(tool.metadata.name for tool in tools))
