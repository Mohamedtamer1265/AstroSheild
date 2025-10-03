
import bgImg from "../assets/img/intro.jpg";

function Home() {
  return (
    <div
      className="h-screen w-full bg-cover bg-center flex items-center justify-center text-white"
      style={{ backgroundImage: `url(${bgImg})` }}
    >
      {/* Optional overlay for readability */}
      <div className="bg-black/50 p-8 rounded-xl text-center">
        <h1 className="text-5xl font-bold mb-4 drop-shadow-lg">AstroSheild</h1>
      </div>
    </div>
  );
}

export default Home;
