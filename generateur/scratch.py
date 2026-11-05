"""Génère un projet Scratch 3 (.sb3) pour chaque conte.
Usage : python3 scratch.py <dossier_de_sortie>"""
import json, hashlib, zipfile, sys, os, subprocess, wave, tempfile, shutil
from xml.sax.saxutils import escape

HERE = os.path.dirname(os.path.abspath(__file__))
STORIES = json.load(open(os.path.join(HERE, "stories.json"), encoding="utf-8"))
OUT = sys.argv[1]

# ---------- données des contes ----------
# sprite: (nom, couleur, [(nom_costume, couleur), ...])
# étapes: ("show",spr,x,y) ("hide",spr) ("say",spr,texte) ("glide",spr,x,y,s)
#         ("goto",spr,x,y) ("costume",spr,nom)
D = {}
D["cinderella"] = dict(
 backdrops=[("البيت","#f3e3c3"),("القصر","#e8d5f2"),("الطريق","#cfe8c8")],
 sprites=[("سندريلا","#5b8dd6",[("سندريلا · فستان","#f2a6c8")]),("زوجة الأب","#7a4a8a",[]),("الأختان","#c76a8f",[]),
          ("الجنية","#8fd6e8",[]),("الأمير","#2d4e9c",[]),("الحذاء","#9ad5ee",[])],
 scenes=[
  (0,[("show","سندريلا",-120,-60),("show","زوجة الأب",120,-60),("say","زوجة الأب","نظفي البيت يا سندريلا!"),("say","سندريلا","حاضر يا سيدتي.")]),
  (0,[("show","الأختان",0,-60),("say","الأختان","سنذهب إلى الحفلة!"),("glide","الأختان",320,-60,2),("hide","الأختان"),("hide","زوجة الأب"),("say","سندريلا","أنا حزينة، لا أستطيع الذهاب.")]),
  (0,[("show","الجنية",60,40),("say","الجنية","لا تحزني!"),("costume","سندريلا","سندريلا · فستان"),("say","الجنية","عودي قبل منتصف الليل!")]),
  (1,[("hide","الجنية"),("show","الأمير",100,-60),("goto","سندريلا",-100,-60),("say","الأمير","ما أجملك!"),("glide","سندريلا",0,-60,2)]),
  (1,[("say","الأمير","دقت الساعة الثانية عشرة!"),("say","سندريلا","يجب أن أذهب!"),("show","الحذاء",0,-110),("glide","سندريلا",-320,-60,2),("hide","سندريلا")]),
  (2,[("show","سندريلا",-100,-60),("say","الأمير","الحذاء يناسب سندريلا!"),("glide","الحذاء",-100,-110,1.5)])])
D["layla"] = dict(
 backdrops=[("بيت ليلى","#f3e3c3"),("الغابة","#bfe0b0"),("بيت الجدة","#e6d3b8")],
 sprites=[("ليلى","#d23b3b",[]),("الأم","#8a5a3a",[]),("الذئب","#6b6b78",[("الذئب · جدة","#c9a9d6")]),("الجدة","#b79ad0",[]),("الحطاب","#2f7d4a",[]),("السلة","#c9a063",[])],
 scenes=[
  (0,[("show","ليلى",-100,-60),("show","الأم",100,-60),("show","السلة",-100,-10),("say","الأم","لا تتأخري، ولا تكلمي الغرباء."),("say","ليلى","حاضرة يا أمي."),("hide","السلة"),("hide","الأم"),("glide","ليلى",-320,-60,2)]),
  (1,[("goto","ليلى",-200,-60),("show","ليلى",-200,-60),("show","الذئب",200,-60),("say","الذئب","إلى أين تذهبين يا ليلى؟"),("say","ليلى","إلى بيت جدتي."),("glide","الذئب",320,-60,2),("hide","الذئب")]),
  (2,[("hide","ليلى"),("costume","الذئب","الذئب · جدة"),("show","الذئب",60,-60),("say","الذئب","ادخلي يا حبيبتي!")]),
  (2,[("show","ليلى",-120,-60),("say","ليلى","لماذا عيناك كبيرتان يا جدتي؟"),("say","الذئب","لأراك جيدا."),("say","ليلى","ولماذا أسنانك كبيرة؟")]),
  (2,[("say","ليلى","النجدة!"),("show","الحطاب",320,-60),("glide","الحطاب",170,-60,2)]),
  (2,[("say","الحطاب","ابتعد أيها الذئب!"),("glide","الذئب",-320,-60,2),("hide","الذئب"),("show","الجدة",60,-60),("say","الجدة","شكرا يا حطاب!")])])
