import { motion } from "framer-motion";
import { FiCpu, FiDatabase, FiGitBranch, FiLayers, FiMap, FiTrendingUp } from "react-icons/fi";

import styles from "./About.module.css";

const pipeline = [
  { icon: FiDatabase, title: "Collect", text: "Ingests news from RSS feeds, APIs, and curated source lists into a unified article stream." },
  { icon: FiGitBranch, title: "Cluster", text: "Embeddings group similar stories into coherent events instead of isolated headlines." },
  { icon: FiCpu, title: "Understand", text: "NLP extracts people, organizations, locations, confidence scores, summaries, and impact signals." },
  { icon: FiMap, title: "Visualize", text: "The dashboard presents timelines, related sources, entity chips, and searchable intelligence views." },
];

const tech = ["React 19", "Vite", "React Router", "Axios", "CSS Modules", "Framer Motion", "React Icons", "FastAPI Ready"];
const features = ["AI event clustering", "Semantic search", "Entity extraction", "Source traceability", "Timeline analysis", "Responsive SaaS dashboard"];
const future = ["Real-time alerts", "User watchlists", "Bias and sentiment scoring", "Multilingual clustering", "Exportable intelligence reports", "Source reliability ranking"];

function About() {
  return (
    <motion.div
      className={styles.page}
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -12 }}
      transition={{ duration: 0.24 }}
    >
      <section className={styles.hero}>
        <span>Final Year Project</span>
        <h1>NewsLens AI turns noisy headlines into structured news intelligence.</h1>
        <p>
          The platform collects articles from multiple sources, clusters related coverage into
          events, extracts key entities, summarizes developments, and presents decision-ready
          context in a modern dashboard.
        </p>
      </section>

      <section className={styles.pipeline} aria-labelledby="pipeline-title">
        <div className={styles.sectionHeader}>
          <FiLayers />
          <h2 id="pipeline-title">How the AI Pipeline Works</h2>
        </div>
        <div className={styles.pipelineGrid}>
          {pipeline.map(({ icon: Icon, title, text }) => (
            <article className={styles.pipelineCard} key={title}>
              <Icon />
              <h3>{title}</h3>
              <p>{text}</p>
            </article>
          ))}
        </div>
      </section>

      <section className={styles.split}>
        <div>
          <div className={styles.sectionHeader}>
            <FiCpu />
            <h2>Technology Stack</h2>
          </div>
          <div className={styles.tags}>{tech.map((item) => <span key={item}>{item}</span>)}</div>
        </div>
        <div>
          <div className={styles.sectionHeader}>
            <FiTrendingUp />
            <h2>Features</h2>
          </div>
          <div className={styles.tags}>{features.map((item) => <span key={item}>{item}</span>)}</div>
        </div>
      </section>

      <section className={styles.future} aria-labelledby="future-title">
        <h2 id="future-title">Future Scope</h2>
        <div className={styles.tags}>{future.map((item) => <span key={item}>{item}</span>)}</div>
      </section>
    </motion.div>
  );
}

export default About;
