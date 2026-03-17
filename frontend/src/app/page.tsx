import CabinetBuilder from "@/components/CabinetBuilder";

export default function Home() {
  return (
    <main className="min-h-screen">
      <CabinetBuilder />
    </main>
  );
}

export const metadata = {
  title: "Modology Cabinet Designer",
  description: "Design cabinets, generate optimized cut lists, and prepare for CNC fabrication",
};