D["djeha"] = dict(
 backdrops=[("الطريق","#e9d9a8"),("الجسر والنهر","#bfdcec")],
 sprites=[("جحا","#3a5a9c",[]),("الابن","#6c8fd6",[]),("الحمار","#9e8b72",[]),("المارة 1","#c07a3a",[]),("المارة 2","#8a4a7a",[])],
 scenes=[
  (0,[("show","الحمار",-120,-70),("show","الابن",-190,-60),("show","جحا",-250,-60),("say","جحا","هيا إلى السوق!"),("glide","جحا",-90,-60,1.5),("glide","الابن",-20,-60,1.5),("glide","الحمار",50,-70,1.5)]),
  (0,[("goto","جحا",50,-10),("show","المارة 1",200,-60),("say","المارة 1","يا لقسوة هذا الأب!")]),
  (0,[("hide","المارة 1"),("goto","جحا",-90,-60),("goto","الابن",50,-10),("show","المارة 2",200,-60),("say","المارة 2","ما أسوأ هذا الابن!")]),
  (0,[("hide","المارة 2"),("goto","جحا",30,-10),("goto","الابن",75,-10),("show","المارة 1",200,-60),("say","المارة 1","يا للقسوة على الحمار!")]),
  (0,[("hide","المارة 1"),("goto","جحا",-90,-60),("goto","الابن",-20,-60),("show","المارة 2",200,-60),("say","المارة 2","ما أغباهما! عندهما حمار ولا يركبانه!")]),
  (1,[("hide","المارة 2"),("goto","جحا",-100,-60),("goto","الابن",-170,-60),("goto","الحمار",0,-20),("say","جحا","النجدة! سقط الحمار!"),("glide","الحمار",0,-200,2),("hide","الحمار")])])
D["alibaba"] = dict(
 backdrops=[("الجبل","#cfd8c0"),("المغارة","#4a3f36"),("البيت","#f3e3c3")],
 sprites=[("علي بابا","#8a5a2a",[]),("قاسم","#4a6fa5",[]),("مرجانة","#d46a9e",[]),("رئيس اللصوص","#333333",[]),("اللصوص","#555555",[]),("باب المغارة","#7a6a5a",[("باب المغارة · مفتوح","#2a2a2a")])],
 scenes=[
  (0,[("show","باب المغارة",60,-30),("show","علي بابا",-180,-60),("show","اللصوص",300,-60),("glide","اللصوص",120,-60,1.5),("show","رئيس اللصوص",180,-60),("say","رئيس اللصوص","افتح يا سمسم!"),("costume","باب المغارة","باب المغارة · مفتوح"),("glide","اللصوص",60,-30,1.5),("hide","اللصوص"),("hide","رئيس اللصوص")]),
  (1,[("goto","علي بابا",-100,-60),("goto","باب المغارة",60,-30),("costume","باب المغارة","باب المغارة"),("say","علي بابا","افتح يا سمسم!"),("costume","باب المغارة","باب المغارة · مفتوح"),("say","علي بابا","ما أكثر الذهب!")]),
  (2,[("hide","باب المغارة"),("show","قاسم",100,-60),("say","قاسم","من أين لك هذا الذهب؟"),("say","علي بابا","سأحكي لك السر."),("glide","قاسم",320,-60,1.5),("hide","قاسم")]),
  (1,[("show","باب المغارة",60,-30),("costume","باب المغارة","باب المغارة"),("show","قاسم",-100,-60),("say","قاسم","افتح يا شعير!"),("say","قاسم","لماذا لا يفتح الباب؟")]),
  (2,[("hide","باب المغارة"),("hide","قاسم"),("show","مرجانة",60,-60),("show","اللصوص",320,-60),("say","مرجانة","لن أترككم تدخلون!"),("glide","اللصوص",420,-60,1),("hide","اللصوص")]),
  (2,[("say","علي بابا","شكرا يا مرجانة!")])])
