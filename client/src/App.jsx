import Home from "./pages/Home";
import Game from "./pages/Game";
import MainLayout from "./layout/MainLayout";
import {
  Route,
  createBrowserRouter,
  createRoutesFromElements,
  RouterProvider,
} from "react-router-dom";

const router = createBrowserRouter(
  createRoutesFromElements(
    <>
      {/* Routes with MainLayout */}
      <Route path="/" element={<MainLayout />}>
        <Route index element={<Home />} />
        {/* <Route path="*" element={<NotFoundPage />} /> */}
      </Route>

      {/* Standalone Game route */}
      <Route path="/Game" element={<Game />} />
    </>
  )
);

const App = () => {
  return <RouterProvider router={router} />;
};

export default App;
