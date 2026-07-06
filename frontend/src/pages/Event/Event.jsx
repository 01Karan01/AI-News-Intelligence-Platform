import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { useParams } from "react-router-dom";

import ErrorState from "../../components/Error/ErrorState";
import EventDetails from "../../components/EventDetails/EventDetails";
import PageLoader from "../../components/Loading/PageLoader";
import { getEventById } from "../../services/api";
import styles from "./Event.module.css";

function Event() {
  const { id } = useParams();
  const [event, setEvent] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let active = true;

    async function loadEvent() {
      setLoading(true);
      const result = await getEventById(id);
      if (active) {
        setEvent(result);
        setLoading(false);
      }
    }

    loadEvent();

    return () => {
      active = false;
    };
  }, [id]);

  if (loading) {
    return <PageLoader label="Loading event intelligence" />;
  }

  if (!event) {
    return (
      <ErrorState
        title="Event not found"
        message="The event cluster you requested is not available in the current intelligence index."
      />
    );
  }

  return (
    <motion.div
      className={styles.page}
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -12 }}
      transition={{ duration: 0.24 }}
    >
      <EventDetails event={event} />
    </motion.div>
  );
}

export default Event;
