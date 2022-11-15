import axios from "axios";
import { useEffect, useState } from "react";
import "./App.css";
import bunchImage from "./images/bunch.jpeg";
import TimeItem from "./Time-Item/index.js";

const TimeTracker = (props) => {
  const [customers, setCustomers] = useState([]);
  const [info, setInfo] = useState(null);
  useEffect(() => {
    axios
      .get("https://timetracker-backend.datafortress.cloud/timer/clients")
      .then((res) => setCustomers(res.data));
    axios
      .get("https://timetracker-backend.datafortress.cloud/timer/info")
      .then((res) => setInfo(res.data));
  }, []);
  console.log(customers, "from customers");
  console.log(info, "from info,s");
  const renderCustomers = info
    ? customers.map((customer) => {
        const customerInfo = info.find((item) => item.customer === customer);

        return (
          <TimeItem
            companyLogo={bunchImage}
            companyName={customer}
            key={customer}
            info={customerInfo}
          />
        );
      })
    : "";
  return (
    <div className="App">
      {customers.length ? renderCustomers : "no customers foun"}
    </div>
  );
};

export default TimeTracker;
