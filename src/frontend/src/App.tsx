import { Outlet } from "react-router-dom";
import NavBar from "./components/navbar";

function App() {
  return (
    <div className="flex flex-col items-center min-h-screen bg-my-secondary-color">
      <NavBar />
      <Outlet />
    </div>
  );
}

export default App;
