import { useContext } from "react";

import { EventContext } from "../context/EventContextObject";

export function useEventContext() {
  const context = useContext(EventContext);

  if (!context) {
    throw new Error("useEventContext must be used inside EventProvider");
  }

  return context;
}
