import axios from "axios";

export const BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000/api";

const API = axios.create({
  baseURL: BASE_URL,
  timeout: 6000,
  headers: {
    "Content-Type": "application/json",
  },
});

const today = new Date();
const isoDaysAgo = (days) => {
  const date = new Date(today);
  date.setDate(today.getDate() - days);
  return date.toISOString();
};

const mockEvents = [
  {
    id: "global-ai-regulation-summit",
    title: "Global AI Regulation Summit Sets New Transparency Rules",
    summary:
      "Governments and major AI labs agreed on shared audit standards, model disclosure practices, and incident reporting rules for frontier AI systems.",
    date: isoDaysAgo(0),
    category: "Artificial Intelligence",
    confidence: 94,
    articleCount: 48,
    globalImpact:
      "The agreement is likely to shape compliance requirements for AI products across North America, Europe, and Asia, especially in finance, health, and education.",
    people: ["Sam Altman", "Ursula von der Leyen", "Sundar Pichai", "Satya Nadella"],
    organizations: ["OpenAI", "European Commission", "Google DeepMind", "Microsoft"],
    locations: ["Brussels", "Washington DC", "London", "New Delhi"],
    sources: [
      { id: "src-ai-1", headline: "AI labs endorse common safety disclosure framework", source: "Reuters", publishedAt: isoDaysAgo(0), url: "https://www.reuters.com" },
      { id: "src-ai-2", headline: "New frontier model audit rules gain global backing", source: "Bloomberg", publishedAt: isoDaysAgo(0), url: "https://www.bloomberg.com" },
      { id: "src-ai-3", headline: "Regulators move toward shared AI incident database", source: "The Verge", publishedAt: isoDaysAgo(0), url: "https://www.theverge.com" },
    ],
    timeline: [
      { time: "08:30", label: "Draft framework published by summit chairs" },
      { time: "11:15", label: "Major labs announce voluntary adoption" },
      { time: "16:40", label: "Market analysts publish first compliance outlook" },
    ],
  },
  {
    id: "iran-energy-market-shock",
    title: "Middle East Tensions Push Energy Markets Into Volatile Session",
    summary:
      "Oil prices climbed after renewed regional tensions raised concerns about shipping routes, energy supply continuity, and inflation pressure.",
    date: isoDaysAgo(0),
    category: "Geopolitics",
    confidence: 89,
    articleCount: 36,
    globalImpact:
      "A sustained price rise could affect transport costs, central bank policy expectations, and import-heavy economies in Asia and Europe.",
    people: ["Masoud Pezeshkian", "Antony Blinken", "Mohammed bin Salman"],
    organizations: ["OPEC", "IEA", "U.S. State Department"],
    locations: ["Tehran", "Strait of Hormuz", "Riyadh", "Dubai"],
    sources: [
      { id: "src-oil-1", headline: "Oil rallies as shipping risk returns to focus", source: "CNBC", publishedAt: isoDaysAgo(0), url: "https://www.cnbc.com" },
      { id: "src-oil-2", headline: "Energy traders price in fresh Gulf uncertainty", source: "Financial Times", publishedAt: isoDaysAgo(0), url: "https://www.ft.com" },
    ],
    timeline: [
      { time: "07:10", label: "Asian markets open with higher crude futures" },
      { time: "12:00", label: "OPEC officials signal supply monitoring" },
      { time: "18:25", label: "Airline and logistics stocks close lower" },
    ],
  },
  {
    id: "gta-6-release-economy",
    title: "GTA 6 Publisher Update Sparks Gaming Industry Rally",
    summary:
      "A new release-window update from Take-Two lifted gaming stocks and renewed debate about console demand, preorders, and creator economy spillovers.",
    date: isoDaysAgo(1),
    category: "Technology",
    confidence: 86,
    articleCount: 27,
    globalImpact:
      "The launch cycle may influence console sales, advertising budgets, streaming viewership, and game-sector hiring over the next year.",
    people: ["Strauss Zelnick"],
    organizations: ["Take-Two Interactive", "Rockstar Games", "Sony", "Microsoft Xbox"],
    locations: ["New York", "Los Angeles", "Tokyo"],
    sources: [
      { id: "src-gta-1", headline: "Gaming shares rise after GTA 6 release update", source: "MarketWatch", publishedAt: isoDaysAgo(1), url: "https://www.marketwatch.com" },
      { id: "src-gta-2", headline: "Analysts expect record entertainment launch", source: "IGN", publishedAt: isoDaysAgo(1), url: "https://www.ign.com" },
    ],
    timeline: [
      { time: "09:00", label: "Publisher update reaches investors" },
      { time: "13:20", label: "Retail analysts raise preorder forecasts" },
      { time: "19:00", label: "Creator platforms report trending search spike" },
    ],
  },
  {
    id: "openai-enterprise-copilots",
    title: "OpenAI Enterprise Copilots Expand Across Regulated Industries",
    summary:
      "Banks, insurers, and health networks are adopting controlled AI assistants for research, support, compliance review, and internal knowledge workflows.",
    date: isoDaysAgo(2),
    category: "Business",
    confidence: 91,
    articleCount: 42,
    globalImpact:
      "Enterprise AI adoption is shifting from experiments to department-wide deployments with stricter governance, observability, and data controls.",
    people: ["Brad Lightcap", "Jamie Dimon"],
    organizations: ["OpenAI", "JPMorgan Chase", "PwC", "Mayo Clinic"],
    locations: ["San Francisco", "New York", "London"],
    sources: [
      { id: "src-ent-1", headline: "Enterprise AI moves deeper into bank workflows", source: "The Wall Street Journal", publishedAt: isoDaysAgo(2), url: "https://www.wsj.com" },
      { id: "src-ent-2", headline: "Hospitals pilot assistants for clinical administration", source: "STAT", publishedAt: isoDaysAgo(2), url: "https://www.statnews.com" },
    ],
    timeline: [
      { time: "10:10", label: "New deployment case studies released" },
      { time: "14:30", label: "Consultancies announce AI governance packages" },
    ],
  },
  {
    id: "europe-heat-health-alert",
    title: "European Heat Alerts Trigger Public Health Response",
    summary:
      "Several countries issued heat-health warnings as cities opened cooling centers, adjusted work schedules, and prepared hospitals for vulnerable patients.",
    date: isoDaysAgo(3),
    category: "Climate",
    confidence: 88,
    articleCount: 31,
    globalImpact:
      "Extreme heat is increasing pressure on urban infrastructure, labor policy, public health planning, and electricity demand management.",
    people: ["Tedros Adhanom Ghebreyesus"],
    organizations: ["WHO", "European Environment Agency", "Meteo France"],
    locations: ["Paris", "Madrid", "Rome", "Athens"],
    sources: [
      { id: "src-heat-1", headline: "Heat alerts spread across southern Europe", source: "BBC", publishedAt: isoDaysAgo(3), url: "https://www.bbc.com" },
      { id: "src-heat-2", headline: "Hospitals prepare for heat-related admissions", source: "Associated Press", publishedAt: isoDaysAgo(3), url: "https://apnews.com" },
    ],
    timeline: [
      { time: "06:00", label: "Meteorological warnings issued" },
      { time: "12:45", label: "Cities open public cooling centers" },
      { time: "17:50", label: "Grid operators report elevated demand" },
    ],
  },
  {
    id: "india-semiconductor-investment",
    title: "India Announces New Semiconductor Manufacturing Incentives",
    summary:
      "A fresh incentive package aims to attract chip fabrication, packaging, and design investments while strengthening supply-chain resilience.",
    date: isoDaysAgo(4),
    category: "Economy",
    confidence: 92,
    articleCount: 34,
    globalImpact:
      "The policy could diversify chip supply chains and increase competition for advanced electronics manufacturing investments across Asia.",
    people: ["Narendra Modi", "Ashwini Vaishnaw"],
    organizations: ["Ministry of Electronics and IT", "Tata Electronics", "Micron"],
    locations: ["New Delhi", "Gujarat", "Bengaluru"],
    sources: [
      { id: "src-chip-1", headline: "India widens incentives for chip manufacturing", source: "Economic Times", publishedAt: isoDaysAgo(4), url: "https://economictimes.indiatimes.com" },
      { id: "src-chip-2", headline: "Global chip firms evaluate new India package", source: "Nikkei Asia", publishedAt: isoDaysAgo(4), url: "https://asia.nikkei.com" },
    ],
    timeline: [
      { time: "09:30", label: "Policy package announced in New Delhi" },
      { time: "15:00", label: "Electronics firms brief investors" },
    ],
  },
  {
    id: "trump-campaign-economy-message",
    title: "Trump Campaign Refocuses Economic Messaging Ahead of Debates",
    summary:
      "The campaign sharpened its message on inflation, trade, immigration, and manufacturing as policy groups prepared new briefing material.",
    date: isoDaysAgo(5),
    category: "Politics",
    confidence: 84,
    articleCount: 29,
    globalImpact:
      "Campaign positions may influence investor expectations for tariffs, industrial policy, immigration rules, and foreign-policy posture.",
    people: ["Donald Trump", "J.D. Vance"],
    organizations: ["Republican National Committee", "U.S. Chamber of Commerce"],
    locations: ["Washington DC", "Pennsylvania", "Michigan"],
    sources: [
      { id: "src-trump-1", headline: "Campaign leans into economy before debate cycle", source: "Politico", publishedAt: isoDaysAgo(5), url: "https://www.politico.com" },
      { id: "src-trump-2", headline: "Trade policy questions return to market focus", source: "Axios", publishedAt: isoDaysAgo(5), url: "https://www.axios.com" },
    ],
    timeline: [
      { time: "08:45", label: "Campaign releases economic memo" },
      { time: "13:10", label: "Business groups respond to tariff language" },
    ],
  },
];

