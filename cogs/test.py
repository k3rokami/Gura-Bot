from enkacard import encbanner
import asyncio

async def card():
    async with encbanner.ENC(lang="en", save=True) as encard:
        ENCpy = await encard.enc(uids = "811455610")
        return await encard.creat(ENCpy,1)

result = asyncio.run(card()) 

print(result)
