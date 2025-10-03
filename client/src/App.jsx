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
    <Route path="/" element={<MainLayout></MainLayout>}>
      <Route index element={<Home></Home>} />
      <Route path="/jobs" element={<Game></Game>} />
     {/* <Route path="*" element={<NotFoundPage />} />*/}
    </Route>
  )
);
const App = () => {
  return <RouterProvider router={router} />;
};

export default App;