D["sindbad"] = dict(
 backdrops=[("الميناء","#cfe6f2"),("البحر","#8fc4e0"),("الجزيرة","#bfe3d0"),("الشاطئ","#f2e3b0")],
 sprites=[("السندباد","#2f6b8a",[]),("البحارة","#8a5a3a",[]),("السفينة","#8b5a2b",[]),("الجزيرة","#5a9a6a",[("حوت","#5a7a96")]),("اللوح","#a9783f",[])],
 scenes=[
  (0,[("show","السفينة",-100,-60),("show","السندباد",-180,-50),("say","السندباد","سأسافر للتجارة!"),("glide","السندباد",-100,-10,1)]),
  (1,[("show","البحارة",-140,-10),("show","الجزيرة",180,-60),("say","البحارة","أرى جزيرة!"),("glide","السفينة",60,-60,3),("glide","السندباد",60,-10,0.5),("glide","البحارة",20,-10,0.5)]),
  (2,[("say","البحارة","ما أجمل هذه الجزيرة!"),("glide","البحارة",180,0,2)]),
  (1,[("costume","الجزيرة","حوت"),("say","السندباد","الأرض تهتز! إنها حوت!"),("glide","الجزيرة",180,-220,2),("hide","الجزيرة")]),
  (1,[("hide","السفينة"),("hide","البحارة"),("show","اللوح",0,-110),("goto","السندباد",0,-90),("say","السندباد","النجدة!")]),
  (3,[("glide","اللوح",100,-110,3),("glide","السندباد",100,-90,0.5),("say","السندباد","الحمد لله على السلامة!")])])
D["crow"] = dict(
 backdrops=[("الغابة","#bfe0b0"),("تحت الشجرة","#a9d49a")],
 sprites=[("الغراب","#222222",[("الغراب · فم مفتوح","#444444")]),("الثعلب","#d9731a",[]),("الجبن","#f2d04a",[])],
 scenes=[
  (0,[("show","الغراب",100,60),("show","الجبن",100,25),("say","الغراب","ما أطيب هذا الجبن!")]),
  (0,[("show","الثعلب",-260,-80),("glide","الثعلب",-60,-80,1.5),("say","الثعلب","ما أجمل رائحة الجبن!")]),
  (0,[("say","الثعلب","ما أجمل ريشك يا غراب!")]),
  (0,[("say","الثعلب","وصوتك لا بد أنه أجمل!")]),
  (1,[("costume","الغراب","الغراب · فم مفتوح"),("say","الغراب","قاق! قاق!"),("glide","الجبن",100,-100,1)]),
  (1,[("glide","الثعلب",100,-90,1),("hide","الجبن"),("say","الثعلب","شكرا على الجبن!"),("glide","الثعلب",-320,-90,2)])])
D["hare"] = dict(
 backdrops=[("خط البداية","#cfe8c8"),("الطريق والشجرة","#bfe0b0"),("خط النهاية","#e8f0c8")],
 sprites=[("الأرنب","#b8b8c8",[("الأرنب · نائم","#8a8aa8")]),("السلحفاة","#4a9a5a",[]),("الحكم","#8a5a2a",[])],
 scenes=[
  (0,[("show","الأرنب",-200,-60),("show","السلحفاة",-150,-100),("say","الأرنب","أنا أسرع منك!"),("say","السلحفاة","هيا نتسابق!")]),
  (0,[("show","الحكم",-100,40),("say","الحكم","واحد، اثنان، ثلاثة، انطلقا!"),("hide","الحكم")]),
  (1,[("goto","الأرنب",-200,-60),("goto","السلحفاة",-200,-100),("glide","الأرنب",80,-60,1),("say","الأرنب","هي بطيئة جدا!"),("glide","السلحفاة",-60,-100,3)]),
  (1,[("costume","الأرنب","الأرنب · نائم"),("say","الأرنب","سأرتاح قليلا.")]),
  (1,[("say","السلحفاة","سأمشي دون توقف."),("glide","السلحفاة",200,-100,3)]),
  (2,[("goto","السلحفاة",200,-100),("goto","الأرنب",60,-60),("show","الحكم",-100,40),("say","الحكم","فازت السلحفاة!"),("costume","الأرنب","الأرنب"),("say","الأرنب","لقد تأخرت!")])])
