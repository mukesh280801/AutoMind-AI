import Navbar from "../components/Navbar";

function Dashboard() {
  return (
    <div className="min-h-screen bg-slate-950 text-white">
      <Navbar />

      <div className="flex items-center justify-center h-[80vh]">
        <h1 className="text-5xl font-bold text-cyan-400">
          Dashboard
        </h1>
      </div>
    </div>
  );
}

export default Dashboard;