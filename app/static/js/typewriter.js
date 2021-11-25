function sleep(ms)
{
	return new Promise(resolve => setTimeout(resolve, ms));
}

async function typewriter(object, text)
{
	for (let i = 0; i <= text.length; i++)
	{
		await sleep(100);
		object.text(text.slice(0, i));
	}
}
