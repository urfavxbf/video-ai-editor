/** Tagalog/Taglish long-form episode script. All times are PRELIMINARY until actual WAV alignment. */
export type Y2038Speaker = 'urfavxbf' | 'pix';
export type Y2038Cue = {chapter:number;speaker:Y2038Speaker;stat:string;text:string;startFrame:number;endFrame:number};
export const Y2038_CHAPTERS = [
  "ANG ORAS NA BUMALIK",
  "BAKIT BINIBILANG ANG SEGUNDO",
  "ISANG NUMBER NA MAY HANGGANAN",
  "ANO ANG POSIBLENG MASIRA",
  "BAKIT MAY LIGTAS NA SYSTEMS",
  "ANG BUG NA MAAGANG DUMATING",
  "PAANO ITO INAAYOS",
  "HINDI KATAPUSAN NG MUNDO"
] as const;
const raw: Array<{chapter:number;speaker:Y2038Speaker;stat:string;text:string}> = [
  {
    "chapter": 1,
    "speaker": "pix",
    "stat": "2038",
    "text": "UrFavXBF, may nabasa akong kakaiba. Totoo bang may mga computer na puwedeng biglang mag-isip na taong 1901 na ulit kapag dumating ang 2038?"
  },
  {
    "chapter": 1,
    "speaker": "urfavxbf",
    "stat": "19 JAN 2038",
    "text": "Posible sa ilang lumang system, PIX. Hindi ito time travel. Problema ito sa paraan ng pag-iimbak ng oras gamit ang signed 32-bit number."
  },
  {
    "chapter": 1,
    "speaker": "pix",
    "stat": "03:14:07 UTC",
    "text": "So may eksaktong segundo talaga? Parang countdown sa pelikula! Pero bakit may particular na petsa at oras?"
  },
  {
    "chapter": 1,
    "speaker": "urfavxbf",
    "stat": "03:14:08 UTC",
    "text": "Sa January 19, 2038, alas tres katorse at walong segundo ng umaga sa UTC, hindi na kasya ang susunod na Unix timestamp sa signed 32-bit value."
  },
  {
    "chapter": 1,
    "speaker": "pix",
    "stat": "HINDI LAHAT",
    "text": "Teka, bago tayo mag-panic, affected ba lahat ng laptop, server, ATM, o smartphone? O may importante tayong kailangang linawin?"
  },
  {
    "chapter": 2,
    "speaker": "urfavxbf",
    "stat": "1970 = ZERO",
    "text": "Balik tayo sa 1970. May konsepto na tinatawag na Unix epoch: January 1, 1970, midnight UTC. Mula rito, binibilang ang mga segundo para kumatawan sa oras."
  },
  {
    "chapter": 2,
    "speaker": "pix",
    "stat": "1 SECOND = +1",
    "text": "Ibig sabihin, bawat lumipas na segundo, nadadagdagan ng isa ang number? Mas simple kaysa isulat ang buong petsa sa bawat operation."
  },
  {
    "chapter": 2,
    "speaker": "urfavxbf",
    "stat": "TIMESTAMP",
    "text": "Tama. Ginagamit ang timestamp para sa pag-save ng events, pag-expire ng sessions, pag-schedule ng tasks, at pag-compare kung alin ang mas nauna."
  },
  {
    "chapter": 2,
    "speaker": "pix",
    "stat": "BILLIONS OF SECONDS",
    "text": "Pero kung seconds lang ito, ang daming nadadagdag mula 1970! Bakit hindi na lang bigyan ng walang limitasyong space?"
  },
  {
    "chapter": 2,
    "speaker": "urfavxbf",
    "stat": "LIMITED BITS",
    "text": "Dahil sa computing, may fixed-size data types. Kapag limitado ang bilang ng bits, limitado rin ang pinakamalaking numerong puwedeng katawanin."
  },
  {
    "chapter": 3,
    "speaker": "pix",
    "stat": "32 BITS",
    "text": "Thirty-two bits. Parang thirty-two na maliliit na switch na puwedeng zero o one. Pero bakit hindi nito kayang umabot nang walang katapusan?"
  },
  {
    "chapter": 3,
    "speaker": "urfavxbf",
    "stat": "2,147,483,647",
    "text": "Kung signed 32-bit integer ang gamit, ang pinakamataas na positive value ay 2,147,483,647. Iyan mismo ang Unix timestamp sa January 19, 2038, 03:14:07 UTC."
  },
  {
    "chapter": 3,
    "speaker": "pix",
    "stat": "NEXT SECOND?",
    "text": "At kapag lumipas ang isa pang segundo, kailangan na ang 2,147,483,648. Isang hakbang lang ang pagitan, pero hindi na siya kasya."
  },
  {
    "chapter": 3,
    "speaker": "urfavxbf",
    "stat": "OVERFLOW",
    "text": "Dito nagsisimula ang problema. Sa mga implementation na nagwa-wrap ang value, puwedeng maging negative ang number at basahin bilang petsa noong December 1901."
  },
  {
    "chapter": 3,
    "speaker": "pix",
    "stat": "1901 IS AN EXAMPLE",
    "text": "So ang petsang 1901 ay posibleng resulta ng wraparound, hindi automatic na mangyayari sa bawat computer?"
  },
  {
    "chapter": 4,
    "speaker": "urfavxbf",
    "stat": "RESULTS VARY",
    "text": "Eksakto. Puwedeng mag-error, tumanggi sa date, magpakita ng maling oras, o magkaroon ng ibang undefined behavior. Depende iyon sa software at system."
  },
  {
    "chapter": 4,
    "speaker": "pix",
    "stat": "REAL-WORLD EFFECTS",
    "text": "Kung may lumang system na umaasa sa maling date, posibleng masira ang scheduling, data ordering, expiry checks, o mga log na ginagamit sa troubleshooting."
  },
  {
    "chapter": 4,
    "speaker": "urfavxbf",
    "stat": "LEGACY SOFTWARE",
    "text": "Pinakamahalagang suriin ang legacy code at embedded devices na matagal nang naka-deploy. Hindi sapat na sabihing bagong hardware, kaya siguradong safe."
  },
  {
    "chapter": 4,
    "speaker": "pix",
    "stat": "NO GLOBAL BLACKOUT",
    "text": "Pero hindi natin dapat sabihing sabay-sabay mawawala ang internet o titigil ang mundo sa 2038. Walang ebidensiyang ganoon ang universal na mangyayari."
  },
  {
    "chapter": 4,
    "speaker": "urfavxbf",
    "stat": "DEPENDENCIES",
    "text": "Ang tunay na risk ay magkakaiba: anong data type, operating system, library, storage format, at external device ang umaasa sa old timestamps?"
  },
  {
    "chapter": 5,
    "speaker": "pix",
    "stat": "MODERN SYSTEMS",
    "text": "Paano naman ang modern systems? Marami na bang nakalampas sa problemang ito, o kailangan pa rin nating maghanda?"
  },
  {
    "chapter": 5,
    "speaker": "urfavxbf",
    "stat": "64-BIT TIME",
    "text": "Marami nang platforms ang gumagamit ng mas malawak na 64-bit time representations. Sa tamang implementation, hindi sila matatamaan ng 2038 boundary na ito."
  },
  {
    "chapter": 5,
    "speaker": "pix",
    "stat": "64 BITS",
    "text": "Gaano kalaki ang agwat ng 32 at 64 bits? Hindi ba parang dinoble lang ang laki ng lalagyan?"
  },
  {
    "chapter": 5,
    "speaker": "urfavxbf",
    "stat": "MUCH LARGER RANGE",
    "text": "Oo, doble ang bits, pero napakalaking paglawak ng representable range. Kaya praktikal na solusyon ang 64-bit timestamps para sa problema ng 2038."
  },
  {
    "chapter": 5,
    "speaker": "pix",
    "stat": "CHECK THE WHOLE STACK",
    "text": "May catch ba? Halimbawa, 64-bit na ang operating system pero may lumang database column o application library na thirty-two-bit pa rin?"
  },
  {
    "chapter": 6,
    "speaker": "urfavxbf",
    "stat": "FUTURE DATES",
    "text": "Tama, at dito mas nagiging interesante. Posibleng lumitaw ang bug bago pa ang 2038 kapag nagko-compute ang software ng future date na lampas sa limit."
  },
  {
    "chapter": 6,
    "speaker": "pix",
    "stat": "EXPIRY 2040",
    "text": "Halimbawa, ngayong 2026, may device na kailangang mag-store ng expiration date na 2040. Maaari na bang lumabas ang problema ngayon?"
  },
  {
    "chapter": 6,
    "speaker": "urfavxbf",
    "stat": "EARLY FAILURE",
    "text": "Oo, kung ang code path na iyon ay gumagamit pa rin ng 32-bit signed Unix timestamp. Hindi kailangang hintayin ang mismong countdown."
  },
  {
    "chapter": 6,
    "speaker": "pix",
    "stat": "AUDIT NOW",
    "text": "Ibig sabihin, mas maganda ang proactive tests kaysa maghintay kung ano ang mangyayari. Aling bahagi ba ng system ang dapat unahin?"
  },
  {
    "chapter": 6,
    "speaker": "urfavxbf",
    "stat": "HIGH-RISK PATHS",
    "text": "Unahin ang long-lived embedded equipment, firmware, old dependencies, serialized timestamps, time-related APIs, at business logic na umaasa sa date comparisons."
  },
  {
    "chapter": 7,
    "speaker": "pix",
    "stat": "HOW TO FIX",
    "text": "Okay, engineer mode tayo. Paano natin malalaman kung may Y2038 bug, at paano natin ito aayusin nang hindi masisira ang existing data?"
  },
  {
    "chapter": 7,
    "speaker": "urfavxbf",
    "stat": "TEST BOUNDARIES",
    "text": "Una, i-test ang mga timestamp bago, eksakto, at pagkatapos ng January 19, 2038 boundary sa isolated test environment. Huwag baguhin basta ang production clock."
  },
  {
    "chapter": 7,
    "speaker": "pix",
    "stat": "MIGRATE SAFELY",
    "text": "Pangalawa, tingnan ang storage at API contracts. Kahit gawing 64-bit ang isang function, paano kung 32-bit pa rin ang kabilang system?"
  },
  {
    "chapter": 7,
    "speaker": "urfavxbf",
    "stat": "TIME64 + COMPAT",
    "text": "Kailangang planuhin ang data migration, compatibility testing, at release strategy. Sa ilang Linux build, may supported time64 options depende sa library at architecture."
  },
  {
    "chapter": 7,
    "speaker": "pix",
    "stat": "VERIFY RESULTS",
    "text": "At panghuli, hindi sapat na gumana sa isang computer. Dapat kasama ang backups, test coverage, error handling, at monitoring kapag na-deploy na."
  },
  {
    "chapter": 8,
    "speaker": "urfavxbf",
    "stat": "NOT THE END",
    "text": "Kaya ang Year 2038 Problem ay totoong engineering challenge, pero hindi propesiya ng katapusan ng teknolohiya. May malinaw nang mga paraan para iwasan ito."
  },
  {
    "chapter": 8,
    "speaker": "pix",
    "stat": "ONE BIT TOO FAR",
    "text": "Ang nakakagulat, isang segundo lang pagkatapos ng pinakamataas na number ang puwedeng magbunyag ng maling assumption sa code. Ang liit ng simula, ang laki ng epekto."
  },
  {
    "chapter": 8,
    "speaker": "urfavxbf",
    "stat": "CHECK ASSUMPTIONS",
    "text": "At iyan ang aral: kapag may limit ang data, dapat alam natin kung saan ito nagtatapos. Ang magandang software ay handa kahit sa mga petsang malayo pa."
  },
  {
    "chapter": 8,
    "speaker": "pix",
    "stat": "YOUR TURN",
    "text": "Ikaw, may kilala ka bang lumang gadget o system na umaandar pa hanggang ngayon? I-comment mo, at sabihin kung anong technology mystery ang susunod nating susuriin."
  },
  {
    "chapter": 8,
    "speaker": "urfavxbf",
    "stat": "END // 2038",
    "text": "Ako si UrFavXBF, at kasama natin si PIX. Sa susunod, isa na namang misteryo ng teknolohiya ang bubusisiin natin, gamit ang ebidensya, hindi takot."
  }
];
/** About 2.1 Tagalog words/sec with breathing room; replace after voice synthesis. */
const frameLength = (text:string) => Math.max(135, Math.ceil((text.trim().split(/\s+/u).length / 2.12 + 1.2) * 30));
let cursor = 0;
export const Y2038_CUES: Y2038Cue[] = raw.map((cue) => {const startFrame=cursor;cursor+=frameLength(cue.text);return {...cue,startFrame,endFrame:cursor};});
export const Y2038_TOTAL_FRAMES=cursor;
export const Y2038_FPS=30;
