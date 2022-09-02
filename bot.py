import asyncio
from threading import Thread
import discord
from discord.ext.commands import Bot
import os
import random
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, ContextTypes, PicklePersistence

load_dotenv()

class DiscordCommand:
    def __init__(self, name, handler, ctx = False):
      self.name = name
      self.handler = handler
      self.ctx = ctx

    async def execute_command(self, channel, args, ctx):
        await self.handler(channel, args, ctx)


async def handle_spam_command(channel, args, message):
    if message.author.guild_permissions.administrator:
        text_channel_list = []
        for server in client.guilds:
            for schannel in server.channels:
                if str(schannel.type) == 'text':
                    text_channel_list.append(schannel)

        quotes = [
            "Wer hastig läuft, der fällt.",
            "Liebe ist eine bloße Tollheit, und ich sage Euch, verdient ebensogut eine dunkle Zelle und Peitsche als andre Tolle; und die Ursache, warum sie nicht so gezüchtigt und geheilt wird, ist, weil sich diese Mondsucht so gemein gemacht hat, daß die Zuchtmeister selbst verliebt sind.",
            "Denn das eigentliche Wesen des Ehrgeizes ist nur der Schatten eines Traumes. Horch, horch, die Lerch' im Äther blau!",
            "Gehorchen mag, wer nicht zu herrschen weiß.",
            "Das bessere Teil der Tapferkeit ist – Besonnenheit.",
            "Brav, alter Maulwurf! Wühlst so hurtig fort? O trefflicher Minierer! Daß wir die Übel, die wir haben, lieber ertragen, als zu Unbekanntem fliehn. So macht Bewußtsein Feige aus uns allen; der angebornen Farbe der Entschließung wird des Gedankens Blässe angekränkelt; und Unternehmungen voll Mark und Nachdruck durch diese Rücksicht aus der Bahn gelenkt, verlieren so den Namen Handlung.",
            "Die lieben nicht, die ihre eigene Liebe nicht zeigen.",
            "Und wenn du den Eindruck hast, daß das Leben ein Theater ist, dann suche dir eine Rolle aus, die dir so richtig Spaß macht.",
            "Aneignen nennt es der Gebildete.",
            "Wär's abgetan, so wie's getan ist, dann wär's gut, Man tät' es eilig. Liebe ist ein Kobold; Liebe ist ein Teufel; es gibt keinen böseren Engel als die Liebe!",
            "Lieber eine Hagebutte im Strauch als eine Rose in eurem Garten.",
            "Mit einem lachenden und einem weinenden Auge.",
            "Gradheit ist 'ne Törin, Die das verfehlt, wonach sie strebt.",
            "Schmeichelnd kitzelt die Schlange, wo sie sticht.",
            "Wie Knaben aus der Schul' Eilt Liebe hin zum Lieben, Wie Knaben an ihr Buch, Wird sie hinweggetrieben.",
            "Ist Lieb' ein zartes Ding? Sie ist zu rauh, Zu wild, zu tobend; und sie sticht wie Dorn.",
            "Ehre ist nichts als ein gemaltes Schild beim Leichenzug, und so endigt mein Katechismus.",
            "Der Teufel hat Gewalt, sich zu verkleiden, in lockende Gestalt…",
            "Nicht umzukehren ist des Schicksals Spruch.",
            "Es gibt so Leute, deren Angesicht Sich überzieht gleich einem steh'nden Sumpf, Und die ein eigensinnig Schweigen halten, Aus Absicht sich in einen Schein zu kleiden Von Weisheit, Würdigkeit und tiefem Sinn. O mein' Antonia, ich kenne derer, Die man deswegen bloß für Weise hält, Wei sie nichts sagen: sprächen sie, sie brächten Die Ohren, die sie hörten, in Verdammnis, Weil sie die Brüder Narren schelten würden.",
            "Die Krähe singt so lieblich wie die Lerche, wenn man auf keine lauscht.",
            "Doch Brutus ist ein ehrenwerter Mann. Das sind sie alle, alle ehrenwert.",
            "Nach dem Tod eines Blinden spricht man von seinen Mandelaugen, nach dem Tod eines Glatzkopfs von seinem goldblonden Haar.",
            "Wir überrennen Durch jähe Eil' das Ziel, Nach dem wir rennen Und gehn's verlustig.",
            "Alte tun, als lebten sie nicht mehr, träg, unbehülflich und wie Blei so schwer.",
            "Man wirkt durch Witz und nicht durch Zauber; Und Witz beruht auf Stund' und günst'ger Zeit.",
            "Man sagt, alte Leute werden wieder Kinder.",
            "Der Köter Wahrheit gehört in's Hundeloch und muß hinausgepeitscht werden; die Möpsin Ruhmredigkeit darf am Kaminfeuer stehen und stinken.",
            "Weil das Los der Menschen niemals sicher, laßt uns bedacht sein auf den schlimmsten Fall.",
            "Verschämte Lieb', ach! sie verrät sich schnell, Wie Blutschuld: ihre Nacht ist sonnenhell.",
            "Ein Mann kann mit einem Wurm fischen, der von einem König gegessen hat, und essen von dem Fisch, der den Wurm verzehrt hat.",
            "Natur bringt wunderliche Käuz' ans Licht. Der drückt die Augen immer ein, und lacht Wie'n Starmatz über einen Dudelsack; Ein andrer von so sauerm Angesicht, Daß er die Zähne nicht zum Lachen wiese, Schwür' Nestor auch, der Spaß sei lachenswert.",
            "Es gibt noch keine Kunst, die innerste Gestalt des Herzens im Gesicht zu lesen.",
            "– Ich lehr' euch, selbst den Teufel meistern. – Und ich lehr' euch den Teufel frisch verhöhnen Durch Wahrheit. Erziehe zum Adel deinen Sinn, daß du, für Schmach selbst unverwundbar und im Kriege ragst ein heller Leuchtturm, der in Stürmen rettet den, der dich anblickt.",
            "Es fallen eure Gründ' auf euch zurück wie Hunde,die den eignen Herrn zerfleischen.",
            "Liebe ist dein Meister, denn sie meistert dich! Und der, den eine Närrin spannt ins Joch, Den kann man nicht ins Buch der Weisen schreiben.",
            "Bonasera, Bonasera, was habe ich dir getan, dass du mich so respektlos behandelst. Du kommst in mein Haus, am Hochzeitstag meiner Tochter und bittest mich einen Mord zu begehen.",
            "Man erkennt einen Philosophen daran, daß er drei glänzenden und lauten Dingen aus dem Wege geht: dem Ruhme, den Fürsten und den Frauen - womit nicht gesagt ist, daß sie nicht zu ihm kämen.",
            "Verschiebe nicht auf morgen, was genausogut auf übermorgen verschoben werden kann.",
            "Es gibt Dinge, die den meisten Menschen unglaublich erscheinen, die nicht Mathematik studiert haben.",
            "Zwei Dinge sind vom Vatikan schwer zu bekommen; Ehrlichkeit und eine Tasse Kaffee.",
            "Ein Mann, der keine Zeit mit seiner Familie verbringt, ist kein richtiger Mann.",
            "Ein freundlicher Stachelbär bedeutet einen ständigen Vorrat an scharfen Speeren. Ein unfreundlicher Stachelbär bedeutet einen ständigen Vorrat an kleinen Löchern",
            "Von der Stirne heiß, rinnen muss der Schweiß, soll das Werk den Meister loben.",
            "Leute, achtet ihr bitte auf euren ökologischen Fußabdruck während ihr auf der Erde seid? Ihr könnt nicht immer alles fallen lassen und darauf warten, dass irgendein Idiot es aufsammelt.",
            "Mach was, Jerome! - Hmmm...ich kann es mit nem Satelliten versuchen, aber das dauert zwei Tage und dann hab ich wieder den BND am Hals...",
            "Doch der Segen kommt von oben.",
            "Mein ganzes Budget geht ja drauf für die Verwaltung der Strafanzeigen und das Entfernen der Graffiti.",
            "Jemanden lieben heißt, als Einziger ein Wunder begreifen, das für alle anderen unsichtbar bleibt.",
            "Oh, ich hab eigentlich gar keinen Bock auf Schlägerei, ne.",
            "Da werden Weiber zu Hyänen und treiben mit Entsetzen Scherz. ",
            "Du darfst nie einen Menschen, der nicht zur Familie gehört, merken lassen, was du denkst.",
            "Und? Will er eine Elternkonferenz? - Nee, der meint, Daniel hat ne Macke und ich kann ihm ruhig ab und zu eine runter hauen. Das ist der einzige Weg, wie man ihn zur Vernunft kriegt.",
            "Was zieht man eigentlich an in so nem Heizungskeller?",
            "Denn wo das Strenge mit dem Zarten, wo Starkes sich und Mildes paarten, da gibt es einen guten Klang.",
            "Ausspähen unter Freunden, das geht gar nicht.",
            "Ich habe eine sentimentale Schwäche für meine Söhne und habe sie zu sehr verwöhnt. Sie reden, wenn sie zuhören sollten.",
            "Wenn du mich noch einmal anfickst, dann steck ich dir die eigene Faust so tief in den Arsch, dass du dich von innen am Hals kratzen kannst, du scheiß Petze.",
            "Wie sich alle denken können, wird sie dieses Jahr nicht mehr unterrichten, falls sie es denn überhaupt jemals getan hat.",
            "Wir arbeiten auch hier. - Mein Beileid.",
            "Frag mich niemals nach meinen Geschäften, Kay.",
            "Drum prüfe, wer sich ewig bindet. Ob sich das Herz zum Herzen findet!",
            "Doch mit des Geschickes Mächten ist kein ew´ger Bund zu flechten.",
            "Ich weiß, dass du es warst, Fredo, und es bricht mir das Herz! Hörst du? Es bricht mir das Herz.",
            "Der ersten Liebe goldne Zeit!",
            "Wohltätig ist des Feuers Macht, wenn sie der Mensch bezähmt, bewacht.",
            "Freiheit und Gleichheit! hört man schallen.",
            "Ein Sizilianer darf am Hochzeitstag seiner Tochter keinem eine Bitte abschlagen.",
            "Wo rohe Kräfte sinnlos walten, da kann sich kein Gebild gestalten.",
            "Gefährlich ist´s, den Leu zu wecken, verderblich ist des Tigers Zahn. Jedoch der schrecklichste der Schrecken, das ist der Mensch in seinem Wahn.",
            "Da werden Weiber zu Hyänen.",
            "Heute Nacht rechnet die Familie Corleone ab.",
            "Wo rohe Kräfte sinnlos walten.",
            "Gefährlich ist´s, den Leu zu wecken.",
            "Von der Stirne heiß, rinnen muss der Schweiß, soll das Werk den Meister loben. Doch der Segen kommt von oben.",
            "Wenn gute Reden sie begleiten, dann fließt die Arbeit munter fort.",
            "Die Jahre fliegen pfeilgeschwind.",
            "Es fallen eure Gründ' auf euch zurück wie Hunde,die den eignen Herrn zerfleischen.",
            "Liebe ist dein Meister, denn sie meistert dich! Und der, den eine Närrin spannt ins Joch, Den kann man nicht ins Buch der Weisen schreiben.",
            "Scheitert der Euro, scheitert Europa.",
            "Charlie, kannst du mit der mal was machen? - Hmm, operative Eingriffe machen wir hier gar nicht.",
            "Das Unglück schreitet schnell.",
            "Das ist ein Restaurant. Ich hab Hunger. - Äthiopisch? Fliegensuppe und Reispudding, oder was? Ich brauch Fleisch, Mann!",
            "Gefährlich ist es, den Leu zu wecken, erderblich ist des Tigers Zahn, jedoch der schrecklichste Schrecken, das ist der Mensch in seinem Wahn.",
            "Das ist ein sauberes Etablissement, okay? - Du hast ein LSD-Labor auf dem Dachboden! - Eben. Da muss man doppelt vorsichtig sein.",
            "Deine Schülerin weint. - Chantal! - Ja? - Heul leise!",
            "Wehe, wenn sie losgelassen!",
            "Ich habe gewisse kamelartige Fähigkeiten. Ich habe eine gewisse Speicherfähigkeit. Aber dann muss ich mal wieder auftanken.",
            "Die Fahrräder darf man nicht umfahren. - Quatsch nicht so viel und drück dir lieber mal ein paar von deinen Mondkratern aus.",
            "Die Lebenden rufe ich. Die Toten beklage ich. Blitze breche ich.",
            "Drücken sie sich mal aus, Frau Schnabelstedt. Ich versteh echt kein wehleidig.",
            "Von der Stirne heiß, rinnen muss der Schweiß.",
            "Du hast mein Zeugnis geklaut. - Hast du zu viel Tintenkiller eingeatmet?",
            "Du Zeki, wenn du das Geld hast, krieg ich dann neue Titten?",
            "Die Räume wachsen, es dehnt sich das Haus.",
            "Wir sagen den Sparerinnen und Sparern, dass ihre Einlagen sicher sind. Auch dafür steht die Bundesregierung ein.",
            "Elisabeth! Häng ihm jetzt nicht am Arsch wie so ‘ne ungebumste Jungfer!",
            "Ey, wie soll ich die zum Lesen kriegen? Die sind geisteskrank. - Weißt du was? Du musst Chantal und Danger unter Kontrolle kriegen. Wenn du die Anführer hast, dann ziehen die anderen mit.",
            "Hey, verpisst euch vom Schulhof oder ich tret euch in eure unbehaarten Ärsche und polier euch eure Metallfressen!",
            "Es schwelgt das Herz in Seligkeit.",
            "Ich hab dir ein paar K.O.-Tropfen in deinen Zecken-Tee gemischt. Ich würd dich nicht mal mit der Kneifzange anfassen, also laber keinen Schrott.",
            "Ich komm mir langsam vor wie so eine lesbische Adoptivmutter, wenn du mich da immer mit rein ziehst. Ich muss auch mal runter kommen.",
            "Kanack' mich nicht an!"
        ];
        #while(True):
            #time.sleep(1 * 60 * 60 * 12) # every 12 hours
            #for send_to_channel in text_channel_list:
        msg = random.choice(quotes)
        await channel.send(msg)
    else:
        msg = "You're an average joe {0.author.mention}".format(message)


