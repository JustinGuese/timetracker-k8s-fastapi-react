import axios from "axios";
import { useEffect, useState } from "react";
import pauseButton from "../images/pause_button.png";
import playButton from "../images/play_button.png";
import "./Time-item.css";

function millisToMinutesAndSeconds(millis) {
  var minutes = Math.floor(millis / 60000);
  var seconds = ((millis % 60000) / 1000).toFixed(0);
  console.log(seconds, "from seconds");
  if (seconds == -1) return "0:00";
  return minutes + ":" + (seconds < 10 ? "0" : "") + seconds;
}

const calculateTimePassed = (startDate, endDate) => {
  return millisToMinutesAndSeconds(endDate.getTime() - startDate.getTime());
};

const TimeItem = ({ companyLogo, companyName, info }) => {
  const [startTime, setStartTime] = useState(
    info.start_time ? new Date(info.start_time) : null
  );
  const [endTime, setEndTime] = useState(new Date());

  const [timeStarted, setTimeStarted] = useState(false);

  let actionsButtonSrcImage = playButton;
  console.log("is time started? ", timeStarted);
  if (info.start_time) actionsButtonSrcImage = pauseButton;

  useEffect(() => {
    let intervalKey;
    if (timeStarted)
      intervalKey = setInterval(() => {
        setEndTime(new Date());
      }, 1000);

    return () => {
      clearInterval(intervalKey);
    };
  }, [timeStarted]);

  const handleActionsClick = () => {
    if (timeStarted) {
      setTimeStarted(false);
      const date = new Date();
      setEndTime(date);
      axios({
        method: "put",
        url: "https://timetracker-backend.datafortress.cloud/timer/stop",
        data: {
          customer: info.customer,
          end_time: date.toISOString(),
        },
      });
    } else {
      setTimeStarted(true);
      if (!startTime) {
        setStartTime(new Date());
        axios({
          method: "put",
          url: "https://timetracker-backend.datafortress.cloud/timer/start",
          data: {
            customer: info.customer,
            start_time: new Date().toISOString(),
          },
        });
      }
    }
  };
  console.log("updated");
  return (
    <div class="card">
      <button className="card__btn" onClick={handleActionsClick}>
        <img src={actionsButtonSrcImage} />
      </button>
      <div className="card__logo">
        <div className="card__logo__image">
          <img src={companyLogo} alt={companyName} />
        </div>
        <h1 className="card__logo__name">{companyName}</h1>
      </div>
      {startTime ? calculateTimePassed(startTime, endTime) : <div></div>}
    </div>
  );
};

export default TimeItem;
