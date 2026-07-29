function Navbar() {
  return (
    <nav className="flex items-center justify-between px-10 py-5 border-b border-slate-800">
      <h1 className="text-2xl font-bold text-cyan-400">
        AutoMind AI
      </h1>

      <button className="bg-cyan-500 hover:bg-cyan-600 px-5 py-2 rounded-lg font-semibold transition">
        Get Started
      </button>
    </nav>
  );
}

export default Navbar;