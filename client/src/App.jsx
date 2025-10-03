import Home from "./pages/Home";
import Game from "./pages/Game";
import MainLayout from "./layout/MainLayout";
import {
  Route,
  createBrowserRouter,
  createRoutesFromElements,
  RouterProvider,
} from "react-router-dom";
import MeteorPage from "./pages/MeteorPage";
import MeteorInfo from "./pages/MeteorInfo";


const router = createBrowserRouter(
  createRoutesFromElements(
    <>
      <Route path="/" element={<MainLayout></MainLayout>}>
        <Route index element={<Home></Home>} />
        <Route path="/Game" element={<Game></Game>} />

        {/* <Route path="*" element={<NotFoundPage />} />*/}
      </Route>
      <Route path="/MeteorPage" element={<MeteorPage></MeteorPage>} />
      <Route path="/MeteorInfo" element={<MeteorInfo></MeteorInfo>} />
    </>
    
  )
);
const App = () => {
  return <RouterProvider router={router} />;
};

export default App;
