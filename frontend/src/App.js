import hplogo from './hplogo.png';
import bwlogo from './bwlogo.png';

import TimeItem from './TimeItem';

class App extends React.Component {
  render() {
    return (
      <h1>Timesheet</h1>
      <TimeItem image={hplogo} />
      <TimeItem image={bwlogo} />
    );
}

export default App;
