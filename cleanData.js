const fs = require("node:fs");
const path = require("node:path");

const dataPath = path.join(__dirname, "data", "ai-engineer.json");
const fileContents = fs.readFileSync(dataPath, { encoding: "utf-8" });

const data = JSON.parse(fileContents);

const tracks = data.props.pageProps.schedule.result.data;

const sessions = tracks
  .flatMap((track) => {
    const trackSessions = track.attributes.sessions.data;
    return trackSessions.map((trackSession) => {
      const session = trackSession.attributes;
      const presenters = session.presenters?.data.map(
        (presenter) =>
          `${presenter.attributes.name}, ${presenter.attributes.tagline}, ${presenter.attributes.company?.data.attributes.name}`
      );
      if (presenters.length === 0) {
        return null;
      }
      return `Session: ${session.title}
Presenters: ${presenters.join(", ")}
Date: ${session.date}
Start Time: ${session.startTime}
About: ${session.about}`;
    });
  })
  .filter(Boolean);

const outPath = path.join(__dirname, "data", "ai-engineer-sessions.json");
fs.writeFileSync(outPath, JSON.stringify(sessions, null, 2), {
  encoding: "utf-8",
});
