import discord
import freesound
import zapsplat
import envato
import os

freesound_web = freesound.FreeSoundWeb()
zapsplat_web = zapsplat.ZapsplatWeb()
envato_web = envato.EnvatoWeb()

no_results_message = '''Sorry, I couldn't find any SFX that matched your search.'''

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    message_content = message.content.lower()
    un = message.author.name

    if '/sfx' in message.content:

      key_words, search_words = freesound_web.key_words_search_words(message_content)
      print(f"Generated keywords: {key_words}")
      print(f"Original search words: {search_words}")
      fs_result = freesound_web.search(key_words)
      fs_url = freesound_web.free_link(key_words)
      zs_result = zapsplat_web.search(key_words)
      zs_url = zapsplat_web.free_link(key_words)
      en_result = envato_web.search(key_words)
      en_url = envato_web.free_link(key_words)     

      embed = discord.Embed(title=f"{un}'s SFX Search Results for '**{search_words}**'", description="", color=discord.Color.yellow())
      
      if fs_result:
        fs_msg = f"[FreeSound]({fs_url}) | **{fs_result}** SFX"
        embed.add_field(name="Free", value=fs_msg, inline=True)
      else:
        print("No results found")

      if zs_result:
        zs_msg = f"[Zapsplat]({zs_url}) | **{zs_result}** SFX"
        embed.add_field(name="Free", value=zs_msg, inline=True)
      else:
        print("No results found")

      if en_result:
        en_msg = f"[Envato]({en_url}) | **{en_result}** SFX"
        embed.add_field(name="From $16.50/mo", value=en_msg, inline=False)
      else:
        print("No results found")

      ss_url = f"[SoundSnap](https://www.soundsnap.com/search/audio?query={key_words})"
      ep_url = f"[Epidemic Sound](https://www.epidemicsound.com/sound-effects/search/?term={key_words})"
      pb_url = f"[Pixabay](https://pixabay.com/sound-effects/search/{key_words})"
      sb_url = f"[SoundBible](https://www.soundbible.com/search.php?q={key_words})"
      paid_sfx = f"{ep_url} from **$9.99/mo**\n{ss_url} from **$21/mo**"
      free_sfx = f"{pb_url}\n{sb_url}"
      embed.add_field(name="Other Free SFX Searches", value=free_sfx, inline=True)
      embed.add_field(name="Other Paid SFX Searches", value=paid_sfx, inline=True)
      await message.channel.send(embed=embed)
client.run(os.environ['TOKEN'])