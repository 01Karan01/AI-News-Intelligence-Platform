import { FiExternalLink } from "react-icons/fi";

import { cleanDisplayText } from "../../utils/text";
import styles from "./RelatedArticles.module.css";

function RelatedArticles({ articles = [] }) {
  const items = Array.isArray(articles) ? articles : [];
  if (items.length === 0) return null;

  return (
    <section className={styles.card} aria-labelledby="related-title">
      <div className={styles.header}>
        <h2 id="related-title">Related Articles</h2>
        <span>{items.length} sources</span>
      </div>
      <div className={styles.list}>
        {items.map((article) => (
          <article className={styles.article} key={article.id}>
            <div>
              <h3>{cleanDisplayText(article.headline, "Untitled article")}</h3>
              <p>
                {cleanDisplayText(article.source, "Unknown source")} {" | "}
                <time dateTime={article.publishedAt}>
                  {new Intl.DateTimeFormat("en", {
                    month: "short",
                    day: "numeric",
                    hour: "2-digit",
                    minute: "2-digit",
                  }).format(new Date(article.publishedAt))}
                </time>
              </p>
            </div>
            <a href={article.url} target="_blank" rel="noreferrer">
              Read Original
              <FiExternalLink />
            </a>
          </article>
        ))}
      </div>
    </section>
  );
}

export default RelatedArticles;