intents = discord.Intents.default()
intents.message_content = True

prompt = '>_'
client = Bot(description="My Cool Bot", command_prefix=prompt, pm_help = False, intents=intents)
defined_commands = [DiscordCommand('spam', handle_spam_command)]

async def send_to_telegram(msg):
    await app.bot.send_message(chat_id=os.getenv('TELEGRAM_CHANNEL'), text=msg) # AIAMOND Chat

@client.event
async def on_ready():
    print("Ready")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if not message.content.startswith(prompt):
        if str(message.channel.category_id) == str(os.getenv('DISCORD_CATEGORY')):
            await send_to_telegram('Discord--> ' + message.channel.name + " (" + message.author.name + "): " + message.content)
        return

    cmd = next((c for c in defined_commands if message.content.startswith(prompt + ' ' + c.name)))
    if cmd is not None:
        await cmd.execute_command(message.channel, message.content.replace(prompt + ' ' + cmd.name, ''), message)

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(update.message.from_user.username)
    if update.message.from_user.username == "discord_connector_bot":
        return

    print(update.message.reply_to_message.text)
    if update.message.reply_to_message.text[0:10] == "Discord-->":
        found_channel = ""
        for server in client.guilds:
            for schannel in server.channels:
                if str(schannel.type) == 'text' and schannel.name == update.message.reply_to_message.text[11:update.message.reply_to_message.text.find("(")].strip():
                    found_channel = schannel

        if found_channel:
            await found_channel.send("Telegram (" + update.message.from_user.first_name + "): " + update.message.text)


my_persistence = PicklePersistence(filepath='./pers', update_interval=1)
app = ApplicationBuilder().token(os.getenv('TELEGRAM_TOKEN')).persistence(persistence=my_persistence).build()
echo_handler = MessageHandler(filters.REPLY, echo)
app.add_handler(echo_handler)

async def startT():
    await app.initialize()
    await app.updater.initialize()
    await app.updater.start_polling()
    await app.start()

async def startD():
    await client.start(os.getenv('DISCORD_TOKEN'))

async def main():
    tasks = [await startT(), await startD()]
    await asyncio.gather(*tasks)

asyncio.run(main())
