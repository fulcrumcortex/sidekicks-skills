import { Sparkles, Rocket, Zap } from "lucide-react";

const features = [
  { icon: "⚡", title: "Feature one", body: "Lorem ipsum dolor sit amet." },
  { icon: "🔒", title: "Secure by default", body: "Supercharge your team." },
  { icon: "📈", title: "Grow faster", body: "Transform your pipeline." },
];

export function Hero() {
  return (
    <section className="relative overflow-hidden text-center bg-gradient-to-br from-purple-600 via-indigo-600 to-violet-700">
      <div className="absolute -top-24 left-1/2 h-96 w-96 rounded-full bg-fuchsia-500/40 blur-3xl" />
      <h1 className="text-4xl font-bold bg-clip-text text-transparent">
        Unlock seamless growth
      </h1>
      <p className="text-center text-lg text-white/80">
        Elevate your workflow with our next-gen platform.
      </p>
      <div className="mt-12 grid gap-6 md:grid-cols-3">
        {features.map((f) => (
          <div key={f.title} className="rounded-2xl bg-white/10 p-6 shadow-lg backdrop-blur-md transition-all hover:scale-105">
            <span className="text-2xl">{f.icon}</span>
            <h3 className="text-xl font-semibold">{f.title}</h3>
            <p className="text-sm">{f.body}</p>
          </div>
        ))}
      </div>
      <button className="mt-10 rounded-2xl px-6 py-3 shadow-lg transition-all animate-pulse">
        <Sparkles /> Get started
      </button>
    </section>
  );
}