D["lion"] = dict(
 backdrops=[("الغابة","#bfe0b0"),("مكان الفخ","#d8cfa0")],
 sprites=[("الأسد","#d9a030",[("الأسد · محبوس","#a07820")]),("الفأر","#888888",[]),("الصياد","#6a4a2a",[]),("الشبكة","#7a7a50",[])],
 scenes=[
  (0,[("show","الأسد",-50,-60),("say","الأسد","أنا ملك الغابة!"),("say","الأسد","سأنام قليلا.")]),
  (0,[("show","الفأر",-260,-90),("glide","الفأر",-50,-90,2),("say","الأسد","من أيقظني؟")]),
  (0,[("say","الفأر","اتركني! سأساعدك يوما ما."),("say","الأسد","ها ها! أنت صغير جدا."),("glide","الفأر",-260,-90,1.5),("hide","الفأر")]),
  (1,[("goto","الأسد",0,-60),("show","الصياد",200,-60),("show","الشبكة",0,-60),("costume","الأسد","الأسد · محبوس"),("say","الأسد","النجدة! أنا محبوس!"),("hide","الصياد")]),
  (1,[("show","الفأر",-260,-90),("glide","الفأر",-40,-90,2),("say","الفأر","سأقرض الحبال!")]),
  (1,[("hide","الشبكة"),("costume","الأسد","الأسد"),("say","الأسد","شكرا يا صديقي!")])])
D["frog"] = dict(
 backdrops=[("الحديقة والبئر","#cfe8b8"),("القصر","#e8d5f2")],
 sprites=[("الأميرة","#f0a0c8",[]),("الضفدع","#4aa85a",[("أمير","#3a5aa8")]),("الملك","#d4a017",[]),("الكرة","#f2c230",[])],
 scenes=[
  (0,[("show","الأميرة",-100,-60),("show","الكرة",-60,10),("say","الأميرة","ما أجمل كرتي الذهبية!")]),
  (0,[("glide","الكرة",100,-150,1.5),("say","الأميرة","لقد سقطت كرتي في البئر!")]),
  (0,[("show","الضفدع",150,-90),("say","الضفدع","سأخرجها إن صادقتني.")]),
  (0,[("goto","الكرة",-60,-60),("say","الأميرة","شكرا!"),("glide","الأميرة",-320,-60,2),("hide","الأميرة")]),
  (1,[("hide","الكرة"),("goto","الضفدع",50,-90),("show","الملك",180,-40),("say","الضفدع","افتحي لي كما وعدتني!"),("say","الملك","هل وعدتِه يا ابنتي؟")]),
  (1,[("show","الأميرة",-100,-60),("say","الأميرة","أنا آسفة، أنت صديقي."),("costume","الضفدع","أمير"),("say","الضفدع","شكرا لك!")])])

D["shepherd"] = dict(
 backdrops=[("التل","#bfe0a8"),("التل في المساء","#e8a868")],
 sprites=[("الراعي","#8a5a2a",[]),("الغنم","#f0f0f0",[]),("الذئب","#6b6b78",[]),("القرويون","#6a8a4a",[])],
 scenes=[
  (0,[("show","الراعي",-150,-60),("show","الغنم",60,-80),("say","الراعي","ما أجمل هذا اليوم، لكنني أشعر بالملل!")]),
  (0,[("say","الراعي","الذئب! الذئب!"),("show","القرويون",320,-60),("glide","القرويون",100,-60,2),("say","القرويون","أين الذئب؟")]),
  (0,[("say","الراعي","ها ها! كنت أمزح."),("say","القرويون","هذا كذب!"),("glide","القرويون",330,-60,2),("hide","القرويون")]),
  (0,[("say","الراعي","الذئب! الذئب!"),("show","القرويون",320,-60),("glide","القرويون",100,-60,2),("say","القرويون","لن نصدقك مرة أخرى."),("glide","القرويون",330,-60,2),("hide","القرويون")]),
  (1,[("show","الذئب",320,-80),("glide","الذئب",120,-80,2),("say","الراعي","النجدة! الذئب حقيقي!")]),
  (1,[("hide","الغنم"),("glide","الذئب",330,-80,2),("hide","الذئب"),("say","الراعي","ضاعت أغنامي لأنني كذبت.")])])
