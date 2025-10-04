import Home from "./pages/Home";
import Game from "./pages/Game";
import MainLayout from "./layout/MainLayout";
import { useNavigate } from "react-router-dom";
import {
  Route,
  createBrowserRouter,
  createRoutesFromElements,
  RouterProvider,
} from "react-router-dom";
import MeteorPage from "./pages/MeteorPage";
import MeteorInfo from "./pages/MeteorInfo";
import AsteroidDashboard from "./pages/asteroid";
import { AccessibilityProvider } from "./contexts/AccessibilityContext";
import "./styles/accessibility.css";
const router = createBrowserRouter(
  createRoutesFromElements(
    <>
      <Route path="/" element={<MainLayout></MainLayout>}>
        <Route index element={<Home></Home>} />

        {/* <Route path="*" element={<NotFoundPage />} />*/}
      </Route>
      <Route path="/MeteorPage" element={<MeteorPage></MeteorPage>} />
      <Route path="/meteor-info" element={<MeteorInfo></MeteorInfo>} />
      <Route path="/Game" element={<Game></Game>} />
      <Route
        path="/astroid"
        element={<AsteroidDashboard></AsteroidDashboard>}
      />
    </>
  )
);

const App = () => {
  return (
    <AccessibilityProvider>
      <RouterProvider router={router} />
    </AccessibilityProvider>
  );
};

export default App;
