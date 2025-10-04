import { Outlet } from "react-router-dom"
import NavBar from "../components/NavBar"
import AccessibilityToggle from "../components/AccessibilityToggle"

const MainLayout = () => {
  return (
    <>
    <NavBar/>
    <AccessibilityToggle />
    <Outlet/>
    {/* Outlet is where the child routes will be rendered */}
    </>
  )
}

export default MainLayout