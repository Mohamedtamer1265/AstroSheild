import { Outlet } from "react-router-dom"
import NavBar from "../components/NavBar"
const MainLayout = () => {
  return (
    <>
    <NavBar/>
    <Outlet/>
    {/* Outlet is where the child routes will be rendered */}
    </>
  )
}

export default MainLayout