D["pigs"] = dict(
 backdrops=[("المرج","#bfe4a8"),("أمام بيت الآجر","#cfe0b0")],
 sprites=[("الخنزير الأول","#f2a0b0",[]),("الخنزير الثاني","#e88aa0",[]),("الخنزير الثالث","#d87090",[]),("الذئب","#6b6b78",[]),
          ("البيت","#c9a063",[("بيت القش","#e8d070"),("بيت الخشب","#a8743a"),("بيت الآجر","#c0563a"),("بيت منهار","#8a7a6a")])],
 scenes=[
  (0,[("show","البيت",60,-50),("costume","البيت","بيت القش"),("show","الخنزير الأول",-150,-70),("say","الخنزير الأول","سأبني بيتي من القش!")]),
  (0,[("costume","البيت","بيت الخشب"),("show","الخنزير الثاني",-150,-70),("say","الخنزير الثاني","وأنا سأبني بيتي من الخشب!")]),
  (0,[("costume","البيت","بيت الآجر"),("show","الخنزير الثالث",-90,-70),("say","الخنزير الثالث","وأنا سأبني بيتي من الآجر القوي!")]),
  (0,[("costume","البيت","بيت القش"),("show","الذئب",330,-70),("glide","الذئب",160,-70,2),("say","الذئب","سأنفخ وأنفخ وأهدم بيتك!"),("costume","البيت","بيت منهار"),("say","الخنزير الأول","النجدة!")]),
  (0,[("costume","البيت","بيت الخشب"),("say","الذئب","سأنفخ وأنفخ!"),("costume","البيت","بيت منهار"),("say","الخنزير الثاني","اهرب إلى بيت أخي!")]),
  (1,[("costume","البيت","بيت الآجر"),("say","الذئب","سأنفخ وأنفخ!"),("say","الخنزير الثالث","لن تهدم بيتي الآجر القوي!"),("glide","الذئب",340,-70,2),("hide","الذئب")])])
D["duckling"] = dict(
 backdrops=[("المزرعة والبركة","#cfe8b8"),("البركة في الشتاء","#dfe8f0"),("البركة في الربيع","#c8ecb0")],
 sprites=[("البطة الأم","#f5d94a",[]),("الإخوة","#f2e07a",[]),("البطة الصغيرة","#b0b0b0",[("بجعة","#ffffff")]),("البجعات","#f4f4f4",[])],
 scenes=[
  (0,[("show","البطة الأم",-130,-60),("show","الإخوة",10,-80),("show","البطة الصغيرة",150,-80),("say","البطة الأم","هيا يا صغاري، تعالوا إلى البركة!")]),
  (0,[("say","الإخوة","ما أقبحك!"),("say","البطة الصغيرة","أنا حزينة.")]),
  (0,[("say","البطة الصغيرة","سأرحل بعيدا."),("glide","البطة الصغيرة",340,-80,2),("hide","البطة الصغيرة"),("hide","الإخوة"),("hide","البطة الأم")]),
  (1,[("show","البطة الصغيرة",-100,-80),("say","البطة الصغيرة","ما أشد البرد! أنا وحيدة.")]),
  (2,[("show","البجعات",330,-80),("glide","البجعات",90,-80,2),("say","البجعات","تعالي معنا يا صديقتنا!")]),
  (2,[("costume","البطة الصغيرة","بجعة"),("say","البطة الصغيرة","أنا بجعة جميلة!"),("say","البجعات","مرحبا بك بيننا!")])])