const mockStatistics = {
  articles: 247,
  events: mockEvents.length,
  sources: 38,
  countries: 24,
};

const delay = (payload) =>
  new Promise((resolve) => {
    window.setTimeout(() => resolve(payload), 240);
  });

const withFallback = async (request, fallback) => {
  try {
    const response = await request();
    return response.data;
  } catch {
    return delay(fallback);
  }
};

const normalize = (value) => value.toLowerCase().trim();

export const getEvents = () => withFallback(() => API.get("/events"), mockEvents);

export const getEventById = (id) =>
  withFallback(
    () => API.get(`/events/${id}`),
    mockEvents.find((event) => event.id === id) ?? null,
  );

export const searchEvents = (query = "") => {
  const term = normalize(query);
  const results = term
    ? mockEvents.filter((event) =>
        [
          event.title,
          event.summary,
          event.category,
          ...event.people,
          ...event.organizations,
          ...event.locations,
        ]
          .join(" ")
          .toLowerCase()
          .includes(term),
      )
    : mockEvents;

  return withFallback(() => API.get("/events/search", { params: { q: query } }), results);
};

export const getTimeline = () => {
  const groups = Array.from({ length: 6 }, (_, daysAgo) => ({
    daysAgo,
    label: daysAgo === 0 ? "Today" : daysAgo === 1 ? "Yesterday" : `${daysAgo} Days Ago`,
    events: mockEvents.filter((event) => {
      const eventDate = new Date(event.date);
      const targetDate = new Date(today);
      targetDate.setDate(today.getDate() - daysAgo);
      return eventDate.toDateString() === targetDate.toDateString();
    }),
  }));

  return withFallback(() => API.get("/timeline"), groups);
};

export const getStatistics = () => withFallback(() => API.get("/statistics"), mockStatistics);

export default API;