# ---------- fabrication ----------
def svg_sprite(label, fill):
    fs = max(11, min(20, int(150 / max(len(label), 1))))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100">'
            f'<circle cx="50" cy="50" r="46" fill="{fill}" stroke="#222222" stroke-width="3"/>'
            f'<text x="50" y="{50+fs//3}" text-anchor="middle" font-family="Sans Serif" font-size="{fs}" font-weight="bold" fill="#ffffff" stroke="#222222" stroke-width="0.6">{escape(label)}</text></svg>')
def svg_backdrop(label, fill):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="480" height="360" viewBox="0 0 480 360">'
            f'<rect width="480" height="360" fill="{fill}"/><rect y="250" width="480" height="110" fill="#000000" fill-opacity="0.12"/>'
            f'<text x="240" y="36" text-anchor="middle" font-family="Sans Serif" font-size="26" font-weight="bold" fill="#222222">{escape(label)}</text></svg>')
def svg_banner(text):
    fs = max(12, min(20, int(560 / max(len(text), 1))))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="440" height="46" viewBox="0 0 440 46">'
            f'<rect x="2" y="2" width="436" height="42" rx="10" fill="#ffffff" stroke="#222222" stroke-width="3"/>'
            f'<text x="220" y="{23+fs//3}" text-anchor="middle" font-family="Sans Serif" font-size="{fs}" font-weight="bold" fill="#222222">{escape(text)}</text></svg>')

HAS_TTS = shutil.which("espeak-ng") is not None
_voice_cache = {}
def voice(zf, store, text):
    """Voix de synthèse arabe (espeak-ng) -> (md5, rate, frames, durée). None si indisponible."""
    if not HAS_TTS: return None
    if text in _voice_cache: return _voice_cache[text]
    with tempfile.TemporaryDirectory() as td:
        f = os.path.join(td, "v.wav")
        subprocess.run(["espeak-ng", "-v", "ar", "-s", "125", "-p", "45", "-w", f, text], check=True, stderr=subprocess.DEVNULL)
        data = open(f, "rb").read()
        w = wave.open(f); rate, frames = w.getframerate(), w.getnframes(); w.close()
    md5 = hashlib.md5(data).hexdigest()
    if md5 not in store: zf.writestr(md5 + ".wav", data); store.add(md5)
    _voice_cache[text] = (md5, rate, frames, frames / rate)
    return _voice_cache[text]

class Blocks:
    def __init__(self): self.b = {}; self.n = 0
    def nid(self): self.n += 1; return f"b{self.n}"
    def add(self, opcode, inputs=None, fields=None, shadow=False):
        i = self.nid()
        self.b[i] = {"opcode": opcode, "next": None, "parent": None, "inputs": inputs or {}, "fields": fields or {}, "shadow": shadow, "topLevel": False}
        return i
    def chain(self, ids, x=0, y=0):
        ids[0] and None
        for a, c in zip(ids, ids[1:]):
            self.b[a]["next"] = c; self.b[c]["parent"] = a
        h = ids[0]; self.b[h]["topLevel"] = True; self.b[h]["x"] = x; self.b[h]["y"] = y
        # parents des menus d'ombre
        for i in ids:
            for v in self.b[i]["inputs"].values():
                if isinstance(v[1], str) and v[1] in self.b: self.b[v[1]]["parent"] = i
    def num(self, v): return [1, [4, str(v)]]
    def txt(self, v): return [1, [10, v]]
    def hat_flag(self): return self.add("event_whenflagclicked")
    def hat_recv(self, name, bid): return self.add("event_whenbroadcastreceived", fields={"BROADCAST_OPTION": [name, bid]})
    def bc(self, name, bid, wait=False): return self.add("event_broadcastandwait" if wait else "event_broadcast", inputs={"BROADCAST_INPUT": [1, [11, name, bid]]})
    def play(self, name):
        m = self.add("sound_sounds_menu", fields={"SOUND_MENU": [name, None]}, shadow=True)
        return self.add("sound_play", inputs={"SOUND_MENU": [1, m]})
    def say(self, t, s): return self.add("looks_sayforsecs", inputs={"MESSAGE": self.txt(t), "SECS": self.num(s)})
    def glide(self, x, y, s): return self.add("motion_glidesecstoxy", inputs={"SECS": self.num(s), "X": self.num(x), "Y": self.num(y)})
    def goto(self, x, y): return self.add("motion_gotoxy", inputs={"X": self.num(x), "Y": self.num(y)})
    def show(self): return self.add("looks_show")
    def hide(self): return self.add("looks_hide")
    def wait(self, s): return self.add("control_wait", inputs={"DURATION": [1, [5, str(s)]]})
    def size(self, v): return self.add("looks_setsizeto", inputs={"SIZE": self.num(v)})
    def costume(self, name):
        m = self.add("looks_costume", fields={"COSTUME": [name, None]}, shadow=True)
        return self.add("looks_switchcostumeto", inputs={"COSTUME": [1, m]})
    def backdrop(self, name):
        m = self.add("looks_backdrops", fields={"BACKDROP": [name, None]}, shadow=True)
        return self.add("looks_switchbackdropto", inputs={"BACKDROP": [1, m]})

def asset(zf, svg, store):
    data = svg.encode("utf-8"); md5 = hashlib.md5(data).hexdigest()
    if md5 not in store: zf.writestr(md5 + ".svg", data); store.add(md5)
    return md5

def build(key):
    d = D[key]; s = STORIES[key]
    path = os.path.join(OUT, key + ".sb3")
    zf = zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED); store = set()
    # messages
    bcs = {}; 
    def mid(name):
        if name not in bcs: bcs[name] = f"msg{len(bcs)+1}"
        return bcs[name]
    # --- sprites : ordre + scripts
    handlers = {sp[0]: [] for sp in d["sprites"]}   # liste de (message, [actions])
    handlers["الحكمة"] = []
    scene_lines = []   # par scène : liste de messages
    for si, (bd, steps) in enumerate(d["scenes"], 1):
        msgs = []
        for k, st in enumerate(steps, 1):
            m = f"مشهد {si} · {k}"; msgs.append(m); mid(m)
            op, spr = st[0], st[1]
            handlers[spr].append((m, st))
        scene_lines.append(msgs)
    last = len(d["scenes"]) + 1
    for si in range(1, last + 1): mid(f"مشهد {si}")
    mid("الحكمة")
    # --- Stage
    sb = Blocks()
    ids = [sb.hat_flag(), sb.wait(0.3), sb.bc("مشهد 1", mid("مشهد 1"))]
    sb.chain(ids, 0, 0)
    for si, (bd, steps) in enumerate(d["scenes"], 1):
        name = f"مشهد {si}"
        ids = [sb.hat_recv(name, mid(name)), sb.backdrop(d["backdrops"][bd][0])]
        for m in scene_lines[si - 1]: ids += [sb.bc(m, mid(m), True), sb.wait(0.5)]
        if si < len(d["scenes"]): ids.append(sb.bc(f"مشهد {si+1}", mid(f"مشهد {si+1}")))
        else: ids.append(sb.bc("الحكمة", mid("الحكمة")))
        sb.chain(ids, 0, 200 * si)
    bd_costumes = []
    for (n, c) in d["backdrops"]:
        md5 = asset(zf, svg_backdrop(n, c), store)
        bd_costumes.append({"assetId": md5, "name": n, "md5ext": md5 + ".svg", "dataFormat": "svg", "rotationCenterX": 240, "rotationCenterY": 180})
    stage = {"isStage": True, "name": "Stage", "variables": {}, "lists": {}, "broadcasts": {}, "blocks": sb.b, "comments": {},
             "currentCostume": 0, "costumes": bd_costumes, "sounds": [], "volume": 100, "layerOrder": 0, "tempo": 60,
             "videoTransparency": 50, "videoState": "on", "textToSpeechLanguage": None}
    targets = [stage]
    # --- Sprites
    def sprite(name, costumes, w, h, hs, layer):
        b = Blocks()
        first = costumes[0][0]
        ids = [b.hat_flag(), b.hide(), b.size(80 if w == 100 else 100), b.costume(first)]
        b.chain(ids, 0, 0)
        y = 160
        sounds = []; snames = {}
        for (m, st) in hs:
            if st[0] == "say" and st[2] not in snames:
                v = voice(zf, store, st[2])
                if v: snames[st[2]] = f"صوت {len(snames)+1}"; sounds.append({"assetId": v[0], "name": snames[st[2]], "dataFormat": "wav", "rate": v[1], "sampleCount": v[2], "md5ext": v[0] + ".wav"})
        for (m, st) in hs:
            ids = [b.hat_recv(m, mid(m))]
            op = st[0]
            if op == "show": ids += [b.goto(st[2], st[3]), b.show()]
            elif op == "hide": ids += [b.hide()]
            elif op == "say":
                if st[2] in snames:
                    dur = _voice_cache[st[2]][3]
                    ids += [b.play(snames[st[2]]), b.say(st[2], max(2, round(dur + 0.5, 1)))]
                else: ids += [b.say(st[2], 2)]
            elif op == "glide": ids += [b.glide(st[2], st[3], st[4])]
            elif op == "goto": ids += [b.goto(st[2], st[3])]
            elif op == "costume": ids += [b.costume(st[2])]
            b.chain(ids, 0, y); y += 160
        cs = []
        for (n, svg) in costumes:
            md5 = asset(zf, svg, store)
            cs.append({"assetId": md5, "name": n, "md5ext": md5 + ".svg", "dataFormat": "svg", "rotationCenterX": w // 2, "rotationCenterY": h // 2})
        return {"isStage": False, "name": name, "variables": {}, "lists": {}, "broadcasts": {}, "blocks": b.b, "comments": {},
                "currentCostume": 0, "costumes": cs, "sounds": sounds, "volume": 100, "layerOrder": layer, "visible": False,
                "x": 0, "y": 0, "size": 80 if w == 100 else 100, "direction": 90, "draggable": False, "rotationStyle": "all around"}
    layer = 1
    for (n, col, alts) in d["sprites"]:
        cos = [(n, svg_sprite(n, col))] + [(an, svg_sprite(an.split(" · ")[-1] if " · " in an else an, ac)) for an, ac in alts]
        targets.append(sprite(n, cos, 100, 100, handlers[n], layer)); layer += 1
    # bandeau de la morale
    morale = s["morale"]
    bb = Blocks()
    ids = [bb.hat_flag(), bb.hide(), bb.goto(0, 150)]; bb.chain(ids, 0, 0)
    mv = voice(zf, store, morale)
    msounds = [{"assetId": mv[0], "name": "صوت الحكمة", "dataFormat": "wav", "rate": mv[1], "sampleCount": mv[2], "md5ext": mv[0] + ".wav"}] if mv else []
    ids = [bb.hat_recv("الحكمة", mid("الحكمة")), bb.show()] + ([bb.play("صوت الحكمة")] if mv else []); bb.chain(ids, 0, 160)
    md5 = asset(zf, svg_banner(morale), store)
    targets.append({"isStage": False, "name": "الحكمة", "variables": {}, "lists": {}, "broadcasts": {}, "blocks": bb.b, "comments": {},
        "currentCostume": 0, "costumes": [{"assetId": md5, "name": "الحكمة", "md5ext": md5 + ".svg", "dataFormat": "svg", "rotationCenterX": 220, "rotationCenterY": 23}],
        "sounds": msounds, "volume": 100, "layerOrder": layer, "visible": False, "x": 0, "y": 150, "size": 100, "direction": 90, "draggable": False, "rotationStyle": "all around"})
    stage["broadcasts"] = {v: k for k, v in bcs.items()}
    proj = {"targets": targets, "monitors": [], "extensions": [], "meta": {"semver": "3.0.0", "vm": "0.2.0", "agent": "Mozilla/5.0"}}
    zf.writestr("project.json", json.dumps(proj, ensure_ascii=False))
    zf.close()

os.makedirs(OUT, exist_ok=True)
for k in D: build(k)
print("ok", len(D))
